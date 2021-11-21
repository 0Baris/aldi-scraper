from bs4 import BeautifulSoup, Tag
import requests
import lxml
import csv

# base url which contains all the submenus
groceries_url = "https://www.aldi.com.au/en/groceries/"
links = []


# return soup object for the given url
def get_soup(url):
    response = requests.get(url).text
    return BeautifulSoup(response, "lxml")

# checks if product tile exists for the given url
def tile_exist(url):
    soup = get_soup(url)
    tiles = soup.find_all("a", class_="box--wrapper ym-gl ym-g25")
    return bool(tiles)

# some sub-menus from the groceries contain further sub-categories
# product tiles exist in those sub-categories
def process_category(soup):
    category_class = "csc-textpic-imagerow csc-textpic-imagerow-last ym-clearfix"
    categories = soup.find('div', class_=category_class)
    for i in categories:    
        if isinstance(i, Tag):
            links.append(i.a.get("href"))


# write product infos to the csv file from the given url
def write_to_csv(url):
    soup = get_soup(url)
    # finds all product tiles 
    tiles = soup.find_all("a", class_="box--wrapper ym-gl ym-g25")
    for tile in tiles:
        product_name = tile.find(name="div", class_="box--description--header")
        product_img = tile.find(name="img")["src"]
        pack_size = tile.find(name="span", class_="box--amount")
        price_dollar = tile.find(name="span", class_="box--value")
        price_cent = tile.find(name="span", class_="box--decimal")
        unit_price = tile.find(name="span", class_="box--baseprice")
       
        product_row = []
        if product_name:
            product_row.append(product_name.getText().strip())
        if product_img:
            product_row.append(product_img)
        if pack_size:
            product_row.append(pack_size.getText().strip())
        else:
            product_row.append("None")
        if price_dollar and price_cent:
            product_row.append(f"{price_dollar.getText().strip()}{price_cent.getText().strip()}")
        if unit_price:
            product_row.append(unit_price.getText().strip())
        else:
            product_row.append("no unit price")

        with open("products_info.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow(product_row)


soup = get_soup(groceries_url)
# obtaining all the submenus from groceries
menus = soup.select("li[class*='tab-nav--item dropdown--list--item']")



for menu in menus:
    url = menu.a.get("href")
    if url == "https://www.aldi.com.au/en/about-aldi/returns-policy/":
        continue
    if tile_exist(url):
        links.append(url)
    else:
        soup = get_soup(url)
        process_category(soup)
        
csv_header = ['Product_title', 'Product_image', 'Packsize', 'Price', 'Price per unit']
with open("products_info.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(csv_header)

for link in links:
    write_to_csv(link)