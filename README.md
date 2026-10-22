# Semantic Search & LLM Application: E-Commerce FAQ Assistant

A customer service assistant prototype that retrieves the most relevant FAQ entries **semantically** (by meaning, not keyword matching) and then uses an LLM to compose a natural answer based **only** on the retrieved FAQs. This prototype is the foundation for a full RAG (Retrieval-Augmented Generation) system.

**Stack:** Python · Pandas · Gemini Embeddings API · FAISS · Gemini API

---

## 1. Problem Statement

### Objective
An e-commerce customer service team receives hundreds of repetitive questions every day about ordering, shipping, payment, and returns. This prototype aims to:

1. **Find the most relevant FAQ** for a customer question, even when the customer uses different words, synonyms, or informal language than the FAQ text.
2. **Generate natural and accurate answers** with an LLM that stay grounded in the official FAQ, so the system never invents policies.
3. **Admit when it doesn't know**: if a question is not covered by the FAQ, say so and refer the customer to customer service.

### Knowledge Base Source & Structure
- File: `data/ecommerce_faq_knowledge_base.csv` (provided by the program, **left unmodified**)
- **59 FAQ entries** in Indonesian, 4 columns:

| Column | Description |
|---|---|
| `faq_id` | Unique entry ID (1–59) |
| `category` | One of 8 categories |
| `question` | FAQ question |
| `answer` | Official answer (1–2 sentences) |

| Category | Entries |
|---|---|
| Pemesanan (Ordering) | 9 |
| Pengiriman (Shipping) | 9 |
| Pembayaran (Payment) | 8 |
| Pengembalian (Returns) | 8 |
| Akun (Account) | 7 |
| Produk (Product) | 7 |
| Promo (Promotions) | 6 |
| Customer Service | 5 |

### Constraints & Assumptions
- The system **answers only from the available FAQ**. The LLM's general knowledge must not be used as a source of facts.
- One FAQ entry = one retrieval unit. Entries are short, so **no chunking** is applied.
- The system is not connected to customer transaction data (order status, tracking numbers, etc.), so it only provides general policy information.
- Input and output language: Indonesian, including informal style.
- The prototype is single-turn (no conversation memory) and does not yet use re-ranking or hybrid search.

---

## 2. Architecture & System Flow

```
               ┌──────────────────────── OFFLINE (once) ──────────────────────────┐
  FAQ CSV ──►  │ INGEST           EMBED                         STORE               │
               │ Pandas: merge    Gemini Embeddings             FAISS IndexFlatIP   │
               │ category+Q+A ──► task=RETRIEVAL_DOCUMENT ──►   (cosine) ──► disk   │
               └───────────────────────────────────────────────────────────────────┘
               ┌──────────────────────── ONLINE (per query) ──────────────────────┐
  Question ──► │ RETRIEVE                               GENERATE                  │
               │ embed query (RETRIEVAL_QUERY) ──►      Persona/Task/Context/      │
               │ FAISS top-3 + cosine score       ──►   Format prompt ──► Gemini   │ ──► Answer + FAQ source
               └───────────────────────────────────────────────────────────────────┘
```

| Stage | Implementation | Design decision |
|---|---|---|
| **Ingest** | `pd.read_csv`, then a `content` column = `Category + Question + Answer` | Answers are embedded too, because many key terms (e.g. *Virtual Account*, *resi*/tracking number) appear only in the answer. The category adds a topic signal. |
| **Embed** | `gemini-embedding-001`, batched requests | Separate `task_type`: `RETRIEVAL_DOCUMENT` for FAQs, `RETRIEVAL_QUERY` for questions (asymmetric retrieval). Vectors are L2-normalized. |
| **Store** | `faiss.IndexFlatIP`, saved to `vector_store/faq.index` and `faq_metadata.json` | With normalized vectors, inner product = **cosine similarity** (an easy-to-read 0–1 score). Exact search is sufficient for 59 entries. Verified with `index.ntotal == len(df)`. |
| **Retrieve** | `semantic_search(query, top_k=3)` | Returns rank, ID, category, question, answer, and score. |
| **Generate** | `build_prompt()` then `generate_answer()` using `gemini-flash-latest`, temperature 0.2 | Structured prompt (see below). Low temperature keeps answers consistent rather than "creative". |

