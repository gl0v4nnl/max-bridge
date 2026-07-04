from browser import Browser
from max_client import MaxClient

browser = Browser("/data/session.json")
browser.connect()

try:
    client = MaxClient(browser)
    chats = client.get_chats()
    print(f"Found {len(chats)} chats\n")

    for chat in chats:
        print(chat)

    print("\nOpening chat: Дети\n")
    client.open_chat("Дети")
    browser.page.wait_for_timeout(2000)
    msgs = client.get_messages()
    for m in msgs:
        print(m)
        print("-" * 60)

finally:
    browser.disconnect()