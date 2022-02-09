import requests
import os
import youtube_dl
from config import VK_TOKEN


def main():
    TOKEN = VK_TOKEN

    VERSION = 5.131
    DOMAIN = 'biobezpredel'

    link_1 = 'https://vk.com/biobezpredel?z=photo-76771597_'
    link_2 = '%2Falbum-76771597_00%2Frev'

    def give_phtVd_links(attach: dict):
        res = []
        res_vid = []
        if len(attach) > 1:
            for i in range(len(attach)):
                if attach[i]['type'] == 'photo':
                    res.append(link_1 + str(attach[i]['photo']['id']) + link_2)
                if attach[i]['type'] == 'video':
                    print()
                    lnk = 'vk.com/video' + \
                        str(attach[i]['video']['owner_id']) + \
                        '_' + str(attach[i]['video']['id'])
                    res_vid.append(lnk)

        else:
            if attach[0]['type'] == 'photo':
                res.append(link_1 + str(attach[0]['photo']['id']) + link_2)
            elif attach[0]['type'] == 'video':
                lnk = 'vk.com/video' + \
                    str(attach[0]['video']['owner_id']) + \
                    '_' + str(attach[0]['video']['id'])
                res_vid.append(lnk)

        return res, res_vid

    responce = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                'access_token': TOKEN,
                                'v': VERSION,
                                'domain': DOMAIN,
                                'count': 2,
                            })

    data = responce.json()['response']['items']

    text = data[1]['text']
    photo_links, video_links = give_phtVd_links(data[1]['attachments'])
    video_names = []
    if video_links:
        ydl_opts = {}
        for link in video_links:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            video_names.append(
                f'Video by BioBeZpredel [Биохакинг _ Спорт _ Дизмораль]-{link[-19:]}.mp4')

    return (text, photo_links, video_names)


def is_new_post_piblished(last_post):
    TOKEN = VK_TOKEN

    VERSION = 5.131
    DOMAIN = 'biobezpredel'

    responce = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                'access_token': TOKEN,
                                'v': VERSION,
                                'domain': DOMAIN,
                                'count': 2,
                            })

    data = responce.json()['response']['items']

    text = data[1]['text']
    if text == last_post:
        return False
    return True

def delete_videos(video_list: list):
    if video_list:
        for video in video_list:
            os.remove(video)

if __name__ == '__main__':
    main()

