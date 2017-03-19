from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
import configparser
import time
import utilities
import hashlib
import logging


class Hotel:
    def __init__(self, hotel_url):
        self.info = dict(
            url=hotel_url, name="", rating="", num_reviews="", price="", address="")

        self.hotel = utilities.setup_browser()

        # self.hotel.get(self.info["url"])
        # time.sleep(3)
        self.hotel.get(self.info["url"])
        self.page_source = urlopen(hotel_url)
        self.hotel_source = BeautifulSoup(self.page_source, "html5lib")
        #print(self.hotel_source.prettify())
        print(self.hotel_source.prettify()/asd)

        self.NOT_FOUND_MSG = "From {}: could not find ".format(self.info["url"])
        self.wait_5 = WebDriverWait(self.hotel, 5)
        self.wait_2 = WebDriverWait(self.hotel, 2)
        self.wait_1 = WebDriverWait(self.hotel, 1)

    def get_name(self):
        try:
            self.info["name"] = self.hotel.find_element_by_id("hp_hotel_name").text.strip()
        except:
            logging.error(self.NOT_FOUND_MSG + "name")

    def get_address(self):
        try:
            #self.info["address"] = self.hotel.find_element_by_xpath(".//*[@id='b_tt_holder_1']").text.strip()
            #self.info["address"] = self.hotel.find_element(By.XPATH, ".//*[@id='b_tt_holder_1']").text.strip()
            #self.info["address"] = self.wait_5.until(EC.presence_of_element_located((By.XPATH, ".//*[@id='b_tt_holder_1']"))).text
            #pass

            self.info["address"] = self.hotel_source.find("span", {"id", "b_tt_holder_1"}).text.strip()
        except TimeoutException:
            print("asdadsadsad")
        except Exception as e:
            print(str(e))
            logging.error(self.NOT_FOUND_MSG + "address")

    def get_rating(self):
        try:
            #self.info["rating"] = self.hotel.find_element_by_css_selector(".average.js--hp-scorecard-scoreval").text.strip()
            self.info["rating"] = self.hotel.find_elements_by_css_selector("span.average.js--hp-scorecard-scoreval")
            #self.info["rating"] = self.hotel_source.find("div", {"id", "js--hp-gallery-scorecard"}).find("span", {"class": "best"}).text.strip()
        except:
            logging.error(self.NOT_FOUND_MSG + "rating")

    def get_number_of_reviews(self):
        try:
            self.info["num_reviews"] = self.hotel.find_element_by_xpath(".//*[@id='js--hp-gallery-scorecard']/span/strong").text.strip()
            #self.info["num_reviews"] = self.hotel_source.find("div", {"id", "js--hp-gallery-scorecard"}).find("span", {"class": "count"}).text.strip()
        except:
            logging.error(self.NOT_FOUND_MSG + "number of reviews")

    def get_price(self):
        try:
            self.info["price"] = self.hotel.find_element_by_xpath(".totalPrice_rack-rate").text.strip()
        except:
            logging.error(self.NOT_FOUND_MSG + "price")
        # try:
        #     self.info["price"] = self.hotel.

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

    def extract(self):
        # try:
        self.get_name()
        self.get_address()
        self.get_number_of_reviews()
        self.get_price()
        self.hotel.quit()
