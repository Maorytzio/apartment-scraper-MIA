import json

import requests as requests
from bs4 import BeautifulSoup
import time

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def init_driver():
    chrome_driver_path = "C:\Development\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    return driver


# driver = init_driver()

GOOGLE_FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSfn9kDZIbMzlKk-PVxW01SEqJA-S6KjYvLH4VHvWkj9vpWG2A/" \
                   "viewform?usp=sf_link"

ZILLOW_URL = "https://www.zillow.com/miami-fl/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds" \
             "%22%3A%7B%22north%22%3A25.879527583425485%2C%22east%22%3A-80.07785136572265%2C%22south%22%3A25" \
             ".526247572624758%2C%22west%22%3A-80.61000163427734%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22" \
             "%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%2C%22max%22%3A1%7D%2C" \
             "%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22" \
             "%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22" \
             "%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22" \
             "%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A12700%2C" \
             "%22regionType%22%3A6%7D%5D%2C%22usersSearchTerm%22%3A%22Miami%20FL%22%2C%22mapZoom%22%3A11%7D"

# driver.get(ZILLOW_URL)
# links_elements = driver.find_elements(By.XPATH, '//*[@id="swipeable"]/div[1]/a')
# links = [link.get_attribute('href') for link in links_elements]
# print(links)


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

# print(rent_data["props"]["pageProps"]["searchPageState"]["cat1"]["searchResults"]["listResults"])

#
results_list = rent_data["props"]["pageProps"]["searchPageState"]["cat1"]["searchResults"]["listResults"]

all_links = []
all_addresses = []
all_prices = []
for link in results_list:

    address = link["address"]
    all_addresses.append(address)

    if "units" in link and link["units"]:
        price = link["units"][0]["price"]
    else:
        price = 0
    all_prices.append(price)

    pure_link = link["detailUrl"]
    if "http" not in pure_link:
        all_links.append(f"https://www.zillow.com{pure_link}")
    else:
        all_links.append(pure_link)

print(len(all_links))
print(len(all_addresses))
print(len(all_prices))
