from urllib import response
from scrapy.loader import ItemLoader
from scrapy import Selector
from .items import GbAutoYoulaItem
from itemloaders.processors import TakeFirst, MapCompose
import re
import base64



def get_characteristics(item):
    selector = Selector(text=item)
    data = {
        'name': selector.xpath('//div[contains(@class, "AdvertSpecs_label")]/text()').extract_first(),
        'value': selector.xpath('//div[contains(@class, "AdvertSpecs_data")]//text()').extract_first(),
    }
    return data

def get_author(item):
    try:
        selector = Selector(text=item)
        author = selector.xpath('//script[contains(text(),"youlaId")]/text()').extract_first()
        pattern = re.compile(r'youlaId%22%2C%22([a-zA-Z|\d]+)%22%2C%22avatar')
        result = re.findall(pattern, author)
        return f"https://youla.ru/user/{result[0]}" if result else None
    except TypeError:
        pass

def get_phone(item):
    try:
        selector = Selector(text=item)
        phone = selector.xpath('//script[contains(text(),"phone")]/text()').extract_first()
        pattern = re.compile(r'phone%22%2C%22([a-zA-Z|\d]+)%3D%3D%22%2C%22time')
        result = re.findall(pattern, phone)
        correct_code = f"{result[0]}=="
        decoded = base64.b64decode(correct_code)
        decoded_phone = base64.b64decode(decoded)
        result_2 = bytes.decode(decoded_phone)
        return result_2 if result else None
    except TypeError:
        pass



class AutoyoulaLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()
    title_out = TakeFirst()
    characteristics_in = MapCompose(get_characteristics)
    description_out = TakeFirst()
    author_in = MapCompose(get_author)
    phone_in = MapCompose(get_phone)


