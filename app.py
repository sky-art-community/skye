import os
from decouple import config
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

# Load local env
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
# get LINE_CHANNEL_ACCESS_TOKEN from your environment variable
line_bot_api = LineBotApi(
    config("LINE_CHANNEL_ACCESS_TOKEN",
           default=os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
)
# get LINE_CHANNEL_SECRET from your environment variable
handler = WebhookHandler(
    config("LINE_CHANNEL_SECRET",
           default=os.getenv('LINE_CHANNEL_SECRET'))
)

print(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
print(os.environ.get('LINE_CHANNEL_SECRET'))

# # get LINE_CHANNEL_ACCESS_TOKEN from your environment variable
# line_bot_api = LineBotApi(
#     config("LINE_CHANNEL_ACCESS_TOKEN",
#            default='d5449232756c655e65343d53477ecaaf')
# )
# # get LINE_CHANNEL_SECRET from your environment variable
# handler = WebhookHandler(
#     config("LINE_CHANNEL_SECRET",
#            default='j4Mv5oDA2FKWmKQz6pbi0xSd3Ghhy98JzpjgJB5XDuioQHMGH7Gb3635TwKEHVO+bS2lQGwMv0Ma+T0WUVIBhJ8+5GdBiOPhsdsy20t39zmphYzY8B95IR0MmYmTutsGQRzpXpe2HdKEtvn6VeEmdwdB04t89/1O/w1cDnyilFU=')
# )


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
    print(event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)