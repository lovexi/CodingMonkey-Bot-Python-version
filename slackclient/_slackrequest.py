import time
from future.moves.urllib.parse import urlparse, urlencode
from future.moves.urllib.request import urlopen, Request
from future.moves.urllib.error import HTTPError


class SlackRequest(object):
    def __init__(self):
        pass

    def do(self, token, request="?", post_data={}, domain="slack.com"):
        post_data["token"] = token
        post_data = urlencode(post_data)
        post_data = self.parse_to_javascript(post_data)
        url = 'https://{}/api/{}'.format(domain, request)
        return urlopen(url, post_data.encode('utf-8'))

    def parse_to_javascript(self, post_data):
        post_data = post_data.replace("+", "%20")
        post_data = post_data.replace("%27", "%22")
        post_data = post_data.replace("%21", "!")
        post_data = post_data.replace("%100", "'")
        post_data = post_data.replace("%28", "(")
        post_data = post_data.replace("%29", ")")
        return post_data
