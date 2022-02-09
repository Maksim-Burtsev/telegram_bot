import telebot
from telebot import types
import time
import requests
from parse_and_delete_f import main, is_new_post_piblished, delete_videos
from threading import Thread
from config import TOKEN

TXT = ""
PHOTO_LIST = []
VIDEOS = []


def update_data():
    global TXT, PHOTO_LIST, VIDEOS

    while True:
        TXT, PHOTO_LIST, VIDEOS = main()
        time.sleep(60)


def thread_handler(message):
    bot.send_message(message.chat.id, 'Привет, сейчас вышлю последний пост!')
    last_post_text = ''
    videos_for_delete = []
    while True:
        text, photos_list, videos = TXT, PHOTO_LIST, VIDEOS
        if TXT != last_post_text:
            medias = []

            bot.send_message(message.chat.id, text)

            if photos_list:
                for i in photos_list:
                    medias.append(types.InputMediaPhoto(i))
                bot.send_media_group(message.chat.id, medias)

            if videos:
                for i in videos:
                    video = open(i, 'rb')
                    bot.send_video(message.chat.id, video,
                                   supports_streaming=True)

            last_post_text = text
            videos_for_delete.extend(videos)
            time.sleep(60)

        else:
            if videos_for_delete and len(videos_for_delete) > 1:
                delete_videos(videos_for_delete[:-1])
                videos_for_delete = videos_for_delete[-1:]
            time.sleep(60)


bot = telebot.TeleBot(TOKEN)

data_t = Thread(target=update_data)
data_t.start()


@bot.message_handler(commands=['start'])
def start(message):
    t = Thread(target=thread_handler, args=(message,))
    t.start()


bot.polling(non_stop=True)
