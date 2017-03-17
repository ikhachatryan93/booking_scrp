from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from datetime import datetime
import configparser
import time
import utilities
import hashlib
import logging


class HotelInfo:
    def __init__(self, hotel_url):
        self.hotel_info = dict(
            url=hotel_url, destination="", hotel_name="",
            user_rating="", number_of_reviews="", price="", address="")

        self.hotel_page = utilities.setup_browser(utilities.configs.get("driver"), maximize=True)

        self.hotel_page.get(self.hotel_info["url"])
        self.hotel_page_source = BeautifulSoup(self.hotel_page.page_source, "html5lib")

        self.NF = "From {}: could not find ".format(self.hotel_info["url_name"])
        self.wait_5 = WebDriverWait(self.hotel_page, 5)
        self.wait_2 = WebDriverWait(self.hotel_page, 2)
        self.wait_1 = WebDriverWait(self.hotel_page, 1)

    def get_hotel_name(self):
        return

    def get_destination(self):
        return

    def get_number_of_reviews(self):
        return

    def get_price(self):
        return

        # def get_address(self):
        #     try:
        #         old_url = self.company_page.current_url
        #         see_more = self.wait_1.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".square-gallery__see"
        #                                                                                            "-more")))
        #         self.company_page.execute_script("return arguments[0].scrollIntoView();", see_more[len(see_more) - 1])
        #         see_more = self.wait_5.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".square-gallery__see-more")))
        #         self.company_page.execute_script("return arguments[0].click();", see_more)
        #         while old_url in self.company_page.current_url:
        #             time.sleep(0.1)
        #         photos_tags = self.wait_5.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".square"
        #                                                                                               "-gallery__link")))
        #         for p in photos_tags:
        #             self.company_info['shop_photos_links'].append(p.get_attribute("href"))

        #         # go back to company main page
        #         self.company_page.execute_script("window.history.go(-1)")
        #     except:
        #         try:
        #             photos_tags = self.company_page.find_elements_by_css_selector(".square-gallery__link")
        #             self.company_page.execute_script("return arguments[0].scrollIntoView();", photos_tags[0])
        #             for p in photos_tags:
        #                 self.company_info['shop_photos_links'].append(p.get_attribute("href"))
        #         except:
        #             logging.warning(self.NF + "photos")

    def extract_hotel_info(self):
        # try:
        parse_extraction_info_from_config_file()
        self.get_hotel_name()
        self.get_destination()
        self.get_number_of_reviews()
        self.get_price()
        self.hotel_page.quit()
