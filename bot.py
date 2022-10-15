import telebot
from selenium import webdriver
from bs4 import BeautifulSoup as BS
import time
from random import randint
# при отправки рандомного сообщения боту, он его переворачивает
# также бот выдает комикс с xkcd через команду /comics, и парсит ютуб канала через /get_videos


bot = telebot.TeleBot("your token")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет")


@bot.message_handler(commands=['get_videos'])
def search_videos(message):
    msg = bot.send_message(message.chat.id, "Введите ссылку на youtube канал")
    bot.register_next_step_handler(msg, search)

@bot.message_handler(commands=['comics'])
def search_channel(message):
    bot.send_message(message.chat.id, "Одну секунду...")
    URL = "https://xkcd.com/"+str(randint(1,2000))
    driver = webdriver.Chrome()
    driver.get(URL)
    html = driver.page_source

    soup = BS(html, "html.parser")
    data = soup.find_all("div", {"id": "comic"})
    for d in data:
        a = d.find('img')
        comic = a.get("src")
    bot.send_message(message.chat.id, comic[2:])



@bot.message_handler(content_types=['text'])
def text(message):
    bot.send_message(message.chat.id, message.text[::-1].lower())


def search(message):
    msg = bot.send_message(message.chat.id, "Идёт обработка запроса, подождите")
    URL = message.text +"/videos"
    driver = webdriver.Chrome()
    driver.get(URL)
    html = driver.page_source

    soup = BS(html, "html.parser")
    videos = soup.find_all("ytd-grid-video-renderer", {"class": "style-scope ytd-grid-renderer"})
    for video in videos[:10]:
        a = video.find("a", {"id": "video-title"})
        name = a.get("title")
        link = "https://www.youtube.com/" + a.get("href")
        s=f"{name}: {link}"
        bot.send_message(message.chat.id, s)

bot.polling()







