import time
from playwright.sync_api import sync_playwright

class IMDBScraper:
    def __init__(self, headless=False):
        self.headless = headless
        self.browser = None
        self.page = None

    def start(self):
        p = sync_playwright().start()
        self.browser = p.chromium.launch(headless=self.headless)
        context = self.browser.new_context()
        self.page = context.new_page()

    def open_list_page(self):
        # IMDb resmi Top 250 listesi
        url = "https://www.imdb.com/chart/top/"
        self.page.goto(url, wait_until="domcontentloaded")

    def scrape_top_10(self):
        self.open_list_page()

        # IMDb 2024–2025 yeni layout stable selector
        SELECTOR = 'li.ipc-metadata-list-summary-item h3.ipc-title__text'

        try:
            self.page.wait_for_selector(SELECTOR, timeout=15000)
        except:
            print("❌ IMDb listesi yüklenemedi. Selector değişmiş olabilir.")
            return []

        elements = self.page.query_selector_all(SELECTOR)

        # Format: "1. The Shawshank Redemption" → Sadece film ismini almak için bölüyoruz
        movies = []
        for el in elements[:10]:
            text = el.inner_text().strip()
            # "1. The Shawshank Redemption" → sadece film adı
            parts = text.split(". ", 1)
            movie_name = parts[1] if len(parts) > 1 else text
            movies.append(movie_name)

        if not movies:
            print("❌ Film listesi boş döndü.")
            return []

        # Kaydet
        file_name = "top_10_imdb_filmler.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("--- IMDb Top 10 Film Listesi ---\n")
            f.write(f"Çekilme Zamanı: {time.ctime()}\n\n")
            for i, title in enumerate(movies, 1):
                f.write(f"{i}. {title}\n")

        print(f"✅ İlk 10 IMDb filmi başarıyla çekildi ve '{file_name}' dosyasına kaydedildi.")
        return movies

    def close(self):
        if self.browser:
            self.browser.close()


if __name__ == "__main__":
    scraper = IMDBScraper(headless=False)
    scraper.start()
    results = scraper.scrape_top_10()
    scraper.close()

    if results:
        print("\n--- ÇEKİLEN IMDb FİLMLERİ ---")
        for i, movie in enumerate(results, 1):
            print(f"{i}. {movie}")
    else:
        print("❌ Film listesi boş döndü.")
