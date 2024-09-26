import os
import copy

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from TCSWebScrapping.Framework.utilities.payload import Payload
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv('SLACK_BOT_TOKEN')
message_thread = None


class SlackBot:

    def __init__(self):
        self.client = WebClient(token=TOKEN)
        self.channel_id = "C03NTE1GN5Q"  # slack group id: bots-dx(C030Q5KJV35) and bots-dx-test (C03NTE1GN5Q)
        self.message_ts = None
        self.message_ts2 = None

    def post_file_on_slack(self, log_files=None, msg_text=""):
        global message_thread

        if message_thread:
            thread_ts = message_thread
        else:
            thread_ts = None

        try:
            payload = copy.deepcopy(Payload.BLOCKS)
            divider = copy.deepcopy(Payload.DIVIDER)
            mark_down = copy.deepcopy(Payload.MARK_DOWN)

            mark_down['text']['text'] = msg_text

            payload['blocks'].append(divider)
            payload['blocks'].append(mark_down)
            payload['blocks'].append(divider)

            print('Sending and uploading file message using Bot..')
            response = self.client.files_upload(
                channels=self.channel_id,
                file=log_files,
                initial_comment=msg_text,
                thread_ts=thread_ts,
                blocks=payload['blocks']
            )
            if response.status_code == 200:
                print("Successfully completed posting file on slack "
                              "and status code %s" % response.status_code)
            else:
                print("Failed to post report on slack "
                              "and status code %s" % response.status_code)

        except SlackApiError as e:
            print("Error uploading file: {}".format(e))

    def post_message_on_slack(self, text=""):
        global message_thread

        try:
            payload = copy.deepcopy(Payload.BLOCKS)
            divider = copy.deepcopy(Payload.DIVIDER)
            mark_down = copy.deepcopy(Payload.MARK_DOWN)
            mark_down['text']['text'] = text
            payload['blocks'].append(divider)
            payload['blocks'].append(mark_down)
            payload['blocks'].append(divider)

            if text:
                print('Sending message using Bot')
                response = self.client.chat_postMessage(
                    channel=self.channel_id,
                    text=text,
                    thread_ts=self.message_ts,
                    blocks=payload['blocks']
                )
                self.message_ts = response.data['ts']
                message_thread = self.message_ts

                if response.status_code == 200:
                    print("Successfully completed posting message on slack and status code %s" % response.status_code)
                else:
                    print("Failed to post report on slack and status code %s" % response.status_code)

        except SlackApiError as e:
            print("Error uploading file: {}".format(e))
