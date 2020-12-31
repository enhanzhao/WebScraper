# 370 Fall 2020: Billabong Scraper Test File

# This file tests the file billapong_scraper.py


import billabong_scraper
from bs4 import BeautifulSoup
import requests
import pytest
import io


# Constants

# website being explored by this scraper
baseurl = "https://www.billabong.com/en-ca"

# header to be used by scraper to avoid being blocked
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
}


def get_test_data():
    """
    Opens "billabong_data.html" to retrieve BeautifulSoup data
    used in testing billabong_scraper. The page represented by this
    data is "https://www.billabong.com/en-ca/womens-dresses/?start=47&sz=48"
    :return: page_data: (BeautifulSoup) data from billabong.com
    """
    with open("billabong_data.html") as f:
        page_data = BeautifulSoup(f, "lxml")

    return page_data


def get_item_test_data():
    """
    Opens "billabong_item_data.html" to retrieve BeautifulSoup data representing
    the page "https://www.billabong.com/en-ca/mid-day-dress-194843369087.html"
    :return: item_data: (BeautifulSoup) data from billabong.com
    """
    with io.open('billabong_item_data.html', encoding="utf-8") as f:
        item_data = BeautifulSoup(f, "lxml")

    return item_data


def test_number_of_products():
    """
    Replicates get_number_of_products in billabong_scraper, but replaces
    BeautifulSoup object creation with saved data.
    """
    soup = get_test_data()

    results = BeautifulSoup.find(soup, "div", class_="sorthitscontainer").text.strip()
    # extract numbers from string
    i = 0
    count = ""
    while results[i] != " ":
        count += results[i]
        i += 1
    # convert to integer
    number_of_products = int(count)

    assert number_of_products == 199


def test_product_links():
    """
    Replicates get_product_links in billabong_scraper, but replaces
    BeautifulSoup object creation with saved data.
    """
    page_data = get_test_data()
    number_of_products = 199

    product_links = []

    x = 0
    while x < number_of_products:
        # 48 items per page (sz in the url below) is the Billabong standard
        soup = page_data

        product_list = soup.find_all("div", class_="jsThumbnailReplace")

        page_links = []

        for product in product_list:
            for link in product.find_all("a", href=True):
                # baseurl not required in url assembly as it is already included in href
                page_links.append(link["href"])

        product_links.extend(page_links)

        # update x
        x = len(product_links)

    # Each product has multiple images and all links are being retrieved
    assert x == 240


def test_attributes():
    """
    Replicates get_attributes in billabong_scraper, but replaces
    BeautifulSoup object creation with saved data.
    """

    soup = get_item_test_data()

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

    link = "https://www.billabong.com/en-ca/mid-day-dress-194843369087.html"

    result = [name, gender, regular_price, sales_price, colors_as_string, link, first_image_link]

    assert result == ['Mid Day Dress', 'Women', '59.95', 'N/A', 'MULTI (mul)',
     'https://www.billabong.com/en-ca/mid-day-dress-194843369087.html',
     'https://images.boardriders.com/global/billabong-products/all/default/small/abjkd00132_billabong,wg_mul_frt1.jpg']


def get_link_list():
    """
    Uses billabong_scraper.get_category_links() to get dictionary containing
    urls, then extracts links from keys.
    :return: link_list: (list) urls
    """
    category_links = billabong_scraper.get_category_links()
    link_list = []
    for key in category_links:
        link_list.append(category_links[key])
    return link_list


@pytest.mark.parametrize('link', get_link_list())
def test_live_links(link):
    """
    Test that all category urls are still live
    :return: N/A
    """
    assert requests.get(link, headers=header).status_code == 200, "Website not found."
