import pytest
from selenium import webdriver


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_alphabetical_order_of_countries(driver):
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    driver.find_element_by_name('username').send_keys('admin')
    driver.find_element_by_name('password').send_keys('admin')
    driver.find_element_by_name('login').click()
    table = driver.find_elements_by_css_selector('table')[1].find_element_by_css_selector('tbody')
    rows = table.find_elements_by_class_name('row')
    countries_list = []
    for row in rows:
        columns = row.find_elements_by_css_selector('td')
        country_name = columns[4].find_element_by_css_selector('a').text
        countries_list.append(country_name)
    i = 0
    while i < len(countries_list):
        result = 0
        if countries_list[i] != sorted(countries_list)[i]:
            assert result != 0
        i += 1
