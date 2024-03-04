from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.holiday.by/by/gid"
f = open('gid-holiday-results.txt', 'a')

options = Options()
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument("start-maximized")
# options.headless = True

driver = webdriver.Chrome(options=options)
driver.get(BASE_URL)

cookies_accept = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH,
                                "//div[@id='pop-up-policy']/div[@class='pop-up-contacts__content']/div/a[@id='pop-up-policy-accept']"))
)
cookies_accept.click()
close_subscribe = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                    "//div[@id='js-subscription-box']/span[@class='icon icon_close js-subscription-hide']")))
close_subscribe.click()


for page in range(1, 8):
    titles = driver.find_elements(By.XPATH, "//h3[@class='line-card-v4__title']/a")
    print(len(titles))
    for i in range(1, len(titles)+1):
        city = driver.find_element(By.XPATH, "//a[@class='line-card-v4__location-link']").get_attribute('textContent')
        if city != 'Минск':
            continue
        agency = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                            f"//article[@class='line-card-v4  line-card-v4_one-photo '][{i}]/div[@class='line-card-v4__content']/div[@class='line-card-v4__wrap-title']/h3[@class='line-card-v4__title']/a")))
        agency.click()
        agency_title = driver.find_element(By.XPATH, "//h1[@class='category-title h1']").get_attribute('textContent')
        try:
            agency_email = driver.find_element(By.CLASS_NAME, 'contact-link-apartment-card__link').get_attribute('textContent')
        except:
            agency_email = "null"

        try:
            agency_phones = driver.find_elements(By.XPATH,
                                             "//li[@class='pop-up-contacts-list__item']/a[@class='pop-up-contacts-list__link']")
        except:
            agency_phones = "null"

        cleaned_phones = [''.join(p for p in phone.get_attribute('textContent') if p.isnumeric()) for phone in agency_phones]
        agency_info = f"{i}; {agency_title}; {agency_email}; {'; '.join([phone for phone in cleaned_phones])} \n"
        print(agency_info)
        f.write(agency_info)
        driver.back()
    driver.find_element(By.XPATH, "//div[@class='list-pagination-wrap']/div[@class='list-pagination']/a[@class='list-pagination__control list-pagination__control_next']").click()

f.close()
driver.quit()
