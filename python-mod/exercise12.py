import pytest
from selenium import webdriver
import time
import random
import os
from datetime import date, timedelta
import string


@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    wd = webdriver.Chrome(options=options)
    request.addfinalizer(wd.quit)
    return wd


def random_char():
    return ''.join(random.choice(string.ascii_letters) for x in range(10))


def test_correct_product_page(driver):

    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_name('username').send_keys('admin')
    driver.find_element_by_name('password').send_keys('admin')
    driver.find_element_by_name('login').click()

    driver.find_element_by_id('box-apps-menu').find_elements_by_id('app-')[1].click()
    driver.find_element_by_xpath('//*[@class="button"][text()=" Add New Product"]').click()
    time.sleep(1)

    product_name = 'NewProduct_' + random_char()
    code = 'ProductCode_' + random_char()
    quantity = random.uniform(1, 10000000000000)
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'blue_orange.jpeg')
    current_date = date.today()
    valid_from = current_date.strftime('%m/%d/%Y')
    valid_to = (current_date + timedelta(days=30)).strftime('%m/%d/%Y')
    description = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla egestas sagittis auctor. Nulla facilisi. Integer dapibus mauris lobortis ultrices scelerisque. Donec consequat, libero eu commodo egestas, enim velit luctus leo, vel pharetra tortor lorem bibendum enim. Nulla quis lacus nibh. Suspendisse commodo sit amet ante a facilisis. In hac habitasse platea dictumst. Curabitur sed risus malesuada, imperdiet turpis sit amet, malesuada lacus. Quisque a mauris congue, tincidunt lectus eget, blandit purus. Proin porta et enim ut tristique. Morbi ornare, nunc a suscipit aliquam, justo ipsum ornare magna, ut sollicitudin nunc neque sit amet felis. Vivamus rutrum urna mauris, vitae sagittis nibh mattis et. In hac habitasse platea dictumst. Aliquam consectetur a quam vel finibus. Proin ut est vel ante ornare faucibus ut non risus. Aliquam urna nulla, vehicula et lorem sed, ultrices dapibus mi. Proin quis ligula dictum, ornare nisi eget, scelerisque enim. Nulla suscipit vel mi sed elementum. Suspendisse eu metus eget dolor tincidunt posuere. Fusce facilisis iaculis nisl. Maecenas rhoncus ex non accumsan accumsan. Nam volutpat quis nisi nec consequat. Nullam lectus lorem, fringilla sit amet risus vel, molestie egestas sapien.'
    head_title = 'HeadTitle_' + random_char()
    purchase_price = random.uniform(1, 10000000000000)

    # 1st tab
    driver.find_element_by_name('status').click()
    driver.find_element_by_name('name[en]').send_keys(product_name)
    driver.find_element_by_name('code').send_keys(code)
    product_groups = driver.find_elements_by_name('product_groups[]')
    product_groups[(random.randint(0, len(product_groups)-1))].click()
    quantity_input = driver.find_element_by_name('quantity')
    quantity_input.send_keys(str(quantity))
    so_status = driver.find_element_by_name('sold_out_status_id')
    so_status.click()
    sos_options = so_status.find_elements_by_css_selector('option')
    sos_options[(random.randint(0, len(sos_options)-1))].click()
    driver.find_element_by_name('new_images[]').send_keys(filename)
    driver.find_element_by_name('date_valid_from').send_keys(valid_from)
    driver.find_element_by_name('date_valid_to').send_keys(valid_to)

    tabs = driver.find_element_by_class_name('tabs').find_elements_by_css_selector('li')

    # 2nd tab
    tabs[1].click()
    manufacturers = driver.find_element_by_name('manufacturer_id')
    manufacturers.click()
    man_options = manufacturers.find_elements_by_css_selector('option')
    man_options[(random.randint(0, len(man_options)-1))].click()
    driver.find_element_by_class_name('trumbowyg-editor').send_keys(description)
    driver.find_element_by_name('head_title[en]').send_keys(head_title)

    # 3rd tab
    tabs[3].click()
    pur_price_input = driver.find_element_by_name('purchase_price')
    pur_price_input.clear()
    pur_price_input.send_keys(str(purchase_price))
    currency = driver.find_element_by_name('purchase_price_currency_code')
    currency.click()
    cur_options = currency.find_elements_by_css_selector('option')
    cur_options[(random.randint(0, len(cur_options)-1))].click()

    driver.find_element_by_name('save').click()

    # check new product created
    time.sleep(1)
    names = []
    table_rows = driver.find_element_by_class_name('dataTable').find_elements_by_class_name('row')
    for row in table_rows:
        name = row.find_element_by_css_selector('a')
        names.append(name.text)
    assert product_name in names
