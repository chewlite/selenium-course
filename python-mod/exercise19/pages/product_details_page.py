import random
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class ProductDetailsPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def get_quantity_in_basket(self):
        q = self.driver.find_element_by_id('cart').find_element_by_class_name('quantity').text
        return q

    def set_random_size(self):
        dropdown = self.driver.find_element_by_name('options[Size]')
        dropdown.click()
        options = self.driver.find_elements_by_css_selector('option')
        options[(random.randint(1, len(options)-1))].click()
        return self

    def add_to_cart(self):
        self.driver.find_element_by_name('add_cart_product').click()
        return self

    def wait_until_cart_updated(self, required_quantity):
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'quantity'), required_quantity))
        return self

    def open_main_page(self):
        self.driver.find_element_by_class_name('general-0').click()
