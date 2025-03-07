import json

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Firefox()
    driver.get('https://petfriends.skillfactory.ru/login')
    yield driver
    driver.quit()

def login_pet_friends(driver):
    wait = WebDriverWait(driver, 10)
    email_input = wait.until(EC.element_to_be_clickable((By.ID, 'email')))
    email_input.send_keys('vasya@mail.com')
    password_input = wait.until(EC.element_to_be_clickable((By.ID, 'pass')))
    password_input.send_keys('12345')
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
    login_button.click()




def has_duplicates(dict_list):
    seen = set()
    for d in dict_list:
        d_str = json.dumps(d, sort_keys=True)  
        if d_str in seen:
            return True  
        seen.add(d_str)
    return False

def get_pets_dict(driver):
    driver.implicitly_wait(10)

    pets = []
    table = driver.find_element(By.TAG_NAME, "table")
    rows = table.find_elements(By.TAG_NAME, "tr")
    keys = [key.text for key in driver.find_elements(By.XPATH, '//thead/tr/th[@scope="col"]')]
    photos = driver.find_elements(By.XPATH, '//tbody/tr/th[@scope="row"]/img')

    for i, row in enumerate(rows[1:]):
        cells = row.find_elements(By.TAG_NAME, "td")
        pet = {}
        for key, cell in zip(keys[1:], cells):
            pet[key] = cell.text
        try:
            pet["Фото"] = photos[i].get_attribute("src")
        except (IndexError, AttributeError):
            pet["Фото"] = ""
        del pet['']
        pets.append(pet)
    return pets


class TestPets:

    def test_show_all_pets(self, driver):
        wait = WebDriverWait(driver, 10)

        email_input = wait.until(EC.element_to_be_clickable((By.ID, 'email')))
        email_input.send_keys('vasya@mail.com')
        password_input = wait.until(EC.element_to_be_clickable((By.ID, 'pass')))
        password_input.send_keys('12345')
        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
        login_button.click()
        assert wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), "PetFriends"))
        end_point = "/all_pets"
        assert driver.current_url[-len(end_point):] == end_point


    def test_pet_cards(self, driver):
        driver.implicitly_wait(10)
        login_pet_friends(driver)
        images = driver.find_elements(By.CLASS_NAME, 'card-img-top')
        names = driver.find_elements(By.CLASS_NAME, 'card-title')
        descriptions = driver.find_elements(By.CLASS_NAME, 'card-text')
        for i in range(len(names)):
            driver.execute_script("arguments[0].scrollIntoView();", images[i])
            pet_description = descriptions[i].text
            assert images[i].get_attribute('src') != ''
            assert names[i].text == ''
            assert pet_description == ''
            assert ', ' in descriptions[i].text
            parts = pet_description.split(", ")
            assert len(parts[0]) > 0
            assert len(parts[1]) > 0

    def test_all_pets_excist(self, driver):
        wait = WebDriverWait(driver, 10)
        login_pet_friends(driver)
        my_pets = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Мои питомцы")))
        my_pets.click()

        pets = get_pets_dict(driver)
        pets_count = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'col-sm-4 left')]")))
        pets_count = int(pets_count.text.split("\n")[1].split(": ")[1])
        assert len(pets) == pets_count

    def test_half_of_pets_has_info(self, driver):
        wait = WebDriverWait(driver, 10)
        login_pet_friends(driver)
        my_pets = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Мои питомцы")))
        my_pets.click()
        pets = get_pets_dict(driver)
        count = 0
        for pet in pets:
            if count >= len(pets) // 2:
                break
            if pet['Имя'] and pet['Порода'] and pet['Возраст'] != '':
                count += 1
        assert count >= len(pets) // 2

    def test_all_pets_has_photo(self, driver):
        wait = WebDriverWait(driver, 10)
        login_pet_friends(driver)
        my_pets = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Мои питомцы")))
        my_pets.click()
        pets = get_pets_dict(driver)
        count = 0
        for pet in pets:
            if pet['Фото'] == '':
                break
            else:
                count += 1
        assert len(pets) == count

    def test_all_pets_has_unique_name(self, driver):
        wait = WebDriverWait(driver, 10)
        login_pet_friends(driver)
        my_pets = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Мои питомцы")))
        my_pets.click()
        pets = get_pets_dict(driver)
        names = [x['Имя'] for x in pets]
        unique_names = set(names)
        assert len(names) == len(unique_names)

    def test_all_pets_are_unique(self, driver):
        wait = WebDriverWait(driver, 10)
        login_pet_friends(driver)
        my_pets = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Мои питомцы")))
        my_pets.click()
        pets = get_pets_dict(driver)
        assert has_duplicates(pets) == False
