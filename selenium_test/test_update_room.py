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
    print("TEST CASE: UPDATE ROOM")
    print("========================")

    room_no = input("Enter Existing Room Number: ")

    room_row = find_room_row(room_no)

    if room_row is None:

        print("\nTEST PASSED: Invalid room number was rejected.")
        print("Room", room_no, "was not found in the room table.")

    else:

        edit_button = room_row.find_element(
            By.CLASS_NAME,
            "table-edit-btn"
        )

        edit_button.click()

        time.sleep(1)

        updated_price = input("Enter Updated Price: ")
        updated_capacity = input("Enter Updated Capacity: ")
        updated_student = input("Enter Updated Present Student: ")
        updated_type = input("Enter Updated Room Type (AC/Non-AC): ")

        price_field = driver.find_element(By.ID, "price")
        price_field.clear()
        price_field.send_keys(updated_price)

        capacity_field = driver.find_element(By.ID, "capacity")
        capacity_field.clear()
        capacity_field.send_keys(updated_capacity)

        student_field = driver.find_element(
            By.ID,
            "present_student"
        )

        student_field.clear()
        student_field.send_keys(updated_student)

        if updated_type.strip().lower() == "ac":
            driver.find_element(By.ID, "ac").click()

        else:
            driver.find_element(By.ID, "non_ac").click()

        driver.find_element(By.ID, "update-btn").click()

        try:
            confirmation = wait.until(
                EC.alert_is_present()
            )

            confirmation.accept()

        except:
            print("Update confirmation alert was not found.")

        time.sleep(2)

        error_boxes = driver.find_elements(
            By.CLASS_NAME,
            "error-box"
        )

        if len(error_boxes) > 0:

            print("\nTEST PASSED: Invalid room information was rejected.")
            print("Reason:", error_boxes[0].text)

        else:

            updated_row = find_room_row(room_no)

            if updated_row is None:

                print("\nTEST FAILED: Unexpected system response.")
                print("Room was not found after the update.")

            else:

                cells = updated_row.find_elements(
                    By.TAG_NAME,
                    "td"
                )

                actual_price = cells[2].text.strip()
                actual_type = cells[3].text.strip()
                actual_capacity = cells[4].text.strip()
                actual_student = cells[5].text.strip()

                if (
                    actual_price == updated_price
                    and actual_type.lower() == updated_type.lower()
                    and actual_capacity == updated_capacity
                    and actual_student == updated_student
                ):

                    print(
                        "\nTEST PASSED: Valid room information "
                        "was updated successfully."
                    )

                    print(
                        "Room",
                        room_no,
                        "was updated successfully."
                    )

                else:

                    print("\nTEST FAILED: Updated values did not match.")

                    print("Expected Price:", updated_price)
                    print("Actual Price:", actual_price)

                    print("Expected Type:", updated_type)
                    print("Actual Type:", actual_type)

                    print("Expected Capacity:", updated_capacity)
                    print("Actual Capacity:", actual_capacity)

                    print("Expected Student:", updated_student)
                    print("Actual Student:", actual_student)

else:

    print("\nLOGIN FAILED")
    print("UPDATE ROOM TEST WAS NOT EXECUTED")
    print(
        "Reason: Login is required before accessing "
        "Room Management."
    )


input("\nPress Enter to close browser...")

driver.quit()