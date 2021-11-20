from bs4 import BeautifulSoup
import requests
import lxml
import csv


def tile_exist(link):
    response = requests.get(link).text
    soup = BeautifulSoup(response, "lxml")
    tiles = soup.find_all("a", class_="box--wrapper ym-gl ym-g25")
    return bool(tiles)

def write_to_csv(link):
    response = requests.get(link).text
    soup = BeautifulSoup(response, "lxml")
    tiles = soup.find_all("a", class_="box--wrapper ym-gl ym-g25")
    for tile in tiles:
        product_name = tile.find(name="div", class_="box--description--header")
        product_img = tile.find(name="img")["src"]
        price_dollar = tile.find(name="span", class_="box--value")
        price_cent = tile.find(name="span", class_="box--decimal")
        unit_price = tile.find(name="span", class_="box--baseprice")

        
        product_row = []
        if product_name:
            product_row.append(product_name.getText().strip())
        if product_img:
            product_row.append(product_img)
        if price_dollar and price_cent:
            product_row.append(f"{price_dollar.getText().strip()}{price_cent.getText().strip()}")
        if unit_price:
            product_row.append(unit_price.getText().strip())
        else:
            product_row.append("no unit price")


        with open("products_info.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow(product_row)


response = requests.get("https://www.aldi.com.au/en/groceries/")
soup = BeautifulSoup(response.text, "lxml")
menus = soup.select("li[class*='tab-nav--item dropdown--list--item']")


for menu in menus:
    link = menu.a.get("href")
    if tile_exist(link):
        write_to_csv(link)



# for menu in menus.find_all(name="a"):
#     links.append(menu.get("href"))