### Prompt Design

| Section | Content |
|---|---|
| **Persona** | "Asisten CS", a friendly, polite, empathetic e-commerce assistant that replies in Indonesian |
| **Task** | 5 rules: (1) use only the Context; (2) use only the relevant FAQs, since not every top-3 result is relevant; (3) if the answer is not there, reply *"Maaf, informasi tersebut belum tersedia di FAQ kami."* ("Sorry, that information is not yet available in our FAQ.") and refer to customer service; (4) if only partially covered, explain which part is missing; (5) never invent numbers, fees, or policies |
| **Context** | Top-3 FAQs formatted as `[FAQ #id \| Category \| Similarity score]` + question + answer |
| **Format** | Max. 4 sentences, numbered list for steps, end with `Sumber: FAQ #id` so every answer is traceable |

---

## 3. Test Results & Relevance Analysis

Models: `gemini-embedding-001` (3072 dimensions) and `gemini-flash-latest`. Eight test queries: 2 direct, 4 paraphrased/informal, and 2 outside the knowledge base. Queries are in Indonesian (English meaning in italics). Full answers for each query are in [`documentation/retrieval_test_results.md`](documentation/retrieval_test_results.md); raw output is in `documentation/test_results_raw.json`.

### Results Summary

| ID | Type | Query | Top-3 FAQ (cosine score) | Hit@1 | LLM response |
|---|---|---|---|---|---|
| Q1 | Direct | Metode pembayaran apa saja yang tersedia? *(What payment methods are available?)* | **17** (0.796), 22 (0.726), 20 (0.706) | ✅ | Correct, lists the 4 methods from FAQ #17 |
| Q2 | Direct | Bagaimana cara membatalkan pesanan? *(How do I cancel an order?)* | **3** (0.780), 24 (0.714), 8 (0.703) | ✅ | Correct, includes the 'Diproses' (Processing) status condition |
| Q3 | Paraphrase | Saldo saya sudah kepotong tapi orderan masih tertulis belum dibayar, gimana nih? *(My balance was deducted but the order still says unpaid, what now?)* | **21** (0.804), 8 (0.709), 19 (0.706) | ✅ | Correct, "wait 15–30 minutes" as stated in the FAQ |
| Q4 | Paraphrase | Barang yang datang beda sama yang saya beli *(The item I received is different from what I bought)* | **54** (0.799), **24** (0.737), 30 (0.715) | ✅ | Combines FAQ #54 + #24 into numbered steps |
| Q5 | Paraphrase | Bisa nyicil nggak kalau belanja di sini? *(Can I pay in installments here?)* | **20** (0.797), 22 (0.700), 17 (0.695) | ✅ | Correct, credit card and minimum amount conditions |
| Q6 | Paraphrase | Saya kelupaan kata sandi jadi tidak bisa masuk ke akun *(I forgot my password so I can't sign in)* | **32** (0.778), **55** (0.748), 36 (0.676) | ✅ | Correct, 3 password reset steps |
| Q7 | Out of KB | Apakah bisa bayar pakai Bitcoin atau crypto lainnya? *(Can I pay with Bitcoin or other crypto?)* | 17 (0.706), 22 (0.677), 18 (0.673) | – | Honestly declines, refers to customer service |
| Q8 | Out of KB | Jam berapa toko offline kalian buka di Jakarta? *(What time does your offline store in Jakarta open?)* | 43 (0.635), 9 (0.632), 58 (0.629) | – | Honestly declines, refers to customer service |

**Retrieval metrics (6 answerable queries):** Hit@1 = **100%**, Hit@3 = **100%**. Mean top-1 score: **0.792** for answerable queries vs **0.671** for out-of-KB queries.

### Analysis

**1. Semantic search captures meaning, not just keywords.**
All four paraphrased queries use informal language and synonyms that share almost no words with the FAQ, yet every one was retrieved correctly at rank 1:
- Q3: *"saldo kepotong"* (balance got cut), *"orderan"* (slang for order) → FAQ #21 *"pembayaran berhasil dipotong"* (payment was deducted), *"status pesanan"* (order status). This was the highest top-1 score of all queries (0.804).
- Q5: the slang *"nyicil"* → FAQ #20 *"cicilan"* (installments) (0.797).
- Q6: *"kata sandi"*, *"masuk"* (Indonesian for password, sign in) → FAQ #32 *"password"*, *"login"*. This is a cross-lingual (Indonesian–English) match that plain keyword search could never catch.
- Q4 and Q6 each have two relevant FAQs, and **both appear in the top 2**.

**2. Ranking separation is clear.** The gap between the top-1 and top-2 scores is 0.06–0.10 (Q1 0.070, Q2 0.066, Q3 0.095, Q5 0.097). The exception is Q6 (0.030), but there the rank-2 FAQ (#55, account cannot log in) is also relevant.

**3. There is still noise at ranks 2–3.** For Q2 ("cancel an order"), rank 2 is FAQ #24 (*return procedure*, a different category), ranked above FAQ #8 (*order automatically cancelled*), which is closer in topic. The embedding treats "membatalkan" (cancel) and "mengembalikan" (return) as semantically close. This noise does not hurt the answer because Task rule #2 ("use only the FAQs that actually answer the question") makes the LLM ignore that FAQ. In other words, the LLM also acts as a relevance filter.

**4. Out-of-KB queries: retrieval still returns results, the LLM does the declining.**
FAISS always returns the *k* nearest results and has no notion of "no answer":
- Q7 (crypto) retrieved payment-related FAQs with a score of 0.706. The topic is close but does not answer the question. This is the trickiest case: from the retrieval side it looks "fairly relevant".
- Q8 (offline store hours) retrieved unrelated FAQs (stock, delivery estimate, reseller orders) with the lowest score, 0.635.

In both cases the LLM **did not hallucinate**. It did not invent "we don't accept crypto" or opening hours; it replied with the decline sentence defined in the prompt and cited `Sumber: -` (no source). However, the Q7 answer is **too conservative**. The LLM could have listed the available methods (FAQ #17) and explained that crypto is not among them, per Task rule #4 (partial answers), but it did not apply that rule.

**5. Cosine scores are compressed, so absolute values must be read relatively.** Completely unrelated text (Q8) still scores about 0.63, while the correct FAQ scores about 0.78–0.80. In this sample, a threshold of about 0.75 would already separate answerable queries (min 0.778) from out-of-KB ones (max 0.706). But 8 queries are too few to set a threshold, and Q7 shows that an out-of-KB query on a neighboring topic can score close to relevant queries.

**6. LLM answer quality: grounded and traceable.** Every fact in the answers was checked against the original FAQ text: "15–30 minutes" (Q3 → FAQ #21), "within 3 days of receiving the item" (Q4 → FAQ #24), and the password reset steps (Q6 → FAQ #32). No numbers or policies were invented. All eight answers cite their source, and a numbered list is used when the answer consists of steps (Q4, Q6). In Q4 the LLM combined two FAQs (the "Barang Tidak Sesuai" (item not as described) complaint from #54 and the 3-day limit from #24) and cited both. This synthesis is helpful, but carries a small risk of mixing two policies that are actually different (complaint vs return).

**7. Style weakness:** forms of address are inconsistent across answers ("Kak", "Kamu", "Anda", even mixed within the Q6 answer), because the Persona does not specify a form of address.

**8. Operational note:** during testing the Gemini API returned `503 UNAVAILABLE` (high demand) several times. The retry-with-backoff logic in `call_llm()` handled it, so the notebook still finished without errors.

---

## 4. System Limitations

1. **No relevance threshold.** FAISS always returns the top-k even when nothing is relevant (Q7, Q8), so declining depends entirely on the LLM following the prompt. A production system needs a calibrated score threshold as a second safety layer.
2. **Compressed cosine scores** (about 0.63 for unrelated text, about 0.80 for correct matches). Scores cannot be read as probabilities and need calibration on a larger test set.
3. **Small evaluation:** 8 queries with manual relevance labels. Decline detection (`llm_says_unavailable`) uses string matching, so answer quality is not yet scored automatically.
4. **Cross-category noise** at lower ranks (Q2: a returns FAQ appears for a cancellation query). There is no re-ranking or hybrid search (BM25 + vectors) yet to sharpen the ordering.
5. **The LLM is too conservative with partial answers** (Q7): it declines outright even when part of the information is available. Forms of address are also inconsistent.
6. **Combining several FAQs** can blend different policies (Q4).
7. **Small, static knowledge base** (59 entries with general answers such as "biasanya" (usually)). It is not connected to transaction data, so it cannot answer specific cases such as the status of a particular order. Any FAQ change requires re-embedding.
8. **Single-turn** with no conversation memory, so follow-up questions ("what about the one before?") cannot be understood.
9. **Dependency on an external API:** 503 errors and rate limits occur. The `gemini-flash-latest` alias can move to a new version, so answers may change between runs. For reproducible results, the model version should be pinned.

**Next steps (toward full RAG):** a score threshold with fallback to customer service, hybrid search, a re-ranker, a fixed form of address in the Persona, few-shot examples of partial answers, a larger evaluation (e.g. LLM-as-judge for faithfulness), and pinned model versions.

---

## 5. Project Structure

```
assignment-semantic-search/
├── data/
│   └── ecommerce_faq_knowledge_base.csv        # original knowledge base (unmodified)
├── notebook/
│   └── starter_notebook_semantic_search.ipynb  # full pipeline + testing + analysis
├── src/
│   └── faq_search.py                           # script version: build index, search, ask (CLI)
├── vector_store/
│   ├── faq.index                               # FAISS index (59 vectors)
│   └── faq_metadata.json                       # mapping from vector position → FAQ entry
├── documentation/
│   ├── retrieval_test_results.md               # per-query test details
│   └── test_results_raw.json                   # raw test output
├── run_all.sh                                  # set up venv + run the notebook end to end
├── .env.example
├── requirements.txt
└── README.md
```

---

## 6. How to Run

**Prerequisites:** Python 3.10+ and a Gemini API key ([Google AI Studio](https://aistudio.google.com/apikey)).

```bash
# 1. Clone the repository
git clone https://github.com/arielshakaramiro/assignment-semantic-search.git
cd assignment-semantic-search

# 2. Create a virtual environment & install dependencies
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Add your API key
cp .env.example .env               # then set GEMINI_API_KEY in .env
```

### Option A: Notebook (full pipeline + testing)
```bash
jupyter notebook notebook/starter_notebook_semantic_search.ipynb
```
Run **Kernel → Restart & Run All**. Alternatively, run the whole notebook without opening Jupyter (this also creates the venv and installs dependencies):
```bash
bash run_all.sh
```
The notebook creates the embeddings, saves the index to `vector_store/`, runs the 8 test queries, and saves the results to `documentation/test_results_raw.json`.

### Option B: CLI script
```bash
python src/faq_search.py build                                   # ingest + embed + save FAISS index
python src/faq_search.py search "paket saya belum datang"        # show top-3 FAQs + scores
python src/faq_search.py ask "bisa bayar pakai cicilan?"         # LLM answer + sources
```

Models can be changed via `.env` (`EMBEDDING_MODEL`, `LLM_MODEL`). If you change the embedding model, run `build` again, because vectors from different models are not compatible.
