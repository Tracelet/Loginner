import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException

driver = webdriver.Chrome()
sanmar_url = "https://sanmar.com/login"
sswear_url = "https://www.ssactivewear.com/myaccount/login"
alpha_url = "https://www.alphabroder.com/login"

def check_element(by: str, element: str):

    for i in range(10):
        try:
            driver.find_element(by, element)
        except NoSuchElementException as e:
            print(f"Try to found element \"{element}\" by {by}...       {i + 1}/ 10")
            if i == 9:
                raise NoSuchElementException(e.msg)
            time.sleep(1)
        else:
            break


class Loginner:
    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url

    def check_connection(self):

        for i in range(5):
            try:
                driver.get(self.url)
            except WebDriverException as e:
                if i == 4:
                    raise WebDriverException(e.msg) # заменить raise, чтобы не останавливать парсер
                time.sleep(1)
            else:
                return True

    def sanmar(self):
        check_element(By.ID, 'j_username')
        check_element(By.ID, 'j_password')
        username = driver.find_element(By.ID, 'j_username')
        username.send_keys(self.username)
        password = driver.find_element(By.ID, 'j_password')
        password.send_keys(self.password)
        password.send_keys(Keys.ENTER)


    def ssactivewear(self):
        check_element(By.ID, 'M_M_zEmailTB')
        check_element(By.ID, 'M_M_zPasswordTB')
        email = driver.find_element(By.ID, 'M_M_zEmailTB')
        email.send_keys(self.username)
        password = driver.find_element(By.ID, 'M_M_zPasswordTB')
        password.send_keys(self.password)
        password.send_keys(Keys.ENTER)

    def alphabroder(self):
        check_element(By.ID, 'username')
        check_element(By.ID, 'password')
        username = driver.find_element(By.ID, 'username')
        username.send_keys(self.username)
        password = driver.find_element(By.ID, 'password')
        password.send_keys(self.password)
        password.send_keys(Keys.ENTER)
