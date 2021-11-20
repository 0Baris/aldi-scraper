from bs4 import BeautifulSoup
import requests
import lxml


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
        if product_name:
            print(product_name.getText())
        if product_img:
            print(product_img)
        if price_dollar and price_cent:
            print(f"{price_dollar.getText()}{price_cent.getText()}")
        if unit_price:
            print(unit_price.getText())
        else:
            print("no unit price")


response = requests.get("https://www.aldi.com.au/en/groceries/")
soup = BeautifulSoup(response.text, "lxml")
menus = soup.select("li[class*='tab-nav--item dropdown--list--item']")


for menu in menus:
    link = menu.a.get("href")
    if tile_exist(link):
        write_to_csv(link)



# for menu in menus.find_all(name="a"):
#     links.append(menu.get("href"))





