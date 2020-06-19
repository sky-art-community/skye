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

def info(event, options):
    # Initialize default response if no option below will match
    message_text = "Sorry, currently we don't have that kind of information for you :("

    if options[0] == 'free-game':
        # Set update date
        last_update_date = Game.objects.order_by('updated_at').first().updated_at
        message_text = "Last update date: {}\n".format(last_update_date.strftime("%d-%m-%Y %T"))

        # Add the provider of games
        free_games = Game.objects.filter(discount=100.0)
        
        # Set proper response message
        if len(free_games) > 0:
            message_text += "Free games (100% off):\n"
            message_text += helper.create_game_list(free_games)
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