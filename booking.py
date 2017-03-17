import time
import json
import logging
import threading

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.request import urljoin
import os.path
import sys
import time

import utilities
from hotel import HotelInfo

main_url = "http://www.booking.com"


def get_hotel_urls(driver):
    wait = WebDriverWait(driver, 5)
    while True:
        soup = BeautifulSoup(driver.page_source, "html5lib")
        a_tags = soup.findAll("a", {"class", "hotel_name_link"})
        urls = []
        for tag in a_tags:
            urls.append(urljoin(main_url, tag["href"].split("?")[0]))

        try:
            paginator = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".paging-next")))
        except TimeoutException:
            break

        driver.execute_script("return arguments[0].scrollIntoView(false);", paginator)
        paginator.click()

    return urls


def run_category_extraction(url, hotel_info, keyword):
    return ""
    # try:
    #     company = HomestarCompanyInfo(urljoin(homestars_url, url), keyword)
    #     company.extract_company()
    #     hotel_info.append(company.company_info)
    # except:
    #     time.sleep(3)
    #     try:
    #         company = HomestarCompanyInfo(urljoin(homestars_url, url), keyword)
    #     except Exception as e:
    #         logging.error("url : {}.  {}".format(url, str(e)))


def extract_category(driver, threads_num):
    hotels_url = get_hotel_urls(driver)

    hotel_info = []
    trds = []
    i = 0
    total = len(hotels_url)
    for url in hotels_url:
        i += 1
        sys.stdout.write("\r[Extracting: {}/{}]".format(i, total))
        sys.stdout.flush()
        time.sleep(0.3)
        t = threading.Thread(target=run_category_extraction, args=(url, hotel_info))
        t.daemon = True
        t.start()
        trds.append(t)
        while threading.active_count() > threads_num:
            time.sleep(0.4)
    print("l2")
    for i in trds:
        i.join(10)
    print("l4")
    logging.info("Finished. keyword: {},  companies: {}".format(keyword, len(hotel_info)))

    return hotel_info
