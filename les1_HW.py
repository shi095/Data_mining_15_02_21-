import time
import json
from pathlib import Path
import requests


class Parse5ka:
    headers = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0"}
    def __init__(self,start_url:str,save_path:Path): # вводим аннотации типов
        self.start_url = start_url
        self.save_path = save_path

    def _get_response(self, url): # шлем запросы пока не получим ответ
        while True:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response
            time.sleep(0.5)

    def run(self):
        for product in self._parse(self.start_url): # продукт конкретный
            product_path = self.save_path.joinpath(f"{product['id']}.json") # формируем путь для продукта
            self._save(product, product_path) #записываем продукт

    def _parse(self, url: str):
        while url:
            response = self._get_response(url) # пока не дождемся ответа дальше не идем
            data: dict = response.json()
            url = data['next']
            for product in data["results"]:
                yield product

    def _save(self, data: dict, file_path: Path):
        file_path.write_text(json.dumps(data, ensure_ascii=False))

class CategoriesParser(Parse5ka):

    def __init__(self, categories_url,start_url,save_path): # перенимаем параметры родителя
        self.categories_url = categories_url
        super().__init__(start_url,save_path)

    def _get_categories(self):
        response = self._get_response(self.categories_url)
        return response.json()

    def run(self):
        for category in self._get_categories():
            category["products"] = []
            params = f"?categories={category['parent_group_code']}"
            url = f"{self.start_url}{params}"

            category["products"].extend(list(self._parse(url)))

            file_name = f"{category['parent_group_code']}_{category['parent_group_name']}.json" # название категории товаров
            cat_path = self.save_path.joinpath(file_name) # формируем путь для категорий
            self._save(category, cat_path) # сохраняем папки категорий

def get_save_path(dir_name):
    save_path = Path(__file__).parent.joinpath(dir_name)
    if not save_path.exists():
        save_path.mkdir()
    return save_path

if __name__ == "__main__":
    url = "https://5ka.ru/api/v2/special_offers/"
    cat_url = "https://5ka.ru/api/v2/categories/"
    save_path_categories = get_save_path("categories")
    cat_parser = CategoriesParser(cat_url, url, save_path_categories)
    cat_parser.run()


# Разобрано и проанализировано ваше решение. Немного скорректировано.
