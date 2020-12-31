import pytest
from bluenotes_scraper import *
import requests
from bs4 import BeautifulSoup
import time
import codecs
import os

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/63.0.3239.132 Safari/537.36 "
}

links = [
    "https://blnts.com/collections/bn_mens_shop-all-mens?Color=&Size="
    "&Waist=&Length=&tag=&price=&vendor=&sorting=&page=1",
    "https://blnts.com/collections/bn_mens_shop-all-mens?Color=&Size="
    "&Waist=&Length=&tag=&price=&vendor=&sorting=&page=2",
    "https://blnts.com/collections/bn_mens_shop-all-mens?Color=&Size="
    "&Waist=&Length=&tag=&price=&vendor=&sorting=&page=3",
    "https://blnts.com/collections/bn_mens_shop-all-mens?Color=&Size="
    "&Waist=&Length=&tag=&price=&vendor=&sorting=&page=4",
    "https://blnts.com/collections/bn_mens_shop-all-mens?Color=&Size="
    "&Waist=&Length=&tag=&price=&vendor=&sorting=&page=5",
    "https://blnts.com/collections/bn_mens_shop-all-mens?Color=&Size="
    "&Waist=&Length=&tag=&price=&vendor=&sorting=&page=6",
    "https://blnts.com/collections/bn_womens_shop-all-womens?Color=&Size="
    "&Waist=&Length=&tag=&price=&vendor=&sorting=&page=1",
    "https://blnts.com/collections/bn_womens_shop-all-womens?Color=&Size="
    "&Waist=&Length=&tag=&price=&vendor=&sorting=&page=2",
    "https://blnts.com/collections/bn_womens_shop-all-womens?Color=&Size="
    "&Waist=&Length=&tag=&price=&vendor=&sorting=&page=3",
    "https://blnts.com/collections/bn_womens_shop-all-womens?Color=&Size="
    "&Waist=&Length=&tag=&price=&vendor=&sorting=&page=4",
    "https://blnts.com/collections/bn_womens_shop-all-womens?Color=&Size="
    "&Waist=&Length=&tag=&price=&vendor=&sorting=&page=5",
    "https://blnts.com/collections/bn_womens_shop-all-womens?Color=&Size="
    "&Waist=&Length=&tag=&price=&vendor=&sorting=&page=6",
    "https://blnts.com/collections/bn_womens_shop-all-womens?Color=&Size="
    "&Waist=&Length=&tag=&price=&vendor=&sorting=&page=7",
    "https://blnts.com/collections/bn_womens_shop-all-womens?Color=&Size="
    "&Waist=&Length=&tag=&price=&vendor=&sorting=&page=8",
    "https://blnts.com/collections/bn_womens_shop-all-womens?Color=&Size="
    "&Waist=&Length=&tag=&price=&vendor=&sorting=&page=9"
]


def get_soup():
    """
    This function reads a html code in a text documnet
    called "bluenotes_testing.txt" and parse it as
    a soup object.
    :return: the soup object of the html
    """
    f = codecs.open("bluenotes_html", "r")
    soup = BeautifulSoup(f, "lxml")
    return soup


@pytest.mark.parametrize('link', links)
def test_request(link):
    """
    Unit Test all of the links currently being used
    in the scraper to see if they are still valid.
    :param link: The list of links to be tested.
    :return: None
    """
    time.sleep(1.0)
    assert requests.get(link, headers=header).status_code == 200, "Website not found."


def test_name():
    """
    This function tests the get_name() function.
    :return: None
    """
    soup = get_soup()
    list_of_names = get_name(soup)
    assert len(list_of_names) == 48, "Didn't get all the products names"
    assert list_of_names[0] == 'Eat Me Crew Neck Sweater', "Wrong product name!"
    assert list_of_names[-1] == 'Ice Cube Low Rider Tie Dye Graphic Tee', "Wrong product name!"


def test_links():
    """
    This function tests the get_link() function.
    :return: None
    """
    soup = get_soup()
    list_of_links = get_link(soup)
    assert len(list_of_links) == 48, "Didn't get all the products links"
    assert list_of_links[0] == 'https://blnts.com//products/' \
                               '0885-48342085-eat-me-crew-neck-sweater', "Wrong product link!"
    assert list_of_links[-1] == 'https://blnts.com//products/' \
                                '0888-61171130-ice-cube-low-rider-tie-dye-graphic-tee', "Wrong product link!"


def test_price():
    """
    This function tests get_price() function.
    :return: None
    """
    soup = get_soup()
    list_of_prices = get_price(soup)
    assert len(list_of_prices) == 48, "Didn't get all the products prices"
    assert list_of_prices[0] == '$49.99', "Wrong product price!"
    assert list_of_prices[-1] == '$29.99', "Wrong product price!"


def test_discount():
    """
    This function tests get_discount() function.
    :return: None
    """
    soup = get_soup()
    list_of_discounts = get_discount(soup)
    assert len(list_of_discounts) == 48, "Didn't get all the products discounts"
    assert list_of_discounts[0] == '$25.00', "Wrong product discount!"
    assert list_of_discounts[-1] == '$15.00', "Wrong product discount!"


