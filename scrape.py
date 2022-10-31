import requests
from bs4 import BeautifulSoup
import csv

URL = "https://www.cdkeys.com/halloween-sale"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

products = soup.find_all("div", class_="product-item-info")

data = []
for product in products:
    item_type = product.find("div", class_="product-item-ribbons").text.strip()
    item_name = product.find("a", class_="product-item-link").text.strip()
    rrp = product.find("span", {"data-price-type":"oldPrice"})
    item_rrp = "£0.00"
    if rrp:
        item_rrp = rrp.text.strip()
    item_price = product.find("span",{"data-price-type":"finalPrice"}).text.strip()
   
    new_row = {
        'Name': item_name,
        'Type': item_type,
        'Price': float(item_price.replace("£","")),
        'RRP': float(item_rrp.replace("£",""))
    }

    data.append(new_row)

keys = data[0].keys()

with open('Output.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(data)

