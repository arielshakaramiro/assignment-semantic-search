# Hasil Pengujian Retrieval & Respons LLM

Embedding model: `gemini-embedding-001` · LLM: `gemini-flash-latest` · top-k = 3 · skor = cosine similarity

## Rincian per Query

### Q1 · Langsung

**Query:** Metode pembayaran apa saja yang tersedia?  
**FAQ yang diharapkan:** #17

| Rank | Skor | FAQ | Kategori | Pertanyaan FAQ | Relevan |
|---|---|---|---|---|---|
| 1 | 0.796 | #17 | Pembayaran | Metode pembayaran apa saja yang tersedia? | ✅ |
| 2 | 0.726 | #22 | Pembayaran | Apakah bisa membayar menggunakan lebih dari satu metode sekaligus? | – |
| 3 | 0.706 | #20 | Pembayaran | Apakah saya bisa membayar dengan cicilan? | – |

**Jawaban LLM:**

> Halo! Saat ini kami menyediakan metode pembayaran melalui transfer bank, kartu kredit/debit, e-wallet, serta pembayaran melalui minimarket rekanan. Silakan pilih metode yang paling nyaman untuk transaksi Anda, ya.
>
> Sumber: FAQ #17

### Q2 · Langsung

**Query:** Bagaimana cara membatalkan pesanan?  
**FAQ yang diharapkan:** #3

| Rank | Skor | FAQ | Kategori | Pertanyaan FAQ | Relevan |
|---|---|---|---|---|---|
| 1 | 0.780 | #3 | Pemesanan | Bagaimana cara membatalkan pesanan yang sudah dibuat? | ✅ |
| 2 | 0.714 | #24 | Pengembalian | Bagaimana prosedur pengembalian barang yang tidak sesuai? | – |
| 3 | 0.703 | #8 | Pemesanan | Kenapa pesanan saya otomatis dibatalkan sistem? | – |

**Jawaban LLM:**

> Halo! Kamu dapat membatalkan pesanan melalui halaman 'Pesanan Saya' selama status pesanan masih 'Diproses'. Mohon diperhatikan bahwa setelah status berubah menjadi 'Dikirim', pembatalan sudah tidak dapat dilakukan lagi.
>
> Sumber: FAQ #3

### Q3 · Parafrase

**Query:** Saldo saya sudah kepotong tapi orderan masih tertulis belum dibayar, gimana nih?  
**FAQ yang diharapkan:** #21

| Rank | Skor | FAQ | Kategori | Pertanyaan FAQ | Relevan |
|---|---|---|---|---|---|
| 1 | 0.804 | #21 | Pembayaran | Kenapa pembayaran saya berhasil dipotong tapi status pesanan masih belum terbayar? | ✅ |
| 2 | 0.709 | #8 | Pemesanan | Kenapa pesanan saya otomatis dibatalkan sistem? | – |
| 3 | 0.706 | #19 | Pembayaran | Berapa lama batas waktu pembayaran sebelum pesanan dibatalkan? | – |

**Jawaban LLM:**

> Halo, mohon maaf atas ketidaknyamanan yang dialami. Hal ini biasanya terjadi karena adanya keterlambatan sinkronisasi pada sistem pembayaran. Silakan tunggu 15-30 menit atau hubungi customer service jika status pesanan masih belum berubah.
>
> Sumber: FAQ #21

### Q4 · Parafrase

**Query:** Barang yang datang beda sama yang saya beli  
**FAQ yang diharapkan:** #54, #24

| Rank | Skor | FAQ | Kategori | Pertanyaan FAQ | Relevan |
|---|---|---|---|---|---|
| 1 | 0.799 | #54 | Pengembalian | Saya menerima barang yang salah, apa yang harus saya lakukan? | ✅ |
| 2 | 0.737 | #24 | Pengembalian | Bagaimana prosedur pengembalian barang yang tidak sesuai? | ✅ |
| 3 | 0.715 | #30 | Pengembalian | Apakah bisa menukar barang dengan ukuran/warna lain daripada refund? | – |

**Jawaban LLM:**

> Mohon maaf atas ketidaknyamanan yang Anda alami, silakan ikuti langkah-langkah berikut:
> 1. Buka menu 'Pesanan Saya' dan ajukan komplain 'Barang Tidak Sesuai'.
> 2. Sertakan bukti foto barang yang diterima untuk mempercepat proses verifikasi.
> Pastikan pengajuan pengembalian ini dilakukan maksimal 3 hari sejak barang diterima.
>
> Sumber: FAQ #24, FAQ #54

