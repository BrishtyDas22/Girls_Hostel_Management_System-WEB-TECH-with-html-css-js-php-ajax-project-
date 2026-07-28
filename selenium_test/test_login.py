from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

username = input("Enter Username: ")
email = input("Enter Email: ")
password = input("Enter Password: ")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.maximize_window()

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

if "Login successful!" in message:
    print("TEST PASSED: Valid login successful.")
else:
    print("TEST PASSED: Invalid username/email/password. Login rejected.")

input("\nPress Enter to close browser...")

driver.quit()