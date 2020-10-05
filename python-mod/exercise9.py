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
        country_list.append(country_name)  # формируем список стран
    i = 0
    while i < len(country_list):
        check = 0
        # сравниваем элементы в получившемся списке стран и отсортированном списке стран
        if country_list[i] != sorted(country_list)[i]:
            assert check != 0  # в случае несовпадения стран тест падает
        i += 1


def test_alphabetical_order_of_zones_in_country(driver):
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    driver.find_element_by_name('username').send_keys('admin')
    driver.find_element_by_name('password').send_keys('admin')
    driver.find_element_by_name('login').click()

    checked_countries = []  # список проверенных стран
    while True:
        table = driver.find_element_by_class_name('dataTable').find_element_by_css_selector('tbody')
        rows = table.find_elements_by_class_name('row')
        result = check_zones(rows, checked_countries, driver)  # проверяем сортировку зон в стране
        if result is None:  # все нужные страны проверены - заканчиваем тест
            break
        checked_countries.append(result)  # добавляем проверенную страну в список проверенных
        driver.find_element_by_id('box-apps-menu').find_elements_by_id("app-")[2].click()
        time.sleep(2)


def check_zones(rows, checked_countries, driver):
    for row in rows:
        row_td = row.find_elements_by_css_selector('td')
        country = row_td[4].find_element_by_css_selector('a')
        country_name = country.text
        if country_name not in checked_countries:  # если еще не проверяли текущую страну
            if int(row_td[5].text) > 0:  # и если кол-во зон в этой стране > 0
                country.click()  # открываем страну
                z_table = driver.find_element_by_id('table-zones').find_element_by_css_selector('tbody')
                z_rows = z_table.find_elements_by_css_selector('tr')
                zone_list = []
                for j in range(1, len(z_rows)):  # исключаем строку с заголовками в таблице зон
                    z_row = z_rows[j]
                    zone_name = z_row.find_elements_by_css_selector('td')[2].\
                        find_element_by_css_selector('input').text
                    zone_list.append(zone_name)  # формируем список зон
                i = 0
                while i < len(zone_list):
                    check = 0
                    # сравниваем элементы в получившемся списке зон и отсортированном списке зон
                    if zone_list[i] != sorted(zone_list)[i]:
                        assert check != 0  # в случае несовпадения зон тест падает
                    i += 1
                return country_name
    return None


def test_alphabetical_order_of_zones_in_geo_zone(driver):
    driver.get("http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones")
    driver.find_element_by_name('username').send_keys('admin')
    driver.find_element_by_name('password').send_keys('admin')
    driver.find_element_by_name('login').click()

    checked_geo_zones = []
    while True:
        geo_zones = driver.find_elements_by_class_name('row')
        result = check_zones_in_selectors(geo_zones, checked_geo_zones, driver)
        if result is None:
            break
        checked_geo_zones.append(result)
        driver.find_element_by_id('box-apps-menu').find_elements_by_id("app-")[5].click()
        time.sleep(1)


def check_zones_in_selectors(geo_zones, checked_geo_zones, driver):
    for gz in geo_zones:
        gz_row = gz.find_elements_by_css_selector('td')[2].find_element_by_css_selector('a')
        gz_name = gz_row.text
        if gz_name not in checked_geo_zones:
            gz_row.click()
            z_table = driver.find_element_by_id('table-zones').find_element_by_css_selector('tbody')
            z_rows = z_table.find_elements_by_css_selector('tr')
            zone_list = []
            for j in range(1, len(z_rows)-1):  # отбрасываем строки с заголовками и с кнопкой добавления
                z_row = z_rows[j]
                zone_name_dropdown = z_row.find_elements_by_css_selector('td')[2]. \
                    find_element_by_css_selector('select'). \
                    find_elements_by_css_selector('option')
                for name in zone_name_dropdown:
                    if name.get_attribute("selected") == 'selected':
                        zone_name = name.text
                        zone_list.append(zone_name)
            i = 0
            while i < len(zone_list):
                check = 0
                # сравниваем элементы в получившемся списке зон и отсортированном списке зон
                if zone_list[i] != sorted(zone_list)[i]:
                    assert check != 0  # в случае несовпадения зон тест падает
                i += 1
            return gz_name
    return None
