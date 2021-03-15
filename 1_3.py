#a_1 = response.css('script').extract()
#b_1 = response.css('script')[14].getall()
@staticmethod

def get_author(response):
    elem = "window.transitState = decodeURIComponent"
    for script in response.css("script"):
        try:
            if elem in script.css("::text").extract_first():
                re_pattern = re.compile(r"youlaId%22%2C%22([a-zA-Z|\d]+)%22%2C%22avatar")
                result = re.findall(re_pattern, script.css("::text").extract_first())
                return resp.urljoin(f"/user/{result[0]}") if result else None
        except TypeError:
            pass


