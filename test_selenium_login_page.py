import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')

    yield driver

    driver.quit()


def test_show_all_pets(driver):
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('vasya@mail.com')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

for i in range(len(names)):
   assert images[i].get_attribute('src') != ''
   assert names[i].text != ''
   assert descriptions[i].text != ''
   assert ', ' in descriptions[i]
   parts = descriptions[i].text.split(", ")
   assert len(parts[0]) > 0
   assert len(parts[1]) > 0