import sys
import logging
import threading
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup
from urllib.request import urljoin

from hotel import Hotel

main_url = "http://www.booking.com"

logging.info("extracting hotels list")
logging.error("extracting hotels list")
logging.debug("extracting hotels list")
logging.critical("extracting hotels list")
logging.warning("extracting hotels list")


def get_hotel_urls(driver):
    logging.info("extracting hotels list")
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


def extract_hotel(url, hotels_info):
    try:
        hotel = Hotel(url)
        hotel.extract()
        hotels_info.append(hotel.info)
    except Exception as e:
        logging.error(str(e) + " while getting information from " + url)


def extract(driver, threads_num):
    hotels_url = get_hotel_urls(driver)

    hotels_info = []
    trds = []
    i = 0
    total = len(hotels_url)
    for url in hotels_url:
        i += 1
        sys.stdout.write("\r[Extracting: {}/{}]".format(i, total))
        sys.stdout.flush()
        time.sleep(0.3)
        t = threading.Thread(target=extract_hotel, args=(url, hotels_info))
        t.daemon = True
        t.start()
        trds.append(t)
        while threading.active_count() > threads_num:
            time.sleep(0.4)
    for t in trds:
        t.join(10)

    return hotels_info
