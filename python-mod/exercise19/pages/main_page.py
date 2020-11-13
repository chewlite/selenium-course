from selenium.webdriver.support.wait import WebDriverWait
import time


class MainPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get("http://localhost/litecart/")
        return self

    def open_product_details(self, index):
        p = self.driver.find_elements_by_class_name('product')[index]
        p.click()

    def open_cart(self):
        cart = self.driver.find_element_by_id('cart')
        cart.find_element_by_class_name('link').click()
        time.sleep(1)
