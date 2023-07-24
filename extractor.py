import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from loginner import Loginner, check_element, driver # запихнуть переменные внутрь класса


class Extractor (Loginner):

    def __no_results(self, url: str) -> bool: # сделать через try catch

        self.url = url
        self.check_connection()  # какую из переменных driver он изменит?
        time.sleep(3)

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
        driver.find_element(By.CLASS_NAME, "product-image").click()

    def __big_button_click(self):
        check_element(By.LINK_TEXT, "Check Inventory and Pricing")
        driver.find_element(By.LINK_TEXT, "Check Inventory and Pricing").click()

    def __get_cell_indexes(self):
        sale = "Sale Price: $"

        th = driver.find_elements(By.XPATH, "//table[@id='table-inventory-1']/thead/tr/th[position() > 1]")
        head_list: list = []
        for item in th:
            head_list.append(item.text)

        col_index = head_list.index("L")

        td = driver.find_elements(By.XPATH, "//form[@name='warehouseHouseGridForm']/table/tbody/tr/td[position() < 6]")
        row_list: list = []
        for item in td:
            row_list.append(item.text)

        row_index = 0
        if sale in row_list:
            row_index = row_list.index(sale)

        return row_index, col_index


    def __get_data(self, row_index, col_index) -> str:

        cost = driver.find_element(By.XPATH, f"//table[@id='table-inventory-1']/tbody/tr[{row_index + 1}]/td[{col_index + 2}]")
        return cost.text

    def extract(self, request_url) -> str:

        if self.__no_results(request_url):
            return "0"

        self.__click_first_item()
        time.sleep(1)
        self.__big_button_click()
        time.sleep(1)
        index1, index2 = self.__get_cell_indexes()
        return self.__get_data(index1, index2)


sanmar = Extractor(username="dlhscreenprint", password="Lafd135!", url=None)
sanmar.sanmar()
time.sleep(3)
cost = sanmar.extract("https://sanmar.com/search/?text=3001")
print(cost)
assert cost == "3.89"
