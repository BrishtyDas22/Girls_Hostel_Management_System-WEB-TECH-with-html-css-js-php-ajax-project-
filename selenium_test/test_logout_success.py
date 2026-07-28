from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from login import login

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

wait = WebDriverWait(driver,10)

try:

    if login(driver):

        print("\nLOGIN PASSED")

        wait.until(
            EC.element_to_be_clickable((By.ID,"logout"))
        ).click()

        wait.until(EC.alert_is_present())

        alert = driver.switch_to.alert

        print("Alert Message :",alert.text)

        # Click OK
        alert.accept()

        wait.until(
            EC.presence_of_element_located((By.ID,"login_button"))
        )

        if "adminlogin.php" in driver.current_url.lower():

            print("\nLOGOUT TEST PASSED")
            print("User logged out successfully.")

        else:

            print("\nLOGOUT TEST FAILED")

    else:

        print("LOGIN FAILED")

except Exception as e:

    print("\nLOGOUT TEST FAILED")
    print(e)

input("\nPress Enter to close browser...")

driver.quit()