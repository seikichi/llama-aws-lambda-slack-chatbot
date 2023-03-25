import os
import logging
import re

from slack_bolt import App, Ack
from slack_bolt.adapter.aws_lambda import SlackRequestHandler

from chat import chat

TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SECRET = os.environ.get('SLACK_SIGNING_SECRET')

app = App(process_before_response=True,
          token=TOKEN,
          signing_secret=SECRET)


def just_ack(ack: Ack):
    ack()


def handle_app_mention(request, body, say):
    print(body)  # debug
    if 'X-Slack-Retry-Num' in request.headers:
        return
    message = re.sub(r'^<[^>]+>\s*', '', body['event']['text'])
    say(chat(message), thread_ts=body['event']['ts'], reply_broadcast=True)


app.event('app_mention')(ack=just_ack, lazy=[handle_app_mention])


if __name__ == "__main__":
    app.start()


SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)


def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)
