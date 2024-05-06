# %%

import os
import time
import logging
import csv
from .db import insert
from .utils import send_telegram


from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)


# enable debug logging
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

HEADLESS = os.environ.get("HEADLESS", "true").lower() == "true"


if not os.environ.get("ETC_USER") or not os.environ.get("ETC_PASSWORD"):
    raise ValueError("ETC_USER or ETC_PASSWORD is not set")

print("=== JAPAN ETC ===")
print("Run at", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        context = browser.new_context(
            locale="ja-JP",
            accept_downloads=True,
        )
        page = context.new_page()
        page.goto("https://www.etc-meisai.jp/index.html")

        page.wait_for_load_state("networkidle")

        # ul.menuList > li > a が複数あるので、最後のログインをクリックする

        page.locator(
            "//ul[@class='menuList']/li/a[contains(text(),'ログイン')]"
        ).last.click()

        logger.debug("Waiting for login page")
        # fill username by input name=risLoginId
        page.fill("input[name=risLoginId]", os.environ.get("ETC_USER"))
        # fill password by input name=risPassword
        page.fill("input[name=risPassword]", os.environ.get("ETC_PASSWORD"))
        # click login button by button text=ログイン and input type=button
        page.click("button:text('ログイン'), input[type=button]")

        # recv download file and read
        logger.debug("Waiting for download")
        with page.expect_download() as download_info:
            # click a text=全頁選択
            page.click("text=全頁選択")
            # page.click("text=")
            page.click("text=明細ＣＳＶ")
        download = download_info.value
        logger.debug("Downloaded %s", download.path())

        new_csv = csv.DictReader(open(download.path(), "r", encoding="shift-jis"))
        for row in new_csv:
            logger.debug("Inserting %s", row["利用年月日（自）"])
            if insert(row):
                logger.debug("Inserted %s", row["利用年月日（自）"])

                message = (
                    f"ETC利用明細:\n"
                    f"* 利用年月日: {row['利用年月日（自）']} {row['時分（自）']} ~ {row['利用年月日（至）']} {row['時分（至）']}\n"
                    f"* 利用ＩＣ: {row['利用ＩＣ（自）']} ~ {row['利用ＩＣ（至）']}\n"
                    f"* 車両番号: {row['車両番号']}\n"
                    f"* 通行料金: {row['通行料金']}円\n"
                    f"* 備考: {row['備考']}\n"
                )
                send_telegram(message)
        page.close()
        print("Done")
        browser.close()
