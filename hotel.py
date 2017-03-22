import json
import re
import logging

import utilities

from bs4 import BeautifulSoup


class Hotel:
    def __init__(self, hotel_url):
        self.info = dict(
            url="", type="", image_url="", name="", rating="", num_reviews="",
            price="", address="", description="", map_url="", room_type="")

        self.hotel = utilities.setup_browser()
        self.hotel.get(hotel_url)
        self.hotel_source = BeautifulSoup(self.hotel.page_source, "html5lib")
        self.hotel.quit()
        dict_source = self.hotel_source.find("script", {"type": "application/ld+json"}).next
        self.dict = json.loads(dict_source)

        self.NOT_FOUND_MSG = "From {}: could not find ".format(hotel_url)

    def get_name(self):
        try:
            self.info["name"] = self.dict["name"]
        except:
            logging.error(self.NOT_FOUND_MSG + "name")

    def get_type(self):
        try:
            self.info["type"] = self.dict["@type"]
        except:
            logging.error(self.NOT_FOUND_MSG + "type")

    def get_map_url(self):
        try:
            self.info["map_url"] = self.dict["hasMap"]
        except:
            logging.error(self.NOT_FOUND_MSG + "map url")

    def get_image_url(self):
        try:
            self.info["image_url"] = self.dict["image"]
        except:
            logging.error(self.NOT_FOUND_MSG + "image")

    def get_address(self):
        try:
            self.info["address"] = self.dict["address"]["streetAddress"]
        except:
            logging.error(self.NOT_FOUND_MSG + "address")

    def get_rating(self):
        try:
            self.info["rating"] = self.dict["aggregateRating"]["ratingValue"]
        except:
            logging.error(self.NOT_FOUND_MSG + "rating")

    def get_number_of_reviews(self):
        try:
            self.info["num_reviews"] = self.dict["aggregateRating"]["reviewCount"]
        except:
            logging.error(self.NOT_FOUND_MSG + "number of reviews")

    def get_price(self):
        try:
            try:
                price = self.hotel_source.find("strong", {"class", "totalPrice_rack-rate"}).get_text()
            except:
                price = self.hotel_source.find("tfoot"). \
                    find("td", {"class": "totalPrice"}). \
                    find("span", {"class", "totalPrice_lead-in"}). \
                    nextSibling.strip()
            self.info["price"] = re.findall("\d+", price.replace(",", ""))[0]
        except:
            logging.error(self.NOT_FOUND_MSG + "price")

    def get_description(self):
        try:
            self.info["description"] = self.dict["description"]
        except:
            logging.error(self.NOT_FOUND_MSG + "description")

    def get_url(self):
        try:
            self.info["url"] = self.dict["url"]
        except:
            logging.error(self.NOT_FOUND_MSG + "url")

    def get_room_type(self):
        try:
            self.info["room_type"] = self.hotel_source.find("a", {"class": "togglelink"}).get_text().strip()
        except:
            logging.error(self.NOT_FOUND_MSG + "room type")

    def extract(self):
        # try:
        self.get_name()
        self.get_url()
        self.get_address()
        self.get_number_of_reviews()
        self.get_rating()
        self.get_price()
        self.get_description()
        self.get_image_url()
        self.get_map_url()
        self.get_room_type()
        self.get_type()
