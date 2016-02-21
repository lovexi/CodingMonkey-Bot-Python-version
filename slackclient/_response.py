import json
import random
import math
import os
from crawling._twitter import twitter_crawling

class Response(object):
    def __init__(self, token):
        self.name = ""
        self.token = token
        self.greetingList = ['Hello {}, welcome to the Equifax Hackathon channel! Have fun :). You can type help for more details!'
                        , 'Nice to see you here, {} ! What can I do for you (please type help!)'
                        , 'I am willing to do anything for you {} ! Type help so I can help you!']
        self.help_msg = {"text": 'Don\'t Worry  {} ! I will show you how to communicate with me :).',
                        "attachments":[{"pretext": "Command line:",
                             "color": "#36a64f", "text": "hi: Say hello to me, so that I know you are here!"},
                            {"color": "#36a64f", "text": "print message: I will grab all detailed ID message for you, such as channel id or user id :)"},
                            {"color": "#e2ffb6", "text": "help: I can show you all commands I can understand :)"},
                            {"color": "#415677", "text": "show name or nameID: I can know that your target ID"},
                            {"color": "#b27485", "text": "select dataLocation: I can know where I can grab data for you"}
                            ]}
        self.select_msg = {"text": "Where do you want to grab personal information for {} ?",
            "attachments": [{"pretext": "You can choose:", "color": "#36a64f", "text": "Facebook + limits"},
            {"color": "#36a64f", "text": "Twitter + limits"},
            {"color": "#415677", "text": "Craigslist"}
            ]}


    def response(self, data, channel, sc, user):
        type = data["type"]
        user_info = sc.api_read("users.info", token = self.token, user = user)
        username = user_info["user"]["name"]

        if type == "hello":
            sc.rtm_send_message(channel, self.greetingList[int(math.floor(random.random()*3))].format(username))

        if "user" in data.keys() and data["user"] == user:
            if (type == "message"):
                text = data["text"].lower()

                if (text.startswith("hi")):
                    sc.rtm_send_message(channel, "I am CodingMonkey Bot. Nice to meet you here {0}!".format(username))

                if (text.startswith("print")):
                    sc.rtm_send_message(channel, data[text[5:].strip()])

                if (text.startswith("help")):
                    sc.api_call("chat.postMessage", token = self.token, channel = channel,
                                username = "codingmonkey", text = self.help_msg["text"].format(username), attachments = self.help_msg["attachments"])

                if (text.startswith("show")):
                    command_msg = str(text).split(' ')
                    self.name = command_msg[1]
                    sc.api_call("chat.postMessage", token = self.token, channel = channel,
                                username = "codingmonkey", text = self.select_msg["text"].format(username),
                                attachments = self.select_msg["attachments"])

                if (text.startswith("select")):
                    command_msg = str(text).split(' ')

                    if (command_msg[1].lower() == "twitter"):
                        twi = twitter_crawling()
                        limits = 5

                        if len(command_msg) == 3:
                            limits = int(command_msg[2])

                        twitter_info = json.dumps(twi.spiderInfo(self.name, limits))
                        sc.api_call("chat.postMessage", token = self.token, channel = channel,
                                    username = "codingmonkey", text = "Here are the results in Twitter:", attachments = twitter_info)

                    elif (command_msg[1].lower() == "facebook"):
                        root = os.getcwd()
                        relative_path = "slackclient/data/facebookY.json"
                        abs_path = os.path.join(root, relative_path)
                        with open(abs_path) as facebook_file:
                            facebook_info = json.load(facebook_file)
                            facebook_info = json.dumps(facebook_info)
                            sc.api_call("chat.postMessage", token = self.token, channel = channel,
                                        username = "codingmonkey", text = "Here are the results in Facebook:", attachments = facebook_info)
                    elif (command_msg[1].lower() == "craigslist"):
                        root = os.getcwd()
                        relative_path = "slackclient/data/craigslist.json"
                        abs_path = os.path.join(root, relative_path)
                        with open(abs_path) as craigslist_file:
                            craigslist_info = json.load(craigslist_file)
                            craigslist_info = json.dumps(craigslist_info)
                            craigslist_info = craigslist_info.replace("'", "%100")
                            sc.api_call("chat.postMessage", token = self.token, channel = channel,
                                        username = "codingmonkey", text = "Here are the results in Craigslist:", attachments = craigslist_info)
