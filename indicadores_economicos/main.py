from config_reader import ConfigReader
from web_scraper import Spider, WebProperties, HumanBehaviorSimulator, PIB
from playwright.sync_api import sync_playwright


def main():
    config_file_path = r'./config.json' 
    config_reader = ConfigReader(config_file_path)
    pages_config = config_reader.read_config()

    with sync_playwright() as playwright:
        web_properties = WebProperties(browser_type=playwright.chromium)
        behavior_simulator = HumanBehaviorSimulator()

        pib_scraper = PIB(web_properties, behavior_simulator)

        for page in pages_config:
            if page['name'] == 'PIB':
                scraped_data = pib_scraper.scrape(page['url'], page['selectors'])
        

if __name__ == "__main__":
    main()