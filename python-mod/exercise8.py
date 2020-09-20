import pytest
from selenium import webdriver


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_sticker_on_product(driver):
    driver.get("http://localhost/litecart/")
    box_list = driver.find_elements_by_class_name('box')
    for box in box_list:
        product_list = box.find_elements_by_class_name('product')
        for product in product_list:
            sticker_exists = product.find_elements_by_class_name('sticker')
            assert len(sticker_exists) > 0