### Q5 · Parafrase

**Query:** Bisa nyicil nggak kalau belanja di sini?  
**FAQ yang diharapkan:** #20

| Rank | Skor | FAQ | Kategori | Pertanyaan FAQ | Relevan |
|---|---|---|---|---|---|
| 1 | 0.797 | #20 | Pembayaran | Apakah saya bisa membayar dengan cicilan? | ✅ |
| 2 | 0.700 | #22 | Pembayaran | Apakah bisa membayar menggunakan lebih dari satu metode sekaligus? | – |
| 3 | 0.695 | #17 | Pembayaran | Metode pembayaran apa saja yang tersedia? | – |

**Jawaban LLM:**

> Halo Kak, bisa ya! Fitur cicilan tersedia untuk transaksi menggunakan kartu kredit tertentu dengan nominal minimal yang ditentukan oleh pihak bank. 
>
> Sumber: FAQ #20

### Q6 · Parafrase

**Query:** Saya kelupaan kata sandi jadi tidak bisa masuk ke akun  
**FAQ yang diharapkan:** #32, #55

| Rank | Skor | FAQ | Kategori | Pertanyaan FAQ | Relevan |
|---|---|---|---|---|---|
| 1 | 0.778 | #32 | Akun | Saya lupa password akun, bagaimana cara mengaturnya ulang? | ✅ |
| 2 | 0.748 | #55 | Akun | Kenapa akun saya tiba-tiba tidak bisa login? | ✅ |
| 3 | 0.676 | #36 | Akun | Apakah data pribadi saya aman di platform ini? | – |

**Jawaban LLM:**

> Halo, Kak. Jangan khawatir, Anda dapat mengatur ulang kata sandi akun Anda dengan langkah-langkah berikut:
>
> 1. Klik 'Lupa Password' pada halaman login.
> 2. Masukkan email terdaftar.
> 3. Ikuti instruksi reset password yang dikirim ke email Anda.
>
> Sumber: FAQ #32

### Q7 · Di luar KB

**Query:** Apakah bisa bayar pakai Bitcoin atau crypto lainnya?  
**FAQ yang diharapkan:** tidak ada (di luar KB)

| Rank | Skor | FAQ | Kategori | Pertanyaan FAQ | Relevan |
|---|---|---|---|---|---|
| 1 | 0.706 | #17 | Pembayaran | Metode pembayaran apa saja yang tersedia? | – |
| 2 | 0.677 | #22 | Pembayaran | Apakah bisa membayar menggunakan lebih dari satu metode sekaligus? | – |
| 3 | 0.673 | #18 | Pembayaran | Apakah ada biaya tambahan untuk pembayaran menggunakan kartu kredit? | – |

**Jawaban LLM:**

> Halo, terima kasih telah menghubungi kami. Maaf, informasi tersebut belum tersedia di FAQ kami. Silakan hubungi customer service kami untuk mendapatkan bantuan dan informasi lebih lanjut mengenai metode pembayaran tersebut.
>
> Sumber: -

### Q8 · Di luar KB

**Query:** Jam berapa toko offline kalian buka di Jakarta?  
**FAQ yang diharapkan:** tidak ada (di luar KB)

| Rank | Skor | FAQ | Kategori | Pertanyaan FAQ | Relevan |
|---|---|---|---|---|---|
| 1 | 0.635 | #43 | Produk | Apakah stok yang tertera di aplikasi selalu update secara real-time? | – |
| 2 | 0.632 | #9 | Pengiriman | Berapa lama estimasi waktu pengiriman barang? | – |
| 3 | 0.629 | #58 | Pemesanan | Apakah bisa memesan dalam jumlah besar untuk kebutuhan reseller? | – |

**Jawaban LLM:**

> Halo! Maaf, informasi tersebut belum tersedia di FAQ kami. Silakan hubungi tim customer service kami untuk bantuan dan informasi lebih lanjut.
>
> Sumber: -

## Analisis Relevansi

### Ringkasan Hasil

