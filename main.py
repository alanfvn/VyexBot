#util
import os
import random
import re
import uuid

#time
from datetime import datetime, timedelta
import time

#twitter
import tweepy
#utility
from util import TwUtil


#keys.
key = os.environ.get('key')
secret = os.environ.get('secret')
token = os.environ.get('token')
token_secret = os.environ.get('token_secret')




def getApi():
 auth = tweepy.OAuthHandler(key, secret)
 auth.set_access_token(token, token_secret)
 api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
 return api



def mentions():

  api = getApi()
  replies = 0

  for tweet in tweepy.Cursor(api.search, q="@"+api.me().screen_name).items(10):
    now = datetime.utcnow()-timedelta(minutes=20)
    if(now < tweet.created_at):
      sendTweet(tweet.id_str)
      replies += 1
  return replies


def sendTweet(reply = None):
  api = getApi()
  text = TwUtil.getText()
  urls = re.findall('https?:.*?(?:\.png|\.jpg|\.gif)', text)


  #data
  images = TwUtil.getImages(urls) #convert images to bytes.
  text = TwUtil.clearUrls(text, urls) #remove urls.
  ids = [api.media_upload(filename=str(uuid.uuid4())+".png", file=im).media_id for im in images] 
 

  #send
  if reply is None:
    api.update_status(status = text, media_ids = ids)
  else:
    api.update_status(status = text, media_ids = ids, in_reply_to_status_id = reply, auto_populate_reply_metadata = True)

  print("Tweet sent!")



while True:
  sendTweet()
  mentions()
  time.sleep(60*10)