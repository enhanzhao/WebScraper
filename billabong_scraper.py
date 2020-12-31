# 370 Fall 2020: Billabong Scraper

# This file visits the Billabong web page to collect and store clothing
# information.
# Web Scraping with Python: Ecommerce Product Pages. In Depth including
# troubleshooting tutorial by John Watson Rooney as found at
# https://www.youtube.com/watch?v=nCuPv3tf2Hg was used in developing
# this program.


import csv
import requests
from bs4 import BeautifulSoup


# Constants

# website being explored by this scraper
baseurl = "https://www.billabong.com/en-ca"

# header to be used by scraper to avoid being blocked
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
}


def get_category_links():
    """
    Stores relevant category urls
    :return: (dict) contains the urls of all pages to be visited within website.
    """
    category_urls = {
                        "mens_tshirts": "https://www.billabong.com/en-ca/mens-tshirts/",
                        "mens_tanks": "https://www.billabong.com/en-ca/mens-tanks/",
                        "mens_shirts": "https://www.billabong.com/en-ca/mens-shirts/",
                        "mens_flannelshirts": "https://www.billabong.com/en-ca/mens-shirts-flannel/",
                        "mens_sweaters": "https://www.billabong.com/en-ca/mens-sweatshirts/",
                        "mens_jackets": "https://www.billabong.com/en-ca/mens-jackets/",
                        "mens_shorts": "https://www.billabong.com/en-ca/mens-shorts/",
                        "mens_pants": "https://www.billabong.com/en-ca/mens-pants/",
                        "womens_dresses": "https://www.billabong.com/en-ca/womens-dresses/",
                        "womens_jumpsuits": "https://www.billabong.com/en-ca/womens-jumpsuits/",
                        "womens_tops": "https://www.billabong.com/en-ca/womens-tops/",
                        "womens_tshirts": "https://www.billabong.com/en-ca/womens-tshirts/",
                        "womens_hoodies": "https://www.billabong.com/en-ca/womens-sweatshirts/",
                        "womens_sweaters": "https://www.billabong.com/en-ca/womens-sweaters/",
                        "womens_jackets": "https://www.billabong.com/en-ca/womens-jackets/",
                        "womens_shorts": "https://www.billabong.com/en-ca/womens-shorts/",
                        "womens_pants": "https://www.billabong.com/en-ca/womens-pants/",
                        "womens_skirts": "https://www.billabong.com/en-ca/womens-skirts/"
                     }

    return category_urls


def get_category_groups():
    """
    Stores relevant category groups
    :return: (dict) contains the titles of all groups belonging to
    each umbrella group.
    """
    category_groups = {
                        "tops_men": ["mens_tshirts", "mens_tanks",
                                     "mens_shirts", "mens_flannelshirts",
                                     "mens_sweaters", "mens_jackets"],
                        "bottoms_men": ["mens_shorts", "mens_pants"],
                        "tops_women": ["womens_tops", "womens_tshirts",
                                       "womens_hoodies", "womens_sweaters",
                                       "womens_jackets"],
                        "bottoms_women": ["womens_shorts", "womens_pants",
                                          "womens_skirts"],
                        "overall_women": ["womens_dresses", "womens_jumpsuits"],
                     }

    return category_groups


