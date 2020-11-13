import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from exercise19.pages.main_page import MainPage
from exercise19.pages.product_details_page import ProductDetailsPage
from exercise19.pages.cart_page import CartPage


@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    wd = webdriver.Chrome(options=options)
    request.addfinalizer(wd.quit)
    return wd


def test_basket(driver):

    main = MainPage(driver)
    product = ProductDetailsPage(driver)
    cart = CartPage(driver)

    main.open()

    i = 0
    while i < 3:
        main.open_product_details(0)
        required_quantity = str(int(product.get_quantity_in_basket()) + 1)
        try:
            product.set_random_size()
        except NoSuchElementException:
            pass
        product.add_to_cart()
        product.wait_until_cart_updated(required_quantity)
        product.open_main_page()
        i += 1

    main.open_cart()
    products_in_basket = cart.get_quantity_of_positions()
    # после каждого удаления проверяем, что товар, который был на последней строчке в таблице, исчез - список уменьшился
    j = 0
    while j < products_in_basket:
        last_product = cart.get_last_product_in_table(products_in_basket-j)
        cart.remove_some_product()
        wait = WebDriverWait(driver, 5)
        wait.until(EC.staleness_of(last_product))
        j += 1
