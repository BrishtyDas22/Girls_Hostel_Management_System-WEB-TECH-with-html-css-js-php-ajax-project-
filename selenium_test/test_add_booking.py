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


# Find a booking row using username and transaction ID
def find_booking_row(username, transaction_id):

    rows = driver.find_elements(
        By.CSS_SELECTOR,
        ".styled-table tbody tr"
    )

    for row in rows:

        cells = row.find_elements(By.TAG_NAME, "td")

        if len(cells) >= 8:

            table_username = cells[1].text.strip()
            table_transaction_id = cells[5].text.strip()

            if (
                table_username.lower() == username.lower()
                and table_transaction_id == transaction_id
            ):
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
        print("TEST CASE: ADD BOOKING")
        print("==============================")

        # Take booking information from the user
        username = input("Enter Existing Username: ").strip()
        room_number = input("Enter Existing Room Number: ").strip()
        transaction_number = input("Enter Transaction Number: ").strip()
        payment_method = input(
            "Enter Payment Method (Bkash/Nagad): "
        ).strip()
        transaction_id = input("Enter Transaction ID: ").strip()
        status = input(
            "Enter Booking Status (Pending/Approved): "
        ).strip()
        amount = input(
            "Enter Amount or press Enter to use room price: "
        ).strip()

        # Fill the username field
        driver.find_element(
            By.ID,
            "username"
        ).send_keys(username)

        # Fill the room number field
        driver.find_element(
            By.ID,
            "room_num"
        ).send_keys(room_number)

        # Fill the transaction number field
        driver.find_element(
            By.ID,
            "t_num"
        ).send_keys(transaction_number)

        # Select the payment method
        if payment_method.lower() == "bkash":

            driver.find_element(
                By.ID,
                "bkash"
            ).click()

        elif payment_method.lower() == "nagad":

            driver.find_element(
                By.ID,
                "nagad"
            ).click()

        else:

            print("\nADD BOOKING TEST FAILED")
            print("Reason: Invalid payment method.")

            input("\nPress Enter to close browser...")
            driver.quit()
            raise SystemExit

        # Fill the transaction ID field
        driver.find_element(
            By.ID,
            "t_id"
        ).send_keys(transaction_id)

        # Select the booking status
        if status.lower() == "pending":

            driver.find_element(
                By.ID,
                "pending"
            ).click()

        elif status.lower() == "approved":

            driver.find_element(
                By.ID,
                "approved"
            ).click()

        else:

            print("\nINVALID ADD BOOKING TEST PASSED")
            print("Reason: Invalid booking status.")

            input("\nPress Enter to close browser...")
            driver.quit()
            raise SystemExit

        # Fill the amount only when the user provides a value
        if amount != "":

            driver.find_element(
                By.ID,
                "amount"
            ).send_keys(amount)

        # Click the Add Student button
        driver.find_element(
            By.ID,
            "add-btn"
        ).click()

        # Wait for the page to reload
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

            print("\nADD BOOKING TEST FAILED")
            print("Reason:", error_boxes[0].text)

        else:

            # Check whether the new booking appears in the table
            added_row = find_booking_row(
                username,
                transaction_id
            )

            if added_row is not None:

                cells = added_row.find_elements(
                    By.TAG_NAME,
                    "td"
                )

                actual_username = cells[1].text.strip()
                actual_room = cells[2].text.strip()
                actual_transaction_number = cells[3].text.strip()
                actual_payment = cells[4].text.strip()
                actual_transaction_id = cells[5].text.strip()
                actual_status = cells[6].text.strip()
                actual_amount = cells[7].text.strip()

                print("\nADD BOOKING TEST PASSED")
                print("Booking was added successfully.")

                print("\nAdded Booking Information:")
                print("Username:", actual_username)
                print("Room Number:", actual_room)
                print(
                    "Transaction Number:",
                    actual_transaction_number
                )
                print("Payment Method:", actual_payment)
                print("Transaction ID:", actual_transaction_id)
                print("Status:", actual_status)
                print("Amount:", actual_amount)

            else:

                print("\nADD BOOKING TEST FAILED")
                print(
                    "Reason: The booking was not found "
                    "in the booking table."
                )

    else:

        print("\nLOGIN FAILED")
        print("ADD BOOKING TEST WAS NOT EXECUTED")


except Exception as error:

    print("\nADD BOOKING TEST FAILED")
    print("Technical Error:", error)


input("\nPress Enter to close browser...")

driver.quit()