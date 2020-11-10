import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time


@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    wd = webdriver.Chrome(options=options)
    request.addfinalizer(wd.quit)
    return wd


def test_basket(driver):
    driver.get("http://localhost/litecart/")

    i = 0
    while i < 3:
        driver.find_elements_by_class_name('product')[0].click()
        initial_quantity = driver.find_element_by_id('cart').find_element_by_class_name('quantity').text
        required_quantity = str(int(initial_quantity) + 1)
        try:
            driver.find_element_by_name('options[Size]').click()
            options = driver.find_elements_by_css_selector('option')
            options[(random.randint(1, len(options)-1))].click()
        except NoSuchElementException:
            pass
        driver.find_element_by_name('add_cart_product').click()
        wait = WebDriverWait(driver, 5)
        wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'quantity'), required_quantity))
        driver.find_element_by_class_name('general-0').click()
        i += 1

    driver.find_element_by_class_name('link').click()
    time.sleep(1)
    products_in_basket = len(driver.find_element_by_class_name('dataTable').find_elements_by_class_name('item')) - 1
    # после каждого удаления проверяем, что товар, который был на последней строчке в таблице, исчез - список уменьшился
    j = 0
    while j < products_in_basket:
        last_product = driver.find_element_by_class_name('dataTable').find_elements_by_class_name('item')[products_in_basket-j]
        driver.find_element_by_name('remove_cart_item').click()
        wait = WebDriverWait(driver, 5)
        wait.until(EC.staleness_of(last_product))
        j += 1
