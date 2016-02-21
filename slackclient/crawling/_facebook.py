import requests
import json

token1 = ''


def picture_by_id(userID):
    r = requests.get('https://graph.facebook.com/v2.3/'+userID+'?fields=picture&access_token='+token1)
    pic=r.json()
    picURL=pic['picture']['data']['url']
    return picURL


def search_by_id(userID):
    r = requests.get('https://graph.facebook.com/v2.3/'+userID+'?access_token='+token1)
    user=r.json()
    user['picture']=picture_by_id(userID)
    return user


def search_by_name(name,limit):
    userList=[]
    r = requests.get('https://graph.facebook.com/v2.5/search?q='+name+'&type=user&limit='+str(limit)+'&access_token='+token1)
    idList=r.json()
    print idList
    data=idList['data']
    for content in data:
        userID=content['id']
        userList.append(search_by_id(userID))
    return userList

print search_by_name('Ting Shen',5)
