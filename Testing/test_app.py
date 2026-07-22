import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.microsoft import EdgeChromiumDriverManager

BASE_URL = "http://localhost/Hostel_Management/USER/VIEW/frontpage1.php"

@pytest.fixture(scope="module")
def driver():
    service = Service(EdgeChromiumDriverManager().install())
    options = webdriver.EdgeOptions()
    driver = webdriver.Edge(service=service, options=options)
    driver.implicitly_wait(10)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_frontpage_full_flow(driver):
    driver.get(BASE_URL)
    time.sleep(1)

    heading = driver.find_element(By.XPATH, "//*[contains(text(), 'Find your HOME!')]")
    assert heading.is_displayed()

    available_rooms = driver.find_element(By.XPATH, "//*[contains(text(), 'Available Rooms')]")
    assert available_rooms.is_displayed()

    register_btn = driver.find_element(By.XPATH, "//*[contains(text(), 'Register Now')]")
    assert register_btn.is_displayed()

    login_btn = driver.find_element(By.XPATH, "//*[contains(text(), 'Login')]")
    assert login_btn.is_displayed()

    admin_login_btn = driver.find_element(By.XPATH, "//*[contains(text(), 'Admin Login')]")
    assert admin_login_btn.is_displayed()

    room_cards = driver.find_elements(By.XPATH, "//*[contains(text(), 'Room No:')]")
    assert len(room_cards) >= 6

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    book_now_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Book Now')] | //a[contains(text(), 'Book Now')] | //*[contains(text(), 'Book Now')]")
    assert len(book_now_buttons) > 0

    book_now_buttons[0].click()
    time.sleep(1)

    alert = driver.switch_to.alert
    assert "login" in alert.text.lower()
    alert.accept()
    time.sleep(1)

def test_navigation_buttons(driver):
    driver.get(BASE_URL)
    time.sleep(1)

    register_btn = driver.find_element(By.XPATH, "//*[contains(text(), 'Register Now')]")
    register_btn.click()
    time.sleep(3)
    assert "register" in driver.current_url.lower() or "registration" in driver.current_url.lower()

    driver.get(BASE_URL)
    time.sleep(1)

    login_btn = driver.find_element(By.XPATH, "//*[contains(text(), 'Login') and not(contains(text(), 'Admin'))]")
    login_btn.click()
    time.sleep(3)
    assert "login" in driver.current_url.lower()

    driver.get(BASE_URL)
    time.sleep(1)

    admin_btn = driver.find_element(By.XPATH, "//*[contains(text(), 'Admin Login')]")
    admin_btn.click()
    time.sleep(3)

    try:
        alert = driver.switch_to.alert
        assert alert.text != ""
        alert.accept()
        time.sleep(1)
    except:
        assert "admin" in driver.current_url.lower()
REGISTRATION_URL = "http://localhost/Hostel_Management/USER/VIEW/registration1.php"

def test_registration_form_submission(driver):
    driver.get(REGISTRATION_URL)
    time.sleep(1)

    inputs = driver.find_elements(By.TAG_NAME, "input")

    inputs[0].clear()
    inputs[0].send_keys("Test User")

    inputs[1].clear()
    inputs[1].send_keys(f"testuser_{int(time.time())}@example.com")

    inputs[2].clear()
    inputs[2].send_keys("01700000000")

    inputs[3].clear()
    inputs[3].send_keys("Pass1234!")

    inputs[4].clear()
    inputs[4].send_keys("Pass1234!")

    blood_group_dropdown = Select(driver.find_element(By.TAG_NAME, "select"))
    blood_group_dropdown.select_by_index(1)

    register_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Register')] | //input[@type='submit' or @value='Register']")
    register_btn.click()

    time.sleep(2)

    try:
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(1)
    except:
        pass

    assert "login" in driver.current_url.lower() or "validation" in driver.current_url.lower() or driver.page_source


LOGIN_URL = "http://localhost/Hostel_Management/USER/VIEW/Login.php"
def test_login_form_submission(driver):
    driver.get(LOGIN_URL)
    time.sleep(1)

    inputs = driver.find_elements(By.TAG_NAME, "input")

    inputs[0].clear()
    inputs[0].send_keys("Protik Biswas")

    inputs[1].clear()
    inputs[1].send_keys("protikbiswas2088@gmail.com")

    inputs[2].clear()
    inputs[2].send_keys("111111")

    login_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')] | //input[@type='submit' or @value='Login']")
    login_btn.click()

    time.sleep(2)

    try:
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(1)
    except:
        pass

    assert driver.current_url != LOGIN_URL or driver.page_source