"""
Semantic Search & LLM Application - pipeline script.

Alur: ingest -> embed -> store (FAISS) -> retrieve -> generate.

Penggunaan (dari root project):
    python src/faq_search.py build                 # ingest + embed + simpan index FAISS
    python src/faq_search.py search "pertanyaan"   # semantic search saja (top-k + skor)
    python src/faq_search.py ask "pertanyaan"      # semantic search + jawaban LLM
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

import faiss
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ---------------------------------------------------------------------------
# Konfigurasi
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "ecommerce_faq_knowledge_base.csv"
INDEX_PATH = ROOT / "vector_store" / "faq.index"
META_PATH = ROOT / "vector_store" / "faq_metadata.json"

load_dotenv(ROOT / ".env")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-flash-latest")
TOP_K = 3

_client: genai.Client | None = None


def get_client() -> genai.Client:
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY belum diisi. Salin .env.example menjadi .env lalu isi API key.")
        _client = genai.Client(api_key=api_key)
    return _client


# ---------------------------------------------------------------------------
# 1. Ingest
# ---------------------------------------------------------------------------
def load_knowledge_base(path: Path = DATA_PATH) -> pd.DataFrame:
    """Memuat CSV FAQ (read-only) dan membentuk satu unit teks per entri."""
    df = pd.read_csv(path)
    df["content"] = (
        "Kategori: " + df["category"] + "\n"
        + "Pertanyaan: " + df["question"] + "\n"
        + "Jawaban: " + df["answer"]
    )
    return df


# ---------------------------------------------------------------------------
# 2. Embed
# ---------------------------------------------------------------------------
def embed_texts(texts: list[str], task_type: str, batch_size: int = 50, retries: int = 3) -> np.ndarray:
    """Mengubah daftar teks menjadi matriks embedding float32 (dinormalisasi L2)."""
    vectors: list[list[float]] = []
    for start in range(0, len(texts), batch_size):
        batch = texts[start:start + batch_size]
        for attempt in range(retries):
            try:
                result = get_client().models.embed_content(
                    model=EMBEDDING_MODEL,
                    contents=batch,
                    config=types.EmbedContentConfig(task_type=task_type),
                )
                vectors.extend(e.values for e in result.embeddings)
                break
            except Exception:
                if attempt == retries - 1:
                    raise
                time.sleep(2 ** attempt * 5)
    arr = np.array(vectors, dtype="float32")
    faiss.normalize_L2(arr)  # setelah dinormalisasi, inner product = cosine similarity
    return arr


# ---------------------------------------------------------------------------
# 3. Store
# ---------------------------------------------------------------------------
def build_index(df: pd.DataFrame) -> faiss.Index:
    embeddings = embed_texts(df["content"].tolist(), task_type="RETRIEVAL_DOCUMENT")
    print(f"Shape embeddings: {embeddings.shape}")
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    assert index.ntotal == len(df), "Jumlah vektor tidak sama dengan jumlah entri knowledge base"
    print(f"Jumlah vektor tersimpan: {index.ntotal} (entri knowledge base: {len(df)})")
    return index


def save_index(index: faiss.Index, df: pd.DataFrame) -> None:
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(INDEX_PATH))
    meta = df[["faq_id", "category", "question", "answer"]].to_dict(orient="records")
    META_PATH.write_text(json.dumps({"embedding_model": EMBEDDING_MODEL, "entries": meta},
                                    ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Index disimpan ke {INDEX_PATH.relative_to(ROOT)}")


def load_index() -> tuple[faiss.Index, pd.DataFrame]:
    index = faiss.read_index(str(INDEX_PATH))
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))
    return index, pd.DataFrame(meta["entries"])


# ---------------------------------------------------------------------------
# 4. Retrieve
# ---------------------------------------------------------------------------
def semantic_search(query: str, index: faiss.Index, df: pd.DataFrame, top_k: int = TOP_K) -> list[dict]:
    query_vec = embed_texts([query], task_type="RETRIEVAL_QUERY")
    scores, ids = index.search(query_vec, top_k)
    results = []
    for rank, (idx, score) in enumerate(zip(ids[0], scores[0]), start=1):
        row = df.iloc[int(idx)]
        results.append({
            "rank": rank,
            "faq_id": int(row["faq_id"]),
            "category": row["category"],
            "question": row["question"],
            "answer": row["answer"],
            "score": round(float(score), 4),  # cosine similarity, makin tinggi makin mirip
        })
    return results


# ---------------------------------------------------------------------------
# 5. Generate
# ---------------------------------------------------------------------------
PROMPT_TEMPLATE = """### PERSONA
Kamu adalah "Asisten CS", customer service virtual sebuah platform e-commerce di Indonesia.
Kamu ramah, sopan, empatik, dan menjawab dalam Bahasa Indonesia yang mudah dipahami pelanggan.

