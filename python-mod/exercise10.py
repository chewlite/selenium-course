import pytest
from selenium import webdriver
import re


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
        result = check_details(products, checked_products, driver)
        if result is None:
            break
        checked_products.append(result)
        driver.back()


def check_details(products, checked_products, driver):
    for p in products:

        card = p.find_element_by_css_selector('a')

        name_main = card.get_property('title')  # название продукта в списке

        if name_main not in checked_products:

            price_main_value = ''
            discount_price_main_value = ''

            simple_price_main = card.find_elements_by_class_name('price')
            regular_price_main = card.find_elements_by_class_name('regular-price')
            campaign_price_main = card.find_elements_by_class_name('campaign-price')

            if len(simple_price_main) > 0:
                price_main = simple_price_main[0]
                price_main_value = price_main.text  # единственная цена в списке

            if len(regular_price_main) > 0 and len(campaign_price_main) > 0:

                price_main = regular_price_main[0]
                price_main_value = price_main.text  # обычная цена в списке

                # проверка: цвет обычной цены в списке - серый
                pm_color = price_main.value_of_css_property("color")
                match = re.search(r"(rgb|rgba)\((\d{1,3}), (\d{1,3}), (\d{1,3})\)", pm_color)
                if match:
                    assert match.group(2) == match.group(3) == match.group(4)

                # проверка: обычная цена в списке - зачеркнутая
                pm_style = price_main.value_of_css_property("text-decoration-line")
                assert pm_style == 'line-through'

                discount_price_main = campaign_price_main[0]
                discount_price_main_value = discount_price_main.text  # акционная цена в списке

                # проверка: цвет акционной цены в списке - красный
                dpm_color = discount_price_main.value_of_css_property("color")
                match = re.search(r"(rgb|rgba)\((\d{1,3}), (\d{1,3}), (\d{1,3})\)", dpm_color)
                if match:
                    assert match.group(3) == match.group(4) == '0'

                # проверка: акционная цена в списке - жирная
                dpm_style = discount_price_main.value_of_css_property("font-weight")
                assert int(dpm_style) >= 700

                # проверка: акционная цена в списке больше обычной цены
                pm_size = float(price_main.value_of_css_property("font-size").split('px')[0])
                dpm_size = float(discount_price_main.value_of_css_property("font-size").split('px')[0])
                assert pm_size < dpm_size

            # переход на страницу деталей продукта
            card.click()

            # проверка: имена продукта в списке и в деталях совпадают
            name_details = driver.find_element_by_css_selector('h1').text
            assert name_details == name_main

            price_wrapper = driver.find_element_by_class_name('price-wrapper')
            simple_price_details = price_wrapper.find_elements_by_class_name('price')
            regular_price_details = price_wrapper.find_elements_by_class_name('regular-price')
            campaign_price_details = price_wrapper.find_elements_by_class_name('campaign-price')

            # проверка: единственная цена в списке и в деталях совпадают
            if len(simple_price_details) > 0:
                price_details = simple_price_details[0].text
                assert price_details == price_main_value

            if len(regular_price_details) > 0 and len(campaign_price_details) > 0:

                # проверка: обычная цена в списке и в деталях совпадают
                price_details = regular_price_details[0]
                price_details_value = price_details.text
                assert price_details_value == price_main_value

                # проверка: обычная цена в деталях - серая
                pd_color = price_details.value_of_css_property("color")
                match = re.search(r"(rgb|rgba)\((\d{1,3}), (\d{1,3}), (\d{1,3})\)", pd_color)
                if match:
                    assert match.group(2) == match.group(3) == match.group(4)

                # проверка: обычная цена в деталях - зачеркнутая
                pd_style = price_details.value_of_css_property("text-decoration-line")
                assert pd_style == 'line-through'

                # проверка: обычная цена в деталях - серая
                discount_price_details = campaign_price_details[0]
                discount_price_details_value = discount_price_details.text
                assert discount_price_details_value == discount_price_main_value

                # проверка: акционная цена в деталях - красная
                dpd_color = discount_price_details.value_of_css_property("color")
                match = re.search(r"(rgb|rgba)\((\d{1,3}), (\d{1,3}), (\d{1,3})\)", dpd_color)
                if match:
                    assert match.group(3) == match.group(4) == '0'

                # проверка: акционная цена в деталях - жирная
                dpd_style = discount_price_details.value_of_css_property("font-weight")
                assert int(dpd_style) >= 700

                # проверка: акционная цена в деталях больше обычной цены
                rpd_size = float(price_details.value_of_css_property("font-size").split('px')[0])
                dpd_size = float(discount_price_details.value_of_css_property("font-size").split('px')[0])
                assert rpd_size < dpd_size

            return name_main
    return None
