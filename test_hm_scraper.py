import pytest
import codecs
from hm_scraper import *
import time
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
        "537.24 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.24"
          }

links = [
"https://www2.hm.com/en_ca/men/shop-by-product/"
"hoodies-sweatshirts/hoodies.html",
"https://www2.hm.com/en_ca/men/shop-by-product/hoodies-sweatshirts/"
"sweatshirts.html",
"https://www2.hm.com/en_ca/men/shop-by-product/jackets-and-coats/"
"jackets.html",
"https://www2.hm.com/en_ca/sale/shopbyproductmen/jacketscoats/"
"jackets.html",
"https://www2.hm.com/en_ca/men/shop-by-product/jackets-and-coats/"
"coats.html",
"https://www2.hm.com/en_ca/sale/shopbyproductmen/jacketscoats/"
"coats.html",
"https://www2.hm.com/en_ca/men/shop-by-product/"
"shirts.html",
"https://www2.hm.com/en_ca/sale/shopbyproductmen/"
"shirts.html",
"https://www2.hm.com/en_ca/men/shop-by-product/t-shirts-and-tank-tops/"
"short-sleeves.html",
"https://www2.hm.com/en_ca/sale/shopbyproductmen/tshirtstanks/"
"shortsleeve.html",
"https://www2.hm.com/en_ca/men/shop-by-product/t-shirts-and-tank-tops/"
"tanks.html",
"https://www2.hm.com/en_ca/men/shop-by-product/cardigans-and-sweaters/"
"cardigans.html",
"https://www2.hm.com/en_ca/men/shop-by-product/cardigans-and-sweaters/"
"sweaters.html",
"https://www2.hm.com/en_ca/men/shop-by-product/pants/pants.html",
"https://www2.hm.com/en_ca/men/shop-by-product/pants/joggers.html",
"https://www2.hm.com/en_ca/men/shop-by-product/jeans.html",
"https://www2.hm.com/en_ca/men/shop-by-product/shorts.html",
"https://www2.hm.com/en_ca/sale/shopbyproductmen/trousers/"
"joggers.html",
"https://www2.hm.com/en_ca/sale/shopbyproductmen/jeans.html",
"https://www2.hm.com/en_ca/sale/shopbyproductmen/shorts.html",
"https://www2.hm.com/en_ca/men/shop-by-product/shoes/sneakers.html",
"https://www2.hm.com/en_ca/sale/shopbyproductmen/shoes/sneakers.html",
"https://www2.hm.com/en_ca/men/shop-by-product/socks.html",
"https://www2.hm.com/en_ca/men/shop-by-product/accessories/"
"sunglasses.html",
"https://www2.hm.com/en_ca/men/shop-by-product/accessories/hats.html",
"https://www2.hm.com/en_ca/men/shop-by-product/accessories/bags.html",
"https://www2.hm.com/en_ca/sale/shopbyproductmen/accessories/"
"hats.html",
"https://www2.hm.com/en_ca/women/shop-by-product/hoodies-sweatshirts/"
"hoodies.html",
"https://www2.hm.com/en_ca/women/shop-by-product/hoodies-sweatshirts/"
"sweatshirts.html",
"https://www2.hm.com/en_ca/women/shop-by-product/tops/t-shirts.html",
"https://www2.hm.com/en_ca/women/shop-by-product/shirts-and-blouses/"
"shirts-and-blouses.html",
"https://www2.hm.com/en_ca/women/shop-by-product/shirts-and-blouses/"
"blouses.html",
"https://www2.hm.com/en_ca/women/shop-by-product/cardigans-and-jumpers"
"/cardigans.html",
"https://www2.hm.com/en_ca/women/shop-by-product/cardigans-and-jumpers"
"/jumpers.html",
"https://www2.hm.com/en_ca/women/shop-by-product/jackets-and-coats/"
"jackets.html",
"https://www2.hm.com/en_ca/women/shop-by-product/jackets-and-coats/"
"coats.html",
"https://www2.hm.com/en_ca/sale/shopbyproductladies/shirtsblouses/"
"shirts.html",
"https://www2.hm.com/en_ca/sale/shopbyproductladies/shirtsblouses/"
"blouses.html",
"https://www2.hm.com/en_ca/sale/shopbyproductladies/cardigansjumpers/"
"cardigans.html",
"https://www2.hm.com/en_ca/sale/shopbyproductladies/cardigansjumpers/"
"jumpers.html",
"https://www2.hm.com/en_ca/sale/shopbyproductladies/jacketscoats/"
"jackets.html",
"https://www2.hm.com/en_ca/sale/shopbyproductladies/jacketscoats/"
"coats.html",
"https://www2.hm.com/en_ca/sale/shopbyproductladies/hoodies-sweatshirt"
"s/hoodies.html",
"https://www2.hm.com/en_ca/sale/shopbyproductladies/hoodies-sweatshirt"
"s/sweatshirts.html",
"https://www2.hm.com/en_ca/women/shop-by-product/trousers/"
"joggers.html",
"https://www2.hm.com/en_ca/women/shop-by-product/trousers/"
"paperbag-pants.html",
"https://www2.hm.com/en_ca/women/shop-by-product/trousers/"
"dress-pants.html",
"https://www2.hm.com/en_ca/women/shop-by-product/jeans.html",
"https://www2.hm.com/en_ca/women/shop-by-product/skirts.html",
"https://www2.hm.com/en_ca/women/shop-by-product/shorts.html",
"https://www2.hm.com/en_ca/women/shop-by-product/trousers/"
"leggings.html",
"https://www2.hm.com/en_ca/sale/shopbyproductladies/trousers/"
"leggings.html",
"https://www2.hm.com/en_ca/sale/shopbyproductladies/jeans.html",
"https://www2.hm.com/en_ca/sale/shopbyproductladies/shorts.html",
"https://www2.hm.com/en_ca/sale/shopbyproductladies/skirts.html",
"https://www2.hm.com/en_ca/women/shop-by-product/shoes/sneakers.html",
"https://www2.hm.com/en_ca/women/shop-by-product/shoes/slippers.html",
"https://www2.hm.com/en_ca/women/shop-by-product/socks-and-tights/"
"socks.html",
"https://www2.hm.com/en_ca/sale/shopbyproductladies/shoes/"
"sneakers.html",
"https://www2.hm.com/en_ca/women/shop-by-product/accessories/"
"hats.html",
"https://www2.hm.com/en_ca/sale/shopbyproductladies/accessories/"
"hats.html",
"https://www2.hm.com/en_ca/women/shop-by-product/accessories/"
"sunglasses.html",
"https://www2.hm.com/en_ca/women/shop-by-product/accessories/"
"bags.html",
"https://www2.hm.com/en_ca/sale/shopbyproductladies/accessories/"
"bags.html",
'https://www2.hm.com/en_ca/women/shop-by-product/dresses.html',
"https://www2.hm.com/en_ca/women/shop-by-product/jumpsuits-rompers/"
"overalls.html",
"https://www2.hm.com/en_ca/women/shop-by-product/jumpsuits-rompers/"
"long-jumpsuits.html",
"https://www2.hm.com/en_ca/sale/shopbyproductladies/dresses.html",
"https://www2.hm.com/en_ca/sale/shopbyproductladies/jumpsuits.html"
]


