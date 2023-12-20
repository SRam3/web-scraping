from config_reader import ConfigReader
from web_scraper import WebScraper
from playwright.sync_api import sync_playwright


def main():
    config_file_path = r'./config.json' 
    config_reader = ConfigReader(config_file_path)
    pages_config = config_reader.read_config()

    with sync_playwright() as playwright:
        scraper = WebScraper(playwright.chromium)
        

if __name__ == "__main__":
    main()