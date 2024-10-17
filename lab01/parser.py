from bs4 import BeautifulSoup
import requests, json, functools

# Task 2
url = 'https://darwin.md/laptopuri'

response = requests.get(url)
# print(response.content)

# Task 3
soup = BeautifulSoup(response.content, 'html.parser')
products = soup.find_all('a', attrs={'data-ga4': True}, title=True)

product_list = []

for product in products:

    link = product['href']

    data_ga4 = json.loads(product['data-ga4'])

    name = product['title']

    ecommerce = data_ga4.get('ecommerce', {})
    price = ecommerce.get('value')
    currency = ecommerce.get('currency')

    product_list.append({
        'name': name,
        'price': price,
        'currency': currency,
        'link': link
    })


id: int = 1
with open('files/products-task-three.txt', 'w', encoding='utf-8') as file:
    for product in product_list:
        file.write(f"Id: {id}\n")
        file.write(f"Name: {product['name']}\n")
        file.write(f"Price: {product['price']}\n")
        file.write(f"Currency: {product['currency']}\n")
        file.write(f"Link: {product['link']}\n")
        file.write("\n")
        id += 1

# Task 4
product_list = []

for product in products:
    link = product['href']

    data_ga4 = json.loads(product['data-ga4'])

    name = product['title']

    ecommerce = data_ga4.get('ecommerce', {})
    price = ecommerce.get('value')
    currency = ecommerce.get('currency')

    items = ecommerce.get('items', [])
    brand = items[0].get('item_brand')

    product_list.append({
        'name': name,
        'price': price,
        'currency': currency,
        'brand': brand,
        'link': link
    })


id = 1
with open('files/products-task-four.txt', 'w', encoding='utf-8') as file:
    for product in product_list:
        file.write(f"Id: {id}\n")
        file.write(f"Name: {product['name']}\n")
        file.write(f"Brand: {product['brand']}\n")
        file.write(f"Price: {product['price']}\n")
        file.write(f"Currency: {product['currency']}\n")
        file.write(f"Link: {product['link']}\n")
        file.write("\n")
        id += 1

# Task 5
id = 1
with open('files/products-task-five.txt', 'w', encoding='utf-8') as file:
    for product in product_list:
        if isinstance(product['brand'], str) and isinstance(product['price'], int):
            file.write(f"Id: {id}\n")
            file.write(f"Name: {product['name']}\n")
            file.write(f"Brand: {product['brand']}\n")
            file.write(f"Price: {product['price']}\n")
            file.write(f"Currency: {product['currency']}\n")
            file.write(f"Link: {product['link']}\n")
            file.write("\n")
            id += 1


# Task 6
def filt(variable):
    min_price = 500
    max_price = 750
    price = variable['price']
    if min_price < price < max_price:
        return True
    else:
        return False


def mop(variable):
    EUR = 19.32
    variable['price'] = round(variable['price'] / EUR, 2)
    variable['currency'] = 'EUR'


mapped_list = list(map(mop, product_list))
filtered_list = list(filter(filt, product_list))

id = 1
with open('files/products-task-six.txt', 'w', encoding='utf-8') as file:
    for product in filtered_list:
        file.write(f"Id: {id}\n")
        file.write(f"Name: {product['name']}\n")
        file.write(f"Brand: {product['brand']}\n")
        file.write(f"Price: {product['price']}\n")
        file.write(f"Currency: {product['currency']}\n")
        file.write(f"Link: {product['link']}\n")
        file.write("\n")
        id += 1

    som = functools.reduce(lambda a, b: a + b['price'], filtered_list, 0.0)
    file.write(f"Sum of prices: {som} EUR")

