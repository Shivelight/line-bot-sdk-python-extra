import os
import sys
from argparse import ArgumentParser

from sanic import Sanic, response
from sanic.log import logger
from sanic.exceptions import abort
from linebot import WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from linebotx import AioHttpClient, LineBotApiAsync

app = Sanic(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

parser = WebhookParser(channel_secret)


@app.listener("before_server_start")
async def setup_bot(app, loop):
    transport = AioHttpClient(loop=loop)
    app.bot = LineBotApiAsync(channel_access_token, http_client=transport)


@app.listener('after_server_stop')
async def close_bot(app, loop):
    await app.bot.close()


@app.route("/callback", methods=["POST"])
async def callback(request):
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.body.decode()
    logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        await app.bot.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return response.text("OK")


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage="Usage: python " + __file__ + " [--port <port>] [--help]"
    )
    arg_parser.add_argument("-p", "--port", type=int, default=8000, help="port")
    arg_parser.add_argument("-d", "--debug", default=False, help="debug")
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
