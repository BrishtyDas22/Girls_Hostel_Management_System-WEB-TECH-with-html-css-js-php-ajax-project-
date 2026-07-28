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

        # Wait until the booking form is visible
        wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )

        print("ROOM BOOKINGS PAGE OPENED")

        print("\n==============================")
        print("TEST CASE: UPDATE BOOKING")
        print("==============================")

        booking_id = input(
            "Enter Existing Booking ID: "
        ).strip()

        # Find the selected booking row
        booking_row = find_booking_row(booking_id)

        if booking_row is None:

            print("\nUPDATE BOOKING TEST FAILED")
            print("Reason: Booking ID was not found.")

        else:

            # Click the Edit button of the selected booking
            edit_button = booking_row.find_element(
                By.CLASS_NAME,
                "btn-edit"
            )

            edit_button.click()

            time.sleep(1)

            # Take updated booking information
            updated_transaction_number = input(
                "Enter Updated Transaction Number: "
            ).strip()

            updated_payment_method = input(
                "Enter Updated Payment Method (Bkash/Nagad): "
            ).strip()

            updated_transaction_id = input(
                "Enter Updated Transaction ID: "
            ).strip()

            updated_status = input(
                "Enter Updated Status (Pending/Approved): "
            ).strip()

            updated_amount = input(
                "Enter Updated Amount: "
            ).strip()

            # Update the transaction number
            transaction_number_field = driver.find_element(
                By.ID,
                "t_num"
            )

            transaction_number_field.clear()
            transaction_number_field.send_keys(
                updated_transaction_number
            )

            # Update the payment method
            if updated_payment_method.lower() == "bkash":

                driver.find_element(
                    By.ID,
                    "bkash"
                ).click()

            elif updated_payment_method.lower() == "nagad":

                driver.find_element(
                    By.ID,
                    "nagad"
                ).click()

            else:

                print("\nINVALID UPDATE BOOKING TEST PASSED")
                print("Reason: Invalid payment method.")

                input("\nPress Enter to close browser...")
                driver.quit()
                raise SystemExit

            # Update the transaction ID
            transaction_id_field = driver.find_element(
                By.ID,
                "t_id"
            )

            transaction_id_field.clear()
            transaction_id_field.send_keys(
                updated_transaction_id
            )

            # Update the booking status
            if updated_status.lower() == "pending":

                driver.find_element(
                    By.ID,
                    "pending"
                ).click()

            elif updated_status.lower() == "approved":

                driver.find_element(
                    By.ID,
                    "approved"
                ).click()

            else:

                print("\nUPDATE BOOKING TEST FAILED")
                print("Reason: Invalid booking status.")

                input("\nPress Enter to close browser...")
                driver.quit()
                raise SystemExit

            # Update the amount
            amount_field = driver.find_element(
                By.ID,
                "amount"
            )

            amount_field.clear()
            amount_field.send_keys(updated_amount)

            # Click the Update button
            driver.find_element(
                By.ID,
                "update-btn"
            ).click()

            # Wait for page reload
            wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "booking-section-box")
                )
            )

            time.sleep(1)

            # Check whether the website displayed a validation error
            error_boxes = driver.find_elements(
                By.CLASS_NAME,
                "error-box"
            )

            if len(error_boxes) > 0:

                print("\nUPDATE BOOKING TEST FAILED")
                print("Reason:", error_boxes[0].text)

            else:

                # Find the booking again after update
                updated_row = find_booking_row(booking_id)

                if updated_row is None:

                    print("\nUPDATE BOOKING TEST FAILED")
                    print(
                        "Reason: Booking was not found "
                        "after update."
                    )

                else:

                    cells = updated_row.find_elements(
                        By.TAG_NAME,
                        "td"
                    )

                    actual_transaction_number = (
                        cells[3].text.strip()
                    )

                    actual_payment_method = (
                        cells[4].text.strip()
                    )

                    actual_transaction_id = (
                        cells[5].text.strip()
                    )

                    actual_status = (
                        cells[6].text.strip()
                    )

                    actual_amount = (
                        cells[7]
                        .text
                        .replace(" TK", "")
                        .strip()
                    )

                    # Compare the updated data with table data
                    if (
                        actual_transaction_number
                        == updated_transaction_number
                        and actual_payment_method.lower()
                        == updated_payment_method.lower()
                        and actual_transaction_id
                        == updated_transaction_id
                        and actual_status.lower()
                        == updated_status.lower()
                        and actual_amount
                        == updated_amount
                    ):

                        print("\nUPDATE BOOKING TEST PASSED")
                        print(
                            "Booking",
                            booking_id,
                            "was updated successfully."
                        )

                    else:

                        print("\nUPDATE BOOKING TEST FAILED")
                        print(
                            "Reason: Updated values "
                            "did not match."
                        )

                        print(
                            "\nExpected Transaction Number:",
                            updated_transaction_number
                        )
                        print(
                            "Actual Transaction Number:",
                            actual_transaction_number
                        )

                        print(
                            "\nExpected Payment Method:",
                            updated_payment_method
                        )
                        print(
                            "Actual Payment Method:",
                            actual_payment_method
                        )

                        print(
                            "\nExpected Transaction ID:",
                            updated_transaction_id
                        )
                        print(
                            "Actual Transaction ID:",
                            actual_transaction_id
                        )

                        print(
                            "\nExpected Status:",
                            updated_status
                        )
                        print(
                            "Actual Status:",
                            actual_status
                        )

                        print(
                            "\nExpected Amount:",
                            updated_amount
                        )
                        print(
                            "Actual Amount:",
                            actual_amount
                        )

    else:

        print("\nLOGIN FAILED")
        print("UPDATE BOOKING TEST WAS NOT EXECUTED")


except Exception as error:

    print("\nUPDATE BOOKING TEST FAILED")
    print("Technical Error:", error)


input("\nPress Enter to close browser...")

driver.quit()