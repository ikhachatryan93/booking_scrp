#! /bin/env python
import utilities
import configparser
import json
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import booking

# from pyvirtualdisplay import Display
#
# display = Display(visible=0, size=(1920, 1080))
# display.start()


booking_url = "https//www.booking.com"

browser = ""
config2 = ""

bool_config_1 = False
bool_config_2 = False

threads_num = 1
max_category_scroll_downs = 1000

main_query = 'http://www.booking.com/searchresults.html?checkin_month=CI_MONTH&checkin_monthday=CI_DAY&checkin_year=CI_YEAR&checkout_month=CO_MONTH&checkout_monthday=CO_DAY&checkout_year=CO_YEAR&group_adults=ADULTS&no_rooms=ROOMS&src_elem=sb&ss=CITY'


def get_query(params, index):
    city = params["city"][index]

    checkin = params["checkin"][index]
    ci_day = str(checkin.day)
    ci_month = str(checkin.month)
    ci_year = str(checkin.year)

    checkout = params["checkout"][index]
    co_day = str(checkout.day)
    co_month = str(checkout.month)
    co_year = str(checkout.year)

    rooms = str(params["rooms"][index])
    adults = str(params["adults"][index])
    query = main_query. \
        replace("CITY", city). \
        replace("CI_DAY", ci_day). \
        replace("CI_MONTH", ci_month). \
        replace("CI_YEAR", ci_year). \
        replace("CO_DAY", co_day). \
        replace("CO_MONTH", co_month). \
        replace("CO_YEAR", co_year). \
        replace("ROOMS", rooms). \
        replace("ADULTS", adults)

    return query, "{}, from {} to {}, {} adults, {} rooms".format(city, str(checkin).split()[0],
                                                                  str(checkout).split()[0], adults, rooms)


def extract(query_url, keyword):
    print("Obtaining information for: {}".format(keyword))

    driver = utilities.setup_browser(utilities.configs.get("driver"), maximize=True)
    driver.get(query_url)

    extracted_data = booking.extract_category(driver, utilities.configs.get("threads"))

    utilities.append_into_file("done_list.txt", keyword)

    driver.quit()
    return extracted_data


def main():
    # parse_config_file()
    params = utilities.read_excel("input.xlsx")

    hotels_info = []
    for index in range(len(params["city"])):
        query_url, keyword = get_query(params, index)
        hotels_info += extract(query_url, keyword)


if __name__ == "__main__":
    main()