def get_number_of_products(url):
    """
    Visits site to retrieve number of products to be scraped from roxy.com
    :return: (int) number of products
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")

    results = soup.find("div", class_="sorthitscontainer").text.strip()
    # extract numbers from string
    i = 0
    count = ""
    while results[i] != " ":
        count += results[i]
        i += 1
    # convert to integer
    number_of_products = int(count)

    return number_of_products


def get_product_links(url, number_of_products):
    """
    Iterates over pages on site to collect product links until the last page has been
    found (when this occurs is based on number_of_products).
    :param url: (string) relevant url for category of interest
    :param number_of_products: (int) number of products to investigate
    :return: list of links to individual product pages
    """

    product_links = []

    x = 0
    while x < number_of_products:
        # 48 items per page (sz in the url below) is the Billabong standard
        r = requests.get(url + f"?start={x}&sz=48")
        soup = BeautifulSoup(r.content, "lxml")

        product_list = soup.find_all("div", class_="jsThumbnailReplace")

        page_links = []

        for product in product_list:
            for link in product.find_all("a", href=True):
                # baseurl not required in url assembly as it is already included in href
                page_links.append(link["href"])

        product_links.extend(page_links)

        # update x
        x = len(product_links)

    return product_links


def get_attributes(link):
    """
    Takes a link to a product page such as "https://www.billabong.com/en-ca/
    switchback-pullover-fleece-194843373299.html" to retrieves attribute data.
    :param link: (string) product link from billabong.com
    :return: (list), [name, gender, price, sale price or N/A, colors,
    product link, image links]
    """

    r = requests.get(link, headers=header)
    soup = BeautifulSoup(r.content, "lxml")

    # Retrieve product name
    try:
        name = soup.find("h1", class_="productname").text.strip()
    except:
        name = "Not Found"

    # Retrieve target gender
    try:
        if soup.find("a", title="Men") is not None:
            gender = "Men"
        else:
            gender = "Women"
    except:
        gender = "Not Found"

    # Retrieve regular and sales prices
    try:
        prices = soup.find("div", class_="price data-price")
        if prices["data-standardprice"] == "-":
            regular_price = prices["data-salesprice"]
            sales_price = "N/A"
        else:
            regular_price = prices["data-standardprice"]
            sales_price = prices["data-salesprice"]
    except:
        regular_price = "Not Found"
        sales_price = "Not Found"

    # Retrieve colors and image urls
    try:
        colors = []
        image_links = []
        swatches = soup.find("ul", class_="swatchesdisplay")
        for swatch in swatches.find_all("li", style=True):
            # extract image_url from "background: url('image_url')"
            image_links.append(swatch["style"][17:-2])
            # extract color associated with image
            for color in swatch.find("span", class_="swatchanchor obflk ajaxlk href-js"):
                colors.append(color)

        # change color list to string
        colors_as_string = ""
        last_color = colors[-1]

        for color in colors:
            if color is not last_color:
                colors_as_string = colors_as_string + color + " || "
            else:
                colors_as_string = colors_as_string + color

        # current policy is to save only the first image url
        first_image_link = image_links[0]
    except:
        colors_as_string = "Not Found"
        first_image_link = "Not Found"

    return [name, gender, regular_price, sales_price, colors_as_string, link, first_image_link]


def create_csv(category_name):
    """
    Create csv file for storing data
    :param: category_name: (string) category to be stored in csv file
    :return: filename: (string) name of csv file with header row and no data
    """
    fields = ["Name", "Gender", "Price", "Sale Price", "Colors",
              "Item Link", "Image Link", "Subcategory", "Store"]
    filename = "billabong_" + category_name + ".csv"
    f = csv.writer(open(filename, "w", newline=''))
    f.writerow(fields)
    return filename


def add_to_csv(filename, attribute_list):
    """
    Append to csv file with data ordered as follows:
    Name | Gender | Price | Sale Price (N/A) | Colors(a||b||c)
    | Item Link | Image Link | Subcategory | Store
    :param filename: (string) csv file where the data will be stored
    :param attribute_list: (list) contains product attributes
    :return: updated csv file
    """
    f = csv.writer(open(filename, "a", newline=''))
    f.writerow(attribute_list)


def main():

    # get guide to category organization
    category_groups = get_category_groups()

    # get dictionary with relevant links
    category_urls = get_category_links()

    for group in category_groups:
        # create csv file
        category_file = create_csv(group)

        for subcategory in category_groups[group]:

            # gather data and update csv file
            number_of_items = get_number_of_products(category_urls[subcategory])
            links = get_product_links(category_urls[subcategory], number_of_items)
            # currently acquiring data from up to 50 products from each category
            # but all products can be scraped if slicing is removed from links
            # below
            number_of_products_to_scrape = min(number_of_items, 50)
            for link in links[0:number_of_products_to_scrape]:
                attributes = get_attributes(link)
                # append subcategory and store for inclusion in csv
                attributes.append(subcategory)
                attributes.append("Billabong")
                add_to_csv(category_file, attributes)


# main
if __name__ == '__main__':
    main()
