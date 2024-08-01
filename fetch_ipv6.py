import requests
from bs4 import BeautifulSoup

# URL of the webpage to scrape
url = 'https://stock.hostmonit.com/CloudFlareYesV6'

# Fetch the webpage
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract IPv6 addresses from the table
ipv6_addresses = set()  # Use a set to avoid duplicates
for row in soup.select('tr.el-table__row'):
    cells = row.find_all('div', class_='cell')
    if len(cells) > 1:
        ipv6_address = cells[1].text.strip()
        ipv6_addresses.add(ipv6_address)

# Write the unique IPv6 addresses to a file
with open('ipv6collect2.txt', 'w') as f:
    for address in ipv6_addresses:
        f.write(f"{address}\n")

print("Fetched and saved the following IPv6 addresses:")
for address in ipv6_addresses:
    print(address)

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
