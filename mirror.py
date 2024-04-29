# -*- coding: utf8 -*-
from config import channelid, channelnames, headers, destination_user_username, api_id, api_hash, phone
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from requests import get
from json import loads
from datetime import datetime

def clear_file_with_messageids():
    clear_file = open('messageids.txt', 'r+')
    clear_file.truncate(0)
    clear_file.close()

def change_time():
    time_now = datetime.now()
    year_now, month_now, day_now,hour_now = time_now.year, time_now.month, time_now.day, time_now.hour
    if hour_now < 3:
        day_now -= 1
    elif hour_now == 3:
        clear_file_with_messageids(hour_now)
    if month_now < 10:
        month_now = '0'+str(month_now)
    if day_now < 10:
        day_now = '0'+str(day_now)
    today = str(year_now) + '-' + str(month_now) + '-' + str(day_now)
    return today

def telegram_client_authorise():
    client = TelegramClient(StringSession(), api_id, api_hash).start(phone=phone)
    client.connect()
    receiver = client.get_entity(destination_user_username)
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Enter the code: '))
    return receiver, client

def telegram_send_message(messages_dict, client, receiver):
    for message in range(len(messages_dict)):
        if messages_dict[message] != 'None':
            try:
                client.send_message(receiver, messages_dict[message], parse_mode='html')
            except Exception as e:
                print(e)

def parse_discord_messages():
    message_list = []
    for channels_change in range(len(channelid)):
        today = change_time()
        page = get(f'https://discord.com/api/v9/channels/{channelid[channels_change]}/messages', headers=headers)
        source_data = page.text
        jsonn = loads(source_data)
        for value in jsonn:
            if str(today) in value['timestamp']:
                with open('messageids.txt', 'r+', encoding='utf-8') as messageids:
                    messageids_read = messageids.read()
                    if value['id'] in messageids_read:
                        pass
                    else:
                        message_list.append('#'+channelnames[channels_change]+'\n'+value['content']+'\n')
                        messageids.write(value['id']+'\n')
    return message_list

if __name__ == '__main__':
    receiver, client = telegram_client_authorise()
    while True:
        telegram_send_message(parse_discord_messages(), client, receiver)