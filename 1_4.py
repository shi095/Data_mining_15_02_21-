import re


response = "https://auto.youla.ru/advert/used/bentley/continental_gt/prv--5d090d9767ab969d/"

def get_author_id(response):
    marker = "window.transitState = decodeURIComponent"
    for script in response.css("script"):
        try:
            if marker in script.css("::text").extract_first():
                re_pattern = re.compile(r"youlaId%22%2C%22([a-zA-Z|\d]+)%22%2C%22avatar")
                result = re.findall(re_pattern, script.css("::text").extract_first())
                return resp.urljoin(f"/user/{result[0]}") if result else None
        except TypeError:
            pass

a_1 = get_author_id(response)
print(a_1)