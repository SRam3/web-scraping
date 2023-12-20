from playwright.sync_api import sync_playwright, BrowserContext
from playwright_stealth import stealth_sync
import random
import time


class WebProperties:
    def __init__(self, viewport_size=None, browser_type=None):
        self.viewport_size = viewport_size
        self.browser_type = browser_type if browser_type else sync_playwright().chromium

    def apply_properties(self, page):
        if self.viewport_size:
            page.set_viewport_size(self.viewport_size)


class HumanBehaviorSimulator:
    def apply_stealth(self, browser_context, page):
        stealth_sync(page)
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.864.48 Safari/537.36 Edg/91.0.864.48",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
        ]

        # Introduce delay on each network request to mimic human browsing speed
        #page.on("request", lambda request: time.sleep(random.uniform(0.5, 1.5)))

    def mimic_human_interaction(self, page):
        # Simulate random mouse movements
        viewport_size = page.viewport_size
        width, height = viewport_size["width"], viewport_size["height"]
        for _ in range(random.randint(3, 5)):
            x, y = random.randint(0, width), random.randint(0, height)
            page.mouse.move(x, y)
            time.sleep(random.uniform(0.5, 1.5))


class Spider:
    def __init__(self, web_properties: WebProperties):
        self.web_properties = web_properties
        self.browser_context = None

    def start_browser(self, user_agent=None):
        self.browser_context = self.web_properties.browser_type.launch(headless=True)

        context_options = {}
        if user_agent:
            context_options['userAgent'] = user_agent

        # Create a new context with the specified user agent
        self.browser_context = self.browser_context.new_context(**context_options)

        self.browser_context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)

        page = self.browser_context.new_page()
        self.web_properties.apply_properties(page)
        return page

    def close_browser(self):
        if self.browser_context:
            self.browser_context.close()


class PIB(Spider):
    def __init__(self, web_properties, behavior_simulator):
        super().__init__(web_properties)
        self.behavior_simulator = behavior_simulator

    def scrape(self, url, selectors):
        page = self.start_browser()
        self.behavior_simulator.apply_stealth(self.browser_context, page)
        self.behavior_simulator.mimic_human_interaction(page)

        page.goto(url)
        data_links_selector = selectors.get('data_links')
        page.query_selector_all(data_links_selector)


        self.close_browser()