| ID | Tipe | Query | Top-3 FAQ (skor cosine) | Hit@1 | Respons LLM |
|---|---|---|---|---|---|
| Q1 | Langsung | Metode pembayaran apa saja yang tersedia? | **17** (0.796), 22 (0.726), 20 (0.706) | ✅ | Tepat, menyebut 4 metode dari FAQ #17 |
| Q2 | Langsung | Bagaimana cara membatalkan pesanan? | **3** (0.780), 24 (0.714), 8 (0.703) | ✅ | Tepat, termasuk syarat status 'Diproses' |
| Q3 | Parafrase | Saldo saya sudah kepotong tapi orderan masih tertulis belum dibayar, gimana nih? | **21** (0.804), 8 (0.709), 19 (0.706) | ✅ | Tepat, "tunggu 15–30 menit" sesuai FAQ |
| Q4 | Parafrase | Barang yang datang beda sama yang saya beli | **54** (0.799), **24** (0.737), 30 (0.715) | ✅ | Menggabungkan FAQ #54 + #24 menjadi langkah bernomor |
| Q5 | Parafrase | Bisa nyicil nggak kalau belanja di sini? | **20** (0.797), 22 (0.700), 17 (0.695) | ✅ | Tepat, syarat kartu kredit dan nominal minimal |
| Q6 | Parafrase | Saya kelupaan kata sandi jadi tidak bisa masuk ke akun | **32** (0.778), **55** (0.748), 36 (0.676) | ✅ | Tepat, 3 langkah reset password |
| Q7 | Di luar KB | Apakah bisa bayar pakai Bitcoin atau crypto lainnya? | 17 (0.706), 22 (0.677), 18 (0.673) | – | Menolak dengan jujur, mengarahkan ke CS |
| Q8 | Di luar KB | Jam berapa toko offline kalian buka di Jakarta? | 43 (0.635), 9 (0.632), 58 (0.629) | – | Menolak dengan jujur, mengarahkan ke CS |

**Metrik retrieval (6 query yang ada jawabannya):** Hit@1 = **100%**, Hit@3 = **100%**. Rata-rata skor top-1: **0.792** untuk query yang ada jawabannya, **0.671** untuk query di luar KB.

### Analisis

**1. Semantic search menangkap makna, bukan sekadar kata kunci.**
Keempat query parafrase memakai bahasa informal dan sinonim yang hampir tidak berbagi kata dengan FAQ, tetapi semuanya tetap tepat di peringkat 1:
- Q3: *"saldo kepotong"*, *"orderan"* → FAQ #21 *"pembayaran berhasil dipotong"*, *"status pesanan"*. Skor top-1 justru yang tertinggi dari semua query (0.804).
- Q5: slang *"nyicil"* → FAQ #20 *"cicilan"* (0.797).
- Q6: *"kata sandi"*, *"masuk"* → FAQ #32 *"password"*, *"login"*. Ini padanan lintas bahasa (Indonesia–Inggris) yang tidak mungkin tertangkap pencarian kata kunci biasa.
- Q4 dan Q6 masing-masing punya dua FAQ relevan, dan **keduanya masuk top-2**.

**2. Pemisahan peringkat cukup jelas.** Selisih skor top-1 dengan top-2 adalah 0.06–0.10 (Q1 0.070, Q2 0.066, Q3 0.095, Q5 0.097). Pengecualiannya Q6 (0.030), tetapi di sana FAQ #2 (#55, akun tidak bisa login) memang juga relevan.

**3. Masih ada noise di peringkat 2–3.** Pada Q2 ("membatalkan pesanan"), peringkat 2 justru FAQ #24 (*prosedur pengembalian barang*, kategori lain), di atas FAQ #8 (*pesanan otomatis dibatalkan*) yang lebih dekat topiknya. Embedding menganggap "membatalkan" dan "mengembalikan" berdekatan secara semantik. Noise ini tidak merusak jawaban karena aturan Task #2 ("pakai hanya FAQ yang benar-benar menjawab") membuat LLM mengabaikan FAQ tersebut. Dengan kata lain, LLM ikut berperan sebagai filter relevansi.

**4. Query di luar KB: retrieval tetap mengembalikan hasil, LLM yang menolak.**
FAISS selalu mengembalikan *k* hasil terdekat dan tidak punya konsep "tidak ada jawaban":
- Q7 (crypto) mengambil FAQ seputar pembayaran dengan skor 0.706. Topiknya dekat, tetapi tidak menjawab. Ini kasus paling menjebak: dari sisi retrieval terlihat "cukup relevan".
- Q8 (jam toko offline) mengambil FAQ yang tidak berhubungan (stok, estimasi kirim, reseller) dengan skor terendah 0.635.

