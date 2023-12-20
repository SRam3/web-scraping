from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import random
import time


class WebProperties:
    def __init__(self, user_agent, viewport_size, browser_type):
        self.user_agent = user_agent
        self.viewport_size = viewport_size
        self.browser_type = browser_type