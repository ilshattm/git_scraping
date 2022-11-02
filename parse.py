import requests
import xmltodict
from bs4 import BeautifulSoup
URL = "https://www.kivano.kg/noutbuki?brands=acer-apple"
URL1 ="https://www.nbkr.kg/XML/daily.xml"
HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "accept": "*/*",

}
LINK = "https://www.kivano.kg/"

response = requests.get('https://www.nbkr.kg/XML/daily.xml')
dict_data = xmltodict.parse(response.content)

def get_usd_currency():
    curreny = dict_data['CurrencyRates']['Currency'][1]['Value']
    curreny = curreny.replace(",",".")
    curreny = float(curreny)
    return curreny
usd = get_usd_currency()

#print(usd)
def get_html(url, headers):
    response = requests.get(url, headers=headers)
    return response

def get_content_from_html(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    items = soup.find_all("div", class_="item product_listbox oh")
    laptops = []

    for item in items:
        laptops.append(
            {
                "title": item.find("div", class_="listbox_title oh").get_text().replace("\n",""),
                "description": item.find("div", class_="product_text pull-left").get_text().replace("\n", ""),
                "price": item.find("div", class_="listbox_price text-center").get_text().replace("\n", ""),
                "image": LINK + item.find("img").get("src")
            }
        )
    print(laptops)
    for item in range(0, len(laptops)):
        som = laptops[item]["price"]
        som = som.split()
        usd_exch = float(som[0]) * usd
        usd_exch = str(usd_exch)
        laptops[item]["price"] = usd_exch + ' $'

    print(laptops)


def get_result_parse():
    html = get_html(URL, HEADERS)
    if  html.status_code == 200:
        get_content_from_html(html.text)
        #print(html.text)
get_result_parse()

