from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from login import login
import time


driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

driver.maximize_window()

wait = WebDriverWait(driver, 10)


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
    print("TEST CASE: DELETE ROOM")
    print("========================")

    room_no = input("Enter Room Number to Delete: ")

    room_row = find_room_row(room_no)

    if room_row is None:

        print("\nTEST PASSED: Invalid room number was rejected.")
        print(
            "Room",
            room_no,
            "was not found in the room table."
        )

    else:

        delete_button = room_row.find_element(
            By.CLASS_NAME,
            "table-delete-btn"
        )

        delete_button.click()
        time.sleep(1)

        driver.find_element(By.ID, "delete-btn").click()

        try:
            confirmation = wait.until(
                EC.alert_is_present()
            )

            confirmation.accept()

        except:
            print("Delete confirmation alert was not found.")

        time.sleep(2)

        deleted_room = find_room_row(room_no)

        if deleted_room is None:

            print(
                "\nTEST PASSED: Valid room deletion "
                "was completed successfully."
            )

            print(
                "Room",
                room_no,
                "was deleted successfully."
            )

        else:

            print("\nTEST FAILED: Unexpected system response.")
            print(
                "Room",
                room_no,
                "is still available in the room table."
            )

else:

    print("\nLOGIN FAILED")
    print("DELETE ROOM TEST WAS NOT EXECUTED")
    print(
        "Reason: Login is required before accessing "
        "Room Management."
    )


input("\nPress Enter to close browser...")

driver.quit()