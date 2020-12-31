import requests
import csv
import time
from bs4 import BeautifulSoup


def get_info(url_list, gender):
    """
    Return a list of dictionaries whose keys contains products' information tags and
     value is its value in list type
    :param url_list: the list of websites' url to be scraped.
    :param gender: male or female depending on information from each url
    :return: (list): a list of dictionary where each dictionary
    contains information of each item
    """
    # initializing category list
    category_list = \
        ["hoodies.html", "jackets.html", "coats.html",
         "shirts.html", "short-sleeves.html", "shortsleeve.html", "tanks.html",
         "cardigans.html", "sweaters.html", "pants.html", "joggers.html",
         "jeans.html", "shorts.html", "sneakers.html", "socks.html",
         "sunglasses.html", "hats.html", "bags.html", "sweatshirts.html",
         "t-shirts.html", "shirts-and-blouses.html", "blouses.html",
         "jumpers.html", "skirts.html", "leggings.html", "slippers.html",
         "dresses.html", "overalls.html", "jumpsuits.html"]
    # initializing user agent to gain permission to access the website
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
        "537.24 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.24"
    }
    all_product_info = []
    # looping through the every single link from list of urls
    for url in url_list[0:len(url_list)-1]:
        # avoid getting information too fast which can lead to website's ban
        time.sleep(2.0)
        # requests and get the content from a link in the list of urls
        html = requests.get(url, headers= headers)
        html_content = BeautifulSoup(html.content, "lxml")
        # get data information of each item from the current url content
        name_list = get_name(html_content)
        price_list = get_price(html_content)
        sale_price_list = get_sale_price(html_content)
        item_link_list = get_item_link(html_content)
        image_link_list = get_image_link(html_content)
        color_list = get_color(html_content)
        subcategory_list = get_subcategory(html_content)
        # looping through information attribute of each item from the url
        # information attribute's list is equal in length
        for i in range(len(name_list)):
            # initializing empty dictionary for the item from the url
            info_dictionary = {}
            # set the key-value pair for the item in the dictionary
            info_dictionary['Name'] = name_list[i]
            info_dictionary['Gender'] = gender
            info_dictionary['Price'] = price_list[i]
            info_dictionary['Sale Price'] = sale_price_list[i]
            info_dictionary['Colors'] = color_list[i]
            info_dictionary['Item link'] = item_link_list[i]
            info_dictionary['Image link'] = image_link_list[i]
            info_dictionary['Sub category'] = subcategory_list[i]
            info_dictionary['Store'] = "H&M"
            # append the dictionary containing information of items to the list
            all_product_info.append(info_dictionary)
    # eliminating every dictionaries whose "Sub category" value is "N/A"
    final_product_info = [i for i in all_product_info if i['Sub category'] != "N/A"]
    # return the list of dictionaries,
    # each dictionary contains information of each item of the url
    return final_product_info


def get_subcategory(html_content):
    """
    Return a list of subcategories (string) of every item from the
    html content achieved from the website url
    :param html_content: the html content of the website url being scraped
    :return: (list): a list of subcategories of every item from html content
    """
    subcategory_list = []
    # initializing category list
    category_list = \
        ["hoodie", "jacket", "pants", "dress",
         "coat",  "t-shirt", "tank top", "sweatshirt",
         "cardigan", "sweater", "joggers", "chinos",
         "skirt", "jeans", "shorts", "sneakers",
         "socks", "sunglasses", "eyeglasses", "hat",
         "bag", "backpack", "blouse", "leggings",
         "jumpsuit", "overalls", "shoes", "cap",
         "shopper", "shirt"]
    name_list = []
    word_list = []
    # achieve all names of every item from the html content of the website
    item_container = html_content.find_all("h3", "item-heading")
    # append the name of each item to name_list
    for name_container in item_container:
        name = name_container.find("a", "link")
        name_string = name.text.strip()
        name_list.append(name_string.lower())
    # separate the name of each item into different words
    for word in name_list:
        splits = word.split()
        word_list.append(splits)
    reverse_word_list = []
    # reverse the order of the words in each name (sublist)
    for sublist in word_list:
        reverse_word_list.append(sublist[::-1])
    # looping through each name in the list and categorize it
    for sublist in reverse_word_list:
        for i in range(len(sublist)):
            if sublist[i] in category_list:
                subcategory_list.append(sublist[i])
                break
            if i == len(sublist) - 1:
                if sublist[i] in category_list:
                    subcategory_list.append(sublist[i])
                # if item does not belong to any subcategory, append "N/A"
                else:
                    subcategory_list.append("N/A")
    return subcategory_list


