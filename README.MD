
# Japan ETC record downloader

![ETC](https://www.etc-meisai.jp/img/common/logo.png)

> This is a tool to download the ETC record from the website of Japan ETC [etc-meisai.jp](https://www.etc-meisai.jp/index.html). You can use it to download the ETC record automatically. before you use it, you should register an account on the website and login. Then you can use this tool to download the ETC record.

## 1. Install

```bash
pdm install
```

## 2. Usage

```bash
pdm run etc
```

if need Telegram notification, you can set the environment variable `TG_BOT_TOKEN` and `TG_CHAT_ID`.

## 3. Crontab schedule

```
0 17 * * * cd YOUR_SRC_DIR && pdm run etc
```
