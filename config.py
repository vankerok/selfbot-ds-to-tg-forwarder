# -*- coding: utf8 -*-

#discord
channelid = ['айди канала1', 'айди канала2', 'айди канала3'] # айди канала, пример: https://discord.com/channels/942857972344823898/942857972810412073 , 942857972810412073 - айди канала
channelnames = ['имя канала1', 'имя канала2', 'имя канала3'] # вводить названия каналов(без хэштега) соответственно к айди, название канала будет перессылаться вместе с сообщением
headers = {
    'authorization': 'токен дискорд аккаунта', #токен дискорд аккаунт
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3538.102 Safari/537.36 Edge/18.19582' #тут ничего не менять
}
#telegram
destination_user_username = 'ссылка или хэштег куда будет перессылка' #ссылка на канал или чат куда будут пересылаться сообщения с дискорда, можно использовать "@хэштег" канала, в таком случае вписывай его без @
api_id = '13758353'
api_hash = 'a9c566d3cc98259425e24cb3b4579169'
phone = '+79811013601' #номер телефона телеграм аккаунта, с которого будет перессылка