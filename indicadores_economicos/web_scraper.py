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
    
    def download_file(self, page, selector, download_folder="downloads"):
        os.makedirs(download_folder, exist_ok=True)

        page.wait_for_selector(selector)
        with page.expect_download() as download_info:
            page.click(selector)
            download = download_info.value

            download_path = os.path.join(download_folder, download.suggested_filename)
            download.save_as(download_path)

        return download_path
    
    def retry_connection_to_url(self, func, max_retries=3):
        attempt = 0
        while attempt < max_retries:
            try:
                return func()
            except PlaywrightError as e:
                if "net::ERR_CONNECTION_RESET" in str(e):
                    delay = 2 ** attempt
                    time.sleep(delay)
                    attempt += 1
                else:
                    raise e
    
    def scroll_to_element(self, page, selector):
        page.locator(selector).scroll_into_view_if_needed()

    def close_browser(self):
        if self.browser_context:
            self.browser_context.close()


class StaticDataScraper(BrowserManager):
    def __init__(self, web_properties):
        super().__init__(web_properties)

    def scrape(self, url, selector, max_retries=3):
        def action():
            page = self.create_browser(enable_downloads=True)
            page.goto(url)
            return self.download_file(page, selector)
        
        return self.retry_connection_to_url(action, max_retries)

    
class InteractiveDataScraper(BrowserManager):
    def __init__(sel, web_properties):
        super().__init__(web_properties)

    def scrape(self, url, actions, max_retries=3):
        def action():
            page = self.create_browser(enable_downloads=True)
            page.goto(url, wait_until="networkidle")
            downloads = []
            for action in actions:
                if action['action_type'] == 'click':
                    self.scroll_to_element(page, action['selector'])
                    if page.is_visible(action['selector']):
                        download = self.download_file(page, action['selector'])
                        downloads.append(download)
            return downloads
        
        return self.retry_connection_to_url(action, max_retries)

 
    
    
    

