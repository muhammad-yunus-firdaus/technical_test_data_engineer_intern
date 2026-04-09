# Technical Test

sebuah *Web Crawler* berbasis Python untuk berita Bisnis.com. Proyek ini dikembangkan sebagai bagian dari pemenuhan tugas *Technical Test* untuk posisi **Data Engineer Intern**.

## Fungsi Dasar
Proyek ini memiliki dua mode operasi utama:
1. **Mode Backtrack (`backtrack.py`):** Berfungsi untuk menarik data historis. Crawler akan menelusuri halaman indeks berita berdasarkan rentang waktu (*start date* & *end date*) yang diinputkan, memfilter artikel agar sesuai dengan rentang tanggal tersebut, dan menyimpannya dalam format JSON.

2. **Mode Standard (`standard.py`):** Berfungsi sebagai program yang berjalan terus-menerus di latar belakang. Crawler akan mengecek halaman utama 
bisnis.com secara berkala sesuai interval waktu yang ditentukan, mengambil artikel , dan menyimpannya ke dalam JSON.

## Arsitektur
Arsitektur dibagi menjadi 2:

(`core/scraper.py`): Berisi *Class* `BisnisScraper` yang bertindak sebagai modul dasar utama. Semua logika ekstraksi HTML (menggunakan `BeautifulSoup`), pembersihan teks , dan format *export* JSON.

 (`backtrack.py` & `standard.py`):** Bertindak sebagai pengeksekusi. Keduanya hanya mengelola *looping* waktu, penangkapan parameter terminal (`argparse`), dan *routing* URL, lalu mendelegasikan tugas ekstraksi datanya ke modul utama.

## Video Demonstrasi
Untuk melihat bagaimana crawler ini bekerja secara langsung, silakan tonton video demonstrasi singkat berikut:
 **https://drive.google.com/drive/folders/18H6a5Ju60W7-mTRwFWqcpa4Jlq8YPRls?usp=sharing)**
