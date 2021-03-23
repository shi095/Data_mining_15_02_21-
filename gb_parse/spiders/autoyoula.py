import scrapy
import re
import base64
from ..loaders import AutoyoulaLoader


class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru'] # на какие домены паук будет переходить
    start_urls = ['https://auto.youla.ru/']


    _css_selectors = {
        'brands':".TransportMainFilters_brandsList__2tIkv .ColumnItemList_container__5gTrc a.blackLink",
        'pagination':"a.Paginator_button__u1e7D",
        'car':".SerpSnippet_titleWrapper__38bZM a.SerpSnippet_name__3F7Yu",
    }

    _xpath_selectors = {
        'brands':"//div[@data-target='transport-main-filters']"
                 "/div[""contains(@class,'TransportMainFilters_brandsList')]"
                 "//a[@data-target='brand']/@href",

    }
    _car_xpaths = {
        'title': "//div[@data-target='advert-title']/text()",
        'photos': "//figure/picture/img/@src",
        'characteristics': "//h3[contains(text(), 'Характеристики')]/.."
                           "//div[contains(@class,'AdvertSpecs_row')]",
    }

    @staticmethod
    def get_phone(response):
        elem = "window.transitState = decodeURIComponent"
        for script in response.css("script"):
            try:
                if elem in script.css("::text").get():
                    pattern = re.compile(r"phone%22%2C%22([a-zA-Z|\d]+)%3D%3D%22%2C%22time")
                    result = re.findall(pattern, script.css("::text").get())
                    correct_code = f"{result[0]}=="
                    decoded = base64.b64decode(correct_code)
                    decoded_phone = base64.b64decode(decoded)
                    result = bytes.decode(decoded_phone)
                    return result if result else None
            except TypeError:
                pass



    def _get_follow(self, response, select_str, callback, **kwargs):
        for a in response.css(select_str):
            link = a.attrib.get("href")
            yield response.follow(link, callback=callback, cb_kwargs=kwargs)

    def _get_follow_xpath(self, response, select_str, callback, **kwargs):
        for link in response.xpath(select_str):
            yield response.follow(link, callback=callback, cb_kwargs=kwargs)


    def parse(self, response, *args, **kwargs):
#        yield from self._get_follow(response,
#                                    self._css_selectors["brands"],
#                                   self.brand_parse,
#                                   hello = "moto")

        yield from self._get_follow_xpath(response,
                                    self._xpath_selectors["brands"],
                                    self.brand_parse)

    def brand_parse(self, response, **kwargs):
        yield from self._get_follow(response,
                                    self._css_selectors["pagination"],
                                    self.brand_parse)

        yield from self._get_follow(response,
                                    self._css_selectors["car"],
                                    self.car_parse)


    def car_parse(self, response):
        loader = AutoyoulaLoader(response=response)
        loader.add_value('url', '')
        loader.add_value('url', response.url)
        for key, xpath in self._car_xpaths.items():
            loader.add_xpath(key, xpath)
        yield loader.load_item()




