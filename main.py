import time

from util.tweetutil import TweetUtil

while True:
    TweetUtil().send_tweet()
    time.sleep(60 * 30)
