from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.maximize_window()

driver.get("http://localhost:8080/Hostel_Management/ADMIN/VIEW/frontpage1.php")

print("Website Opened Successfully")

input("Press Enter to close browser...")

driver.quit()