Pada kedua kasus LLM **tidak berhalusinasi**. LLM tidak mengarang "kami tidak menerima crypto" atau jam buka, melainkan menjawab dengan kalimat penolakan sesuai prompt dan mencantumkan `Sumber: -`. Namun pada Q7 jawabannya **terlalu konservatif**. Sebenarnya LLM bisa menyebutkan metode yang tersedia (FAQ #17) dan menjelaskan bahwa crypto tidak tercantum, sesuai aturan Task #4 (jawaban parsial), tetapi aturan itu tidak diterapkan.

**5. Skor cosine terkompresi, jadi nilai absolutnya harus dibaca relatif.** Teks yang tidak berhubungan sama sekali (Q8) masih mendapat skor ±0.63, sementara FAQ yang tepat ±0.78–0.80. Pada sampel ini, ambang ±0.75 sudah memisahkan query yang ada jawabannya (min 0.778) dari yang di luar KB (maks 0.706). Tetapi 8 query terlalu sedikit untuk menetapkan ambang. Q7 menunjukkan query di luar KB yang topiknya bertetangga bisa mendekati skor query yang relevan.

**6. Kualitas jawaban LLM: grounded dan bisa ditelusuri.** Setiap fakta di jawaban sudah dicocokkan dengan teks FAQ asli: "15–30 menit" (Q3 → FAQ #21), "maksimal 3 hari sejak barang diterima" (Q4 → FAQ #24), langkah reset password (Q6 → FAQ #32). Tidak ada angka atau kebijakan yang dikarang. Kedelapan jawaban mencantumkan sumber, dan format daftar bernomor dipakai saat jawabannya berupa langkah (Q4, Q6). Pada Q4, LLM menggabungkan dua FAQ (komplain "Barang Tidak Sesuai" dari #54 dan batas 3 hari dari #24) lalu mengutip keduanya. Ini sintesis yang membantu, tetapi berisiko kecil mencampur dua kebijakan yang sebenarnya berbeda (komplain vs pengembalian).

**7. Kelemahan gaya:** sapaan tidak konsisten antar jawaban ("Kak", "Kamu", "Anda", bahkan campur dalam satu jawaban di Q6), karena Persona tidak menetapkan kata ganti.

**8. Catatan operasional:** selama pengujian, API Gemini beberapa kali mengembalikan `503 UNAVAILABLE` (high demand). Mekanisme retry dengan backoff di `call_llm()` berhasil menanganinya sehingga notebook tetap selesai tanpa error.


## Keterbatasan Sistem

1. **Tidak ada ambang relevansi.** FAISS selalu mengembalikan top-k meskipun tidak ada yang relevan (Q7, Q8), sehingga penolakan sepenuhnya bergantung pada kepatuhan LLM terhadap prompt. Untuk produksi perlu ambang skor yang dikalibrasi sebagai lapisan pengaman kedua.
2. **Skor cosine terkompresi** (±0.63 untuk teks tak berhubungan, ±0.80 untuk yang tepat). Skor tidak bisa dibaca sebagai probabilitas dan perlu kalibrasi dengan set uji yang lebih besar.
3. **Evaluasi masih kecil:** 8 query dengan label relevansi manual. Deteksi penolakan (`llm_says_unavailable`) memakai pencocokan string, sehingga belum menilai kualitas jawaban secara otomatis.
4. **Noise antar kategori** di peringkat bawah (Q2: FAQ pengembalian muncul untuk query pembatalan). Belum ada re-ranking atau hybrid search (BM25 + vektor) untuk mempertajam urutan.
5. **LLM terlalu konservatif untuk jawaban parsial** (Q7): langsung menolak padahal sebagian informasi tersedia. Sapaan juga tidak konsisten.
6. **Penggabungan beberapa FAQ** bisa mencampur kebijakan yang berbeda (Q4).
7. **Knowledge base kecil dan statis** (59 entri, jawaban umum seperti "biasanya"). Tidak terhubung ke data transaksi, sehingga tidak bisa menjawab kasus spesifik seperti status pesanan tertentu. Setiap perubahan FAQ memerlukan embedding ulang.
8. **Single-turn**, tanpa memori percakapan, sehingga pertanyaan lanjutan ("kalau yang tadi gimana?") tidak bisa dipahami.
9. **Ketergantungan pada API eksternal:** ada error 503 dan rate limit. Alias `gemini-flash-latest` bisa berpindah versi sehingga jawaban bisa berubah antar run. Untuk hasil yang reproducible, versi model sebaiknya di-pin.

**Arah pengembangan (menuju RAG penuh):** ambang skor + fallback ke CS, hybrid search, re-ranker, penetapan sapaan di Persona, contoh jawaban parsial (few-shot), evaluasi lebih besar (mis. LLM-as-judge untuk faithfulness), dan pin versi model.
