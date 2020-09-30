#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 21:54:08 2019

@author: wajgilani
"""
import pip

import numpy as np
import pandas as pd


#!pip install twitter

from twitter import Twitter
from twitter import OAuth


apikey='LmWo260maj5KsmP3wnigGiymR'
apisecretkey='wdFhGB3XV79csLvSI57R1OFavsXNntbdtmlJzy2spNdMIFbnxn'
accesstoken='4012083173-pdPffs50tApeBURWR9QQt22rlhEp0sdEaCFwBvR'
accesstokensecret='PVwr62zsdUF0QQpcRMkPDBLxJ4HhAG4Cjccy49GwPv8pK'

oauth = OAuth(accesstoken,accesstokensecret,apikey,apisecretkey)
api = Twitter(auth=oauth)
help(api)

#lets look at whats trending around the world
t_loc = api.trends.available()
print(t_loc)

from pandas.io.json import json_normalize

df_loc=json_normalize(t_loc)
df_loc.country.value_counts()

dfNew=df_loc[df_loc['name'].str.contains('New')]
ny=dfNew.loc[dfNew.name=='New York','woeid']

dfNew1=df_loc[df_loc['name'].str.contains('D')]

#For conditions, we use loc and not iloc

#It gives an error because ny is series, api needs integer
ny_trend = api.trends.place(_id=ny)

type(ny)
ny.values
ny.values[0]
ny_trend = api.trends.place(_id=ny.values[0])
#Everything that comes from teitter api comes as JSON object. Thats why, ny_trend 
#is JSON object

ny2 = dfNew.loc[373,'woeid']
#We didnt do any conditional slicing and thats the reason it returned as int
#When pandas do conditional slicing it doesnt knows how many objects will return so it creates a series
#but by using loc pandas is sure that it will just return one object


########## Saving and Reading Objects ######################
import json
with open('ny_trend.json', 'w') as outfile:
    json.dump(ny_trend, outfile)

# Getting back the objects:
with open('ny_trend.json') as json_data:
    ny_trend_example = json.load(json_data)

############################################################

dfny=json_normalize(ny_trend)
type(dfny.trends)
dfny.trends.shape

dfny.trends.values
dfny['trends'].values

dfny.loc[0,'trends']

############ Series example #############
s=pd.Series(['ny','nj','ct','tx'])
s.values[0]

dftrends=json_normalize(dfny.trends.values[0])
#Another way of doing it
dftrends=json_normalize(dfny.loc[0,'trends'])

#to pickle is used to save pandas table, extension of this file is .pkl
dftrends.to_pickle('dftrends.pkl')
#To read pickle table use pd.read_pickle
batman = pd.read_pickle('dftrends.pkl')

dftrends.sort_values('tweet_volume',ascending=False,inplace=True)
dftrends.head(5)
#Another way and just to show two specified columns
dftrends.nlargest(5,'tweet_volume')[['name','tweet_volume']]
#One more method:
tt=dftrends.sort_values('tweet_volume',ascending=False).head(5)

api.statuses.update(status="Their is an invasion at the border, someone get Jon Snow!!!")
mytweets=api.statuses.home_timeline()



dfmyt=json_normalize(mytweets)
dfmyt.to_pickle('dfmyt.pkl')

dfmyt=pd.read_pickle('dfmyt.pkl')
dfmyt['text']

mytweets1=api.statuses.home_timeline(count=1)
dfmyt1=json_normalize(mytweets1)

#Searching tweets on prarticular trending topics
dftrends.columns
dftrends.nlargest(5,'tweet_volume')
dftrends.nlargest(5,'tweet_volume')[['name','tweet_volume']]

#To find most recent tweets about RebootX1_2020, tweet_mode is to see all 280 characters
search_result = api.search.tweets(q='RebootX1_2020',count = 100,tweet_mode='extended')


dfsr=json_normalize(search_result)
dfsr.to_pickle('dfsr.pkl')
dfsr=pd.read_pickle('dfsr.pkl')

#to find a ticker, ticker is used for stock market.
tesla_sr = api.search.tweets(q='$tsla',count = 100,tweet_mode='extended')
df_tesla = json_normalize(tesla_sr,'statuses')

twitter_sr = api.search.tweets(q='$twtr',count = 100,tweet_mode='extended')
df_twitter = json_normalize(twitter_sr,'statuses')

#to normalize inner json object without normalizing the outer json object
dfsr=json_normalize(search_result,'statuses')
dfsr1 = dfsr.loc[0]

dfst=json_normalize(dfsr.statuses.values[0])
dfst2=json_normalize(dfsr.loc[0,'statuses'])
dfst.full_text

df0=pd.DataFrame({'Value':dfst.loc[0]})
www=dfst.loc[0]
dd=dfst.iloc[0]

#
njson=api.statuses.user_timeline(screen_name="neeraj_harjani",tweet_mode='extended',count=200)
dfneeraj=json_normalize(njson)

#
tfollow=api.followers.ids(screen_name="realDonaldTrump")
dffol=json_normalize(tfollow)

dffol2=json_normalize(tfollow,'ids')
dffol2.to_pickle('dffol2.pkl')

dffol2=pd.read_pickle('dffol2.pkl')

dfst2=json_normalize(search_result,'statuses')

u = dffol2.loc[3200,0]

u0=api.users.lookup(user_id=dffol2.loc[0,0])
dfu0=json_normalize(u0)
ajson=api.statuses.user_timeline(screen_name="Abdulha23328576",tweet_mode='extended',count=200)
dfabdhu=json_normalize(ajson)

user1=api.statuses.user_timeline(id=dffol2.loc[4,0],tweet_mode='extended')

dfuser1=json_normalize(user1)

tesla_sr = api.search.tweets(q='$tsla',count = 100,tweet_mode='extended')
df_tesla = json_normalize(tesla_sr,'statuses')
df_tesla['id']
df_tesla['id'].min()
mid = df_tesla['id'].min()

mid = mid -1
tesla_sr2 = api.search.tweets(q='tsla',tweet_mode='extended',count=200, max_id=mid)
len(tesla_sr2)
df_tesla2 = json_normalize(tesla_sr2,'statuses')
df_tesla2['id'].max()

mid=0
dfall = pd.DataFrame()
for i in range(32):
    if i==0:
        tesla_sr = api.search.tweets(q='$tsla',count = 100,tweet_mode='extended')    
    else:
        tesla_sr = api.search.tweets(q='$tsla',count = 100,tweet_mode='extended',max_id=mid)
        
    df_tesla = json_normalize(tesla_sr,'statuses')
    dfall = pd.concat([dfall,df_tesla],ignore_index=True)
    mid = dfall['id'].min()
    mid = mid -1
        






#######################  textblob ################################
!pip install textblob
!python -m textblob.download_corpora



