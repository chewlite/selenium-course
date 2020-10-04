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


def test_alphabetical_order_of_countries(driver):
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    driver.find_element_by_name('username').send_keys('admin')
    driver.find_element_by_name('password').send_keys('admin')
    driver.find_element_by_name('login').click()
    table = driver.find_elements_by_css_selector('table')[1].find_element_by_css_selector('tbody')
    rows = table.find_elements_by_class_name('row')
    country_list = []
    for row in rows:
        columns = row.find_elements_by_css_selector('td')
        country_name = columns[4].find_element_by_css_selector('a').text
        country_list.append(country_name)
    i = 0
    while i < len(country_list):
        result = 0
        if country_list[i] != sorted(country_list)[i]:
            assert result != 0
        i += 1


def test_alphabetical_order_of_zones(driver):
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    driver.find_element_by_name('username').send_keys('admin')
    driver.find_element_by_name('password').send_keys('admin')
    driver.find_element_by_name('login').click()

    checked_countries = []
    while True:
        table = driver.find_element_by_class_name('dataTable').find_element_by_css_selector('tbody')
        rows = table.find_elements_by_class_name('row')
        result = check_zones(rows, checked_countries, driver)
        if result is None:
            break
        checked_countries.append(result)
        driver.find_element_by_id('box-apps-menu').find_elements_by_id("app-")[2].click()
        time.sleep(2)


def check_zones(rows, checked_countries, driver):
    for row in rows:
        row_td = row.find_elements_by_css_selector('td')
        country = row_td[4].find_element_by_css_selector('a')
        country_name = country.text
        if country_name not in checked_countries:
            if int(row_td[5].text) > 0:
                country.click()
                z_table = driver.find_element_by_id('table-zones').find_element_by_css_selector('tbody')
                z_rows = z_table.find_elements_by_css_selector('tr')
                zone_list = []
                for j in range(1, len(z_rows)):
                    z_row = z_rows[j]
                    zone_name = z_row.find_elements_by_css_selector('td')[2].\
                        find_element_by_css_selector('input').text
                    zone_list.append(zone_name)
                i = 0
                while i < len(zone_list):
                    check = 0
                    if zone_list[i] != sorted(zone_list)[i]:
                        assert check != 0
                    i += 1
                return country_name
    return None
