from bs4 import BeautifulSoup
from helium import *
import time
import csv


def get_name(soup_object):
    """
    This function returns the name of the products from the soup object
    of a website
    :param soup_object: the soup object of the website being scraped.
    :return: (list): a list of strings of the name of every product.
    """
    productsName = []
    info = soup_object.find_all("h2", "featured-collection__product-title")
    for name in info:
        productsName.append(name.text)
    return productsName


def get_link(soup_object):
    """
    This function returns the webpage link of the products from the soup object
    of a website.
    :param soup_object: the soup object of the website being scraped.
    :return: (list): a list of strings of the name of every product's link.
    """
    productsLink = []
    info = soup_object.find_all("a", "featured-collection__link")
    for link in info:
        fullLink = "https://blnts.com/" + link.get("href")
        productsLink.append(fullLink)
    return productsLink


def get_price(soup_object):
    """
    This function returns the price of the products from the soup object
    of a website.
    :param soup_object: the soup object of the website being scraped.
    :return: (list): a list of the prices "as strings" of every product.
    """
    productsPrice = []
    info = soup_object.find_all("p", "featured-collection__product-price js-product-price")
    for price in info:
        try:
            # print("The price is :", price.find("span", "grid-item-price").text, end=" , ")
            productsPrice.append(price.find("span", "grid-item-price").text)
        except:
            try:
                # print("The price is :", price.find("span", "grid-item-compare").text)
                productsPrice.append(price.find("span", "grid-item-compare").text)
            except:
                pass
    return productsPrice


def get_discount(soup_object):
    """
    This function returns the price of the products from the soup object
    of a website.
    :param soup_object: the soup object of the website being scraped.
    :return: (list): a list of a discount prices "as a strings" of all the products.
    """
    productsDiscount = []
    info = soup_object.find_all("p", "featured-collection__product-price js-product-price")
    for discount in info:
        # Grabbing the discount if found
        try:
            # print("The discount", price.find("span", "discounted").text)
            productsDiscount.append(discount.find("span", "discounted").text)
        except:
            # print("No discount for this product.")
            productsDiscount.append("N/A")
    return productsDiscount


def get_color(soup_object):
    """
    This function returns the color of the products from the soup object
    of a website.
    :param soup_object: the soup object of the website being scraped.
    :return: (list): a list of the colors "as a strings" of all the products.
    """
    productsColor = []
    info = soup_object.find_all("div", "selector-wrapper js product__option-selector quick-add-colors")
    for find in info:
        temp = ""
        for color in find.find_all("input", "swatch-radio js-quick-add-color"):
            temp += color.get("value") + " || "
        productsColor.append(temp)
    return productsColor


def get_img(soup_object):
    """
    This function returns the image link of the products from the soup object
    of a website.
    :param soup_object: the soup object of the website being scraped.
    :return: (list): a list of all the image links "as strings" of all the products.
    """
    productsImg = []
    info = soup_object.find_all("img", "featured_collection__image")
    for img in info:
        productsImg.append("https:" + img["src"])
    return productsImg


def get_all(num_of_pages, gender_url, gender):
    """
    The function will scrape the Bluenotes website using 6 functions:
        1) get_name
        2) get_link
        3) get_price
        4) get_discount
        5) get_color
        6) get_img
    :param num_of_pages: an integer : number of pages in the shop all category in the website.
    :param base_url: a (string): the base url of blue notes website which is : "https://blnts.com/".
    :param gender_url: a (string) : the url of the shop all page.
    :param gender: a (string) : the target gender of the products.
    :return: returns a list of dictionaries, every dictionary is for one product.
    """
    all_products = []

    for page in range(1, num_of_pages + 1):
        # temporary containers for every single web page
        all_names = []
        all_links = []
        all_prices = []
        all_discounts = []
        all_colors = []
        all_images = []
        # modifying the url to be able to loop through all number of pages
        url = gender_url[:len(gender_url) - 1]
        url = url + str(page)
        browser = start_chrome(url, headless=True)
        time.sleep(1.0)
        # getting the page source
        html = browser.page_source
        # creating the soup object
        soup = BeautifulSoup(html, "lxml")
        kill_browser()
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
            products_dict["Gender"] = gender
            products_dict["Price"] = all_prices[item]
            products_dict["Sale Price"] = all_discounts[item]
            products_dict["Colors"] = all_colors[item]
            products_dict["Item link"] = all_links[item]
            products_dict["Image link"] = all_images[item]
            all_products.append(products_dict)
    return all_products


