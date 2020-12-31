import requests
from bs4 import BeautifulSoup
from helium import *
import re
#import time
import os


def get_men_clothing():
    """
    Assemble a database of all men's products by calling get_info() on each product link.
    :return: a dictionary with keys being all men's category, and value being a list of dictionaries
    """
    men_clothing = {"shell-jackets" : None,
                    "insulated-jackets" : None,
                    "pants" : None,
                    "fleece" : None,
                    "base-layer" : None,
                    "shirts-and-tops" : None,
                    "shorts" : None}
    categories = ["shell-jackets", "insulated-jackets", "pants", "fleece", "base-layer", "shirts-and-tops", "shorts"]
    for i in range(len(categories)):
        c = categories[i]
        men_clothing[c] = get_men_link(c)
        for i in range(len(men_clothing[c])):
            men_clothing[c][i] = get_info(men_clothing[c][i])
            men_clothing[c][i]["Gender"] = "Men"
    men_clothing["men_shell_jackets"] = men_clothing.pop("shell-jackets")
    men_clothing["men_insulated_jackets"] = men_clothing.pop("insulated-jackets")
    men_clothing["men_pants"] = men_clothing.pop("pants")
    men_clothing["men_fleece"] = men_clothing.pop("fleece")
    men_clothing["men_base_layer"] = men_clothing.pop("base-layer")
    men_clothing["men_shirts_and_tops"] = men_clothing.pop("shirts-and-tops")
    men_clothing["men_shorts"] = men_clothing.pop("shorts")
    return men_clothing


def get_women_clothing():
    """
    Assemble a database of all women's products by calling get_info() on each product link
    :return: a dictionary with keys being all women's category, and value being a list of dictionaries
    """
    women_clothing = {"shell-jackets": None,
                    "insulated-jackets": None,
                    "pants": None,
                    "fleece": None,
                    "base-layer": None,
                    "shirts-and-tops": None,
                    "dresses-and-skirts" : None,
                    "shorts": None}
    categories = ["shell-jackets", "insulated-jackets", "pants", "fleece", "base-layer", "shirts-and-tops",
                  "dresses-and-skirts", "shorts"]
    for i in range(len(categories)):
        c = categories[i]
        women_clothing[c] = get_women_link(c)
        for i in range(len(women_clothing[c])):
            women_clothing[c][i] = get_info(women_clothing[c][i])
            women_clothing[c][i]["Gender"] = "Women"
    women_clothing["women_shell_jackets"] = women_clothing.pop("shell-jackets")
    women_clothing["women_insulated_jackets"] = women_clothing.pop("insulated-jackets")
    women_clothing["women_pants"] = women_clothing.pop("pants")
    women_clothing["women_fleece"] = women_clothing.pop("fleece")
    women_clothing["women_base_layer"] = women_clothing.pop("base-layer")
    women_clothing["women_shirts_and_tops"] = women_clothing.pop("shirts-and-tops")
    women_clothing["women_dresses_and_skirts"] = women_clothing.pop("dresses-and-skirts")
    women_clothing["women_shorts"] = women_clothing.pop("shorts")
    return women_clothing


def make_product_list_from_soup(link):
    browser = start_chrome(link, headless=True)
    html = browser.page_source
    soup = BeautifulSoup(html, "lxml")
    product_list = soup.find_all("div", class_="product-tile is-filtered")
    return product_list


def get_men_link(category):
    """
    Create a beautiful soup object, from there gather all the unique product links and return a list of links.
    :param: category: a string that is the category to be searched
    :return: a list of links
    """
    assert category in ["shell-jackets", "insulated-jackets", "pants", "fleece", "base-layer", "shirts-and-tops", "shorts"]
    baseurl = "https://arcteryx.com"
    links = {}
    link = f"https://arcteryx.com/ca/en/c/mens/{category}/"
    product_list = make_product_list_from_soup(link)
    for item in product_list:
        for href in item.find_all("a", href=True):
            link = baseurl + href["href"]
            #to get unique links, put links into a dict
            links[link] = None
    unique_links = []
    for i in links:
        unique_links.append(i)
    return unique_links


def get_women_link(category):
    """
    Create a beautiful soup object, from there gather all the unique product links and return a list of links.
    :param category: a string that is the category to be searched
    :return: a list of lists of links
    """
    assert category in ["shell-jackets", "insulated-jackets", "pants", "fleece", "base-layer", "shirts-and-tops",
                        "dresses-and-skirts", "shorts"]
    baseurl = "https://arcteryx.com"
    links = {}
    link = f"https://arcteryx.com/ca/en/c/womens/{category}/"
    product_list = make_product_list_from_soup(link)
    for item in product_list:
        for href in item.find_all("a", href=True):
            link = baseurl + href["href"]
            # to get unique links, put links into a dict
            links[link] = None
    unique_links = []
    for i in links:
        unique_links.append(i)
    return unique_links


