from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Start the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# URL of the webpage to scrape
url = 'https://stock.hostmonit.com/CloudFlareYesV6'
driver.get(url)

# Extract IPv6 addresses from the table
ipv6_addresses = set()  # Use a set to avoid duplicates
rows = driver.find_elements(By.CSS_SELECTOR, 'tr.el-table__row')
for row in rows:
    cells = row.find_elements(By.CSS_SELECTOR, 'div.cell')
    if len(cells) > 1:
        ipv6_address = cells[1].text.strip()
        ipv6_addresses.add(ipv6_address)

# Log the fetched addresses
print("Fetched IPv6 Addresses:")
for address in ipv6_addresses:
    print(address)

# Write the unique IPv6 addresses to a file
with open('ipv6collect2.txt', 'w') as f:
    for address in ipv6_addresses:
        f.write(f"{address}\n")

# Check for duplicates
with open('ipv6collect2.txt', 'r') as f:
    lines = f.readlines()

unique_lines = set(lines)  # Remove duplicates
if len(unique_lines) < len(lines):
    print("Duplicates found and removed.")
    with open('ipv6collect2.txt', 'w') as f:
        f.writelines(unique_lines)
else:
    print("No duplicates found.")

# Close the driver
driver.quit()
