from config_reader import ConfigReader
from web_scraper import WebProperties, DataScraper
from playwright.sync_api import sync_playwright


def scrape_data(scraper, config):
    return scraper.scrape(config['url'], config['selectors'])


def main():
    config_file_path = r'./config.json' 
    config_reader = ConfigReader(config_file_path)
    pages_config = config_reader.read_config()

    with sync_playwright() as playwright:
        web_properties = WebProperties(browser_type=playwright.chromium)
        scraper = DataScraper(web_properties)

        for page_config in pages_config:
            scrape_data(scraper, page_config)
  

if __name__ == "__main__":
    main()