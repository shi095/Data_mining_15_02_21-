import scrapy


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
        'title': lambda response: response.css(".AdvertCard_advertTitle__1S1Ak::text").extract_first(),
        'photos': lambda response: [item for item in response.css(".PhotoGallery_photo__36e_r img::attr(src)").extract()],
        'characteristics':lambda response:[
            {'name': item.css('.AdvertSpecs_label__2JHnS::text').get(),
             'value': item.css('.AdvertSpecs_data__xK2Qx::text').get()
                      or item.css('.AdvertSpecs_data__xK2Qx a::text').get()
             }
        for item in response.css('.AdvertCard_specs__2FEHc .AdvertSpecs_row__ljPcX')
        ],
        'description': lambda response: response.css('.AdvertCard_descriptionInner__KnuRi::text').extract(),
        'author_url':"",
        'phone':""


    }
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

# Обработан урок 4. 09.03.21 будет дополнено выполненным домашним заданием
    def car_parse(self,response):
        print(1)
 #       for key, selector in self.data_question.items():
 #           try:
#                data[key] = selector(response)
#            except (ValueError, AttributeError):
#                continue
# дописать!!!!


