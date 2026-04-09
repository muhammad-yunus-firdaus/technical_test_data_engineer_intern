import time
import argparse
import requests
from bs4 import BeautifulSoup
from core.scraper import BisnisScraper

def main():
    #fungsi untuk menerima input jeda waktu di terminal
    parser = argparse.ArgumentParser(description="Standard Crawler (Long-Running) bisnis.com")
    parser.add_argument('--interval', type=int, default=60, help="Interval penarikan dalam detik (default: 60)")
    args = parser.parse_args()

    print(f"Mengambil artikel setiap {args.interval} detik")
    scraper = BisnisScraper()
    seen_urls = set()

    try:
        while True:
            print("Mengecek artikel terbaru")
            
            latest_urls = []
            try:
                current_time_ms = int(time.time() * 1000)
                url_homepage = f"https://www.bisnis.com/?t={current_time_ms}"
                
                homepage_response = requests.get(url_homepage, headers=scraper.headers, timeout=10)
                homepage_soup = BeautifulSoup(homepage_response.text, 'html.parser')
                
                # Mencari artikel terbaru berdasarkan tag a
                for a_tag in homepage_soup.find_all('a', href=True): 
                    url = a_tag['href']
                    if "/read/" in url and url.startswith("https"):
                        if url not in latest_urls:
                            latest_urls.append(url)
                        #batasan hanya mengecek 10 artiker berita
                        if len(latest_urls) >= 10:
                            break
            except Exception as e:
                print(f"Gagal mengecek halaman utama: {e}")

            new_articles = []

            #memfilter link artikel yang didapatkan,jika link artikel baru maka akan disimpan
            for url in latest_urls:
                if url not in seen_urls:
                    print(f"Artikel baru ditemukan: {url}")
                    article_data = scraper.scrape_article(url)
                    if article_data:
                        new_articles.append(article_data)                
                        seen_urls.add(url) 

            # Menyimpan hasil ke file JSON
            if new_articles:
                timestamp = int(time.time())
                output_filename = f"standard.json"
                scraper.save_to_json(new_articles, output_filename)
            else:
                print("Tidak ada artikel baru saat ini.")

            print(f"Menunggu {args.interval} detik...\n")
            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("\nProses dihentikan.")

if __name__ == "__main__":
    main()