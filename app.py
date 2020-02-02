import os
from pprint import pprint
from decouple import config
from concurrent.futures import ProcessPoolExecutor

from flask import (
    Flask, request, abort
)
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import __helper as helper
from __controller import controller
from __on_running_tasks import Tasks
import time
import asyncio


# Load local env
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
# get LINE_CHANNEL_ACCESS_TOKEN from your environment variable
bot = LineBotApi(
    config("LINE_CHANNEL_ACCESS_TOKEN",
           default=os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
)
# get LINE_CHANNEL_SECRET from your environment variable
handler = WebhookHandler(
    config("LINE_CHANNEL_SECRET",
           default=os.getenv('LINE_CHANNEL_SECRET'))
)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']


    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)


    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)


    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    data = helper.parseMessage(event.message)
    pprint(event)
    if not data["is_valid"]: return

    bot.reply_message(
        event.reply_token,
        TextSendMessage(text=controller(data["command"], data["options"]))
    )


def on_running():
    print("running")
    tasks = Tasks(bot)
    while True:
        tasks.run()
        time.sleep(1)

def run_app():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    executor = ProcessPoolExecutor(2)
    loop = asyncio.get_event_loop()

    loop.run_in_executor(executor, on_running)
    loop.run_in_executor(executor, run_app)
    
    loop.run_forever()