@pytest.mark.parametrize('link', links)
def test_links(link):
    """
    Unit test all of the links currently being used in the scraper to check if
    they are valid or not
    :param link: Current link that being tested
    :return: None
    """
    time.sleep(1.0)
    assert requests.get(link, headers=headers).status_code == 200, "Website not found"


def test_name():
    """
    Test the get_name() function based on working on 'testing.html' file
    :return: first name of the return list should be "Relaxed Fit Hoodie"
    :return: last name of the return list should be "Printed Hoodie"
    :return: length of the name list should be 36
    """
    f = codecs.open("testing.html", "r")
    soup = BeautifulSoup(f, "lxml")
    name_list = get_name(soup)
    assert name_list[0] == "Relaxed Fit Hoodie", "get_name() returned" \
                                                 "the wrong name"
    assert name_list[-1] == "Printed Hoodie", "get_name() returned" \
                                              "the wrong name"
    assert len(name_list) == 36, "Invalid length of name list"


def test_price():
    """
    Test the get_price() function based on working on 'testing.html' file
    :return: first price of the return list should be "$24.99"
    :return: last price of the return list should be "$39.99"
    :return: length of the price list should be 36
    """
    f = codecs.open("testing.html", "r")
    soup = BeautifulSoup(f, "lxml")
    price_list = get_price(soup)
    assert price_list[0] == "$24.99", "get_price() returned wrong price"
    assert price_list[-1] == "$39.99", "get_price() returned wrong price"
    assert len(price_list) == 36, "Invalid length of price list"


