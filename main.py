import requests as requests
from bs4 import BeautifulSoup

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfn9kDZIbMzlKk-PVxW01SEqJA-S6KjYvLH4VHvWkj9vpWG2A/" \
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

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 "
                  "Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,he;q=0.8",
}

response = requests.get(ZILLOW_URL, headers=headers)
response.raise_for_status()
html_doc = response.text

soup = BeautifulSoup(html_doc, 'html.parser')
print(soup.prettify())
