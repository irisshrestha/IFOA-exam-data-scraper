from bs4 import BeautifulSoup
import requests
import os
import time
from urllib.parse import urljoin

# Link of IFoA website page with examiners reports
base_url = "https://actuaries.org.uk/past-exam-papers-and-examiners-reports/"
response = requests.get(base_url)
soup = BeautifulSoup(response.text, "html.parser")

# Find all the links in the page which ends in ".zip"
zip_links = [urljoin(base_url, a['href']) for a in soup.find_all("a", href=True) if a["href"].endswith(".zip")]
print(zip_links)

# Define the folder name to save the zips files in
output_dir = "zips2"
os.makedirs(output_dir, exist_ok=True)

# Download and save all zip files
for url in zip_links:
    # Create full name for the file directory
    filename = os.path.join(output_dir, url.split("/")[-1])

    # If file already exists, append a timestamp to avoid overwrite
    if os.path.exists(filename):
        base, ext = os.path.splitext(filename)
        filename = f"{base}_{int(time.time())}{ext}"
        save_path = os.path.join(output_dir, filename)

    # Open file in write mode
    with open(filename, "wb") as f:
        f.write(requests.get(url).content)
