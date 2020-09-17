import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_admin_menu(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_name('username').send_keys('admin')
    driver.find_element_by_name('password').send_keys('admin')
    driver.find_element_by_name('login').click()
    menu_len = len(driver.find_element_by_id('box-apps-menu').find_elements_by_css_selector('li'))
    i = 0
    while i < menu_len:
        menu = driver.find_element_by_id('box-apps-menu')
        menu.find_elements_by_id("app-")[i].click()
        try:
            driver.find_elements_by_css_selector('td')[2].find_element_by_css_selector('h1')
        except NoSuchElementException:
            print('NO HEADER')
        if len(driver.find_elements_by_class_name('docs')) > 0:
            submenu_len = len(driver.find_element_by_class_name('docs').find_elements_by_css_selector('li'))
            j = 1
            while j < submenu_len:
                submenu = driver.find_element_by_class_name('docs')
                submenu.find_elements_by_css_selector('li')[j].click()
                try:
                    driver.find_elements_by_css_selector('td')[2].find_element_by_css_selector('h1')
                except NoSuchElementException:
                    print('NO HEADER')
                j += 1
        i += 1
