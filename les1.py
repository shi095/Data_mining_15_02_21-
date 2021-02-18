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

if __name__ == '__main__':                                 #обезопасить наш код при импорте
    url = 'https://5ka.ru/api/v2/special_offers/'
    save_path = Path(__file__).parent.joinpath('products') #где мы сохраняем наши документы
    if not save_path.exists():                             #прописываем правило если такая папка существует нужно создать
        save_path.mkdir()                                  #makedir создать директорию

    parser = Parse5ka(url, save_path)
    parser.run()