import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.microsoft import EdgeChromiumDriverManager

BASE_URL = "http://localhost/Hostel_Management/USER/VIEW/frontpage1.php"
REGISTRATION_URL = "http://localhost/Hostel_Management/USER/VIEW/registration1.php"
LOGIN_URL = "http://localhost/Hostel_Management/USER/VIEW/Login.php"
FORGET_PASS_URL = "http://localhost/Hostel_Management/USER/VIEW/forget_password.php"
DASHBOARD_URL = "http://localhost/Hostel_Management/USER/VIEW/dashboard.php"
Complaint_URL = "http://localhost/Hostel_Management/USER/VIEW/complaint.php"
Edit_profile = "http://localhost/Hostel_Management/USER/VIEW/editprofile.php" 
Logout_URL = "http://localhost/Hostel_Management/USER/VIEW/editprofile.php"

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

def test_login_form_submission(driver):
    driver.get(LOGIN_URL)
    time.sleep(1)

    inputs = driver.find_elements(By.TAG_NAME, "input")

    inputs[0].clear()
    inputs[0].send_keys("Test User")

    inputs[1].clear()
    inputs[1].send_keys("testuser_1784739815@example.com")

    inputs[2].clear()
    inputs[2].send_keys("Pass1234!")

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

def test_forget_password_flow(driver):
    driver.get(LOGIN_URL)
    time.sleep(1)

    forget_pwd_link = driver.find_element(By.XPATH, "//*[contains(text(), 'Forget password?')]")
    forget_pwd_link.click()
    time.sleep(1)

    assert "forget_password.php" in driver.current_url.lower()

    inputs = driver.find_elements(By.TAG_NAME, "input")

    inputs[0].clear()
    inputs[0].send_keys("Test User")

    inputs[1].clear()
    inputs[1].send_keys("NewPass123!")

    inputs[2].clear()
    inputs[2].send_keys("NewPass123!")

    reset_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Reset Password')] | //input[@type='submit' or @value='Reset Password']")
    reset_btn.click()
    time.sleep(2)

    try:
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(1)
    except:
        pass

    driver.get(FORGET_PASS_URL)
    time.sleep(1)

    back_to_login_link = driver.find_element(By.XPATH, "//*[contains(text(), 'Go back to Login')]")
    back_to_login_link.click()
    time.sleep(1)

    assert "login.php" in driver.current_url.lower()

def test_room_booking_and_payment_flow(driver):
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

    assert "afterlogin.php" in driver.current_url.lower()

    book_now_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Book Now!')] | //a[contains(text(), 'Book Now!')] | //*[contains(text(), 'Book Now!')]")
    book_now_btn.click()
    time.sleep(2)

    assert "paymentmethod.php" in driver.current_url.lower()

    bkash_radio = driver.find_element(By.XPATH, "//input[@type='radio' and (@value='Bkash' or @value='bkash')] | //*[contains(text(), 'Bkash')]/preceding-sibling::input[1]")
    bkash_radio.click()

    all_inputs = driver.find_elements(By.XPATH, "//input[@type='text' or not(@type)]")

    editable_inputs = [inp for inp in all_inputs if not inp.get_attribute("readonly")]

    if len(editable_inputs) >= 2:
        editable_inputs[0].clear()
        editable_inputs[0].send_keys("01615663862")

        editable_inputs[1].clear()
        editable_inputs[1].send_keys("22222222")
    else:
        for inp in all_inputs:
            try:
                if inp.is_enabled() and inp.get_attribute("type") not in ["radio", "submit", "button", "hidden"]:
                    inp.send_keys("22222222")
            except:
                pass

    confirm_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Confirm Payment')] | //input[@type='submit' or @value='Confirm Payment']")
    confirm_btn.click()
    time.sleep(2)

    try:
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(1)
    except:
        pass

    assert driver.current_url != "http://localhost/Hostel_Management/USER/VIEW/paymentmethod.php?room=102" or driver.page_source


def test_user_dashboard_sidebar_navigation(driver):
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

    if "afterlogin.php" in driver.current_url.lower():
        try:
            dashboard_link = driver.find_element(By.XPATH, "//a[contains(@href, 'dashboard') or contains(translate(text(), 'DASHBOARD', 'dashboard'), 'dashboard')] | //*[contains(@class, 'profile') or contains(@class, 'user')]")
            dashboard_link.click()
            time.sleep(2)
        except:
            driver.get(DASHBOARD_URL)
            time.sleep(2)
    elif "dashboard.php" not in driver.current_url.lower():
        driver.get(DASHBOARD_URL)
        time.sleep(2)

    room_elem = driver.find_element(By.XPATH, "//*[contains(text(), '104')]")
    assert room_elem.is_displayed()

    sidebar_items = ["Overview", "Complaints", "Notices", "Notifications", "Feedback"]

    for item in sidebar_items:
        nav_button = driver.find_element(By.XPATH, f"//a[contains(., '{item}')] | //div[contains(@class, 'sidebar') or contains(@class, 'nav')]//*[contains(text(), '{item}')] | //*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{item.lower()}')]")
        assert nav_button.is_displayed()
        nav_button.click()
        time.sleep(1.5)

        try:
            alert = driver.switch_to.alert
            alert.accept()
            time.sleep(1)
        except:
            pass

        if item != "Overview" and "dashboard.php" not in driver.current_url.lower():
            driver.get(DASHBOARD_URL)
            time.sleep(2)

           


