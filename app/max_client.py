from models import ChatInfo, Message


class MaxClient:

    def __init__(self, browser):
        self._page = browser.page

    # =========================================================
    # CHAT LIST
    # =========================================================

    def get_chats(self) -> list[ChatInfo]:

        chats = self._page.locator("div.item[data-index]")

        result = []

        for i in range(chats.count()):

            chat = chats.nth(i)

            title_locator = chat.locator("h3.title")

            title = title_locator.inner_text().strip() if title_locator.count() else ""

            author_locator = chat.locator("span.author span.name")

            author = ""
            if author_locator.count():
                author = author_locator.inner_text().strip()

            time_locator = chat.locator("span.time")

            time = time_locator.inner_text().strip() if time_locator.count() else ""

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

    # =========================================================
    # OPEN CHAT
    # =========================================================

    def open_chat(self, title: str) -> bool:

        chats = self._page.locator("div.item[data-index]")

        for i in range(chats.count()):

            chat = chats.nth(i)

            t = chat.locator("h3.title span.text")

            if t.count() == 0:
                continue

            if t.inner_text().strip() == title:

                chat.click()

                # 🔥 КЛЮЧ: ждём URL change
                self._page.wait_for_timeout(2000)
                self._page.wait_for_url("**/*")

                return True

        return False

    # =========================================================
    # MESSAGES 
    # =========================================================

    def get_messages(self, limit: int = 30):

        self._page.wait_for_timeout(2000)

        messages = self._page.evaluate("""
        () => {

            const all = Array.from(document.querySelectorAll('div'));

            const isVisible = (el) => {
                const style = window.getComputedStyle(el);
                return style && style.display !== 'none' && style.visibility !== 'hidden';
            };

            const candidates = [];

            for (const el of all) {

                if (!isVisible(el)) continue;

                const rect = el.getBoundingClientRect();
                const text = el.innerText || '';

                // ❌ левый sidebar (режем по X)
                if (rect.x < 300) continue;

                // ❌ слишком широкий блок = не сообщение
                if (rect.width > 1200) continue;

                // ❌ слишком высокий = не сообщение
                if (rect.height > 300) continue;

                // фильтры мусора
                if (text.includes('Settings') && text.includes('Chats')) continue;
                if (text.includes('Calls') && text.includes('Contacts')) continue;
                if (text.includes('New sign in')) continue;

                // message heuristic
                if (text.length < 10) continue;
                if (text.length > 400) continue;

                if (!text.includes('\\n')) continue;

                candidates.push({
                    text,
                    x: rect.x,
                    y: rect.y
                });
            }

            // сортируем сверху вниз (как чат)
            candidates.sort((a,b) => a.y - b.y);

            const seen = new Set();
            const result = [];

            for (const c of candidates) {

                if (seen.has(c.text)) continue;
                seen.add(c.text);

                const lines = c.text.split('\\n').map(l => l.trim()).filter(Boolean);

                let sender = '';
                let time = '';

                for (const l of lines) {
                    if (l.includes(':') && l.length < 40) {
                        sender = l.replace(':','').trim();
                    }
                }

                for (let i = lines.length - 1; i >= 0; i--) {
                    if (lines[i].match(/\\d{1,2}:\\d{2}/) ||
                        lines[i].includes('AM') ||
                        lines[i].includes('PM')) {
                        time = lines[i];
                        break;
                    }
                }

                result.push({ sender, text: c.text, time });

                if (result.length >= 30) break;
            }

            return result;
        }
        """)

        return messages