def get_info(link):
    """
    Takes a specific product link and return a dictionary with the name, price, colors, image link, sale.
    :param link: a string that is the link to the product
    :return: a python dictionary
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.content, "lxml")
    name = get_name(soup)
    price = get_price(soup)
    image_link = get_image(soup)
    colors = get_color(soup)
    info = {
        "Name" : name,
        "Price" : price,
        "Colors" : [color for color in colors],
        "Link": link,
        "Sale" : "N/A",
        "Image link" : re.findall(r'(https?://\S+)', str(image_link))[0]
    }
    return info


def get_name(soup):
    return soup.find("div", "product-name").text.lstrip().rstrip()


def get_price(soup):
    return soup.find("div", "product-price").text.lstrip().rstrip()


def get_image(soup):
    return soup.find("img", src=True)


def get_color(soup):
    colors = soup.find_all("span", style=True)
    for i in range(len(colors)):
        colors[i] = colors[i].text
    return colors


def get_clothing():
    """
    Get all men and women's clothing in one data structure (dictionary)
    Calls get_men_clothing() and get_women_clothing()
    :return: a dict with category as key, and each product info as another dict
    """
    all_items = {}
    men = get_men_clothing()
    women = get_women_clothing()
    all_items.update(men)
    all_items.update(women)
    print(all_items)
    return all_items


def gender_string_cut(string):
    """
    This function deletes the gender in the category names, along with the underscore
    ex: men_shell_jacket -> shell_jacket
    :param string:a string with gender as the first word
    :return:a string, the category name without the gender
    """
    if string[0] == "m":
        return string[4: len(string)]
    else:
        return string[6: len(string)]


def make_csv_files():
    """
    create one csv file for each category in the database
    :param all_info: dict(key = categories, value = list(dic(key = title, value = data)))
    :return: nothing, 15 cvs files are created
    """
    # all_info_dict = t
    all_info_dict = get_clothing()
    keys = ["Name", "Gender", "Price", "Sale Price", "Colors", "Item link", "Image link", "Sub category", "Brand"]
    for each in all_info_dict.items():
        category_string = each[0]
        file_name = "Arc'teryx_" + category_string + ".csv"
        f = open(file_name, "w")
        #write the first rows
        for key in keys:
            f.write(key + ", ")
        f.write("\n")
        #for each dict in list
        for item in each[1]:
            name = item["Name"]
            gender = item["Gender"]
            price = item["Price"]
            sale_price = item["Sale"]
            colors = item["Colors"]
            sub_category = gender_string_cut(category_string)
            brand = "Arc'teryx"
            for i in colors:
                if len(i) < 1:
                    colors.remove(i)
            link = item["Link"]
            img_link = item["Image link"][:-1]
            #write each sub cat
            f.write(name + ", ")
            f.write(gender + ", ")
            f.write("$" + price + ", ")
            f.write("$" + sale_price + ", ")
            color_string = ""
            for color in colors:
                color_string += color + " || "
            f.write(color_string + ", ")
            f.write(link + ", ")
            f.write(img_link + ", ")
            f.write(sub_category + ", ")
            f.write(brand)
            f.write("\n")
        f.close()



def organize_files():
    """
    Open each file, depending on the category, append each line to new file. Then delete file
    :return: nothing, 5 new files are created, 15 old files are deleted.
    """
    file_names = ["men_shell_jackets.csv",
                  "men_insulated_jackets.csv",
                  "men_pants.csv",
                  "men_fleece.csv",
                  "men_base_layer.csv",
                  "men_shirts_and_tops.csv",
                  "men_shorts.csv",
                  "women_dresses_and_skirts.csv",
                  "women_shell_jackets.csv",
                  "women_insulated_jackets.csv",
                  "women_pants.csv",
                  "women_fleece.csv",
                  "women_base_layer.csv",
                  "women_shirts_and_tops.csv",
                  "women_shorts.csv"]
    header = "Name, Gender, Price, Sale Price, Colors, Item link, Image link, Sub category, Brand"
    tops_men = open("Arc'teryx_tops_men.csv", "w")
    bottoms_men = open("Arc'teryx_bottoms_men.csv", "w")
    tops_women = open("Arc'teryx_tops_women.csv", "w")
    bottoms_women = open("Arc'teryx_bottoms_women.csv", "w")
    overall_women = open("Arc'teryx_overall_women.csv", "w")
    tops_men.write(header + "\n")
    bottoms_men.write(header + "\n")
    tops_women.write(header + "\n")
    bottoms_women.write(header + "\n")
    overall_women.write(header + "\n")
    for i in range(15):
        file_name = "Arc'teryx_" + file_names[i]
        f = open(file_name, "r")
        f.readline()
        # women top
        if "women_shell_jackets" in file_name or "women_insulated_jackets" in file_name or "women_fleece" in file_name or "women_base_layer" in file_name or "women_shirts_and_tops" in file_name:
            for line in f:
                tops_women.write(line)
        # women bottom
        elif "women_shorts" in file_name or "women_pants" in file_name:
            for line in f:
                bottoms_women.write(line)
        #men tops
        elif "men_shell_jackets" in file_name or "men_insulated_jackets" in file_name or "men_fleece" in file_name or "men_base_layer" in file_name or "men_shirts_and_tops" in file_name:
            for line in f:
                tops_men.write(line)
        #men bottom
        elif "men_shorts" in file_name or "men_pants" in file_name:
            for line in f:
                bottoms_men.write(line)
        #women overall
        elif "women_dresses_and_skirts" in file_name:
            for line in f:
                overall_women.write(line)
        f.close()
        os.remove(file_name)
    tops_men.close()
    bottoms_men.close()
    tops_women.close()
    bottoms_women.close()
    overall_women.close()


def arcteryx_scrape():
    """
    Run the scraper: from request, make beautifulsoup, extract product info into csv files, output files.
    :return: nothing
    """
    make_csv_files()
    organize_files()


def main():
    arcteryx_scrape()
#start_time = time.time()

# taken = round(time.time() - start_time)
# minutes = taken // 60
# seconds = taken % 60
# print("Scraping finished in", str(minutes) + " minutes and " + str(seconds) + " seconds" ".")

if __name__ == "__main__":
    # start_time = time.time()
    main()
    # taken = round(time.time() - start_time)
    # minutes = taken // 60
    # seconds = taken % 60
    # print("Scraping finished in", str(minutes) + " minutes and " + str(seconds) + " seconds" ".")
