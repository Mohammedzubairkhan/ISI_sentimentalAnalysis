# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vV2SxMxFncbEWM9oGN7JBfWOtuMo4ylt
"""

# Commented out IPython magic to ensure Python compatibility.
import requests
import plotly
import plotly.express as px
from bs4 import BeautifulSoup
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
# %matplotlib inline
import time
import datetime
import json
from nltk import sent_tokenize
import nltk
import re
from tqdm import tqdm

nltk.download('punkt')

r=requests.get('https://www.aljazeera.com/where/mozambique/')
r.encoding = 'utf-8'
html = r.text

print(html)

# Creating a BeautifulSoup object from the HTML
soup = BeautifulSoup(html)
# Getting the text out of the soup
text = soup.get_text()

for y in soup.findAll(class_="gc__content"):
  print(y.find(attrs={"aria-hidden":"true"}).text[:])

class article:
  def __init__(self, title, date, link, content):
    self.date = date
    self.link = link
    self.title = title
    self.content = content

articles = []
counter = 0
for y in tqdm(soup.findAll(class_="gc__content")):
  date_time0 = y.find(attrs={"aria-hidden":"true"}).text
  if(not date_time0.isalpha()):
    # print(y.span.text)
    # print(y.find(attrs={"aria-hidden":"true"}).text)
    # date_time = datetime.datetime.strptime(date_time0,"%d %b %Y")
    r1=requests.get('https://www.aljazeera.com/'+y.a["href"])
    r1.encoding = 'utf-8'
    html1 = r1.text
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"     
    
    # Creating a BeautifulSoup object from the HTML
    soup1 = BeautifulSoup(html1)
    # Getting the text out of the soup
    text1 = soup1.get_text()
    #print(text1)
    str_content = []
    #removing "follow alzeera paragraph"
    soup1.find('p',class_='site-footer__social-section-title css-0').decompose()
    for v in soup1.findAll('p'):
      #print(v.text)
      k = v.text.strip().strip('\n').replace('"','').replace("'",'')

      fg = k.split('\n')
      # print("watch ---->"+str(fg))
      if k == "":
        continue
      url = re.findall(regex,k) 
      if len(url)>0:
        continue
      h = sent_tokenize(k)
      for v in h:
        str_content.extend(v.strip().strip('\n').split('\n'))
      # print("new -------------------------> "+str(h))
      # print("new -------------------------> "+str(len(sent_tokenize(k))))
      # str_content.append(k)

    # print(str_content)
    curr = article(y.span.text, y.find(attrs={"aria-hidden":"true"}).text, y.a["href"], str_content)
    # print(y.find(attrs={"aria-hidden":"true"}).text)
    # print(date_time)
    # print(y.a["href"])
    articles.append(curr)
    counter+=1
    if counter == 10:
      break


    # split into sentences
# from nltk import sent_tokenize
# sentences = sent_tokenize(text)
# print(sentences[0])

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump([z.__dict__ for z in articles], f, ensure_ascii=False, indent=4)

# Opening JSON file
f1 = open('data.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f1)
f1.close()
print(data[0]['content'])

from textblob import TextBlob
mapping = {}
for i in tqdm(data):
  textblob_sentiment=[]
  for s in i['content']:
    txt= TextBlob(s)
    a= txt.sentiment.polarity
    b= txt.sentiment.subjectivity
    print(b)
    textblob_sentiment.append([s,a,b])
  # print(textblob_sentiment)
  mapping[i['title']] = textblob_sentiment

df_textblob = {}
for key in mapping:
  df_textblob[key] = pd.DataFrame(mapping[key], columns =['Sentence', 'Polarity', 'Subjectivity'])

means={}
for key in tqdm(mapping):
  means[key] = df_textblob[key]['Polarity'].mean()
  # print(key,df_textblob[key]['Polarity'].mean())

means_subjectivity={}
for key in tqdm(mapping):
  means_subjectivity[key] = df_textblob[key]['Subjectivity'].mean()
  # print(key,df_textblob[key]['Polarity'].mean())

for h in means:
  print(h,means[h])

# import seaborn as sns
# sns.displot(df_textblob['Floods hit South Africa’s KwaZu­lu-Na­tal province again']["Subjectivity"], height= 5, aspect=1.8)
# plt.xlabel("Sentence Subjectivity (Textblob)")

# sns.displot(df_textblob['Floods hit South Africa’s KwaZu­lu-Na­tal province again']["Polarity"], height= 5, aspect=1.8)
# plt.xlabel("Sentence Polarity (Textblob)")
# plt.title('Floods hit South Africa’s KwaZu­lu-Na­tal province again')

# for key in df_textblob:
#   sns.displot(df_textblob[key]["Subjectivity"], height= 5, aspect=1.8)
#   plt.xlabel("Sentence Subjectivity (Textblob)")
#   plt.title(key+"  | polarity = "+str(means[key]))

# for key in df_textblob:
#   sns.displot(df_textblob[key]["Polarity"], height= 5, aspect=1.8)
#   plt.xlabel("Sentence Polarity (Textblob)")
#   plt.title(key+"  | polarity = "+str(means[key]))

def classify_sentiment(value1):
  if value1>=0.1:
    return "Positive"
  elif value1<0:
    return "Negative"
  else :
    return "Neutral"

for key in tqdm(df_textblob):
  # print(key)
  fig = px.histogram(df_textblob[key], x='Polarity', histnorm='percent', title=key+"  | polarity = "+str(means[key])+" "+classify_sentiment(means[key]))
  #print(means[key])
  fig.show()

for key in tqdm(df_textblob):
  print(key)
  fig = px.histogram(df_textblob[key], x='Subjectivity', histnorm='percent', title=key+"  | Subjectivity = "+str(means_subjectivity[key]))
  fig.show()