from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the webdriver (replace the path with the location of your chromedriver)
driver = webdriver.Chrome('/path/to/chromedriver')

# Navigate to the target website
driver.get('https://example.com')

# Create a WebDriverWait instance with a longer timeout
wait = WebDriverWait(driver, 30)

# Wait for the table element to be present and clickable
try:
    table_presence = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.el-table')))
    table_clickable = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'table.el-table')))
except TimeoutException:
    print("Error: Table element not found within the specified timeout.")
    driver.quit()
    exit(1)

# Perform your desired actions on the table
table_rows = driver.find_elements(By.CSS_SELECTOR, 'tr.el-table__row')
for row in table_rows:
    # Extract data from the row
    # ...

# Close the browser
driver.quit()
