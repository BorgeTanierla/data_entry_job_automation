from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
                  "/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

GOOGLE_LINK = ("https://docs.google.com/forms/d/e/1FAIpQLSfAd7zGmSiazTR5xej5dYfnfe7s5WR3y12Oh8pq7EHIZgISEw"
               "/viewform?usp=dialog")
URL_WILLOW = "https://appbrewery.github.io/Zillow-Clone/"
response = requests.get(URL_WILLOW, headers=header)

# Objects
soup = BeautifulSoup(response.content, "html.parser")
links = soup.find_all('a', class_='property-card-link')
rent_price = soup.find_all(class_='PropertyCardWrapper__StyledPriceLine')
addresses = soup.find_all(class_="StyledPropertyCardDataArea-anchor")

# Create a list of links
links_list = [link.get("href") for link in links]

# Create a list of prices
price_list = [price.get_text().replace("/mo", "").split("+")[0] for price in rent_price]


# Create a list of addresses
address_list = []
for address in addresses:
    data = address.getText()
    data_strip = data.strip()
    clean_data = data_strip.replace("|", "")
    address_list.append(clean_data)

listing = [{"address": address, "price": price, "link": link} for address, price, link in zip(address_list,
                                                                                              price_list, links_list)]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

for per_list in listing:
    driver.get(GOOGLE_LINK)
    time.sleep(2)

    time.sleep(1)
    answer = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div'
                                                    '/div[2]/div/div[1]/div/div[1]/input')
    time.sleep(1)
    answer2 = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]'
                                                     '/div/div/div[2]/div/div[1]/div/div[1]/input')
    time.sleep(1)
    answer3 = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div'
                                                     '[2]/div/div[1]/div/div[1]/input')
    time.sleep(1)
    submit_button = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]'
                                                           '/div[1]/div/span/span')

    answer.send_keys(per_list["address"])
    answer2.send_keys(per_list["price"])
    answer3.send_keys(per_list["link"])
    submit_button.click()


