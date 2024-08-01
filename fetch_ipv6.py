import requests
from bs4 import BeautifulSoup

# URL of the webpage to scrape
url = 'https://stock.hostmonit.com/CloudFlareYesV6'

# Set a User-Agent header
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Fetch the webpage
response = requests.get(url, headers=headers)
print(f"Fetched URL: {url} with status code: {response.status_code}")

# Check if the request was successful
if response.status_code != 200:
    print("Failed to retrieve the webpage.")
    exit(1)

soup = BeautifulSoup(response.text, 'html.parser')

# Extract IPv6 addresses from the table
ipv6_addresses = set()  # Use a set to avoid duplicates
for row in soup.select('tr.el-table__row'):
    cells = row.find_all('div', class_='cell')
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
