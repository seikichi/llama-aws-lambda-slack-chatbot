import os
import logging
import re
import subprocess

from slack_bolt import App, Ack, Say, BoltRequest
from slack_bolt.adapter.aws_lambda import SlackRequestHandler


LLAMA_CPP_MAIN_PATH = os.environ.get("LLAMA_CPP_MAIN_PATH", "./llama.cpp/main")
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")
STOP_SEQUENCE = os.environ.get("STOP_SEQUENCE", "")

with open("prompt.txt", encoding="utf-8") as f:
    PROMPT = f.read()


app = App(
    process_before_response=True,
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET,
)


def answer(question: str) -> str:
    prompt = PROMPT.replace("{{question}}", question)

    p = subprocess.run(
        [LLAMA_CPP_MAIN_PATH, "-m", "./model.bin", "-p", prompt],
        capture_output=True,
        encoding="utf-8",
    )

    print(p.stdout)  # debug
    print(p.stderr)  # debug

    index = p.stdout.find(prompt)
    output = p.stdout[index + len(prompt) :]

    if len(STOP_SEQUENCE) == 0:
        return output.strip()

    stop_index = output.find(STOP_SEQUENCE)
    return output[0 : stop_index if stop_index >= 0 else len(output)].strip()


def just_ack(ack: Ack) -> None:
    ack()


def handle_app_mention(request: BoltRequest, say: Say) -> None:
    # sometimes it takes a while to invoke Lambda function.
    # In that case, Slack try to send notification again.
    # Here we ignore those retry requests.
    if "x-slack-retry-num" in request.headers:
        return

    # remove mention ("@Bot How are you?" -> "How are you?")
    message = re.sub(r"<[^>]+>\s*", "", request.body["event"]["text"])

    say(answer(message), thread_ts=request.body["event"]["ts"], reply_broadcast=True)

# handle_app_mention takes a while because it executes llama.cpp ...
# to execute such method, we need to use lazey listener feature of Bolt.
app.event("app_mention")(ack=just_ack, lazy=[handle_app_mention])


if __name__ == "__main__":
    # if you want to run this bot locally ...
    # 1. configure environment variables (e.g., export SLACK_BOT_TOKEN=...).
    # 2. run `poetry run python app.py`.
    # 3. use ngrok or something and update `settings.event_subscriptions.request_url` in App Manifest.
    app.start()


SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)


def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)
