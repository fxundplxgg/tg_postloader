from datetime import datetime
import os
import re, time, json, asyncio, logging
import sys
from urllib.parse import urlparse
from config import FROM_CHANNEL, TO_CHANNEL, RUN_TITLE, LINK_FOR_REPL, EXCEPT_LINKS, POST_KD
from subprocess import call

try:
    from telethon import TelegramClient, events
    from telethon.tl.types import MessageService
    from colorama import Fore, Style
except:
    print("Установка нужных библиотек!")
    logging.debug("Установка нужных библиотек!")
    call(['pip3', 'install', 'telethon', 'colorama'])

credits = "Made By " + Fore.LIGHTRED_EX + Style.BRIGHT + "FXUNDPLXGG" + Fore.RESET + Style.NORMAL + '\n'

api_id = 6087612
api_hash = '1148dcdf0ec9b2e68e97b0fa104f14a4'
logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s | %(message)s', datefmt='%I:%M:%S')

if RUN_TITLE:
    for ch in credits:
        time.sleep(0.03)
        print(ch, end='', flush=True)

client = TelegramClient('post', api_id, api_hash)
client.start()

print("Постлоадер запущен!")

def get_current_time():
    return datetime.now().time().strftime("%H:%M:%S")

def repl_link(text, link_from, link_to):
    return text.replace(link_from, link_to)

def get_lnks_from_text(text):
    return re.findall("(https?://\S+)", text)

async def main():
    messages = []

    try:
        with open('data.json', 'r') as df:
            data = json.load(df)
            ctr = data["msg_ctr"][str(FROM_CHANNEL)]
    except:
        ctr = 0

    async for message in client.iter_messages(FROM_CHANNEL, reverse=True):
        messages.append(message)

    try:
        if ctr == len(messages):
            print(f"Все посты с канала {FROM_CHANNEL} уже скопированы!")
            choice = input("Скопировать ещё раз? [Y/N]: ")
            if choice == "Y" or choice == "y":
                with open('data.json', 'r') as df:
                    data = json.load(df)

                with open('data.json', 'w') as df:
                    data['msg_ctr'][str(FROM_CHANNEL)] = 0
                    json.dump(data, df, indent=4)

                print("Перезапустите бота!")
                os._exit(0)
            else:
                os._exit(0)

        else:
            print(f"Количество постов в канале {FROM_CHANNEL}: {len(messages)}")
            messages = messages[ctr:]
            for j, message in enumerate(messages):
                if type(message) != MessageService:
                    msg = message

                    print(ctr, ":", msg.message)

                    if len(get_lnks_from_text(msg.message)) > 0:
                        for link in get_lnks_from_text(msg.message):
                            url = urlparse(link)
                            url = url.scheme + "://" + url.netloc + "/"

                            if url in EXCEPT_LINKS:
                                ch_entity = await client.get_entity(TO_CHANNEL)
                                msg.message = repl_link(msg.message, link, LINK_FOR_REPL)
                                await client.send_message(ch_entity, msg)
                                await asyncio.sleep(POST_KD)
                    else:
                        ch_entity = await client.get_entity(TO_CHANNEL)
                        await client.send_message(ch_entity, msg)
                        await asyncio.sleep(POST_KD)
                ctr += 1
    except:
        print("Неизвестная ошибка: ", sys.exc_info())

    with open('data.json', 'r') as df:
        data = json.load(df)

    with open('data.json', 'w') as df:
        data['msg_ctr'][str(FROM_CHANNEL)] = ctr
        json.dump(data, df, indent=4)

if __name__ == '__main__':
    client.loop.run_until_complete(main())