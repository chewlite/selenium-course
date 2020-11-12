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


def test_windows(driver):
    driver.get("http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1")
    driver.find_element_by_name('username').send_keys('admin')
    driver.find_element_by_name('password').send_keys('admin')
    driver.find_element_by_name('login').click()

    rows = driver.find_element_by_class_name('dataTable').find_elements_by_class_name('row')
    i = 0
    while i < len(rows):
        rows = driver.find_element_by_class_name('dataTable').find_elements_by_class_name('row')
        name = rows[i].find_elements_by_css_selector('td')[2].find_element_by_css_selector('a')
        link = name.get_attribute('href')
        if 'product_id=' in link:
            name.click()
            logs = driver.get_log("browser")
            if len(logs) > 0:
                print('There are some browser logs:\n')
                for log in logs:
                    print(log + '\n')
            driver.back()
        time.sleep(1)
        i += 1

    driver.quit()
