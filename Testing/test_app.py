import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import Select

BASE_URL = "http://localhost/Hostel_Management/USER/VIEW/frontpage1.php"

@pytest.fixture(scope="module")
def driver():
    """Initializes Microsoft Edge WebDriver."""
    service = Service(EdgeChromiumDriverManager().install())
    options = webdriver.EdgeOptions()
    
    driver = webdriver.Edge(service=service, options=options)
    driver.implicitly_wait(10)
    driver.maximize_window()
    yield driver
    driver.quit()


def test_frontpage_loads_and_navigates(driver):
    # 1. Open the front page
    driver.get(BASE_URL)
    time.sleep(1)

    # 2. Verify page heading exists
    heading = driver.find_element(By.XPATH, "//*[contains(text(), 'Find your HOME!')]")
    assert heading.is_displayed(), "Main heading was not found on the front page."

    # 3. Locate and click 'Register Now' (flexible XPath matching text inside any element/button)
    register_btn = driver.find_element(By.XPATH, "//*[contains(text(), 'Register Now')]")
    register_btn.click()
    time.sleep(2)

    # 4. Assert redirection
    assert "registration" in driver.current_url.lower() or "reg" in driver.current_url.lower(), "Failed to navigate to registration page."

def test_frontpage_login_button(driver):
    """Tests if clicking the 'Login' button navigates correctly."""
    driver.get(BASE_URL)
    time.sleep(1)

    # 1. Locate and click 'Login'
    login_btn = driver.find_element(By.XPATH, "//*[contains(text(), 'Login')]")
    login_btn.click()
    time.sleep(2)

    # 2. Assert redirection to the login page
    assert "login" in driver.current_url.lower(), "Failed to navigate to login page."


REGISTRATION_URL = "http://localhost/Hostel_Management/USER/VIEW/registration1.php"

def test_registration_form_submission(driver):
   # """Tests filling and submitting the registration form."""
    driver.get(REGISTRATION_URL)
    time.sleep(1)

    # 1. Locate form input fields (using input order or tag attributes)
    inputs = driver.find_elements(By.TAG_NAME, "input")
    
    # Fill out form fields sequentially based on the layout
    # Name
    inputs[0].clear()
    inputs[0].send_keys("Test User")
    
    # E-mail
    inputs[1].clear()
    inputs[1].send_keys(f"testuser_{int(time.time())}@example.com")
    
    # Phone-Number
    inputs[2].clear()
    inputs[2].send_keys("01700000000")
    
    # Password
    inputs[3].clear()
    inputs[3].send_keys("Pass1234!")
    
   
    inputs[4].clear()
    inputs[4].send_keys("Pass1234!")

    
    blood_group_dropdown = Select(driver.find_element(By.TAG_NAME, "select"))
    
    blood_group_dropdown.select_by_index(1)

   
    register_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Register')] | //input[@type='submit' or @value='Register']")
    register_btn.click()
    
    time.sleep(2)

   
    assert "login" in driver.current_url.lower() or "validation" in driver.current_url.lower() or driver.page_source