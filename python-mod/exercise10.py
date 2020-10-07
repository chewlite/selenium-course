import pytest
from selenium import webdriver
import time


@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    wd = webdriver.Chrome(options=options)
    request.addfinalizer(wd.quit)
    return wd


def test_correct_product_page(driver):

    driver.get("http://localhost/litecart/")

    checked_products = []
    while True:
        products = driver.find_elements_by_class_name('product')
        result = compare_names(products, checked_products, driver)
        if result is None:
            break
        checked_products.append(result)
        driver.back()


def compare_names(products, checked_products, driver):
    for p in products:
        card = p.find_element_by_css_selector('a')
        name_main = card.get_property('title')
        if name_main not in checked_products:
            card.click()
            name_details = driver.find_element_by_css_selector('h1').text
            assert name_details == name_main
            return name_details
    return None
