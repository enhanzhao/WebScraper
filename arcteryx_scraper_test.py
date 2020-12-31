import arcteryx_scraper as AS
from bs4 import BeautifulSoup


def test_get_name():
    """
    Tests get_name() in arcteryx_scraper. Should get the name of the product. Data is checked against
    preexisting html file for consistent data comparision (the website updates frequently)
    The correct output is Abbott Pant Men's
    :return: nothing
    """
    with open("arcteryx_product.html", "r", encoding="utf-8") as f:
        html = f.read()
        soup = BeautifulSoup(html, "lxml")
        #item = soup.find("div", "product-name").text.rstrip().lstrip()
        assert AS.get_name(soup) == "Abbott Pant Men's", "function get_name() did not return the correct price!"


def test_get_price():
    """
     Tests get_name() in arcteryx_scraper. Should get the product price Data is checked against
     preexisting html file for consistent data comparision (the website updates frequently)
     Correct output is 170.00
     :return: nothing
     """
    with open("arcteryx_product.html", "r", encoding="utf-8") as f:
        html = f.read()
        soup = BeautifulSoup(html, "lxml")
        #price = soup.find("div", "product-price").text.lstrip().rstrip()
        assert AS.get_price(soup) == "170.00", "function get_price() did not return the correct price!"


def test_get_image():
    """
     Tests get_name() in arcteryx_scraper. Should get the product image link. Data is checked against
     preexisting html file for consistent data comparision (the website updates frequently)
     :return: nothing
     """
    with open("arcteryx_product.html", "r", encoding="utf-8") as f:
        html = f.read()
        soup = BeautifulSoup(html, "lxml")
        image_link = soup.find("img", src=True)
        assert AS.get_image(soup) == image_link, "function get_price() did not return the correct price!"


def test_get_color():
    """
     Tests get_color() in arcteryx_scraper. Should get all product colors in a list. Data is checked against
     preexisting html file for consistent data comparision (the website updates frequently)
     :return: nothing
     """
    with open("arcteryx_product.html", "r", encoding="utf-8") as f:
        html = f.read()
        soup = BeautifulSoup(html, "lxml")
        # colors = soup.find_all("span", style=True)
        # for i in range(len(colors)):
        #     colors[i] = colors[i].text
        assert AS.get_color(soup) == ['Hieroglyph', 'Ultima', 'Carbon Copy'], "function get_price() did not return the correct price!"


def test_gender_string_cut():
    """
    Test gender_string_cut(). Input will always have "men_" or "women_" in the beginning
    :return: nothing
    """

    strings_to_test = ["men_", "women_", "men_jacket", "women_jacket"]
    results = ["", "", "jacket", "jacket"]
    for i in range(4):
        assert AS.gender_string_cut(strings_to_test[i]) == results[i], "function gender_string_cut() did not return correctly"


