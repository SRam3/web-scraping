from config_reader import ConfigReader
from web_scraper import BrowserManager, WebProperties, PIB
from playwright.sync_api import sync_playwright


def main():
    config_file_path = r'./config.json' 
    config_reader = ConfigReader(config_file_path)
    pages_config = config_reader.read_config()

    with sync_playwright() as playwright:
        web_properties = WebProperties(browser_type=playwright.chromium)

        pib_config = pages_config[0]

        pib_scraper = PIB(web_properties)
        file_path = pib_scraper.scrape(pib_config['url'], pib_config['selectors'])
        

if __name__ == "__main__":
    main()