from playwright.sync_api import sync_playwright

class PlaywrightScraper:
    def __init__(self, headless=True):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.page = self.browser.new_page()

    def open_imdb_top(self):
        self.page.goto("https://www.imdb.com/chart/top/", timeout=60000)
        self.page.wait_for_selector("td.titleColumn a")

    def scrape_top_10(self):
        self.open_imdb_top()
        movies = self.page.query_selector_all("td.titleColumn a")
        return [m.inner_text().strip() for m in movies[:10]]

    def close(self):
        self.browser.close()
        self.playwright.stop()
