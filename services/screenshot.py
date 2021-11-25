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
from PIL import Image
from io import BytesIO


def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')


def take_screenshot(url, headless=True, wait=None):
    now = datetime.datetime.now()
    date_time = now.isoformat().split(".")[0]
    name = f"{date_time}-{urlparse(url).netloc}-"
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=900, 600")
    browser = splinter.Browser("chrome", headless=headless, options=options)
    browser.visit("https://" +url)
    filename = Path(browser.screenshot(name=name, full=True))
    browser.quit()
    im = Image.open(filename)
    width, height = im.size

    left = 0
    top = 0
    right = width
    bottom = height / 2

    im1 = im.crop((left, top, right, bottom))
    im1.save(str(filename))
    heyo = get_base64_encoded_image(str(filename))
    if os.path.exists(str(filename)):
        os.remove(str(filename))
    return heyo


async def get_image_async(url: str):
    filepath, filename = None, None

    screenshot_filename = take_screenshot(
        url=url,
        headless=True,
        wait=3,
    )
    return screenshot_filename


