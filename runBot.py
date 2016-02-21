import time
import json
from slackclient import SlackClient
from slackclient._response import Response

# Configuration for tokens. You can choose account token or bot token. Put your own token inside

# account token for channels
# token = ""

# bot token for bots
token = ""

channel = ''
msg_text = ''
user = ''

res = Response(token)
sc = SlackClient(token)

if sc.rtm_connect():
    login_data = sc.api_read("im.list", token = token)
    bot_channel = login_data["ims"]

    for chan in bot_channel:
        if (chan["user"]!="USLACKBOT"):
            channel = chan["id"]
            user = chan["user"]

    while True:
        data = sc.rtm_read()
        for single_data in data:
            if 'type' in single_data.keys():
                res.response(single_data, channel, sc, user)
        time.sleep(1)
else:
    print "Connection Failed, invalid token?"
