from playwright.sync_api import sync_playwright

class Browser:

    def __init__(self, storage_state: str):
        self._storage_state = storage_state
        self._playwright = None
        self._browser = None
        self._context = None
        self.page = None

    def connect(self):
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
            ]
        )

        self._context = self._browser.new_context(
            storage_state=self._storage_state,
            viewport={
                "width": 1920,
                "height": 1080,
            }
        )

        self.page = self._context.new_page()
        self.page.goto("https://web.max.ru")

        #
        # Ждем появления хотя бы одного чата.
        #
        self.page.locator(
            "div.item[data-index]"
        ).first.wait_for(timeout=30000)

    def disconnect(self):

        if self._browser:
            self._browser.close()

        if self._playwright:
            self._playwright.stop()