from selenium.webdriver.common.by import By
import time

def login(driver):

    username = input("Enter Username: ")
    email = input("Enter Email: ")
    password = input("Enter Password: ")

    driver.get("http://localhost:8080/Hostel_Management/ADMIN/VIEW/frontpage1.php")

    time.sleep(1)

    driver.find_element(By.ID, "Alogin").click()

    time.sleep(1)

    driver.find_element(By.ID, "name").send_keys(username)
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)

    driver.find_element(By.ID, "login_button").click()

    time.sleep(1)

    try:
        message = driver.switch_to.alert.text
        driver.switch_to.alert.accept()
    except:
        message = driver.find_element(By.TAG_NAME, "body").text

    return "Login successful!" in message