import time
import requests
from bs4 import BeautifulSoup
import csv

headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Mobile Safari/537.36"
}


def get_url(string_name, vendor):
    url_vendor = "https://imprints.ru/cgi-bin/catalog.cgi?offset={curr_string}&loc=/printers/{vendor}/".format(curr_string=str(string_name), vendor=str(vendor))
    return url_vendor

def create_list_of_vendors_printers(vendor):
    print(vendor)
    all_printers = []
    all_info_printers = []
    string_name = 0
    for i in range(40):
        req = requests.get(get_url(string_name, vendor))
        src = req.text
        soup = BeautifulSoup(src, "lxml")
        all_items = soup.find_all(class_="item")
        all_printers=all_printers+all_items
        string_name = string_name + 14
    list_of_printers = redesign_names_to_links(all_printers)
    count_printers=0
    for printer in range(len(list_of_printers)):
        count_printers = count_printers+1
        print(count_printers)
        create_list_of_carts_on_printer(list_of_printers[printer], vendor)

def redesign_names_to_links(all_printers):
    for printer in range (len(all_printers)):
        all_printers[printer] = ("https://imprints.ru/"+all_printers[printer].find('a').get('href'))
    return all_printers

def create_list_of_carts_on_printer(curr_printer, vendor):
    req = requests.get(curr_printer)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    all_carts_in_page_text = soup.find(class_="same catalog")
    printer_name_f = soup.find(class_="good-top catalog")
    printer_name_s = printer_name_f.find(itemprop="name").text
    if all_carts_in_page_text is not None:
        all_carts_in_page= all_carts_in_page_text.find_all(class_="cell")
        all_carts_in_page = redesign_cart_to_links(all_carts_in_page)
        all_carts_in_page_info=[]
        for cart in range(len(all_carts_in_page)):
            all_carts_in_page_info.append(get_info_about_cart(all_carts_in_page[cart], vendor, curr_printer, printer_name_s))
    else:
        with open("C:\\Users\\1\\Desktop\\testing_py.csv", "a", newline='', encoding='cp1251') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                (
                    vendor,
                    curr_printer,
                    printer_name_s
                )
            )



def redesign_cart_to_links(all_carts_in_page):
    for cart in range(len(all_carts_in_page)):
        all_carts_in_page[cart] = ("https://imprints.ru/" + all_carts_in_page[cart].find('a').get('href'))
    return all_carts_in_page

#create_list_of_carts_on_printer(curr_printer)
def get_info_about_cart(curr_cart, vendor, curr_printer, printer_name_s):
    req = requests.get(curr_cart)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    string_curr = soup.find(class_="good-top catalog")
    if string_curr.find(class_="art") is not None:
        analog = string_curr.find(class_="art").text.replace('Код производителя:', '')
        if "аналог" in str(analog):
            is_analog = "аналог"
            analog=analog.replace("аналог ",'')
        else:
            is_analog = "оригинал"
        analog=analog.lower()
        if ("без_чипа") in str(analog):
            is_chip = "без чипа"

        else:
            is_chip = "с чипом"

        vendor=vendor
        curr_printer = curr_printer
        curr_printer_name = printer_name_s
        link=curr_cart
        full_name=string_curr.find(itemprop="name").text
        small_name=string_curr.find(itemprop="model").get('content')
        if string_curr.find(class_="prop2") is not None:
            resurs=string_curr.find(class_="prop2").find("span").text.split(" ")[0]
        else:
            resurs="0"
        price=string_curr.find(class_="price").find("span").text.replace(' ', '')
        color_supp=soup.find(class_='good')
        khars=color_supp.find(class_='khar')
        all_khars = khars.find_all(class_='item')
        color = "неизвестно"
        for i in all_khars:
            if (("Цвет отпечатка") in ((i.find('p').text))):
                color=(i.find('span').text)
                break
        with open("C:\\Users\\1\\Desktop\\testing_py.csv", "a", newline='', encoding='cp1251') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                (
                    vendor,
                    curr_printer,
                    curr_printer_name,
                    link,
                    full_name,
                    small_name,
                    is_analog,
                    is_chip,
                    resurs,
                    color,
                    price
                )
            )

    else:
        vendor = vendor
        curr_printer = curr_printer
        curr_printer_name = printer_name_s
        link=curr_cart
        full_name=string_curr.find(itemprop="name").text
        small_name=string_curr.find(itemprop="model").get('content')
        is_analog = "Неизвестно"
        is_chip = "Неизвестно"
        resurs=string_curr.find(class_="prop2").find("span").text.split(" ")[0]
        price=string_curr.find(class_="price").find("span").text.replace(' ', '')
        color_supp = soup.find(class_='good')
        khars = color_supp.find(class_='khar')
        all_khars = khars.find_all(class_='item')
        color = "неизвестно"
        for i in all_khars:
            if (("Цвет отпечатка") in ((i.find('p').text))):
                color = (i.find('span').text)
                break
        with open("C:\\Users\\1\\Desktop\\testing_py.csv", "a",newline='', encoding='cp1251') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                (
                    vendor,
                    curr_printer,
                    curr_printer_name,
                    link,
                    full_name,
                    small_name,
                    is_analog,
                    is_chip,
                    resurs,
                    color,
                    price
                )
            )


#a=create_list_of_carts_on_printer(curr_printer)
#print(a)
#a=create_list_of_vendors_printers(vendor)
#print(a)
def create_header():
    title1 ="Вендор"
    title2 ="Ссылка на принтер"
    title3 ="Название принтера"
    title4 ="Ссылка на ЗИП"
    title5 ="Полное наименование ЗИПа"
    title6 ="Сокращенное название ЗИПа"
    title7 ="Аналог или оригинал"
    title8 ="Наличие чипа"
    title9 ="Ресурс, стр"
    title11="Цвет"
    title10 ="Цена, руб"

    with open("C:\\Users\\1\\Desktop\\testing_py.csv", "w",newline='', encoding='cp1251') as file:
        writer=csv.writer(file, delimiter=';')
        writer.writerow(
            (
                title1,
                title2,
                title3,
                title4,
                title5,
                title6,
                title7,
                title8,
                title9,
                title11,
                title10
            )
        )
create_header()

vendor_list=["brother", "canon", "epson", "hp", "konica-minolta", "kyocera-mita", "lexmark", "oki", "panasonic", "ricoh", "samsung", "sharp", "xerox"]
for vendor in vendor_list:
    create_list_of_vendors_printers(vendor)



