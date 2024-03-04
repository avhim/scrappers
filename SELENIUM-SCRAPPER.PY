from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

BASE_URL = "https://traveling.by/agencies/minsk"
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
options.add_argument("start-maximized")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option(
    # this will disable image loading
    "prefs", {"profile.managed_default_content_settings.images": 2}
)

driver = webdriver.Chrome(chrome_options=chrome_options)  # options=options
driver.get(BASE_URL)
time.sleep(15)

f = open("selenium-scrapping.txt", "a")
for page_id in range(1, 15):
    result = driver.find_element(By.ID, 'alltours')
    agencies = result.find_elements(By.CLASS_NAME, 'short')
    for agency in agencies:
        title = agency.find_element(By.TAG_NAME, 'h3')
        print(title.text)
        agency_phones = agency.find_elements(By.CSS_SELECTOR, 'ul.UserPro_telephones li')
        cleaned_phones = [''.join(p for p in phone.text if p.isalnum()) for phone in agency_phones]
        agency_info = f"{title.text};{';'.join([phone for phone in cleaned_phones])} \n"
        f.write(agency_info)

    next_page = driver.find_element(By.CSS_SELECTOR, 'a.next')
    next_page.click()

f.close()
driver.quit()
