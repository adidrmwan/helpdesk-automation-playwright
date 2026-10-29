# Helpdesk QA Automation (GoatFlow)

Automated test untuk aplikasi helpdesk [GoatFlow](https://goatflow.io), dibuat dengan **Playwright + Python + pytest**
memakai **Page Object Model**. Test berjalan di Customer Portal demo publik GoatFlow: login, membuat tiket,
validasi form, pencarian dan filter, sampai perjalanan tiket dari dibuat hingga ditutup.

> 19 automated test · smoke / functional / end-to-end · positive & negative · laporan Allure dengan screenshot dan trace

## Yang diuji

| Area | Contoh | File |
|---|---|---|
| **Smoke** (5) | halaman login terbuka, pengunjung tanpa login diarahkan ke login | `tests/smoke/test_smoke.py` |
| **Login** (3) | akun benar, password salah, kolom kosong | `tests/functional/test_login.py` |
| **Form tiket** (6) | tiket valid, prioritas, subject kosong, pesan kosong (server 400), batas 255 karakter | `tests/functional/test_create_ticket.py` |
| **Cari & filter** (3) | cari judul, tidak ada hasil, filter open/closed | `tests/functional/test_search_ticket.py` |
| **End-to-end** (2) | buat → balas → tutup → tidak bisa dibalas lagi; balasan kosong ditolak | `tests/e2e/test_customer_workflow.py` |

Daftar test case lengkap (ID, langkah, data, hasil yang diharapkan): [`docs/test-cases.md`](docs/test-cases.md).

## Struktur project

```
helpdesk-qa-automation/
├── docs/test-cases.md        # test scenario dan test case
├── tests/
│   ├── config.py             # BASE_URL + akun demo
│   ├── conftest.py           # fixture, urutan test, lampiran Allure
│   ├── helpers.py            # unique_title()
│   ├── pages/                # Page Object Model: satu class per halaman
│   ├── smoke/  functional/  e2e/
├── debug_demo/               # 4 test yang sengaja rusak, untuk latihan debugging
├── examples/01_first_script.py
├── .github/workflows/tests.yml   # GitHub Actions
├── pytest.ini   requirements.txt   .env.example   .gitignore
```

## Instalasi

Butuh **Python 3.9 atau lebih baru**. Pakai `python -m ...` supaya yang terpanggil selalu pytest dan Playwright di dalam venv.

```bash
# macOS / Linux                         # Windows (PowerShell)
python3 -m venv .venv                    # python -m venv .venv
source .venv/bin/activate                # .venv\Scripts\Activate.ps1

pip install -r requirements.txt
python -m playwright install chromium

python -m pytest
```

Hasil yang diharapkan: `19 passed`.

## Menjalankan

| Tujuan | Perintah |
|---|---|
| Semua test (urutan: smoke → functional → e2e) | `python -m pytest` |
| Hanya smoke / functional / e2e | `python -m pytest -m smoke` · `-m functional` · `-m e2e` |
| Hanya negative test | `python -m pytest -m negative` |
| Berhenti di kegagalan pertama | `python -m pytest -x` |
| Ulangi hanya yang gagal tadi | `python -m pytest --lf` |
| Lihat browser bergerak | `python -m pytest --headed --slowmo 500` |

## Laporan dan debugging

Setiap run menghasilkan tiga hal:

| Hasil | Lokasi | Cara membuka |
|---|---|---|
| **Laporan Allure** | `allure-results/` | `allure serve allure-results` |
| Laporan HTML sederhana | `reports/report.html` | buka langsung di browser |
| Trace test yang gagal | `test-results/<nama-test>/trace.zip` | `python -m playwright show-trace <file>` |

Di laporan Allure, setiap test yang gagal punya:

- **langkah-langkah** (contoh: "Langkah 3: customer menutup tiket"), sehingga terlihat di langkah mana test gagal;
- **screenshot** halaman saat gagal, **alamat halaman**, dan **trace.zip**;
- status **failed** (assertion gagal, kemungkinan bug aplikasi) atau **broken** (langkah test tidak bisa jalan, misalnya locator salah).

### Memasang Allure (sekali saja)

Allure butuh **Java 8 atau lebih baru**.

| Sistem | Perintah |
|---|---|
| macOS | `brew install allure` (Java ikut terpasang) |
| Windows | `scoop install allure` (pasang Java dulu, misalnya `scoop install temurin-lts-jdk`) |
| Semua sistem dengan Node.js | `npx allure-commandline serve allure-results` (tanpa install) |

Lalu:

```bash
python -m pytest
allure serve allure-results                                   # langsung membuka laporan di browser
# atau
allure generate allure-results -o allure-report --clean
allure open allure-report
```

File `allure-report/index.html` tidak bisa dibuka dengan klik dua kali. Pakai `allure open` atau `allure serve`.

### Latihan debugging

```bash
python -m pytest debug_demo --tracing=on
allure serve allure-results
```

Empat test di `debug_demo/` sengaja rusak: locator salah, ekspektasi salah, strict mode violation, dan langkah yang terlewat.
Kunci jawabannya ada di bagian bawah file itu.

## Keputusan desain

- **Page Object Model**: locator ada di `tests/pages/`; test terbaca seperti cerita, dan perubahan tampilan cukup diperbaiki di satu tempat.
- **Locator yang stabil**: `get_by_role` dan `get_by_label` dulu; id atau atribut form kalau perlu.
- **Web-first assertion**: `expect(...)` menunggu otomatis (maksimal 15 detik), tanpa `sleep()`.
- **Data uji sendiri**: setiap test membuat tiket dengan judul unik (`[QA-AUTO 48213] ...`), jadi test tidak bergantung pada data orang lain atau urutan test.
- **Urutan cepat dulu**: smoke → functional → e2e.

## Batasan

- Test berjalan di demo publik yang dipakai bersama; satu run penuh membuat 7 tiket. Jangan menjalankan test dalam loop.
- Tiket buatan test tidak dihapus (customer tidak bisa menghapus tiket); demo direset setiap hari pukul 02:00 UTC.
- Setiap test login ulang. Lebih sederhana, tapi lebih lambat. Langkah lanjut: simpan sesi login dengan `storage_state`.

## Continuous integration

`.github/workflows/tests.yml` menjalankan **smoke test** di setiap push ke `main`, dan **semua test** saat dijalankan
manual (tab Actions → Run workflow). Laporan dan trace bisa diunduh dari halaman hasil run.

## Kredit

Target pengujian: [GoatFlow](https://github.com/goatkit/goatflow) (Apache 2.0). Akun demo yang dipakai adalah akun publik
dari https://goatflow.io/demo.
