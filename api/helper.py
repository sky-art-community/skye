from linebot.models import TextSendMessage, ImageSendMessage, VideoSendMessage, AudioSendMessage
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import json

PREFIX_COMMAND = '!'

def parse_message(message):
    message = message.text.lower()
    code = message[0]
    rest = message[1:].split()

    return {
        "is_valid": code == PREFIX_COMMAND,
        "command": rest[0], 
        "options": rest[1:], 
    }

def load_page(url):
    # Fetch HTML page
    html_file = urlopen(Request(
        url=url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
        }
    )).read()

    
    # Parse html and extract list of games
    return BeautifulSoup(html_file, 'html.parser')

def load_json(url):
    return json.loads(urlopen(Request(
        url=url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
        }
    )).read().decode())


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
