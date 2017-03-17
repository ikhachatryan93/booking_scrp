from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pandas import *

import time
import configparser
import logging
import platform
from os import sep, path

dir_path = path.dirname(path.realpath(__file__))

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()

# log_name = datetime.now().strftime('scraping_%H_%M_%d_%m_%Y.log')
# fileHandler = logging.FileHandler(filename=log_name)
# fileHandler.setFormatter(logFormatter)
# rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

logging.basicConfig(level=logging.DEBUG)


def setup_browser(browser, maximize=False):
    bpath = dir_path + sep + "drivers" + sep + browser
    bpath = bpath.replace("//", "/")
    print(bpath)
    print(platform.system())
    if "Windows" in platform.system():
        bpath += ".exe"

    if "chromedriver" in browser:
        driver = setup_chrome(bpath, maximize)
    elif "phantomjs" in browser:
        driver = setup_phantomjs(bpath, maximize)
    elif "firefox" in browser:
        bpath = bpath.replace("firefox", "geckodriver")
        print(bpath)
        driver = setup_firefox(bpath, maximize)
    else:
        driver = setup_chrome(bpath, maximize)
        logging.warning("Invalid browser name specified, using default browser")

    return driver


def setup_chrome(path, maximize):
    driver = webdriver.Chrome(path)
    if maximize:
        driver.maximize_window()
    return driver


def setup_firefox(path, maximize):
    driver = webdriver.Firefox(executable_path=path)
    if maximize:
        driver.maximize_window()
    return driver


def setup_phantomjs(path, maximize):
    service_args = ['--ignore-ssl-errors=true', '--ssl-protocol=any']
    driver = webdriver.PhantomJS(path, service_args=service_args)
    if maximize:
        driver.maximize_window()
    return driver


# def setup_chrome_browser(maximize=True):
#    with open('proxies.txt') as f:
#        lines = f.readlines()
#        PROXY = random.choice(lines)
#    chrome_options = webdriver.ChromeOptions()
#    chrome_options.add_argument('--proxy-server=%s' % PROXY)
#    chrome = webdriver.Chrome("chromedriver", chrome_options=chrome_options)
#    if maximize:
#        chrome.maximize_window()
#    return chrome

def read_urls_from_file(name):
    urls = []
    with open(name, encoding='utf-8') as f:
        urls = f.read().splitlines()
    assert (len(urls) > 0)
    return urls


def read_excel_file(excel_file):
    xls = ExcelFile(excel_file)
    return xls.parse(xls.sheet_names[0])


def append_into_file(file, string):
    with open(file, "a", encoding='utf-8') as myfile:
        myfile.write(string + '\n')


def write_lines_to_file(name, urls):
    with open(name, 'w', encoding='utf-8') as f:
        for url in urls:
            try:
                f.write(url + '\n')
            except Exception as e:
                print(str(e))


# return false if scrolldowns ended
def scroll_down(driver, css_selector, max_scroll_downs):
    wait = WebDriverWait(driver, 10)
    for _ in range(max_scroll_downs):
        try:
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
        except TimeoutException:
            return False
        except OSError:
            print("scroll down error")
            time.sleep(2)
            continue
        driver.execute_script("window.scrollTo(0, 0)")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            click_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        except TimeoutException:
            return False
        try:
            if "disabled" in click_element.get_attribute("class"):
                return False
        except:
            continue

    return True


class configs:
    file = r"./configs.txt"

    config = {"threads": 1, "browser": "chrome"}
    parsed = False

    @staticmethod
    def parse_config_file():
        config_parser = configparser.RawConfigParser()
        config_parser.read(configs.file)

        configs.config["driver"] = config_parser.get('tools', 'driver')
        configs.config["threads"] = config_parser.getint('parameters', 'threads')

        configs.read = True

    @staticmethod
    def get(key):
        if not configs.parsed:
            configs.parse_config_file()
        return configs.config[key]
