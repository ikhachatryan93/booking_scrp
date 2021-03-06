#! /bin/env python
from os import path, sep
import sys
import platform

dir_path = path.dirname(path.realpath(__file__))
sys.path.insert(0, dir_path + sep + "drivers")
sys.path.insert(0, dir_path + sep + "modules")

try:
    from pyvirtualdisplay import Display

    if "Linux" in platform.system():
        display = Display(visible=1, size=(800, 600))
        display.start()
except:
    pass

import utilities
import booking

main_query = 'http://www.booking.com/searchresults.html?checkin_month=CI_MONTH&checkin_monthday=CI_DAY&checkin_year' \
             '=CI_YEAR&checkout_month=CO_MONTH&checkout_monthday=CO_DAY&checkout_year=CO_YEAR&group_adults=ADULTS' \
             '&no_rooms=ROOMS&src_elem=sb&ss=CITY '


def get_query(params, index):
    city = params["city"][index]

    # Checkin date
    checkin = params["checkin"][index]
    ci_day = str(checkin.day)
    ci_month = str(checkin.month)
    ci_year = str(checkin.year)

    # Checkout date
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

    driver = utilities.setup_browser("firefox")
    driver.get(query_url)

    extracted_data = booking.extract(driver, utilities.configs.get("threads"))

    # utilities.append_into_file("done_list.txt", keyword)
    return extracted_data


def main():
    params = utilities.read_excel_file("input.xlsx")

    hotels_info = []
    for index in range(len(params["city"])):
        query_url, keyword = get_query(params, index)
        hotels_info += extract(query_url, keyword)
    utilities.write_output(hotels_info)


if __name__ == "__main__":
    main()
