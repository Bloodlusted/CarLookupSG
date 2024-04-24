import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def input_validation(plate_number):
    pattern = r'^[A-Z]{1,3}\d{1,4}[A-Z]$'
    
    if re.match(pattern, plate_number):
        return True
    else:
        return False

def lookup(vehicle_number):
    # Set up Selenium WebDriver in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://vrl.lta.gov.sg/lta/vrl/action/pubfunc?ID=EnquireRoadTaxExpDtProxy")

    # Find and fill in the vehicle number input field
    vehicle_input = driver.find_element(By.NAME, "vehicleNo")
    vehicle_input.send_keys(vehicle_number)

    # Find and click the "I agree" checkbox
    agree_checkbox = driver.find_element(By.NAME, "agreeTC")
    agree_checkbox.click()

    # Find and click the "Next" button
    next_button = driver.find_element(By.ID, "btnNext")
    next_button.click()

    try:
        # Wait for the page to load before extracting
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "dt-payment-dtls")))

        # Extract required information
        model = driver.find_element(By.XPATH, "//div[@class='dt-payment-dtls']//div[contains(@class, 'col-xs-5')]//p").text
        expiry = driver.find_element(By.XPATH, "//p[contains(@class, 'vrlDT-content-p')]").text
        print("Vehicle Make/Model:", model)
        print("Road Tax Expiry Date:", expiry)

    except TimeoutException:
        print("No record found")
    except Exception as e:
        print("An error occurred:", e)

    driver.quit()

query = input("Enter the vehicle plate number: ")
if input_validation(query) == False:
    print("Error: Please input a valid license plate")
else:
    lookup(query)
