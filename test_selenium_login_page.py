import pytest
from selenium import webdriver
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

def get_pet_table(driver):
    login_pet_friends(driver)
    my_pets = driver.find_element(By.LINK_TEXT, "Мои питомцы")
    my_pets.click()
    pet_count = driver.find_element(By.CSS_SELECTOR,
                                    "body > div.task2.fill > div > div.\.col-sm-4.left").text.split(': ')[1].split('\n')[0]
    pets = []
    table = driver.find_element(By.TAG_NAME, "table")
    rows = table.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        photos = row.find_elements(By.XPATH, '//tbody/tr/th[@scope="row"]')
        cells = row.find_elements(By.TAG_NAME, "td")
        keys = driver.find_elements(By.XPATH, '//thead/tr/th[@scope="col"]')
        pet = {}
        for cell, key in zip(cells, keys):
            if key.text == "":
                continue
            elif key.text == "Фото":
                try:
                    pet[key.text] = photos[len(pets)].get_attribute("src")
                except AttributeError or IndexError:
                    pet[key.text] = ""
            else:
                pet[key.text] = cell.text
        pets.append(pet)
    print(pets)



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
        # print([x.text for x in names])
        # print([x.text for x in descriptions])
        # print([x.get_attribute('src') for x in images])

        # end_point = "/all_pets"
        # assert driver.current_url[-len(end_point):] == end_point
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

    def test_pet_table(self, driver):
        get_pet_table(driver)
        # assert len(cells) == int(pet_count)