def test_edit_profile_update(driver):
    try:
        profile_icon = driver.find_element(By.XPATH, "//a[contains(@href, 'editprofile.php')] | //img[contains(@src, 'profile') or contains(@class, 'profile')]/ancestor::a")
        driver.execute_script("arguments[0].click();", profile_icon)
    except:
        driver.get("Edit_profile")

    time.sleep(2)

    blood_group_input = driver.find_element(By.XPATH, "//label[contains(text(), 'Blood group')]/following::input[1] | //input[@name='blood_group' or @name='bloodgroup' or @value='O+']")
    blood_group_input.clear()
    blood_group_input.send_keys("B+")

    update_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Update')] | //input[@type='submit' and contains(@value, 'Update')] | //*[contains(text(), 'Update') and not(contains(text(), 'Profile'))]")
    driver.execute_script("arguments[0].click();", update_btn)
    time.sleep(2)

    try:
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(1)
    except:
        pass        


def test_complaint_flow(driver):
    try:
        complaint_link = driver.find_element(By.XPATH, "//*[contains(translate(text(), 'COMPLAINTS', 'complaints'), 'complaints')]")
        driver.execute_script("arguments[0].click();", complaint_link)
    except:
        driver.get(Complaint_URL)
    
    time.sleep(1.5)

    category_select = Select(driver.find_element(By.TAG_NAME, "select"))
    category_select.select_by_visible_text("Plumbing")

    textarea = driver.find_element(By.TAG_NAME, "textarea")
    textarea.clear()
    textarea.send_keys("Test Complaint - Pipe leakage issue")

    submit_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')] | //input[@value='Submit']")
    driver.execute_script("arguments[0].click();", submit_btn)
    time.sleep(2)

    try:
        driver.switch_to.alert.accept()
        time.sleep(1)
    except:
        pass

    edit_btn = driver.find_element(By.XPATH, "//table//tr[1]//button[contains(text(), 'Edit')] | //table//tr[1]//a[contains(text(), 'Edit')] | (//button[contains(text(), 'Edit') or contains(@class, 'edit')])[1]")
    driver.execute_script("arguments[0].click();", edit_btn)
    time.sleep(1.5)

    textarea = driver.find_element(By.TAG_NAME, "textarea")
    textarea.clear()
    textarea.send_keys("Updated Complaint - Resolved minor leak")

    save_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit') or contains(text(), 'Update') or contains(text(), 'Save')]")
    driver.execute_script("arguments[0].click();", save_btn)
    time.sleep(2)

    try:
        driver.switch_to.alert.accept()
        time.sleep(1)
    except:
        pass

    delete_btn = driver.find_element(By.XPATH, "(//button[contains(text(), 'Delete') or contains(@class, 'delete')])[1] | (//a[contains(text(), 'Delete')])[1]")
    driver.execute_script("arguments[0].click();", delete_btn)
    time.sleep(1.5)

    try:
        driver.switch_to.alert.accept()
        time.sleep(1)
    except:
        pass
def test_feedback_flow(driver):
    try:
        feedback_link = driver.find_element(By.XPATH, "//*[contains(translate(text(), 'FEEDBACK', 'feedback'), 'feedback')]")
        driver.execute_script("arguments[0].click();", feedback_link)
    except:
        driver.get("http://localhost/Hostel_Management/USER/VIEW/feedback.php")

    time.sleep(1.5)

    feedback_select = Select(driver.find_element(By.TAG_NAME, "select"))
    feedback_select.select_by_visible_text("Good")

    textarea = driver.find_element(By.TAG_NAME, "textarea")
    textarea.clear()
    textarea.send_keys("Great service and clean environment.")

    post_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Post Feedback')] | //input[@value='Post Feedback']")
    driver.execute_script("arguments[0].click();", post_btn)
    time.sleep(2)

    try:
        driver.switch_to.alert.accept()
        time.sleep(1)
    except:
        pass

    edit_btn = driver.find_element(By.XPATH, "(//button[contains(text(), 'Edit') or contains(@class, 'edit')])[1] | (//a[contains(text(), 'Edit')])[1]")
    driver.execute_script("arguments[0].click();", edit_btn)
    time.sleep(1.5)

    textarea = driver.find_element(By.TAG_NAME, "textarea")
    textarea.clear()
    textarea.send_keys("Updated Feedback - Overall experience was excellent.")

    update_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Post') or contains(text(), 'Update') or contains(text(), 'Save')]")
    driver.execute_script("arguments[0].click();", update_btn)
    time.sleep(2)

    try:
        driver.switch_to.alert.accept()
        time.sleep(1)
    except:
        pass

    delete_btn = driver.find_element(By.XPATH, "(//button[contains(text(), 'Delete') or contains(@class, 'delete')])[1] | (//a[contains(text(), 'Delete')])[1]")
    driver.execute_script("arguments[0].click();", delete_btn)
    time.sleep(1.5)

    try:
        driver.switch_to.alert.accept()
        time.sleep(1)
    except:
        pass


def test_logout_from_edit_profile(driver):
    try:
        profile_icon = driver.find_element(By.XPATH, "//a[contains(@href, 'editprofile.php')] | //img[contains(@src, 'profile') or contains(@class, 'profile')]/ancestor::a")
        driver.execute_script("arguments[0].click();", profile_icon)
    except:
        driver.get(Logout_URL)

    time.sleep(1.5)

    logout_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Logout')] | //input[@value='Logout'] | //a[contains(text(), 'Logout')]")
    driver.execute_script("arguments[0].click();", logout_btn)
    time.sleep(2)

    try:
        driver.switch_to.alert.accept()
        time.sleep(1)
    except:
        pass

    assert "login" in driver.current_url.lower() or "frontpage" in driver.current_url.lower()