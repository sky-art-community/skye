# Django library
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Line bot library
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# Load local env
from dotenv import load_dotenv
load_dotenv()

# Local libs
from .helper import parseMessage
from .controller import controller

# Create your views here.
def status(request):
    return JsonResponse(
        { 'isRunning': True },
        content_type = 'json',
        status = 200,
    )

# Line bot setup
bot = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

print(settings.LINE_CHANNEL_ACCESS_TOKEN)
print(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def api(request):
    if request.method == "POST":
        # get X-Line-Signature header value
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        global domain
        domain = request.META['HTTP_HOST']
        
        # get request body as text
        body = request.body.decode('utf-8')
        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseBadRequest()
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    data = parseMessage(event.message)
    
    if not data["is_valid"]: return

    bot.reply_message(
        event.reply_token,
        TextSendMessage(text=controller(data["command"], data["options"]))
    )