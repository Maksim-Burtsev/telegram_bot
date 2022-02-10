from config import VK_TOKEN, TOKEN
import requests
import youtube_dl
import datetime
import os
import telebot
from telebot import types
import time
from config import TEST_TOKEN

from main import VIDEOS

VIDEOS_FOR_DELETE = []

TOKEN = VK_TOKEN

VERSION = 5.131
DOMAIN = 'biobezpredel'

LINK_1 = 'https://vk.com/biobezpredel?z=photo-76771597_'
LINK_2   = '%2Falbum-76771597_00%2Frev'

def delete_videos(video_list: list):
    """Удаляет с компьютера все скаченные видео"""
    if video_list:
        for video in video_list:
            try:
                os.remove(video)
            except:
                pass

def give_phtVd_links(attach: dict):
    """Получает на вход часть json'a со вложениями и достает оттуда все ссылки на фото и видео в самом лучшем качестве."""
    res = []
    res_vid = []
    if len(attach) > 1:
        for i in range(len(attach)):
            if attach[i]['type'] == 'photo':
                res.append(LINK_1 + str(attach[i]['photo']['id']) + LINK_2  )
            if attach[i]['type'] == 'video':    
                print()
                lnk = 'vk.com/video' + \
                    str(attach[i]['video']['owner_id']) + \
                    '_' + str(attach[i]['video']['id'])
                res_vid.append(lnk)

    else:
        if attach[0]['type'] == 'photo':
            res.append(LINK_1 + str(attach[0]['photo']['id']) + LINK_2  )
        elif attach[0]['type'] == 'video':
            lnk = 'vk.com/video' + \
                str(attach[0]['video']['owner_id']) + \
                '_' + str(attach[0]['video']['id'])
            res_vid.append(lnk)

    return res, res_vid

def get_day_from_unix(time: str):
    """Получает из Unix-времени день"""

    return int(datetime.datetime.utcfromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')[8:10])


def is_post_today(day: int):
    """Проверяет, совпадает ли дата поста с текущей"""

    return (datetime.datetime.now().day >= day)


def main():
    TEXT, PHOTOS, VIDEOS = [], [], []
    responce = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                'access_token': TOKEN,
                                'v': VERSION,
                                'domain': DOMAIN,
                                'count': 5,
                            })

    data = responce.json()['response']['items']
    for i in range(1, 5):
        date = int(datetime.datetime.utcfromtimestamp(int(data[i]['date']+3*60*60)).strftime('%Y-%m-%d %H:%M:%S')[8:10]) 
        
        # if (int(time.time())-int(data[i]['date']))/60/60 <= 24:

        if is_post_today(date):
            text = data[i]['text']
            photo_links, video_links = give_phtVd_links(data[i]['attachments'])
            video_names = []
            if video_links:
                ydl_opts = {}
                for link in video_links:
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([link])
                    video_names.append(
                        f'Video by BioBeZpredel [Биохакинг _ Спорт _ Дизмораль]-{link[-19:]}.mp4')      

            TEXT.append(text)
            PHOTOS.append(photo_links)
            VIDEOS.append(video_names)
            VIDEOS_FOR_DELETE.extend(VIDEOS)
    
    return TEXT, PHOTOS, VIDEOS


bot = telebot.TeleBot(TEST_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "<kzdjisfjdl ")
    text_list, photo_list, video_list = main()
    for i in range(len(text_list)):
        bot.send_message(message.chat.id, text_list[i])
        if photo_list[i]:
                medias = []  
                for _ in photo_list[i]:
                    medias.append(types.InputMediaPhoto(_))
                try:
                    bot.send_media_group(message.chat.id, medias)    
                except:
                    with open('log.txt', 'a') as f:
                        f.write(''.join(medias))  
                    
        if video_list[i]:
            for i in video_list[i]:
                video = open(i, 'rb')
                bot.send_video(message.chat.id, video,
                                supports_streaming=True)
        # if VIDEOS_FOR_DELETE:
        #     try:
        #         delete_videos(VIDEOS_FOR_DELETE)
        #     except Exception as e:
        #         with open('log.txt', 'a') as f:
        #             f.write(e)

@bot.message_handler(commands=['24'])
def foo(message):
    bot.send_message(message.chat.id, 'Сейчас вышлю посты за последние 24 часа!')                               


bot.polling(non_stop=True)
