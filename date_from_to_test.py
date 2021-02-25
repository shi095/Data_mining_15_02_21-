from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin
import requests
import bs4
import pymongo

url = "https://magnit.ru/promo/"
file_path = Path(__file__).parent.joinpath('magnit.html')
response = requests.get(url)
soup = bs4.BeautifulSoup(response.text,'lxml')
date = soup.find('div', attrs={"class":"card-sale__date"}).contents[1].text
date_new = date.strip("с ")
print(date_new)


month_dict = {
    "января": 'January, 2021',
    "февраля":'February, 2021',
    "марта": 'March, 2021',
    "апреля": 'April, 2021',
    "майя": 'May, 2021',
    "мая": 'May, 2021',
    "июня": 'June, 2021',
    "июля": 'July, 2021',
    "августа": 'August, 2021',
    "сентября": 'September, 2021',
    "октября": 'October, 2021',
    "ноября": 'November, 2021',
    "декабря": 'January, 2021',
}

for key in month_dict.keys():
    date_new = date_new.replace(key, str(month_dict[key]))

print(date_new)

d = datetime.strptime(date_new, '%d %B, %Y')
print(d.strftime('%Y-%m-%d'))