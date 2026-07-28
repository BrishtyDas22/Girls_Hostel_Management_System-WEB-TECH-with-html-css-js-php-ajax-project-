from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from login import login
import time


driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

driver.maximize_window()


def find_room_row(room_number):
    rows = driver.find_elements(
        By.CSS_SELECTOR,
        "#info-table tbody tr"
    )

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")

        if len(cells) >= 2:
            table_room_number = cells[1].text.strip()

            if table_room_number == room_number:
                return row

    return None


if login(driver):

    print("\nLOGIN PASSED")
    print("Precondition satisfied: User is logged into the system.")

    driver.find_element(By.ID, "roominfo").click()
    time.sleep(2)

    print("\n========================")
    print("TEST CASE: ADD ROOM")
    print("========================")

    room_no = input("Enter New Room Number: ")
    price = input("Enter Room Price: ")
    capacity = input("Enter Room Capacity: ")
    present_student = input("Enter Present Student: ")
    room_type = input("Enter Room Type (AC/Non-AC): ")

    driver.find_element(By.ID, "room_no").send_keys(room_no)
    driver.find_element(By.ID, "price").send_keys(price)
    driver.find_element(By.ID, "capacity").send_keys(capacity)

    driver.find_element(
        By.ID,
        "present_student"
    ).send_keys(present_student)

    if room_type.strip().lower() == "ac":
        driver.find_element(By.ID, "ac").click()
    else:
        driver.find_element(By.ID, "non_ac").click()

    driver.find_element(By.ID, "add-btn").click()

    time.sleep(2)

    error_boxes = driver.find_elements(
        By.CLASS_NAME,
        "error-box"
    )

    if len(error_boxes) > 0:

        print("\nTEST PASSED: Invalid room information was rejected.")
        print("Reason:", error_boxes[0].text)

    else:

        added_room = find_room_row(room_no)

        if added_room is not None:
            print("\nTEST PASSED: Valid room information was accepted.")
            print("Room", room_no, "was added successfully.")

        else:
            print("\nTEST FAILED: Unexpected system response.")
            print("Room was not found in the room table.")

else:

    print("\nLOGIN FAILED")
    print("ADD ROOM TEST WAS NOT EXECUTED")
    print("Reason: Login is required before accessing Room Management.")


input("\nPress Enter to close browser...")

driver.quit()
