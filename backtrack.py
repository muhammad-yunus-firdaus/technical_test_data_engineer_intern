import argparse
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from core.scraper import BisnisScraper

def main():
    #Menyiapkan parameter untuk menerima input tanggal
    parser = argparse.ArgumentParser(description="Backtrack Crawler untuk bisnis.com")
    parser.add_argument('--start', required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument('--end', required=True, help="End date (YYYY-MM-DD)")
    args = parser.parse_args()

    print(f"Memulai mode Backtrack dari {args.start} sampai {args.end}...")
    #memanggil modul 
    scraper = BisnisScraper()
    
    try:
        start_date = datetime.strptime(args.start, "%Y-%m-%d")
        end_date = datetime.strptime(args.end, "%Y-%m-%d")
        end_date_filter = end_date.replace(hour=23, minute=59, second=59)
    except ValueError:
        print("Error: Format tanggal salah! Gunakan format YYYY-MM-DD.")
        return

    #menggunakan set agar tidak ada artikel yang duplikat
    urls_to_scrape = set() 
    current_date = start_date
    delta = timedelta(days=1)

    print("\nMencari daftar link artikel dari halaman Indeks")
    #proses looping agar berjalan dari tanggal mulai hingga tanggal akhir
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        print(f"{date_str}")
        
        #menelusuri halaman bisnis.com berdasarkan indeks
        index_url = f"https://www.bisnis.com/index?date={date_str}"
        
        try:
            #membuka dan meminta requests ke halaman indeks untuk tanggal tertentu
            response = requests.get(index_url, headers=scraper.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # mencari semua tag link <a> di halaman berita
            for a_tag in soup.find_all('a', href=True):
                url = a_tag['href']
                if "/read/" in url and url.startswith("https"):
                    urls_to_scrape.add(url)
                    
        except Exception as e:
            print(f"Gagal mengambil indeks {date_str}: {e}")
            
        current_date += delta
        
    print(f"\nDitemukan total {len(urls_to_scrape)}")
    print("\nMemulai proses scraping isi artikel...")
    results = []

    #proses pengambilan dan pengumpulan data,jika data artikel nya ada akan di cek rentang tanggalnya apakah tanggalnya sesuai dengan yang diminta
    for url in list(urls_to_scrape):
        article_data = scraper.scrape_article(url)
        
        if article_data:
            pub_date_str = article_data["tanggal_terbit"][:10]
            try:
                pub_date = datetime.strptime(pub_date_str, "%Y-%m-%d")
                
                if start_date <= pub_date <= end_date_filter:
                    print(f" [OK] {url}")
                    results.append(article_data)
                else:
                    print(f" {url} (Di luar rentang tanggal)")
            except ValueError:
                pass
    
    #Setelah proses pengecekan selesai, maka hasilnya akan disimpan ke dalam JSON
    if results:
        output_filename = f"backtrack {args.start}_{args.end}.json"
        scraper.save_to_json(results, output_filename)
        print(f"\nSukses! {len(results)} data berhasil disimpan.")
    else:
        print("\nTidak ada data yang berhasil diambil pada rentang tanggal tersebut.")

if __name__ == "__main__":
    main()