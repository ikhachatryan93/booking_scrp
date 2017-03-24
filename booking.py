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
import utilities

main_url = "http://www.booking.com"

drivers = []
max_num_threads = utilities.configs.get("max_browsers")

# for security reasons
assert(max_num_threads < 30)

for j in range(max_num_threads):
    drivers.append({"driver": utilities.setup_browser(), "status": "free"})


def get_hotel_urls(driver):
    logging.info("Extracting hotels list")
    wait = WebDriverWait(driver, 5)

    time.sleep(1)
    try:
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '''.cityWrapper''')))
        elem = element.find_element_by_css_selector(".b-button__text")
        utilities.click(driver, elem)
        time.sleep(5)
    except TimeoutException:
        pass

    urls = []
    testing = utilities.configs.get("testing")
    while True:
        soup = BeautifulSoup(driver.page_source, "lxml")
        a_tags = soup.find("div", {"id": "hotellist_inner"}).findAll("a", {"class", "hotel_name_link"})
        for tag in a_tags:
            urls.append(urljoin(main_url, tag["href"]))

        if testing:
            break

        try:
            paginator = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".paging-next")))
        except TimeoutException:
            break

        driver.execute_script("return arguments[0].scrollIntoView(false);", paginator)
        driver.execute_script("window.scrollBy(0, 150);")
        paginator.click()
        time.sleep(1)

    driver.quit()

    old_num = len(urls)
    filtered = set(urls)
    logging.info("Filtering duplicates... ")
    logging.info("Url extraction is done. Total {} have been filtered from {} extracted".format(len(filtered), old_num))

    return filtered


def get_free_driver():
    while True:
        time.sleep(0.2)
        for i in range(len(drivers)):
            if drivers[i]["status"] == "free":
                drivers[i]["status"] = "used"
                return drivers[i]["driver"], i


def extract_hotel(url, hotels_info, try_again=True):
    driver, i = get_free_driver()
    driver.get(url)
    try:
        hotel = Hotel(driver)
        hotel.extract()
        hotels_info.append(hotel.info)
    except Exception as e:
        logging.critical(str(e) + ". while getting information from " + url)
        logging.info("Trying again")
        if try_again:
            extract_hotel(url, hotels_info, try_again=False)
    drivers[i]["status"] = "free"


def extract(driver, threads_num):
    hotels_url = get_hotel_urls(driver)
    hotels_info = []
    # extract_hotel(hotels_url.pop(), hotels_info)
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
            time.sleep(0.2)

    for t in trds:
        t.join(10)

    for d in drivers:
        d["driver"].quit()

    return hotels_info
