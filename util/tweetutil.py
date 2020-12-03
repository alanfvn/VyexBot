import os
import re
import uuid
import tweepy

from util.wordsutil import WordsUtil


class TweetUtil:

    def __init__(self):
        self.key = os.environ.get('key')
        self.secret = os.environ.get('secret')
        self.token = os.environ.get('token')
        self.token_secret = os.environ.get('token_secret')

    def get_api(self):
        auth = tweepy.OAuthHandler(self.key, self.secret)
        auth.set_access_token(self.token, self.token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        return api

    def get_mentions(self):
        # TODO: use stream api to obtain mentions in real time.
        # https://stackoverflow.com/a/27135570
        pass

    def get_dms(self):
        # TODO: do something with direct messages..
        api = self.get_api()

    def send_tweet(self, reply=None):
        api = self.get_api()
        random_text = WordsUtil.get_text()
        all_urls = re.findall('https?:.*?(?:\.png|\.jpg|\.gif)', random_text)

        images = WordsUtil.get_images(all_urls)  # convert images to bytes.
        text = WordsUtil.clear_urls(random_text, all_urls)  # remove urls.
        ids = [api.media_upload(filename=str(uuid.uuid4()) + ".png", file=im).media_id for im in images]

        if reply is None:
            api.update_status(status=text, media_ids=ids)
        else:
            api.update_status(status=text, media_ids=ids, in_reply_to_status_id=reply,
                              auto_populate_reply_metadata=True)
