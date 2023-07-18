import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from loginner import Loginner, check_element
from bs4 import BeautifulSoup as bs
import requests

driver = webdriver.Chrome()


class Extractor (Loginner):

    def __no_results(self, url: str) -> bool: # сделать через try catch

        self.url = url
        self.check_connection()  # какую из переменных driver он изменит?

        try:
            text = driver.find_element(By.CLASS_NAME, 'title_holder').text.strip()
        except NoSuchElementException as e:
            print(e.msg) #?
            return False

        if text == "No Results Found":
            print("No results")
            return True

        return False

    def __click_first_item(self):
        check_element(By.CLASS_NAME, "product-image")
        driver.find_element(By.CLASS_NAME, "product-image").find_element(By.TAG_NAME, 'a').click()

    def __big_button_click(self):
        check_element(By.LINK_TEXT, "Check Inventory and Pricing")
        driver.find_element(By.LINK_TEXT, "Check Inventory and Pricing").click()

    def __get_col(self) -> int:
        page = requests.get(driver.current_url)
        soup = bs(page.text, "html.parser")
        title_table = soup.find('table', class_="table-inventory-next table-inventory-root table-pricing "
                                             "table-headings mar-t-15").find("thead")
        th_list = title_table.findAll('th')

        # check sale price
        titles: list = []
        for th in th_list:
            titles.append(th.text)
        # исхожу из того, что размер L всегда есть
        return titles.index("L")

    def __get_data(self, index) -> str:
        sale = "Sale Price: $"

        page = requests.get(driver.current_url)
        soup = bs(page.text, "html.parser")
        title_table = soup.find('table', class_="table-inventory-next table-inventory-root table-pricing "
                                                "table-headings mar-t-15").find("tbody")
        tr_list = title_table.findAll('tr', limit=5)

        row_list: list = []
        for tr in tr_list:
            row_list.append(tr.get_text(' ', True))  # должен быть список списков

        tlist: list = []
        for item in row_list:
            tlist.append(item[0])
        if sale in tlist:
            return row_list[tlist.index(sale)][index + 1]

        return row_list[0][index + 1]

    def extract(self, request_url) -> str:

        if self.__no_results(request_url):
            return "0"

        self.__click_first_item()
        self.__big_button_click()
        index = self.__get_col()
        return self.__get_data(index)
