import tweepy
import json
import requests
import csv
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
CONSUMER_KEY= '8khdUqNZXj8UgLwp2K0BFGdVh'
CONSUMER_SECRET= 'TGrVqKKq5mX737GLXsYLadQK1pBZFLfSpy5snqr6X2mwI3GDZ6'
ACCESS_TOKEN='1232024497575940096-f34HOxXdP5jYUj00ROzjjI0faJDwCr'
ACCESS_TOKEN_SECRET='HeOgwcieetkDF0NO9HWTSOnwELQxzlUmcytGQjTBvlX40'

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
#print(auth.)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
# test authentication
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

#json_data=api.search(q="#self-driving cars", lang="en", rpp=5)

# Open/Create a file to append data
csvFile = open('self-driving-cars.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)
csvWriter.writerow(["text"])
searchterms = "selfdrivingcars OR autonomouscars"
for tweet in tweepy.Cursor(api.search,q=searchterms,count=100,
                           lang="en",
                           since="2017-04-03").items():

    if (not tweet.retweeted) and ('RT @' not in tweet.text):
        print (tweet.created_at, tweet.text)

        csvWriter.writerow([tweet.text.encode('utf-8')])

data = pd.read_csv('self-driving-cars.csv')
data.dropna(subset=['text'], inplace=True)

data=data[data.index%2==0]


data["text"]=data.text.str.replace(r'^b','')
data["text"]=data.text.str.replace(r'https?:\/\/.*\/[a-zA-Z0-9]*', '')
data["text"]=data.text.str.replace(r'@[a-zA-Z0-9]{1,10}', '')
data["text"]=data.text.str.replace(r'\$[a-zA-Z0-9]*', '')
data["text"]=data.text.str.replace(r'[0-9]*','')
data["text"]=data.text.str.replace(r'\\[a-z A-Z]{1,2}','')
data["text"]=data.text.str.replace(r'\:','')
data["text"]=data.text.str.replace(r'\\n','')
data["text"]=data.text.str.replace(r'\#','')
data["text"]=data.text.str.replace(r'\/','')
data["text"]=data.text.str.replace(r'\'','')
data["text"]=data.text.str.replace(r'\"','')
data["text"]=data.text.str.replace(r'\-','')
data["text"]=data.text.str.replace(r'\?','')
data["text"]=data.text.str.replace(r'\_','')
data["text"]=data.text.str.replace(r'%','')
data["text"]=data.text.str.replace(r'\,','')
data["text"]=data.text.str.replace(r'.','')
data["text"]=data.text.str.replace(r'\&amp','')
data["text"]=data.text.str.replace(r';','')
data["text"]=data.text.str.replace(r'!','')
data["text"]=data.text.str.replace(r'\\s','')
data["text"]=data.text.str.replace(r'\)','')
data["text"]=data.text.str.replace(r'\(','')
data["text"]=data.text.str.replace(r'\+','')

vectorizer = TfidfVectorizer(min_df=2,max_df=0.9,lowercase="True",stop_words="english")

X = vectorizer.fit_transform(data.text.values.astype('U'))
