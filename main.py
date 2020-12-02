# util
import os
import re
import time
import uuid
# time
from datetime import datetime, timedelta

# twitter
import tweepy

# utility
from util.tw_util import TwUtil

key = os.environ.get('key')
secret = os.environ.get('secret')
token = os.environ.get('token')
token_secret = os.environ.get('token_secret')


def get_api():
    auth = tweepy.OAuthHandler(key, secret)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api


def mentions():
    api = get_api()
    replies = 0

    for tweet in tweepy.Cursor(api.search, q="@" + api.me().screen_name).items(10):
        now = datetime.utcnow() - timedelta(minutes=20)
        if now < tweet.created_at:
            send_tweet(tweet.id_str)
            replies += 1
    return replies


def pms():
    api = get_api()


def send_tweet(reply=None):
    api = get_api()
    text = TwUtil.get_text()
    urls = re.findall('https?:.*?(?:\.png|\.jpg|\.gif)', text)

    # data
    images = TwUtil.get_images(urls)  # convert images to bytes.
    text = TwUtil.clear_urls(text, urls)  # remove urls.
    ids = [api.media_upload(filename=str(uuid.uuid4()) + ".png", file=im).media_id for im in images]

    # send
    if reply is None:
        api.update_status(status=text, media_ids=ids)
    else:
        api.update_status(status=text, media_ids=ids, in_reply_to_status_id=reply, auto_populate_reply_metadata=True)

    print("Tweet sent!")


while True:
    send_tweet()
    mentions()
    time.sleep(60 * 10)
