import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os

class BisnisScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape_article(self, url):
        
        try:
            #mengirimkan permintaan HTTP ke halaman dengan batas waktu 10 detik dan membedah strukturnya
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            #melakukan pencarian berdasarkan tag h1 untuk mendapatkan judul,kemudian div untuk mendapatkan isi artikel
            title_tag = soup.find('h1')
            title = title_tag.text.strip() if title_tag else "No Title"
            content_div = soup.find('div', class_='style__ArticleWrapper-sc-1vlk1b8-0') 

            paragraphs = content_div.find_all('p') if content_div else soup.find_all('p')
            content = " ".join([p.text.strip() for p in paragraphs])

            #pembersihan agar hasil teks lebih bersih dan merapikan teks
            unwanted_texts = [
                "Nyaman tanpa iklan. Langganan BisnisPro",
                "Cek Berita dan Artikel yang lain di Google",
                "News dan WA Channel",
                "Member of",
                "* Ringkasan ini dibantu dengan menggunakan AI"
            ]
            for noise in unwanted_texts:
                content = content.replace(noise, "")
            content = " ".join(content.split())

            #mengambil tanggal terbit artikel
            date_tag = soup.find('meta', property='article:published_time')
            if date_tag:
                published_time = date_tag['content']
            else:
                published_time = datetime.now().isoformat()

            #mengembalikan hasil data yang telah diambil ke dictionary
            return {
                "link": url,
                "judul": title,
                "isi_artikel": content,
                "tanggal_terbit": published_time
            }
        except Exception as e:
            print(f"Error {url}: {e}")
            return None

    #Menyimpan data ke file JSON
    def save_to_json(self, data, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Data berhasil disimpan di {filename}")