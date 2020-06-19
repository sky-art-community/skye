# Python library
from datetime import datetime
from urllib.request import urlopen, Request
import re
import json

# Line library
from linebot.models import TextSendMessage, ImageSendMessage, VideoSendMessage, AudioSendMessage

# Own library
import api.helper as helper
from api.models import Game, Listener 

def status(event, options):
    return TextSendMessage(text="Yo I'm here")


def show(event, options):
    # TODO: Implement show image
    pass

def extract_free_games(raw_games, extract_url, extract_id, extract_title, extract_discount):
    free_games = []
    for raw_game in raw_games:
        discount = extract_discount(raw_game)
        if discount >= 100:
            free_games.append({
                "url": extract_url(raw_game),
                "id": extract_id(raw_game),
                "title": extract_title(raw_game),
                "discount": discount,
            })

    return free_games

def get_steam_free_games():
    def extract_url(raw_game):
        return raw_game['href']

    def extract_id(raw_game):
        return raw_game['data-ds-appid']

    def extract_title(raw_game):
        return raw_game.select_one('*[class*="title"]').get_text()

    def extract_discount(raw_game):
        raw_discount = raw_game.select_one('*[class*="search_discount"]').get_text()
        try:
            return float(re.search("([0-9\.]+)%", raw_discount).group(1))
        except (ValueError, AttributeError):
            # No discount
            return 0

    raw_games = helper.load_page('https://store.steampowered.com/search/?sort_by=Price_ASC&maxprice=free&category1=998').select('a[data-ds-appid*=""]')
    return extract_free_games(
        raw_games,
        extract_url,
        extract_id,
        extract_title,
        extract_discount,
    )

def get_humble_free_games():
    def extract_url(raw_game):
        return 'https://www.humblebundle.com/store/' + raw_game['human_url']

    def extract_id(raw_game):
        return raw_game['human_url']
    
    def extract_title(raw_game):
        return raw_game['human_name']

    def extract_discount(raw_game):
        current_price = raw_game['current_price']['amount']
        full_price = raw_game['full_price']['amount']
        return (1 - (current_price / full_price)) * 100

    raw_games = helper.load_json("https://www.humblebundle.com/store/api/search?sort=discount&filter=all&request=1")['results']

    return extract_free_games(
        raw_games,
        extract_url,
        extract_id,
        extract_title,
        extract_discount,
    )

def info(event, options):
    # Initialize default response if no option below be matched
    message_text = "Sorry, currently we don't have that kind of information for you :("

    if options[0] == 'free-game':
        # Set update date
        message_text = "Last update date: {}\n".format(datetime.now().strftime("%d-%m-%Y %T"))

        # Extract free games from all providers
        steam_games = get_steam_free_games()
        humble_games = get_humble_free_games()

        # Add the provider of games
        games = [{"provider": "Steam", **game} for game in steam_games] + [{"provider": "Humble", **game} for game in humble_games]
        
        # Set proper response message
        if len(games) > 0:
            message_text += "Free games (100% off):\n"
            for index, game in enumerate(games):
                message_text += "{}. [{}] {} - {}\n".format(index + 1, game['provider'], game['title'], game['url'])
        else:        
            message_text += "No free games right now"

    return TextSendMessage(text=message_text)

def notify(event, options):
    message_text = "Sorry, we don't have that kind of notification, let us know if you expect us to have that"

    if options[0] == "free-game":
        source_type = event.source.type
        creator_id = event.source.user_id
        listener_id = None

        if source_type == 'user':
            listener_id = creator_id
        if source_type == 'group':
            listener_id = event.source.group_id
        elif source_type == 'room':
            listener_id = event.source.room_id

        # Check has been on list or not
        if not Listener.objects.filter(listener_id=listener_id).exists():
            listener = Listener(
                type="FREEGAME",
                chat_type=source_type.upper(),
                creator_id=creator_id,
                listener_id=listener_id,
            )
            listener.save()
            message_text = "Roger that, you will be notified of free games!"
        else:
            message_text = "You already on our list for free game notification"

    return TextSendMessage(text=message_text)

def stop_notify(event, options):
    message_text = "Sorry, we don't have that kind of notification"

    if options[0] == "free-game":
        source_type = event.source.type
        listener_id = None

        if source_type == 'user':
            listener_id = event.source.user_id
        if source_type == 'group':
            listener_id = event.source.group_id
        elif source_type == 'room':
            listener_id = event.source.room_id

        listener = helper.get_object_or_none(Listener, listener_id=listener_id)
        
        if listener != None:
            listener.delete()
            message_text = "Thank you for using our service :)"
        else:
            message_text = "You are not even on our list before :)"

    return TextSendMessage(text=message_text)

# All function will be called from controller
commands = {
    "status": status,
    "show": show,
    "sh": show,
    "notify": notify,
    "stop-notify": stop_notify,
    "info": info,
}

def controller(event, command, options):
    try:
        handler = commands[command]
    except KeyError:
        return TextSendMessage(text="Sorry, can't recognize your command")

    try:
        print("[{}] {} {}".format(datetime.now().strftime("%d-%m-%Y %T"), command.upper(), " ".join(options)))
        return handler(event, options)
    except Exception as e:
        print(str(e))
        return TextSendMessage(text="Something is wrong, please make sure you are commanding correctly or read the documentation from !help")