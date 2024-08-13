import requests
import re

# Fetch the webpage
url = 'https://stock.hostmonit.com/CloudFlareYesV6'
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Use regex to find all IPv6 addresses
    ipv6_pattern = r'([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}'
    ipv6_addresses = re.findall(ipv6_pattern, response.text)

    # Use a set to keep unique addresses while maintaining order
    unique_ipv6_addresses = []
    seen = set()
    for address in ipv6_addresses:
        if address not in seen:
            seen.add(address)
            unique_ipv6_addresses.append(address)
        if len(unique_ipv6_addresses) >= 20:  # Limit to 20 addresses
            break

    # Write the extracted addresses to a file
    with open('ipv6-hostmonit.txt', 'w') as f:
        for address in unique_ipv6_addresses:
            f.write(f"[{address}]\n")  # Enclose each address in brackets
else:
    print(f"Failed to retrieve the webpage: {response.status_code}")