def get_price(html_content):
    """
    Returns prices (before sale) of every item
    from the html content achieved from the website url
    :param html_content: the html content of the website url being scraped
    :return: (list): a list containing prices (before sale)
    of every item from html content
    """
    price_list = []
    # achieve all prices (before sale) of every item
    # from the html content of the website
    price_container = html_content.find_all("span", "price regular")
    # append prices of every item to the list
    for price in price_container:
        price_list.append(price.text.strip())
    # return the list of prices of every item
    return price_list


def get_sale_price(html_content):
    """
     Returns sale price of every item
     from the html content achieved from the website url
     :param html_content: the html content of the website url being scraped
     :return: (list): a list containing sale prices (if applicable)
     of every item from html content
     """
    sale_price_list = []
    # achieve all sale prices of every item
    # from the html content of the website
    item_container = html_content.find_all("strong", "item-price")
    # append sale price to the list (if applicable)
    # if sale price does not exist, append string "N/A"
    for item in item_container:
        try:
            sale_item_container = item.find("span", "price sale")
            sale_price_list.append(sale_item_container.text.strip())
        except:
            sale_price_list.append("N/A")
            pass
    # return the list containing sale prices (if applicable) of every item
    return sale_price_list


def get_name(html_content):
    """
     Returns names of every item
     from the html content achieved from the website url
     :param html_content: the html content of the website url being scraped
     :return: (list): a list containing names of every item from html content
     """
    name_list = []
    # achieve all names of every item from the html content of the website
    item_container = html_content.find_all("h3", "item-heading")
    # append the name of each item to the list
    for name_container in item_container:
        name = name_container.find("a", "link")
        name_list.append(name.text.strip())
    # return the list containing names of every item
    return name_list


def get_color(html_content):
    """
     Returns color(s) of every item
     from the html content achieved from the website url
     :param html_content: the html content of the website url being scraped
     :return: (list): a list containing colors of every item from html content
     """
    color_list = []
    # achieving all colors of every item from the html content
    all_color_container = html_content.find_all("ul", "list-swatches")
    # if an item has 2 or more colors, separate it with character '||'
    # append color(s) of each item in the list
    for color_container in all_color_container:
        empty = ""
        for color in color_container.find_all("a", "swatch"):
            empty += color.get('title') + "||"
        color_list.append(empty[:len(empty)-2])
    for i in range(len(color_list)):
        if color_list[i] == "":
            color_list[i] = "N/A"
    # return the list containing color(s) of every item
    return color_list


def get_item_link(html_content):
    """
     Returns links of every item
     from the html content achieved from the website url
     :param html_content: the html content of the website url being scraped
     :return: (list): a list containing links of every item from html content
     """
    item_link_list = []
    baseurl = "https://www2.hm.com"
    # achieving all links of every item from the html content
    item_link_container = html_content.find_all("h3", "item-heading")
    # append link (with HTTPS and base url) of every item to the list
    for link_container in item_link_container:
        link = link_container.find("a", "link")
        if baseurl not in link['href']:
            full_link = baseurl + link['href']
            item_link_list.append(full_link)
        else:
            item_link_list.append(link['href'])
    # return the list containing links of every item
    return item_link_list


def get_image_link(html_content):
    """
    Returns image links of every item from the html content achieved from
    the website url
    :param html_content: the html content of the website url being scraped
    :return: (list): a list containing image links of every item from html
    content
    """
    img_link_container = []
    # achieve all images from html_content
    image_container = html_content.find_all("div", "image-container")
    for image in image_container:
        # filter image links so that image_link_container
        # only contains item images
        image_link_container = image.find_all("img", "item-image")
        # achieve item image links through 2 different ways
        # some item image links can not be achieved through 'data-altimage' class
        # append item image link of each product to the list
        for image_link in image_link_container:
            try:
                image_source_link = image_link['data-altimage']
                img_link_container.append("https:" + image_source_link)
            except:
                # use 'src' class if 'data-altimage' does not work
                image_alt_link = image_link['src']
                img_link_container.append("https:" + image_alt_link)
    # return the list containing image links of every items
    return img_link_container


