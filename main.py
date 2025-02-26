from bs4 import BeautifulSoup
import requests
import sqlite3

# Base category url.
GROCERIES_URL = "https://www.aldi.com.au/en/groceries/"
links = []

# Codes do not access some categories and are added manually.
MANUAL_LINKS = [
    "https://www.aldi.com.au/groceries/freezer/",
    "https://www.aldi.com.au/groceries/liquor/wine/",
    "https://www.aldi.com.au/groceries/liquor/beer-cider/",
    "https://www.aldi.com.au/groceries/liquor/champagne-sparkling/",
    "https://www.aldi.com.au/groceries/liquor/spirits/",
    "https://www.aldi.com.au/groceries/pet-supplies/",
    "https://www.aldi.com.au/groceries/health/",
    "https://www.aldi.com.au/groceries/beauty/"
]

# Links to skip.
EXCLUDED_LINKS = [
    "https://www.aldi.com.au/en/about-aldi/returns-policy/",
    "https://www.aldi.com.au/groceries/super-savers/"
]

# Database connection
conn = sqlite3.connect("products_info.db")
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_title TEXT,
    product_image TEXT,
    pack_size TEXT,
    price TEXT,
    price_per_unit TEXT
);

''')
conn.commit()

# Returns a BeautifulSoup object for the given URL
def get_soup(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, "lxml")
    except requests.RequestException as e:
        print(f"Hata oluştu: {url} - {e}")
        return None

# Checks if there is a product in the sent url
def tile_exist(url):
    soup = get_soup(url)
    if not soup:
        return False
    tiles = soup.find_all("a", class_="box--wrapper ym-gl ym-g25")
    return bool(tiles)

# Categories and subcategories that the code can access on the site
def process_category(soup):
    if not soup:
        return

    category_class = "csc-textpic-imagerow csc-textpic-imagerow-last ym-clearfix"
    categories = soup.find_all("div", class_=category_class)

    for category in categories:
        links_in_category = category.find_all("a", href=True)
        for link in links_in_category:
            href = link["href"]
            full_url = href if href.startswith("http") else f"https://www.aldi.com.au{href}"
            if full_url not in links:
                links.append(full_url)

# Save to products data to db
def write_to_db(url):
    soup = get_soup(url)
    if not soup:
        return

    tiles = soup.find_all("a", class_="box--wrapper ym-gl ym-g25")

    for tile in tiles:
        try:
            product_name = tile.find("div", class_="box--description--header")
            product_img = tile.find("img")["src"] if tile.find("img") else "None"
            pack_size = tile.find("span", class_="box--amount")
            price_dollar = tile.find("span", class_="box--value")
            price_cent = tile.find("span", class_="box--decimal")
            unit_price = tile.find("span", class_="box--baseprice")

            product_row = (
                product_name.getText().strip() if product_name else "No Name",
                product_img,
                pack_size.getText().strip() if pack_size else "None",
                f"{price_dollar.getText().strip()}{price_cent.getText().strip()}" if price_dollar and price_cent else "No Price",
                unit_price.getText().strip() if unit_price else "No Unit Price"
            )

            # Insert using a single SQL command
            cursor.execute('''
                INSERT INTO products (product_title, product_image, pack_size, price, price_per_unit) 
                VALUES (?, ?, ?, ?, ?)
            ''', product_row)
        except Exception as e:
            print(f"Error processing product: {url} - {e}")

    conn.commit()

# Works main menus and collects related links
soup = get_soup(GROCERIES_URL)
if soup:
    menus = soup.select("li[class*='tab-nav--item dropdown--list--item']")
    for menu in menus:
        url = menu.a.get("href")
        if url in EXCLUDED_LINKS:
            continue
        if tile_exist(url):
            links.append(url)
        else:
            process_category(get_soup(url))

# Categories that need to be added manually are added
links.extend(MANUAL_LINKS)

# Pull all data from sent links
for link in links:
    write_to_db(link)
