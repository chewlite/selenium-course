import pytest
from selenium import webdriver


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
        name_main = card.get_property('title')

        if name_main not in checked_products:

            price_main_value = ''
            discount_price_main_value = ''

            simple_price_main = card.find_elements_by_class_name('price')  # единственная цена в списке
            regular_price_main = card.find_elements_by_class_name('regular-price')  # обычная цена в списке
            campaign_price_main = card.find_elements_by_class_name('campaign-price')  # акционная цена в списке

            if len(simple_price_main) > 0:
                price_main = simple_price_main[0]
                price_main_value = price_main.text

            if len(regular_price_main) > 0 and len(campaign_price_main) > 0:

                price_main = regular_price_main[0]
                price_main_value = price_main.text

                # проверка: цвет обычной цены в списке - серый
                pm_color = price_main.value_of_css_property("color")
                pm_rgb = pm_color[5:len(pm_color)-1].split(', ')
                assert pm_rgb[0] == pm_rgb[1] == pm_rgb[2]

                # проверка: обычная цена в списке - зачеркнутая
                pm_style = price_main.value_of_css_property("text-decoration-line")
                assert pm_style == 'line-through'

                # проверка: цвет акционной цены в списке - красный
                discount_price_main = campaign_price_main[0]
                discount_price_main_value = discount_price_main.text
                dpm_color = discount_price_main.value_of_css_property("color")
                dpm_rgb = dpm_color[5:len(dpm_color)-1].split(', ')
                assert dpm_rgb[1] == dpm_rgb[2] == '0'

                # проверка: акционная цена в списке - жирная
                dpm_style = discount_price_main.value_of_css_property("font-weight")
                assert dpm_style == '700'

                # проверка: акционная цена в списке больше обычной цены
                pm_size = float(price_main.value_of_css_property("font-size").split('px')[0])
                dpm_size = float(discount_price_main.value_of_css_property("font-size").split('px')[0])
                assert pm_size < dpm_size

            card.click()

            # проверка: имена продукта в списке и в деталях совпадают
            name_details = driver.find_element_by_css_selector('h1').text
            assert name_details == name_main

            price_wrapper = driver.find_element_by_class_name('price-wrapper')
            simple_price_details = price_wrapper.find_elements_by_class_name('price')  # единственная цена в деталях
            regular_price_details = price_wrapper.find_elements_by_class_name('regular-price')  # обычная цена в деталях
            campaign_price_details = price_wrapper.find_elements_by_class_name('campaign-price')  # акц. цена в деталях

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
                rgb = pd_color[5:len(pd_color)-1].split(', ')
                assert rgb[0] == rgb[1] == rgb[2]

                # проверка: обычная цена в деталях - зачеркнутая
                pd_style = price_details.value_of_css_property("text-decoration-line")
                assert pd_style == 'line-through'

                # проверка: обычная цена в деталях - серая
                discount_price_details = campaign_price_details[0]
                discount_price_details_value = discount_price_details.text
                assert discount_price_details_value == discount_price_main_value

                # проверка: акционная цена в деталях - красная
                dpd_color = discount_price_details.value_of_css_property("color")
                rgb = dpd_color[5:len(dpd_color)-1].split(', ')
                assert rgb[1] == rgb[2] == '0'

                # проверка: акционная цена в деталях - жирная
                dpd_style = discount_price_details.value_of_css_property("font-weight")
                assert dpd_style == '700'

                # проверка: акционная цена в деталях больше обычной цены
                rpd_size = float(price_details.value_of_css_property("font-size").split('px')[0])
                dpd_size = float(discount_price_details.value_of_css_property("font-size").split('px')[0])
                assert rpd_size < dpd_size

            return name_main
    return None
