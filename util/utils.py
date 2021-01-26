import requests
import random
import io


class Util:

    @staticmethod
    def is_reply(status):
        bot_id = '889981111916523520'

        if status.truncated:
            mentions = status.extended_tweet.get("entities").get("user_mentions")
        else:
            mentions = status.entities.get("user_mentions")

        for mention in mentions:
            if mention.get('id_str') == bot_id:
                return True
        return False


class WordsUtil:

    @staticmethod
    def get_text():
        lines = open("./words.txt").read().splitlines()
        sentence = ""
        max_word_size = random.randint(5, 140)
        count = 0
        for r in range(len(lines)):
            text = random.choice(lines)
            count += len(text)
            if max_word_size < count:
                break
            sentence = sentence + " " + text
        return sentence

    @staticmethod
    def get_images(urls):
        images = []
        for url in urls:
            response = requests.get(url)
            images.append(io.BytesIO(response.content))
        return images

    @staticmethod
    def clear_urls(sentence, urls):
        for url in urls:
            sentence = sentence.replace(url, '')
        return sentence
