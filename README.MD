
# Japan ETC use record downloader

![ETC](https://www.etc-meisai.jp/img/common/logo.png)

> This is a tool to download the ETC use record from the website of Japan ETC. [etc-meisai.jp](https://www.etc-meisai.jp/index.html)

## 1. Install

```bash
pdm install
```

## 2. Usage
>
> You can modify the .env file from .env.example. The fist time you can set env FETCH_ALL=true. After that you can set it to false.

```bash
pdm run etc
```

## 3. Crontab schedule

```
0 17 * * * cd YOUR_SRC_DIR && pdm run etc
```
