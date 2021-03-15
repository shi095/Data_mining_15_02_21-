import scrapy
import pymongo
import re
import base64



class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru'] # на какие домены паук будет переходить
    start_urls = ['https://auto.youla.ru/']


    _css_selectors = {
        'brands':".TransportMainFilters_brandsList__2tIkv .ColumnItemList_container__5gTrc a.blackLink",
        'pagination':"a.Paginator_button__u1e7D",
        'car':".SerpSnippet_titleWrapper__38bZM a.SerpSnippet_name__3F7Yu",
    }
    data_question = {
        'title': lambda response: response.css("div.AdvertCard_advertTitle__1S1Ak::text").extract_first(),
        'photos': lambda response: [item for item in response.css("figure.PhotoGallery_photo__36e_r img::attr(src)").extract()],
        'characteristics':lambda response:[
            {'name': item.css('.AdvertSpecs_label__2JHnS::text').get(),
             'value': item.css('.AdvertSpecs_data__xK2Qx::text').get()
                      or item.css('.AdvertSpecs_data__xK2Qx a::text').get()
             }
        for item in response.css('div.AdvertCard_specs__2FEHc .AdvertSpecs_row__ljPcX')
        ],
        'description': lambda response: response.css('.AdvertCard_descriptionInner__KnuRi::text').extract_first(),
        "author": lambda response: AutoyoulaSpider.get_author(response),
        "phone": lambda response: AutoyoulaSpider.get_phone(response),
    }

    @staticmethod
    def get_author(response):
        elem = "window.transitState = decodeURIComponent"
        for script in response.css("script"):
            try:
                if elem in script.css("::text").get():
                    pattern = re.compile(r"youlaId%22%2C%22([a-zA-Z|\d]+)%22%2C%22avatar")
                    result = re.findall(pattern, script.css("::text").get())
                    return response.urljoin(f"/user/{result[0]}") if result else None
            except TypeError:
                pass

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_client = pymongo.MongoClient()

    def _get_follow(self, response, select_str, callback, **kwargs):
        for a in response.css(select_str):
            link = a.attrib.get("href")
            yield response.follow(link, callback=callback, cb_kwargs=kwargs)

    def parse(self, response, *args, **kwargs):
        yield from self._get_follow(response,
                                    self._css_selectors["brands"],
                                    self.brand_parse,
                                    hello = "moto")

    def brand_parse(self, response, **kwargs):
        yield from self._get_follow(response,
                                    self._css_selectors["pagination"],
                                    self.brand_parse)

        yield from self._get_follow(response,
                                    self._css_selectors["car"],
                                    self.car_parse)


    def car_parse(self, response):

        collection_autoyoula= {}
        for key, selector in self.data_question.items():
            try:
                collection_autoyoula[key] = selector(response)
            except (ValueError, AttributeError):
                continue
        result = self.db_client["autoyoula_DB"][self.name].insert_one(collection_autoyoula)