### TASK
Jawab pertanyaan pelanggan di bawah ini dengan aturan berikut:
1. Gunakan HANYA informasi yang ada di bagian CONTEXT. Jangan memakai pengetahuan umum atau asumsi di luar CONTEXT.
2. CONTEXT berisi beberapa FAQ hasil pencarian; tidak semuanya pasti relevan. Pakai hanya FAQ yang benar-benar menjawab pertanyaan.
3. Jika CONTEXT tidak memuat jawabannya, katakan dengan jujur: "Maaf, informasi tersebut belum tersedia di FAQ kami." lalu sarankan pelanggan menghubungi customer service.
4. Jika CONTEXT hanya menjawab sebagian, jawab bagian yang tersedia dan sebutkan bagian mana yang belum ada informasinya.
5. Jangan mengarang angka, biaya, durasi, nama fitur, atau kebijakan yang tidak tertulis di CONTEXT.

### CONTEXT
{context}

### PERTANYAAN PELANGGAN
{query}

### FORMAT JAWABAN
- Maksimal 4 kalimat, natural dan langsung ke inti.
- Jika jawabannya berupa langkah-langkah, gunakan daftar bernomor.
- Jangan menyebut kata "CONTEXT" atau "dokumen" kepada pelanggan.
- Akhiri dengan satu baris: "Sumber: FAQ #<id>" (pisahkan dengan koma bila lebih dari satu), atau "Sumber: -" jika tidak ada FAQ yang relevan.
"""


def build_prompt(query: str, search_results: list[dict]) -> str:
    context = "\n\n".join(
        f"[FAQ #{r['faq_id']} | Kategori: {r['category']} | Skor kemiripan: {r['score']:.3f}]\n"
        f"Pertanyaan: {r['question']}\nJawaban: {r['answer']}"
        for r in search_results
    )
    return PROMPT_TEMPLATE.format(context=context, query=query)


def call_llm(prompt: str, retries: int = 3) -> str:
    for attempt in range(retries):
        try:
            response = get_client().models.generate_content(
                model=LLM_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.2),
            )
            return (response.text or "").strip()
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt * 5)
    return ""


def generate_answer(query: str, index: faiss.Index, df: pd.DataFrame, top_k: int = TOP_K) -> tuple[str, list[dict]]:
    """Satu alur penuh: query -> retrieval -> prompt -> jawaban LLM."""
    results = semantic_search(query, index, df, top_k=top_k)
    answer = call_llm(build_prompt(query, results))
    return answer, results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="FAQ semantic search + LLM")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build", help="Embed knowledge base dan simpan index FAISS")
    for name in ("search", "ask"):
        p = sub.add_parser(name)
        p.add_argument("query")
        p.add_argument("--top-k", type=int, default=TOP_K)
    args = parser.parse_args()

    if args.cmd == "build":
        df = load_knowledge_base()
        print(f"Total entri: {len(df)} | Kategori: {df['category'].nunique()}")
        save_index(build_index(df), df)
        return

    index, df = load_index()
    if args.cmd == "search":
        for r in semantic_search(args.query, index, df, args.top_k):
            print(f"#{r['rank']}  score={r['score']:.4f}  [FAQ {r['faq_id']} - {r['category']}] {r['question']}")
    else:
        answer, results = generate_answer(args.query, index, df, args.top_k)
        print(answer)
        print("\nRetrieved:", ", ".join(f"FAQ {r['faq_id']} ({r['score']:.3f})" for r in results))


if __name__ == "__main__":
    main()
