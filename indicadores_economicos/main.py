from config_reader import ConfigReader
from web_scraper import WebProperties, StaticDataScraper, InteractiveDataScraper
from playwright.sync_api import sync_playwright


def static_scrape_data(scraper, config):
    return scraper.scrape(config['url'], config['selectors']['data_links'])


def interactive_scrape_data(scraper, config):
    return scraper.scrape(config['url'], config['actions'])


def main():
    config_file_path = r'./config.json' 
    config_reader = ConfigReader(config_file_path)
    pages_config = config_reader.read_config()

    with sync_playwright() as playwright:
        web_properties = WebProperties(browser_type=playwright.chromium)
        static_scraper = StaticDataScraper(web_properties)
        interactive_scraper = InteractiveDataScraper(web_properties)

        for page_config in pages_config:
            if "selectors" in page_config:  
                #static_scrape_data(static_scraper, page_config)
                pass
            elif "actions" in page_config:  
                interactive_scrape_data(interactive_scraper, page_config)
                
  

if __name__ == "__main__":
    main()