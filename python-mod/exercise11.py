import pytest
from selenium import webdriver
import time
import random
import string


@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    wd = webdriver.Chrome(options=options)
    request.addfinalizer(wd.quit)
    return wd


def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))


def test_account_creation(driver):

    first_name = 'Jane'
    last_name = 'Doe'
    address = '153 W Parmenter St'
    postcode = '12550'
    city = 'New York'
    country = 'United States'
    email = random_char(7)+'@gmail.com'
    phone = '+1-345-345-33-33'
    password = 'MNw4B6sSLo34K6!'

    driver.get("http://localhost/litecart/en/create_account")

    # заполнение полей
    driver.find_element_by_name('firstname').send_keys(first_name)
    driver.find_element_by_name('lastname').send_keys(last_name)
    driver.find_element_by_name('address1').send_keys(address)
    driver.find_element_by_name('postcode').send_keys(postcode)
    driver.find_element_by_name('city').send_keys(city)
    driver.find_element_by_class_name('select2-selection').click()
    driver.find_element_by_class_name('select2-search__field').send_keys(country)
    driver.find_element_by_class_name('select2-results__options').find_element_by_css_selector('li').click()
    select_state = driver.find_elements_by_name('zone_code')[1]
    states = select_state.find_elements_by_css_selector('option')
    select_state.click()
    states.__getitem__(random.randint(0, len(states)-1)).click()
    driver.find_element_by_name('email').send_keys(email)
    driver.find_element_by_name('phone').send_keys(phone)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_name('confirmed_password').send_keys(password)

    # создать новый аккаунт и разлогиниться
    driver.find_element_by_name('create_account').click()
    driver.find_element_by_link_text('Logout').click()
    time.sleep(2)

    # залогиниться в созданный аккаунт и разлогиниться
    driver.find_element_by_name('email').send_keys(email)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_name('login').click()
    driver.find_element_by_link_text('Logout').click()
