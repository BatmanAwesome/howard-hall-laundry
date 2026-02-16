from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_machine_status(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        
        # Try to find the machine name first
        try:
            name_element = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".screen-title-row p.pt-4.name")
            ))
            machine_name = name_element.text
        except:
            machine_name = "Unknown Machine"
        
        # Check if machine is in use (has timer)
        try:
            timer_element = driver.find_element(By.CLASS_NAME, "time")
            time_remaining = timer_element.text
            status = "IN_USE"
            info = time_remaining
        except:
            # If no timer, check for price (available)
            try:
                price_element = driver.find_element(By.CLASS_NAME, "machine-price__total__value")
                status = "AVAILABLE"
                info = price_element.text
            except:
                status = "UNKNOWN"
                info = None
        
        return {
            "name": machine_name,
            "status": status,
            "info": info,
            "url": url
        }
    
    finally:
        driver.quit()

# Test it
url = "https://mycscgo.com/laundry/press-start/8e6bbe77-24ac-49dc-99e9-2e4cb119ba0b"
result = check_machine_status(url)
print(result)