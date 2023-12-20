from playwright.sync_api import sync_playwright, BrowserContext
from playwright_stealth import stealth_sync
import random
import time


class WebProperties:
    def __init__(self, user_agent, viewport_size=None, browser_type=None):
        self.user_agent = user_agent
        self.viewport_size = viewport_size
        self.browser_type = browser_type if browser_type else sync_playwright().chromium

    def apply_properties(self, page):
        if self.viewport_size:
            page.set_viewport_size(self.viewport_size)
        if self.user_agent:
            page.set_user_agent(self.user_agent)


class HumanBehaviorSimulator:
    def apply_stealth(self, page):
        stealth_sync(page)
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.864.48 Safari/537.36 Edg/91.0.864.48",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
        ]

        page.set_user_agent(random.choice(user_agents))

        page.evaluate_on_new_document(
            """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """
        )

        # Introduce delay on each network request to mimic human browsing speed
        page.on("request", lambda request: time.sleep(random.uniform(0.5, 1.5)))

    def mimic_human_interaction(self, page):
        # Simulate random mouse movements
        viewport_size = page.viewport_size()
        width, height = viewport_size["width"], viewport_size["height"]
        for _ in range(random.randint(3, 5)):
            x, y = random.randint(0, width), random.randint(0, height)
            page.mouse.move(x, y)
            time.sleep(random.uniform(0.5, 1.5))


class Spider:
    def __init__(self, web_properties: WebProperties):
        self.web_properties = web_properties
        self.browser_context = None

    def start_browser(self):
        self.browser_context = self.web_properties.browser_type.launch(headless=True)
        page = self.browser_context.new_page()
        self.web_properties.apply_properties(page)
        return page

    def close_browser(self):
        if self.browser_context:
            self.browser_context.close()
