from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://mycscgo.com/laundry/press-start/8e6bbe77-24ac-49dc-99e9-2e4cb119ba0b"

# 1. Setup the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    # 2. THE MISSING STEP: Tell the driver to go to the page
    driver.get(url)

    # 3. THE SAFETY STEP: Wait for the JavaScript to load the price
    # We wait up to 10 seconds for the element to exist
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "machine-price__total__value")))

    # 4. Extract the text
    print(f"Machine Price: {element.text}")

finally:
    # 5. Close the browser so it doesn't stay open in the background
    driver.quit()