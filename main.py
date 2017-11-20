# !/usr/bin/env python
# -*- coding:utf-8 -*-

import tweepy
import urllib
import datetime
import ast
import json

import http.client, urllib.request, urllib.parse, urllib.error, base64

KEYS_PATH = "keys.json"

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '',
}

params = urllib.parse.urlencode({
    # Request parameters
    'visualFeatures': 'Description',
    'details': 'Celebrities, Landmarks',
    'language': 'en',
})


# key
with open(KEYS_PATH, 'r') as f:
    keys = json.load(f)
    CONSUMER_KEY = keys["CONSUMER_KEY"]
    CONSUMER_SECRET = keys["CONSUMER_SECRET"]
    ACCESS_TOKEN = keys["ACCESS_TOKEN"]
    ACCESS_SECRET = keys["ACCESS_SECRET"]
    headers['Ocp-Apim-Subscription-Key'] = keys["AZURE_KEY"]
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)
my_id = api.me().id

class StreamListener(tweepy.StreamListener):
    # リプライで来た画像を保存

    def on_status(self, status):
        if str(status.in_reply_to_screen_name) == 'kaira_nf':
            if 'media' in status.entities:
                medias = status.entities['media']
                m = medias[0]
                media_url = m['media_url']
                #print("ツイートを確認:", media_url)
                try:
                    body = "{{\"url\":\"{}\"}}".format(media_url)
                    conn = http.client.HTTPSConnection('eastasia.api.cognitive.microsoft.com')
                    conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
                    response = conn.getresponse()
                    data = response.read()
                    #print(data)
                    conn.close()
                except Exception as e:
                    print("[Errno {0}] {1}".format(e.errno, e.strerror))

                try:
                    responseList = json.loads(data.decode('utf-8'))
                    confidence = responseList['description']['captions'][0]['confidence']
                    description = responseList['description']['captions'][0]['text']
                    tweet = '@' + str(status.user.screen_name) + ' この写真は「' + description + '」ですね！ ' + '（自信:' + str(int(confidence*100)) + '%）'
                    #print(tweet)
                    api.update_status(status=tweet, in_reply_to_status_id=status.id)
                except Exception as e:
                    print("ツイート失敗")

    def on_event(self, event):
        if event.event == 'follow':
            source_user = event.source
            if my_id != source_user["id"]:
                try:
                    api.create_friendship(source_user["id"])
                    # print("followed @{}".format(source_user["screen_name"]))
                except Exception as e:
                    print("フォロー失敗", e)

    def on_error(self, status_code):
        print('エラー発生: ' + str(status_code))
        return True

    def on_connect(self):
        print('接続しました')
        return

    def on_disconnect(self, notice):
        print('切断されました:' + str(notice.code))
        return

    def on_limit(self, track):
        print('受信リミットが発生しました:' + str(track))
        return

    def on_timeout(self):
        print('タイムアウト')
        return True

    def on_warning(self, notice):
        print('警告メッセージ:' + str(notice.message))
        return

    def on_exception(self, exception):
        print('例外エラー:' + str(exception))
        return

listener = StreamListener()
stream = tweepy.Stream(auth, listener)
while True:
    try:
        stream.userstream()
    except:
        pass