def test_sale_price():
    """
    Test the get_sale_price() function based on working on 'testing.html' file
    :return: return list should have 36 of "N/A"
    :return: length of the sale price list should be 36
    """
    f = codecs.open("testing.html", "r")
    soup = BeautifulSoup(f, "lxml")
    sale_price_list = get_sale_price(soup)
    correct_list = []
    for i in range(36):
        correct_list.append("N/A")
    assert sale_price_list == correct_list, "get_sale_price()" \
                                            "returned wrong list"
    assert len(sale_price_list) == 36, "Invalid length of sale price list"


def test_color():
    """
    Test the get_color() function based on working on 'testing.html' file
    :return: first color of the return list should be "Purple||Black||White||Beige"
    :return: last color of the return list should be "Black/angels||Black/Rockish"
    :return: length of the color list should be 36
    """
    f = codecs.open("testing.html", "r")
    soup = BeautifulSoup(f, "lxml")
    color_list = get_color(soup)
    assert color_list[0] == "Purple||Black||White||Beige",\
        "get_color() returned wrong color"
    assert color_list[-1] == "Black/angels||Black/Rockish",\
        "get_color() returned the wrong color"
    assert len(color_list) == 36, "Invalid length of color list"


def test_image_link():
    """
    Test the get_image_link() function based on working on 'testing.html' file
    :return: first image link of the return list should be "//lp2.hm.com/hmgoepprod?set=source[/9a/b9/9ab9862ed3fdc7e8d573d7da8eea2bcb334fc145.jpg],origin[dam],category[men_hoodiessweatshirts_hoodies],type[DESCRIPTIVESTILLLIFE],res[y],hmver[2]&call=url[file:/product/main]"
    :return: length of the image link list should be 36
    """
    f = codecs.open("testing.html", "r")
    soup = BeautifulSoup(f, "lxml")
    image_link_list = get_image_link(soup)
    assert image_link_list[0] == "https://lp2.hm.com/hmgoepprod?set=source" \
                                 "[/9a/b9/9ab9862ed3fdc7e8d573d7da8eea2bcb334fc" \
                                 "145.jpg],origin[dam],category[men_hoodi" \
                                 "essweatshirts_hoodies],type[DESCRIPTIVE" \
                                 "STILLLIFE],res[y],hmver[2]&call=url[" \
                                 "file:/product/main]", \
                                 "get_image_link() returned wrong image link"
    assert len(image_link_list) == 36, "Invalid length of image link list"


def test_item_link():
    """
    Test the get_item_link() function based on working on 'testing.html' file
    :return: first item link of the return list should be "https://www2.hm.com/en_ca/productpage.0685814065.html"
    :return: length of the item link list should be 36
    """
    f = codecs.open("testing.html", "r")
    soup = BeautifulSoup(f, "lxml")
    item_link_list = get_item_link(soup)
    assert item_link_list[0] == 'https://www2.hm.com/en_ca/productpage.0685814065.html', \
        'get_item_link() returned wrong item link'
    assert len(item_link_list) == 36, "Invalid length of item link list"


def test_subcategory():
    """
    Test the get_subcategory() function based on working on 'testing.html' file
    :return: first subcategory of the return list should be "hoodie"
    :return: length of the item link list should be 36
    """
    f = codecs.open("testing.html", "r")
    soup = BeautifulSoup(f, "lxml")
    subcategory_list = get_subcategory(soup)
    assert subcategory_list[0] == "hoodie", "get_subcategory() returned" \
                                            "wrong subcategory"
    assert len(subcategory_list) == 36, "Invalid length of subcategory list"

