import telebot
from telebot import types
import time
import requests
from parse_and_delete_f import main, is_new_post_piblished, delete_videos

TOKEN = '5291208463:AAEokJAK6ISX7TiwJ4pBYZKoShUR3kKP3AI'


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(message.chat.id, 'Привет, сейчас вышлю последний пост!')
    last_post_text = ''
    videos_for_delete = []
    while True:
        if is_new_post_piblished(last_post_text):
            text, photos_list, videos = main()
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
            time.sleep(1000)

        else:
            if videos_for_delete and len(videos_for_delete) > 1:
                delete_videos(videos_for_delete[:-1])
                videos_for_delete = videos_for_delete[-1:]
            time.sleep(1000)


bot.polling(non_stop=True)
