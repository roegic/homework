from selenium import webdriver
from bs4 import BeautifulSoup as BS
from random import randint
n = randint(1,2000)
URL = f"https://xkcd.com/{n}" 

# парсит сайт xkcd и выдает прямую ссылку на комикс
driver = webdriver.Chrome()
driver.get(URL)
html = driver.page_source

soup = BS(html, "html.parser")
data = soup.find_all("div", {"id": "comic"})
for d in data:
   a = d.find('img')
   name = a.get("src")
   print(name[2:])

