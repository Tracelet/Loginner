import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from abc import ABC, abstractmethod

sanmar_url = "https://sanmar.com/login"
sswear_url = "https://www.ssactivewear.com/myaccount/login"
alpha_url = "https://www.alphabroder.com/login"


class Loginner(ABC):
    def __init__(self, username, password, url) -> None:
        self.username = username
        self.password = password
        self.url = url
        self.driver = webdriver.Chrome()

    def check_element(self, by: str, element: str) -> None:

        for i in range(10):
            try:
                print(self.driver.current_url)
                self.driver.find_element(by, element)
            except NoSuchElementException as e:
                print(f"Try to found element \"{element}\" by {by}...       {i + 1}/ 10")
                if i == 9:
                    raise NoSuchElementException(e.msg)
                time.sleep(1)
            else:
                break

    def check_connection(self) -> bool:

        for i in range(5):
            try:
                self.driver.get(self.url)
            except WebDriverException as e:
                if i == 4:
                    raise WebDriverException(e.msg) # заменить raise, чтобы не останавливать парсер
                time.sleep(1)
            else:
                return True

    @abstractmethod
    def login(self):
        ...


class SanmarLoginner(Loginner):
    def __init__(self, username, password):
        super().__init__(username, password, url=sanmar_url)

    def login(self):
        self.check_connection()
        self.check_element(By.ID, 'j_username')
        self.check_element(By.ID, 'j_password')
        username = self.driver.find_element(By.ID, 'j_username')
        username.send_keys(self.username)
        password = self.driver.find_element(By.ID, 'j_password')
        password.send_keys(self.password)
        password.send_keys(Keys.ENTER)


class SswearLoginner(Loginner):
    def __init__(self, username, password):
        super().__init__(username, password, url=sswear_url)

    def login(self):
        self.check_connection()
        self.check_element(By.ID, 'M_M_zEmailTB')
        self.check_element(By.ID, 'M_M_zPasswordTB')
        email = self.driver.find_element(By.ID, 'M_M_zEmailTB')
        email.send_keys(self.username)
        password = self.driver.find_element(By.ID, 'M_M_zPasswordTB')
        password.send_keys(self.password)
        password.send_keys(Keys.ENTER)


class AlphaLoginner(Loginner):
    def __init__(self, username, password):
        super().__init__(username, password, url=alpha_url)

    def login(self):
        self.check_connection()
        self.check_element(By.ID, 'username')
        self.check_element(By.ID, 'password')
        username = self.driver.find_element(By.ID, 'username')
        username.send_keys(self.username)
        password = self.driver.find_element(By.ID, 'password')
        password.send_keys(self.password)
        password.send_keys(Keys.ENTER)
