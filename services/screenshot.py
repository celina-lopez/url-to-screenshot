#!/usr/bin/env python3
# requires: pip install splinter
import datetime
import os
import shutil
import time
from urllib.parse import urlparse
from pathlib import Path
import splinter
import base64
import os
from selenium import webdriver


def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')


def take_screenshot(url, headless=True, width=None, height=None, wait=None):
    now = datetime.datetime.now()
    date_time = now.isoformat().split(".")[0]
    name = f"{date_time}-{urlparse(url).netloc}-"
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1280, 960")
    browser = splinter.Browser("chrome", headless=headless, options=options)
    browser.driver.set_window_size(width, height)
    browser.visit("https://" +url)
    tmp_filename = Path(browser.screenshot(name=name, full=True))
    name = tmp_filename.name.rsplit("-", maxsplit=1)[0]
    extension = tmp_filename.name.rsplit(".", maxsplit=1)[-1]
    filename = tmp_filename.parent / (name + "." + extension)
    shutil.move(tmp_filename, filename)
    browser.quit()
    heyo = get_base64_encoded_image(filename)
    if os.path.exists(filename):
        os.remove(filename)
    return heyo


async def get_image_async(url: str):
    filepath, filename = None, None

    screenshot_filename = take_screenshot(
        url=url,
        width=1280,
        height=960,
        headless=True,
        wait=3,
    )
    return screenshot_filename


