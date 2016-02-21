from twython import Twython
import json
import urllib2
import base64
import json

"""
Use Twitter API to grab user information from list of organizations;
export text file
Uses Twython module to access Twitter API
"""

class twitter_crawling(object):
    def __init__(self):
        pass

    def spiderInfo(self, name, limit):
        index = 0
        c = 0
        result_info  = []

        if limit == 0:
            limit = 5
        t = Twython(app_key = "",
            app_secret = "",
            oauth_token = "",
            oauth_token_secret = "")

        while c<limit:
            res = t.search_users(q=name, page=index, count=5)
            length = len(res)
            for content in res:
                single_data={}
                single_data["thumb_url"] = content["profile_image_url"]
                single_data["text"] = content["screen_name"]
                single_data["author_name"] = content["name"]
                single_data["text"] = "\nLocation:      " + json.dumps(content["location"]) +\
                                ", Philippines\n\nLanguage:      " + json.dumps(content["lang"]) +\
                                "\n\nFriends Count: " + json.dumps(content["friends_count"]) +\
                                "\n\nTime Zone:     " + json.dumps(content["time_zone"]) +\
                                "\n\nDescription:   " + json.dumps(content["description"])
                result_info.append(single_data)
                c+=1
                if c==limit:
                    return result_info
            if length<5:
                return result_info
            index+=1
        return result_info

    def encodeImage(self, url):
        if url=="":
            return
        img = urllib2.urlopen(url).read()
        encoded = base64.b64encode(img)
        return encoded
