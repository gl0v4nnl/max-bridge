from models import ChatInfo

class MaxClient:

    def __init__(self, browser):
        self._page = browser.page

    def get_chats(self) -> list[ChatInfo]:
        result = []
        chats = self._page.locator("div.item[data-index]")
        count = chats.count()

        for i in range(count):
            chat = chats.nth(i)

            # --- title ---
            title_locator = chat.locator("h3.title span.text")
            title = title_locator.inner_text() if title_locator.count() else ""

            # --- author ---
            author = ""
            author_locator = chat.locator("span.author span.name")
            if author_locator.count() > 0:
                author = author_locator.inner_text().strip()

            # --- time ---
            time_locator = chat.locator("span.time")
            time = time_locator.inner_text() if time_locator.count() else ""

            # --- preview (пока грубо, как есть в DOM) ---
            preview = chat.inner_text().strip()
            result.append(
                ChatInfo(
                    title=title,
                    author=author,
                    preview=preview,
                    time=time,
                )
            )

        return result

    def open_chat(self, title: str) -> bool:
        """
        Открывает чат по его названию.
        Возвращает True если удалось кликнуть, иначе False.
        """
        chats = self._page.locator("div.item[data-index]")
        count = chats.count()

        for i in range(count):
            chat = chats.nth(i)
            title_locator = chat.locator("h3.title span.text")
            if title_locator.count() == 0:
                continue

            chat_title = title_locator.inner_text().strip()
            if chat_title == title:
                chat.click()
                # даём интерфейсу прогрузиться
                self._page.wait_for_timeout(1500)
                return True

        return False