import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time


@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    wd = webdriver.Chrome(options=options)
    request.addfinalizer(wd.quit)
    return wd


def test_windows(driver):
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    driver.find_element_by_name('username').send_keys('admin')
    driver.find_element_by_name('password').send_keys('admin')
    driver.find_element_by_name('login').click()
    time.sleep(1)

    driver.find_element_by_xpath('//*[@class="button"][text()=" Add New Country"]').click()
    initial_window = driver.current_window_handle

    links = driver.find_elements_by_class_name('fa-external-link')
    for link in links:
        old_windows = driver.window_handles
        link.click()
        wait = WebDriverWait(driver, 5)
        wait.until(EC.new_window_is_opened)
        current_windows = driver.window_handles
        new_window = (set(current_windows) - set(old_windows)).pop()
        driver.switch_to_window(new_window)
        driver.close()
        driver.switch_to_window(initial_window)

    driver.quit()

