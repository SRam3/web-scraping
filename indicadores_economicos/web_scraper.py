from playwright.sync_api import sync_playwright, BrowserContext
from playwright_stealth import stealth_sync
import os
import time
import shutil



class WebProperties:
    def __init__(self, playwright_instance, viewport_size=None, browser_type=None, enable_stealth=True):
        self.playwright_instance = playwright_instance
        self.viewport_size = viewport_size
        self.browser_type = browser_type if browser_type else sync_playwright().chromium
        self.enable_stealth = enable_stealth

    def apply_stealth(self, browser_context):
        if self.enable_stealth:
            stealth_sync(browser_context)


class Spider:
    def __init__(self, web_properties: WebProperties):
        self.web_properties = web_properties
        self.browser_context = None

    def start_browser(self, enable_downloads=False):
        browser = self.web_properties.browser_type.launch(headless=True)

        if enable_downloads:
            context = browser.new_context(accept_downloads=True)
        else:
            context = browser.new_context()

        page = context.new_page()
        if self.web_properties.viewport_size:
            page.set_viewport_size(self.web_properties.viewport_size)
        self.web_properties.apply_stealth(context)

        self.browser_context = context
        return page

    def close_browser(self):
        if self.browser_context:
            self.browser_context.close()


class PIB(Spider):
    def __init__(self, web_properties):
        super().__init__(web_properties)
    
    def scrape(self, url, selectors):
        download_folder = "downloads"
        os.makedirs(download_folder, exist_ok=True)

        page = self.start_browser(enable_downloads=True)

        page.goto(url)
        page.wait_for_selector(selectors['data_links'])

        with page.expect_download() as download_info:
            page.click(selectors['data_links'])
        download = download_info.value

        download_path = download.path()
        while not download_path:
            time.sleep(1)
            download_path = download.path()

        with open(download_path, 'rb') as file:
            file_bytes = file.read()

        # Define the final path with a meaningful name
        file_name = "CTASTRIM124.xlsx"
        final_path = os.path.join(download_folder, file_name)

        os.rename(download_path, final_path)

        self.close_browser()

        return file_bytes, final_path

        








