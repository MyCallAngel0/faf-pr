from bs4 import BeautifulSoup
import requests, json

# Task 2
url = 'https://darwin.md/laptopuri'

response = requests.get(url)
# print(response)

# Task 3
soup = BeautifulSoup(response.content, 'html.parser')
products = soup.find_all('a', attrs={'data-ga4': True}, title=True)

product_list = []

for product in products:

    data_ga4 = json.loads(product['data-ga4'])

    name = product['title']

    ecommerce = data_ga4.get('ecommerce', {})
    price = ecommerce.get('value')
    currency = ecommerce.get('currency')

    product_list.append({
        'name': name,
        'price': str(price) + ' ' + currency
    })


id: int = 1
with open('products-task-three.txt', 'w', encoding='utf-8') as file:
    for product in product_list:
        file.write(f"Id: {id}\n")
        file.write(f"Name: {product['name']}\n")
        file.write(f"Price: ${product['price']}\n")
        file.write("\n")
        id += 1


