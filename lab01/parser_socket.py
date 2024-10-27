import socket, ssl, json, re
from bs4 import BeautifulSoup

# Task 7
host = 'darwin.md'
port = 443

context = ssl.create_default_context()
sock = socket.create_connection((host, port))
ssl_sock = context.wrap_socket(sock, server_hostname=host)

request = f"GET /laptopuri HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

# Trying not to DDOS or something
use_tcp = False

if use_tcp:
    ssl_sock.sendall(request.encode())

    response = b''

    while True:
        data = ssl_sock.recv(4096)
        if not data:
            break
        response += data

    ssl_sock.close()

    response = response.decode()
    headers, body = response.split('\r\n\r\n', 1)

    soup = BeautifulSoup(body, 'html.parser')
    products = soup.find_all('a', attrs={'data-ga4': True})

    product_list = []

    for product in products:

        link = product['href']

        data_ga4 = json.loads(product['data-ga4'])

        ecommerce = data_ga4.get('ecommerce', {})
        price = ecommerce.get('value')
        currency = ecommerce.get('currency')

        items = ecommerce.get('items', [])
        name = items[0].get('item_name')

        product_list.append({
            'name': name,
            'price': price,
            'currency': currency,
            'link': link
        })


# Task 8
def json_serialize(prod_list) -> str:
    serialized_list = "A:["
    for d in prod_list:
        serialized_list += "D:"
        for i, (key, value) in enumerate(d.items()):
            if isinstance(value, str):
                serialized_list += f"k:str({key}):v:str({value})"
            elif isinstance(value, int):
                serialized_list += f"k:str({key}):v:int({value})"
            elif isinstance(value, float):
                serialized_list += f"k:str({key}):v:float({value})"
            if i < len(d) - 1:
                serialized_list += ", "
        serialized_list += "; "
    serialized_list = serialized_list.rstrip("; ") + "]"
    return serialized_list


def xml_serialize(xml_string):
    result = []

    laptops = re.findall(r'<laptop>(.*?)</laptop>', xml_string, re.DOTALL)

    for laptop in laptops:
        item = {}

        pairs = re.findall(r'<(.*?)>(.*?)</\1>', laptop, re.DOTALL)

        for pair in pairs:
            key, value = pair
            if key == 'price':
                item[key] = float(value)
            else:
                item[key] = value

        result.append(item)
    return json_serialize(result)


# Using locally saved parsed data to not to DDOS or something
with open('data.json', 'r') as file:
    product_list = json.load(file)

with open('files/xml.txt', 'r') as file:
    xml_string = file.read()

with open('files/serialized_json.txt', 'w', encoding='utf-8') as file:
    file.write(json_serialize(product_list))

with open('files/serialized_xml.txt', 'w', encoding='utf-8') as file:
    file.write(xml_serialize(xml_string))


# Task 9
def custom_serialization(data):
    result = ""
    if isinstance(data, list):
        result += "A:["
        for item in data:
            result += custom_serialization(item)
        result = result.rstrip() + "]"
    elif isinstance(data, dict):
        result += "D:"
        for i, (key, value) in enumerate(data.items()):
            result += f"k:str({key}):v:" + custom_serialization(value)
            if i < len(data) - 1:
                result += ", "
        result += "; "
    elif isinstance(data, int):
        result += f"int({data})"
    elif isinstance(data, float):
        result += f"float({data})"
    elif isinstance(data, str):
        result += f"str({data})"

    return result


def custom_deserialization(data):
    idx = 0
    def parse_value():
        nonlocal idx
        if data.startswith("A:[", idx):
            idx += 3
            result = []
            while data[idx] != ']':
                result.append(parse_value())
                if data[idx] == ',':
                    idx += 1
            idx += 1
            return result

        elif data.startswith("D:", idx):
            idx += 2
            result = {}
            while data[idx] != ';':
                if data.startswith("k:str(", idx):
                    idx += 6
                    key_end = data.index("):v:", idx)
                    key = data[idx:key_end]
                    idx = key_end + 4
                    result[key] = parse_value()
                    if data[idx] == ',':
                        idx += 2
            idx += 1
            return result

        elif data.startswith("str(", idx) or data.startswith("int(", idx) or data.startswith("float(", idx):
            idx += 6 if data.startswith("float(", idx) else 4
            end_idx = data.index(")", idx)
            value = data[idx:end_idx]
            idx = end_idx + 1
            if value.isdigit():
                return int(value)
            try:
                return float(value)
            except ValueError:
                return value

    return parse_value()


with open('files/serialized_json.txt', 'r', encoding='utf-8') as file:
    serialized_json = file.readline()

with open('files/serialized_xml.txt', 'r', encoding='utf-8') as file:
    serialized_xml = file.readline()

serializer1 = [
    {
        "key1": [2.5, 20, 18],
        "key2": "hello"
    }
]

serializer2 = "Howdy"

with open("files/custom_serialization.txt", 'w', encoding='utf-8') as file:
    file.write(custom_serialization(serializer1))

with open("files/custom_serialization.txt", 'r', encoding='utf-8') as file:
    serialized_str = file.readline()

with open("files/custom_deserialization.txt", 'w', encoding='utf-8') as file:
    file.write(str(custom_deserialization(serialized_str)))
