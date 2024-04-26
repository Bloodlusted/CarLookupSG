import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

#Checksum to determine if plate is valid
def checksum(vehicle_plate):
    vehicle_plate = vehicle_plate.strip().upper()
    
    if len(vehicle_plate) > 7:
        return "INVALID INPUT"
    
    if len(re.findall(r'[A-Z]{1,3}', vehicle_plate)) > 1:
        return "INVALID INPUT"
    
    prefix = re.match(r'^[A-Z]{1,3}', vehicle_plate).group(0)
    if len(prefix) != 2:
        prefix = prefix[1:] if len(prefix) == 3 else prefix
    
    prefix_values = [ord(char) - 64 for char in prefix]
    if len(prefix_values) != 2:
        prefix_values.insert(0, 0)
    
    number_part = re.search(r'[0-9]{1,4}', vehicle_plate).group(0)
    number_part = number_part.zfill(4)
    number_values = [int(char) for char in number_part]
    
    combined_values = prefix_values + number_values
    
    checksum_multipliers = [9, 4, 5, 4, 3, 2]
    checksum_value = sum(value * multiplier for value, multiplier in zip(combined_values, checksum_multipliers)) % 19
    
    return vehicle_plate + "AZYXUTSRPMLKJHGEDCB"[checksum_value]

#Ensure clean user input
def input_validation(plate_number):
    pattern = r'^[A-Z]{1,3}\d{1,4}[A-Z]?$'
    
    if re.match(pattern, plate_number):
        return True
    else:
        return False

#Scrape vehicle info
def lookup(vehicle_number):
    # Set up Selenium WebDriver in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://vrl.lta.gov.sg/lta/vrl/action/pubfunc?ID=EnquireRoadTaxExpDtProxy")

    # Fill in the vehicle number input field
    vehicle_input = driver.find_element(By.NAME, "vehicleNo")
    vehicle_input.send_keys(vehicle_number)

    # Click the "I agree" checkbox
    agree_checkbox = driver.find_element(By.NAME, "agreeTC")
    agree_checkbox.click()

    # Click the "Next" button
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
    if query[-1].isnumeric():
        valid_plate = checksum(query)
    else:
        valid_plate = checksum(query[:-1])
    if query != valid_plate:
        print("Invalid license plate, looking up " + valid_plate + " instead.")
        lookup(valid_plate)
    else:
        lookup(query)