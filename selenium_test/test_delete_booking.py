from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from login import login
import time


# Start Chrome browser
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

driver.maximize_window()

wait = WebDriverWait(driver, 10)


# Find a booking row using booking ID
def find_booking_row(booking_id):

    rows = driver.find_elements(
        By.CSS_SELECTOR,
        ".styled-table tbody tr"
    )

    for row in rows:

        cells = row.find_elements(By.TAG_NAME, "td")

        if len(cells) >= 8:

            table_booking_id = cells[0].text.strip()

            if table_booking_id == booking_id:
                return row

    return None


try:

    # Login using the reusable login function
    if login(driver):

        print("\nLOGIN PASSED")

        # Open the Room Bookings page
        wait.until(
            EC.element_to_be_clickable((By.ID, "managebookings"))
        ).click()

        # Wait until the booking table is visible
        wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "styled-table")
            )
        )

        print("ROOM BOOKINGS PAGE OPENED")

        print("\n==============================")
        print("TEST CASE: DELETE BOOKING")
        print("==============================")

        booking_id = input(
            "Enter Existing Booking ID to Delete: "
        ).strip()

        # Find the selected booking row
        booking_row = find_booking_row(booking_id)

        if booking_row is None:

            print("\nDELETE BOOKING TEST FAILED")
            print("Reason: Booking ID was not found.")

        else:

            # Read booking information before deletion
            cells = booking_row.find_elements(
                By.TAG_NAME,
                "td"
            )

            username = cells[1].text.strip()
            room_number = cells[2].text.strip()
            transaction_id = cells[5].text.strip()

            # Click the Delete button from the selected row
            delete_button = booking_row.find_element(
                By.CLASS_NAME,
                "btn-delete"
            )

            delete_button.click()

            time.sleep(1)

            # Click the form Delete button
            wait.until(
                EC.element_to_be_clickable(
                    (By.ID, "delete-btn")
                )
            ).click()

            # Wait for page reload
            wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "booking-section-box")
                )
            )

            time.sleep(1)

            # Check whether the website displayed an error
            error_boxes = driver.find_elements(
                By.CLASS_NAME,
                "error-box"
            )

            if len(error_boxes) > 0:

                print("\nDELETE BOOKING TEST FAILED")
                print("Reason:", error_boxes[0].text)

            else:

                # Check whether the deleted booking still exists
                deleted_row = find_booking_row(booking_id)

                if deleted_row is None:

                    print("\nDELETE BOOKING TEST PASSED")
                    print(
                        "Booking",
                        booking_id,
                        "was deleted successfully."
                    )

                    print("\nDeleted Booking Information:")
                    print("Username:", username)
                    print("Room Number:", room_number)
                    print("Transaction ID:", transaction_id)

                else:

                    print("\nDELETE BOOKING TEST FAILED")
                    print(
                        "Reason: Booking is still available "
                        "in the booking table."
                    )

    else:

        print("\nLOGIN FAILED")
        print("DELETE BOOKING TEST WAS NOT EXECUTED")


except Exception as error:

    print("\nDELETE BOOKING TEST FAILED")
    print("Technical Error:", error)


input("\nPress Enter to close browser...")

driver.quit()