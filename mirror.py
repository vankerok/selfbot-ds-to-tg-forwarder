# -*- coding: utf8 -*-
import telethon.errors
from config import channels, headers, tg_channel, tg_user, id_to_thread
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import PeerChannel
from requests import get
from json import loads
from datetime import datetime

def clear_food_file():
    with open('food.txt', 'w'):
        pass

def time_checker():
    time_now = datetime.utcnow()
    if time_now.hour == 0 and time_now.minute == 1:
        clear_food_file()
    return str(time_now).split()[0]

def telegram_client_authorise():
    client = TelegramClient(tg_user['name'], tg_user['api_id'], tg_user['api_hash']).start()
    client.connect()
    receiver = client.get_entity(PeerChannel(tg_channel))
    return receiver, client

def telegram_send_message(client, receiver, message, channel_id, message_prefix, files, emptymessage):
    if files:
        for file in files:
            try:
                if files.index(file) + 1 == len(files):
                    client.send_file(receiver, file=file, caption=message, parse_mode='Markdown', link_preview=False, reply_to=id_to_thread[channel_id])
                else:
                    client.send_file(receiver, file=file, caption=message_prefix, parse_mode='Markdown', link_preview=False, reply_to=id_to_thread[channel_id])
            except telethon.errors.MediaCaptionTooLongError:
                client.send_file(receiver, file=file, caption=message_prefix, parse_mode='Markdown', link_preview=False, reply_to=id_to_thread[channel_id])
                client.send_message(receiver, message, reply_to=id_to_thread[channel_id])
            except telethon.errors.WebpageMediaEmptyError:
                if not emptymessage and files.index(file) + 1 == len(files):
                    client.send_message(receiver, message, reply_to=id_to_thread[channel_id])
    else:
        client.send_message(receiver, message, reply_to=id_to_thread[channel_id])

def get_all_messages_before_start():
    for channelid in list(channels.keys()):
        time_now = time_checker()
        page = get(f'https://discord.com/api/v9/channels/{channelid}/messages', headers=headers)
        source_data = page.text
        jsonn = loads(source_data)
        for value in jsonn:
            if time_now in str(value['timestamp']):
                with open('fud.txt', 'r+', encoding='utf-8') as fudtxt:
                    fud = fudtxt.read()
                    if value['id'] not in fud:
                        fudtxt.write('\n' + value['id'])

def parse_discord_messages():
    for channelid in list(channels.keys()):
        time_now = time_checker()
        page = get(f'https://discord.com/api/v9/channels/{channelid}/messages', headers=headers)
        source_data = page.text
        jsonn = loads(source_data)
        for value in jsonn:
            if time_now in str(value['timestamp']):
                with open('fud.txt', 'r+', encoding='utf-8') as fudtxt:
                    files = []
                    fud = fudtxt.read()
                    if value['content'] == '' and value['attachments'] == []:
                        pass
                    elif value['id'] not in fud:
                        if 'content' not in value:
                            emptymessage = True
                        else:
                            emptymessage = False
                        value_id = value['id']
                        value_content = value['content']\
                                            .replace('@', '')\
                                            .replace('*', '')\
                                            .replace('>', '')\
                                            .replace('<', '')
                        message_prefix = '**' + value['author']['username'] + '**' + '\n\n' + '#' + channels[channelid]
                        message = '**' + value['author']['username'] + '**' + '\n' + value_content + '\n\n' + '#' + channels[channelid]
                        attachments = value['attachments']
                        if attachments != []:
                            for value in attachments:
                                files.append(value['url'])
                        print(message)
                        print(files)
                        fudtxt.write('\n' + value_id)
                        telegram_send_message(client, receiver, message, channelid, message_prefix, files, emptymessage)

receiver, client = telegram_client_authorise()
if __name__ == '__main__':
    get_all_messages_before_start()
    while True:
        parse_discord_messages()
