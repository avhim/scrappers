import time
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://traveling.by/agencies/minsk"
# id = 1  # increase after 50 search by 1
# paginator = f"?page={id}"
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}
page = requests.get(BASE_URL, headers=headers)
soup = BeautifulSoup(page.content, "html.parser")
# print(soup)
f = open("result.txt", "a")
results = soup.find(id="alltours")  # id='alltours'
agencies = results.find_all("section", class_='short')
for agency in agencies:
    title = agency.find('h3')
    agency_phones = agency.find('ul', class_='UserPro_telephones')
    phones = agency_phones.text.strip('\n').split('\n')
    cleaned_phones = [''.join(p for p in phone if p.isalnum()) for phone in phones]
    agency_info = f"{title.text};{';'.join([phone for phone in cleaned_phones])} \n"
    f.write(agency_info)
f.close()
#
for page_id in range(3, 15, 2):
    page = requests.get(f"https://traveling.by/agencies/minsk?page={page_id}", headers=headers)
    print(f"https://traveling.by/agencies/minsk?page={page_id}")
    soup = BeautifulSoup(page.content, "html.parser")
    f = open("result.txt", "a")
    results = soup.find(id="alltours")  # id='alltours'
    agencies = results.find_all("section", class_='short')
    for agency in agencies:
        title = agency.find('h3')
        agency_phones = agency.find('ul', class_='UserPro_telephones')
        phones = agency_phones.text.strip('\n').split('\n')
        cleaned_phones = [''.join(p for p in phone if p.isalnum()) for phone in phones]
        agency_info = f"{title.text};{';'.join([phone for phone in cleaned_phones])} \n"
        f.write(agency_info)
    f.close()
    # time.sleep(6)
print("end of script")