def get_csv(data, category):
    """
        Generate .csv file of every items based on input data (dictionary)
        :param data: dictionary containing information of the item
        :param category: category which the item belongs to
        :return: None
    """
    keys = data[0].keys()
    # generate .csv file with format name "hm_" + category + ".csv"
    with open(f"hm_{category}.csv", "w", newline="") as csv_file:
        dict_writer = csv.DictWriter(csv_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    return None


def generate_all_csv():
    """
    Generate all .csv files for every categories
    Each categories contains items which belongs to
    :return: None
    """
    start_time = time.time()
    # initializing lists of men's categories
    men_tops = [
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
        "tops_men"]
    men_bottoms = [
        "https://www2.hm.com/en_ca/men/shop-by-product/pants/pants.html",
        "https://www2.hm.com/en_ca/men/shop-by-product/pants/joggers.html",
        "https://www2.hm.com/en_ca/men/shop-by-product/jeans.html",
        "https://www2.hm.com/en_ca/men/shop-by-product/shorts.html",
        "https://www2.hm.com/en_ca/sale/shopbyproductmen/trousers/"
        "joggers.html",
        "https://www2.hm.com/en_ca/sale/shopbyproductmen/jeans.html",
        "https://www2.hm.com/en_ca/sale/shopbyproductmen/shorts.html",
        "bottoms_men"]
    men_footwear = [
        "https://www2.hm.com/en_ca/men/shop-by-product/shoes/sneakers.html",
        "https://www2.hm.com/en_ca/sale/shopbyproductmen/shoes/sneakers.html",
        "https://www2.hm.com/en_ca/men/shop-by-product/socks.html",
        "footwear_men"]
    men_accessories = [
        "https://www2.hm.com/en_ca/men/shop-by-product/accessories/"
        "sunglasses.html",
        "https://www2.hm.com/en_ca/men/shop-by-product/accessories/hats.html",
        "https://www2.hm.com/en_ca/men/shop-by-product/accessories/bags.html",
        "https://www2.hm.com/en_ca/sale/shopbyproductmen/accessories/"
        "hats.html",
        "accessories_men"]
    men_list = [men_tops, men_bottoms, men_footwear, men_accessories]
    # achieve information of every items for each category, generate .csv file
    for sublist in men_list:
        men_data = get_info(sublist, "men")
        get_csv(men_data, sublist[-1])
    # initializing lists of women's categories
    women_tops = [
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
        "tops_womens"]
    # aaa
    women_bottoms = [
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
        'bottoms_women']
    women_footwear = [
        "https://www2.hm.com/en_ca/women/shop-by-product/shoes/sneakers.html",
        "https://www2.hm.com/en_ca/women/shop-by-product/shoes/slippers.html",
        "https://www2.hm.com/en_ca/women/shop-by-product/socks-and-tights/"
        "socks.html",
        "https://www2.hm.com/en_ca/sale/shopbyproductladies/shoes/"
        "sneakers.html",
        "footwear_women"]
    women_accessories = [
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
        "accessories_women"]
    women_overall = [
        'https://www2.hm.com/en_ca/women/shop-by-product/dresses.html',
        "https://www2.hm.com/en_ca/women/shop-by-product/jumpsuits-rompers/"
        "overalls.html",
        "https://www2.hm.com/en_ca/women/shop-by-product/jumpsuits-rompers/"
        "long-jumpsuits.html",
        "https://www2.hm.com/en_ca/sale/shopbyproductladies/dresses.html",
        "https://www2.hm.com/en_ca/sale/shopbyproductladies/jumpsuits.html",
        "overall_women"]
    women_list = [women_tops, women_overall, women_bottoms,
                  women_footwear, women_accessories]
    # achieve information of every items for each category, generate .csv file
    for sublist in women_list:
        women_data = get_info(sublist, "women")
        get_csv(women_data, sublist[-1])

    time_taken = round(time.time() - start_time)
    time_minutes = time_taken // 60
    time_seconds = time_taken % 60
    print("Scraping finished in", str(time_minutes) +
          " minutes and " + str(time_seconds) + " seconds" ".")
    print("EOF")
    return None


def main():
    generate_all_csv()


if __name__ == "__main__":
    main()