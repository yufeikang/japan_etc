import logging
import os
import requests

logger = logging.getLogger(__name__)


def send_telegram(message):
    if "TG_TOKEN" not in os.environ or "TG_CHAT_ID" not in os.environ:
        logger.debug("No TG_TOKEN or TG_CHAT_ID")
        return
    TG_TOKEN = os.environ.get("TG_TOKEN")
    TG_CHAT_ID = os.environ.get("TG_CHAT_ID")
    if TG_TOKEN and TG_CHAT_ID:
        requests.get(
            f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage?chat_id={TG_CHAT_ID}&text={message}"
        )
    else:
        logger.debug("No TG_TOKEN or TG_CHAT_ID")


def list_chats():
    TG_TOKEN = os.environ.get("TG_TOKEN")
    if TG_TOKEN:
        r = requests.get(f"https://api.telegram.org/bot{TG_TOKEN}/getUpdates")
        return r.json()
    else:
        logger.debug("No TG_TOKEN")


if __name__ == "__main__":
    data = list_chats()
    for update in data["result"]:
        print(
            f"{update['message']['chat']['id']} {update['message']['chat']['username']}"
        )
