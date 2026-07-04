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
    ok = client.open_chat("Дети")
    print("Opened:", ok)

finally:
    browser.disconnect()