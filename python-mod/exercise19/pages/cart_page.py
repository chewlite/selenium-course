from selenium.webdriver.support.wait import WebDriverWait


class CartPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def get_last_product_in_table(self, last_index):
        table = self.get_table()
        lp = table.find_elements_by_class_name('item')[last_index]
        return lp

    def get_quantity_of_positions(self):
        table = self.get_table()
        q = len(table.find_elements_by_class_name('item')) - 1
        return q

    def get_table(self):
        t = self.driver.find_element_by_class_name('dataTable')
        return t

    def remove_some_product(self):
        remove_button = self.driver.find_element_by_name('remove_cart_item')
        remove_button.click()
        return self
