from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from playwright.sync_api import Error as PlaywrightError
import os
import time


class WebProperties:
    def __init__(self, browser_type=None, enable_stealth=True):
        self.browser_type = browser_type if browser_type else sync_playwright().chromium
        self.enable_stealth = enable_stealth

    def apply_stealth(self, browser_context):
        if self.enable_stealth:
            stealth_sync(browser_context)


class BrowserManager:
    def __init__(self, web_properties: WebProperties):
        self.web_properties = web_properties
        self.browser_context = None

    def create_browser(self, enable_downloads=False):
        browser = self.web_properties.browser_type.launch(headless=True)

        if enable_downloads:
            context = browser.new_context(accept_downloads=True)
        else:
            context = browser.new_context()

        page = context.new_page()
        self.web_properties.apply_stealth(context)

        self.browser_context = context
        return page
    
    def download_file(self, page, selectors, download_folder="downloads"):
        os.makedirs(download_folder, exist_ok=True)

        page.wait_for_selector(selectors["data_links"])
        with page.expect_download() as download_info:
            page.click(selectors["data_links"])
            download = download_info.value

            download_path = os.path.join(download_folder, download.suggested_filename)
            download.save_as(download_path)

        return download_path

    def close_browser(self):
        if self.browser_context:
            self.browser_context.close()


class DataScraper(BrowserManager):
    def __init__(self, web_properties):
        super().__init__(web_properties)

    def scrape(self, url, selectors, max_retries=3):
        attempt = 0
        while attempt < max_retries:
            try:
                page = self.create_browser(enable_downloads=True)
                page.goto(url)
                download = self.download_file(page, selectors)
                return download
            except PlaywrightError as e:
                if "net::ERR_CONNECTION_RESET" in str(e):
                    delay = 2 ** attempt
                    time.sleep(delay)
                    attempt += 1
                else:
                    raise Exception
            finally:
                self.close_browser()
        
        print("Failed to scrape data after several attempts")
        return None


    
    
    