def test_color():
    """
    This function tests get_color() function.
    :return: None
    """
    soup = get_soup()
    list_of_colors = get_color(soup)
    assert len(list_of_colors) == 48, "Didn't get all the products colors"
    assert list_of_colors[0] == 'Green || ', "Wrong product color!"
    assert list_of_colors[-1] == 'Black || ', "Wrong product color!"


def test_img():
    """
    This function tests get_img() function.
    :return: None
    """
    soup = get_soup()
    list_of_images = get_img(soup)
    assert len(list_of_images) == 48, "Didn't get all the products images"
    assert list_of_images[0] == 'https://cdn.shopify.com/s/files/1/1981/3329/' \
                                'products/088548342085-30-0_270x400_crop_center.jpg?v=1606231387', "Doesn't match the correct image!"
    assert list_of_images[-1] == 'https://cdn.shopify.com/s/files/1/1981/3329/' \
                                'products/088861171130-01-0_270x400_crop_center.jpg?v=1605030580', "Doesn't match the correct image!"


def test_get_all():
    """
    This function tests get_all() function.
    :param gender: (string) either "men" or "women"
    :return: (list of dictionaries) each dictionary is a product.
    """
    soup = get_soup()
    all_products = []
    all_names = get_name(soup)
    all_links = get_link(soup)
    all_prices = get_price(soup)
    all_discounts = get_discount(soup)
    all_colors = get_color(soup)
    all_images = get_img(soup)
    # adding products in the dictionary
    for item in range(len(all_names)):
        products_dict = {}
        products_dict["Name"] = all_names[item]
        products_dict["Gender"] = "men"
        products_dict["Price"] = all_prices[item]
        products_dict["Sale Price"] = all_discounts[item]
        products_dict["Colors"] = all_colors[item]
        products_dict["Item link"] = all_links[item]
        products_dict["Image link"] = all_images[item]
        all_products.append(products_dict)
        assert all_products[0] == {'Name': 'Eat Me Crew Neck Sweater',
                                    'Gender': 'men', 'Price': '$49.99',
                                    'Sale Price': '$25.00',
                                    'Colors': 'Green || ',
                                    'Item link': 'https://blnts.com//products'
                                                 '/0885-48342085-eat-me-crew-neck-sweater',
                                    'Image link': 'https://cdn.shopify.com/s/files/1/1981'
                                                  '/3329/products/088548342085-30-0_270x400'
                                                  '_crop_center.jpg?v=1606231387'}, "Doesn't match the correct product!"
    assert all_products[-1] == {'Name': 'Ice Cube Low Rider Tie Dye Graphic Tee',
                                     'Gender': 'men', 'Price': '$29.99',
                                     'Sale Price': '$15.00',
                                     'Colors': 'Black || ',
                                     'Item link': 'https://blnts.com//products'
                                                  '/0888-61171130-ice-cube-low-rider-tie-dye-graphic-tee',
                                     'Image link': 'https://cdn.shopify.com/s/'
                                                   'files/1/1981/3329/products/088861171130-01-0_270x400_'
                                                   'crop_center.jpg?v=1605030580'}, "Doesn't match the correct product!"
    return all_products


def test_organize_products():
    """
    This function calls the get_all() function and reorganize the data
    to different categories.
    :param gender: (string) either "men" or "women"
    :return: None
    """
    data = test_get_all()
    categories = organize_products(data, "men")
    assert categories[0][0] == {'Name': 'Eat Me Crew Neck Sweater',
                                'Gender': 'men', 'Price': '$49.99',
                                'Sale Price': '$25.00', 'Colors': 'Green || ',
                                'Item link': 'https://blnts.com//products/0885-'
                                             '48342085-eat-me-crew-neck-sweater',
                                'Image link': 'https://cdn.shopify.com/s/files/1/'
                                              '1981/3329/products/088548342085-30-'
                                              '0_270x400_crop_center.jpg?v=1606231387',
                                'Sub category': 'Sweater', 'Store': 'Bluenotes'}, "file doesn't match the category"

    assert categories[0][-1] == {'Name': 'Ice Cube Low Rider Tie Dye Graphic Tee',
                                 'Gender': 'men', 'Price': '$29.99',
                                 'Sale Price': '$15.00', 'Colors': 'Black || ',
                                 'Item link': 'https://blnts.com//products/0888'
                                              '-61171130-ice-cube-low-rider-tie-dye-graphic-tee',
                                 'Image link': 'https://cdn.shopify.com/s/files'
                                               '/1/1981/3329/products/0888611711'
                                               '30-01-0_270x400_crop_center.jpg?v=1605030580',
                                 'Sub category': 'Tee', 'Store': 'Bluenotes'}, "file doesn't match the category"


def test_csv_files():
    """
    This function tests whether the csv files are
    empty or not.
    :return: None
    """
    src_dir = "C:\\Users\\monaf_000\\PycharmProjects\\BlueNotesScraper"
    for root, dirs, files in os.walk(src_dir):
        for f in files:
            if f.endswith('men.csv') or f.endswith('women.csv'):
                assert os.stat(f).st_size != 0, f"This file '{f}' is empty!"


def main():
    test_name()
    test_links()
    test_price()
    test_discount()
    test_color()
    test_img()
    test_get_all("men")
    test_organize_products("men")
    test_csv_files()
    print("End of testing")


if __name__ == "__main__":
    main()
