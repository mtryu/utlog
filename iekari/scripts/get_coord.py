import requests
from xml.etree import ElementTree

def get_coord(addr):
    r = requests.get('https://www.geocoding.jp/api/',params={'q':addr})

    root = ElementTree.fromstring(r.content)
    coord = root.find('coordinate')

    return float(coord.find('lat').text), float(coord.find('lng').text)