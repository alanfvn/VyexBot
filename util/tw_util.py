import os
import random
from os.path import dirname, abspath
# images
import requests
from io import BytesIO


class TwUtil:

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
            images.append(BytesIO(response.content))
        return images

    @staticmethod
    def clear_urls(sentence, urls):
        for url in urls:
            sentence = sentence.replace(url, '')
        return sentence
