import socket, ssl, json, re
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
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


# Task 8
def json_serialize(prod_list) -> str:
    serialized_list = "L:["
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
def deserialize_json(serialized_json):
    serialized_json = serialized_json[2:]
    entries = serialized_json.split('D:')[1:]
    result = []

    for entry in entries:
        item = {}
        pairs = re.findall(r'k:str\((.*?)\):v:(str|int|float)\((.*?)\)', entry)
        for pair in pairs:
            key = pair[0]
            value_type = pair[1]
            value = pair[2]

            if value_type == 'int':
                item[key] = int(value)
            elif value_type == 'float':
                item[key] = float(value)
            else:
                item[key] = value
        result.append(item)
    return result


def deserialize_xml(serialized_xml):
    serialized_xml = serialized_xml[2:-1].split("; ")

    output = "<Laptops>\n"

    for item_string in serialized_xml:
        output += "\t<laptop>\n"

        pairs = item_string.split(", ")
        for pair in pairs:
            key_value = pair.split(":v:")
            if len(key_value) != 2:
                continue

            key = key_value[0].split("(")[-1].split(")")[0].strip()
            value = key_value[1]

            if value.startswith("float("):
                value = value[6:-1]
            elif value.startswith("str("):
                value = value[4:-1]

            output += f"\t\t<{key}>{value}</{key}>\n"

        output += "\t</laptop>\n"
        
    output += "</Laptops>"

    return output


with open('files/serialized_json.txt', 'r', encoding='utf-8') as file:
    serialized_json = file.readline()

with open('files/serialized_xml.txt', 'r', encoding='utf-8') as file:
    serialized_xml = file.readline()


with open('files/deserialized_json.txt', 'w', encoding='utf-8') as file:
    json.dump(deserialize_json(serialized_json), file, indent=4)

with open('files/deserialized_xml.txt', 'w', encoding='utf-8') as file:
    file.write(deserialize_xml(serialized_xml))
