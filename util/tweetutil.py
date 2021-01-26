import os
import re
import uuid

import tweepy

from util.utils import Util
from util.utils import WordsUtil


class TweetStream(tweepy.StreamListener):

    def on_status(self, status):
        if Util.is_reply(status):
            TweetUtil.send_tweet(status.id_str)


class TweetUtil:

    def __init__(self):
        self.stream = None

    def init_stream(self):
        if self.stream is not None:
            return
        api = TweetUtil.get_api()
        stream_listener = TweetStream()
        self.stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
        self.stream.filter(track=[api.me().screen_name], is_async=True)

    def close_stream(self):
        if self.stream is None:
            return
        self.stream.disconnect()
        self.stream = None

    @staticmethod
    def get_api():
        auth = tweepy.OAuthHandler(os.environ.get('key'), os.environ.get('secret'))
        auth.set_access_token(os.environ.get('token'), os.environ.get('token_secret'))
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        return api

    @staticmethod
    def send_tweet(reply=None):
        api = TweetUtil.get_api()
        random_text = WordsUtil.get_text()
        all_urls = re.findall('https?:.*?(?:.png|.jpg|.gif)', random_text)

        images = WordsUtil.get_images(all_urls)  # convert images to bytes.
        text = WordsUtil.clear_urls(random_text, all_urls)  # remove urls.
        ids = [api.media_upload(filename=str(uuid.uuid4()) + ".png", file=im).media_id for im in images]

        if reply is None:
            api.update_status(status=text, media_ids=ids)
        else:
            api.update_status(status=text, media_ids=ids, in_reply_to_status_id=reply,
                              auto_populate_reply_metadata=True)
