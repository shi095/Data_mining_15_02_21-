from pathlib import Path
from urllib.parse import urljoin
import requests
import bs4
import pymongo
from datetime import datetime


class MagnitParse:
    def __init__(self, start_url, db_client):
        self.start_url = start_url
        self.db = db_client["gb_data_mining_15_02_2021_HW"]
        self.collection = self.db["magnit_products"]

    def _get_response(self, url):
        # TODO: написать обработку ошибки
        return requests.get(url)

    def _get_soup(self, url):
        response = self._get_response(url)
        return bs4.BeautifulSoup(response.text, "lxml")

    def run(self):
        soup = self._get_soup(self.start_url)
        catalog = soup.find("div", attrs={"class": "сatalogue__main"})
        price = soup.find("div", attrs={"class": "сatalogue__main"})
        for prod_a in catalog.find_all("a", recursive=False):
            product_data = self._parse(prod_a)
            self._save(product_data)

    def get_template(self):
        return {
            "url": lambda a: urljoin(self.start_url, a.attrs.get("href", "")),
            "promo_name": lambda a: a.find("div", attrs={"class": "card-sale__name"}).text,
            "product_name": lambda a: a.find("div", attrs={"class": "card-sale__title"}).text,
            "old_price": lambda a: float(a.find(
                    "div", attrs={"class": "label__price label__price_old"}).text.strip("\n").replace("\n",".")
            ),
            "new_price": lambda a: float(a.find(
                    "div", attrs={"class": "label__price label__price_new"}).text.strip("\n").replace("\n",".")
            ),
            "image_url": lambda  a: urljoin(self.start_url, a.find("img").attrs.get("data-src")),
#           "date_from": "DATETIME", есть тестовый вариант заполнения данного параметра структуры в date_from_to_test
#           "date_to": "DATETIME", есть тестовый вариант заполнения данного параметра структуры в date_from_to_test
# осталось причесать красиво и сразу загружу
        }

    def _parse(self, product_a) -> dict:
        data = {}
        for key, funk in self.get_template().items():
            try:
                data[key] = funk(product_a)
            except (AttributeError, ValueError):
                pass
        return data

    def _save(self, data: dict):
        self.collection.insert_one(data)


def get_save_path(dir_name):
    dir_path = Path(__file__).parent.joinpath(dir_name)
    if not dir_path.exists():
        dir_path.mkdir()
    return dir_path


if __name__ == "__main__":
    url = "https://magnit.ru/promo/"
    save_path = get_save_path("magnit_product")
    db_client = pymongo.MongoClient("mongodb://localhost:27017")
    parser = MagnitParse(url, db_client)
    parser.run()

