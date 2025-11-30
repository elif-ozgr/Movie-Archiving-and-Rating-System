import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

class SeleniumScraper:
    def __init__(self, headless=False): 
        
        chrome_options = Options()
        self.headless = headless
        
        # Bot algılamayı önleme ve ayarlar
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
        chrome_options.add_argument(f"user-agent={user_agent}")
        chrome_options.page_load_strategy = 'eager'
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        if self.headless:
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--disable-gpu")

        try:
            # 🔹 ChromeDriver yolunu buraya yaz (senin indirdiğin chromedriver.exe)
            chrome_driver_path = r"C:\tools\chromedriver.exe"
            service = Service(executable_path=chrome_driver_path)

            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
        except WebDriverException as e:
            print(f"HATA: ChromeDriver başlatılamadı. Hata: {e}")
            raise

    def open_list_page(self):
        url = "https://letterboxd.com/visdave3/list/official-top-250-narrative-feature-films/"
        try:
            self.driver.get(url)
            print(f"Sayfa açıldı: {self.driver.title}")
        except WebDriverException as e:
            print(f"HATA: Letterboxd sayfası açılamadı: {e}")
            raise

    def scrape_top_10(self):
        self.open_list_page()

        TITLE_SELECTOR = "h2.headline-2 a"
        
        try:
            wait = WebDriverWait(self.driver, 30)
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, TITLE_SELECTOR)))
            
            movies = self.driver.find_elements(By.CSS_SELECTOR, TITLE_SELECTOR)
            top_movies = [movie.text.strip() for movie in movies[:10]]
            
            if top_movies:
                file_name = "top_10_filmler.txt"
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write("--- Letterboxd Top 10 Film Listesi ---\n")
                    f.write(f"Çekilme Zamanı: {time.ctime()}\n\n")
                    for i, title in enumerate(top_movies, 1):
                        f.write(f"{i}. {title}\n")
                print(f"[DOSYA] BAŞARILI: İlk 10 film '{file_name}' dosyasına kaydedildi.")
            
            if not top_movies:
                print("UYARI: Film çekilemedi.")
                
            return top_movies
            
        except TimeoutException:
            print("HATA: 30 saniye içinde film başlıkları bulunamadı.")
            return []
        except Exception as e:
            print(f"Genel Hata: {e}")
            return []

    def close(self):
        if self.driver:
            self.driver.quit()


# --- TEST ETMEK İÇİN ---
if __name__ == "__main__":
    try:
        print("Scraper test ediliyor. Chrome tarayıcısı açılacak...")
        scraper = SeleniumScraper(headless=False)
        results = scraper.scrape_top_10()
        
        print("\n--- TEST SONUCU ---")
        if results:
            print("BAŞARILI! Çekilen İlk 10 Film Terminalde Görülüyor.")
            for i, movie in enumerate(results, 1):
                print(f"{i}. {movie}")
        else:
            print("HATA: Film listesi boş döndü.")
            
    except Exception as e:
        print(f"\nTEST BAŞARISIZ! Genel Hata: {e}")
    finally:
        if 'scraper' in locals() and scraper.driver:
            scraper.close()
