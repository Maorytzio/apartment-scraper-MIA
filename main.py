import json

import requests as requests
from bs4 import BeautifulSoup
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from links import GOOGLE_FORM_LINK, ZILLOW_URL


def init_driver():
    chrome_driver_path = "C:\Development\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    drivr = webdriver.Chrome(options=options)
    return drivr


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 "
                  "Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,he;q=0.8",
}

response = requests.get(ZILLOW_URL, headers=headers)
response.raise_for_status()
html_doc = response.text

soup = BeautifulSoup(html_doc, 'html.parser')
# print(soup.prettify())

test = soup.findAll("script", attrs={"type": "application/json"})
rent_data = test[1].text
rent_data = rent_data.replace("<!--", "")
rent_data = rent_data.replace("-->", "")
rent_data = json.loads(rent_data)

results_list = rent_data["props"]["pageProps"]["searchPageState"]["cat1"]["searchResults"]["listResults"]

all_links = []
all_addresses = []
all_prices = []
for apt in results_list:

    address = apt["address"]
    all_addresses.append(address)

    if "units" in apt and apt["units"]:
        price = apt["units"][0]["price"].strip("+")
    else:
        price = 0
    all_prices.append(price)

    pure_link = apt["detailUrl"]
    if "http" not in pure_link:
        all_links.append(f"https://www.zillow.com{pure_link}")
    else:
        all_links.append(pure_link)

driver = init_driver()
for i in range(len(all_links)):
    # Substitute your own Google Form URL here 👇
    driver.get(GOOGLE_FORM_LINK)

    time.sleep(2)
    address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div['
                                            '1]/div/div[1]/input')
    price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div['
                                          '1]/div/div[1]/input')
    apt = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div['
                                        '1]/div/div[1]/input')

    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    address.send_keys(all_addresses[i])
    price.send_keys(all_prices[i])
    apt.send_keys(all_links[i])

    submit_button.click()

driver.quit()

# send data to spreadsheet
driver.get('https://docs.google.com/forms/d/1KUrM_v9mHUZRewRZ3knaiO99qEAVToI2ABdGp6eJiek/edit#responses')
driver.implicitly_wait(2)
driver.find_element(By.XPATH,
                    '//*[@id="ResponsesView"]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div/span/span[2]').click()
driver.implicitly_wait(5)

driver.quit()