def organize_products(products, gender):
    """
    This function will take the output of get_all() and organize
    the products into five main categories
    (top, bottom. overall, footwear and accessory).
    :param products: (list of dictionaries) The list of all products.
    :param gender: (String) The target gender for the products.
    :return: five lists of dictionaries of the products.
    """
    top_category = []
    bottoms_category = []
    overall_category = []
    footwear_category = []
    accessory_category = []

    if gender == "men":
        tops = ["Hoodie", "Tee", "Trunk",
                "Sweater", "Jacket", "Flannel",
                "Tank"
                ]
        bottoms = ["Pant", "Jogger", "Short"]
        overall = ["Onesie"]
        footwear = ["Sock"]
        accessories = ["Beanie", "Belt", "Fragrance"]

    elif gender == "women":
        tops = ["Hoodie", "Sweatshirt", "Tee",
                "Sweater", "Top", "Cardigan",
                "Sleeve"
                ]
        bottoms = ["Jogger", "Jegging", "Legging"]
        overall = ["Onesie"]
        footwear = ["Socks", "Slippers"]
        accessories = ["Mask", "Belt"]

    for product in products:
        for item in tops:
            if item in product["Name"]:
                product["Sub category"] = item
                product["Store"] = "Bluenotes"
                top_category.append(product)
        for item in bottoms:
            if item in product["Name"]:
                product["Sub category"] = item
                product["Store"] = "Bluenotes"
                bottoms_category.append(product)
        for item in overall:
            if item in product["Name"]:
                product["Sub category"] = item
                product["Store"] = "Bluenotes"
                overall_category.append(product)
        for item in footwear:
            if item in product["Name"]:
                product["Sub category"] = item
                product["Store"] = "Bluenotes"
                footwear_category.append(product)
        for item in accessories:
            if item in product["Name"]:
                product["Sub category"] = item
                product["Store"] = "Bluenotes"
                accessory_category.append(product)
    return top_category, bottoms_category, overall_category, footwear_category, accessory_category


def output_csv(data, category, gender):
    """
    This function takes a list of dictionaries of products
    and write a csv file form them.
    :param data: (List of dictionary) the list of products
    :param category: (String) the name of the category
    :param gender: (String) the type of the gender
    :return: csv file
    """
    keys = data[0].keys()
    with open(f"Bluenotes_{category}_{gender}.csv", "w", newline="") as csv_file:
        dict_writer = csv.DictWriter(csv_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

def main():
    start_time = time.time()

    # getting men products:
    data_men = get_all(6,"https://blnts.com/collections/bn_mens_shop-all-mens?Color"
                         "=&Size=&Waist=&Length=&tag=&price=&vendor=&sorting=&page=1",
                         "Men")
    # Organize the products into the five main categories
    categories_men = organize_products(data_men, "men")
    output_csv(categories_men[0], "tops", "men")
    output_csv(categories_men[1], "bottoms", "men")
    output_csv(categories_men[2], "overall", "men")
    output_csv(categories_men[3], "footwear", "men")
    output_csv(categories_men[4], "accessories", "men")

    # getting women products:
    data_women = get_all(9,
                         "https://blnts.com/collections/bn_womens_shop-all-womens?Color=&Size=&Waist=&Length=&tag=&price=&vendor=&sorting=&page=1",
                         "Women")
    # Organize the products into the five main categories
    categories_women = organize_products(data_women, "women")
    output_csv(categories_women[0], "tops", "women")
    output_csv(categories_women[1], "bottoms", "women")
    output_csv(categories_women[2], "overall", "women")
    output_csv(categories_women[3], "footwear", "women")
    output_csv(categories_women[4], "accessories", "women")

    taken = round(time.time() - start_time)
    minutes = taken // 60
    seconds = taken % 60
    print("Scraping finished in", str(minutes) + " minutes and " + str(seconds) + " seconds" ".")


if __name__ == '__main__':
    main()
