from linebot.models import TextSendMessage, ImageSendMessage, VideoSendMessage, AudioSendMessage
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import json

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


BROWSER = settings.BROWSER
PREFIX_COMMAND = '!'

def parse_message(message):
    message = message.lower()
    code = message[0]
    rest = message[1:].split()

    return {
        "is_valid": code == PREFIX_COMMAND,
        "command": rest[0], 
        "options": rest[1:], 
    }

def get_object_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except ObjectDoesNotExist:
        return None

def load_page(url):
    # Fetch HTML page
    html_file = BROWSER.get(url).text
    
    # Parse html and extract list of games
    return BeautifulSoup(html_file, 'html.parser')

def load_json(url):
    return json.loads(urlopen(Request(
        url=url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
        }
    )).read().decode())

def create_free_game_list(free_games):
    message_text = "Free games (100% off):\n"
    for index, game in enumerate(free_games):
        message_text += "{}. [{}] {} - {}\n".format(
            index + 1,
            game.provider_name,
            game.name,
            game.source_url,
        )

    return message_text

"""
Don't delete these, perhaps will be used in the future
"""
# class MessageTemplate:
#     # Enums
#     TEXT = 1
#     AUDIO = 2
#     IMAGE = 3
#     VIDEO = 4

#     def __init__(self, type, content):
#         if not isinstance(content, dict): 
#             raise ValueError("Content should be dict type")

#         self.__type = type
#         self.__content = content

#     def get_type(self):
#         return self.__type

#     def get_content(self):
#         return self.__content
