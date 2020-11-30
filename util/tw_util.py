import os 
import random
from os.path import dirname, abspath
#images
import requests
from io import BytesIO





class TwUtil:

  def getText():
    lines = open("./words.txt").read().splitlines()
    sentence = ""
    maxSentenceSize = random.randint(5, 140)
    count = 0
    for r in range(len(lines)):
      text = random.choice(lines)
      count += len(text)
      if maxSentenceSize < count:
        break
      sentence = sentence+" "+text
    return sentence


  def getImages(urls):
    images = []
    for url in urls:
      response = requests.get(url)
      images.append(BytesIO(response.content))
    return images



  def clearUrls(sentence, urls):
    for url in urls:
      sentence = sentence.replace(url, '')
    return sentence
