# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 08:09:18 2020

@author: liu
"""

import pandas as pd
import seaborn as sns 
from scipy import stats
import numpy as np
import statsmodels.api as sm

# =============================================================================
# Want to see if shift team frequently influences the player performance
# =============================================================================
df = pd.read_csv('F:\grid\data\player info.csv')
df['year'] = pd.to_datetime(df['Date']).dt.year
#df.drop(columns='Date')

#changetime=df[['player_id','team_id','year']].groupby(['player_id','year'])['team_id'].nunique().reset_index()
# how many year a player plays
tenure = df[['player_id','year']].groupby('player_id')['year'].nunique().reset_index()

# how many team a player was in
teams = df[['player_id','team_id']].groupby('player_id')['team_id'].nunique().reset_index()
teams=teams.rename(columns={'team_id':'team num'})
df1 = pd.merge(teams,tenure,how='inner',on='player_id')
df1['average change'] = df1['team num']/df1['year']

measure = 'deaths'
df = df[(np.abs(stats.zscore(df[measure])) < 2)].reset_index()
performance = df[['player_id',measure]].groupby('player_id').mean().reset_index()
df1 = pd.merge(df1,performance,on='player_id')
df1 = df1[['average change',measure]].groupby('average change').mean().reset_index()
sns.lmplot(x ='average change', y =measure, data = df1)


X = df1['average change']
Y = df1[measure]
X = sm.add_constant(X) # adding a constant
model = sm.OLS(Y, X).fit()
print_model = model.summary()

## the influence of changing team to player
### use the id=7 player
#df2 = df.where(df['player_id']==7).dropna()
#df2 = df2.sort_values('team_id')
##rating per team
#dfr = df2[['rating', 'team_id']].groupby('team_id').mean().reset_index()
##duration in each team
#start = df2[['team_id','Date']].groupby('team_id').min().reset_index()
#end = df2[['team_id','Date']].groupby('team_id').max().reset_index()
#duration = pd.to_datetime(end['Date']) - pd.to_datetime(start['Date'])
#dfr['duration']=duration
#dfr['start date'] = start['Date']
#dfr['end date'] = end['Date']


#
##check data https://www.hltv.org/stats/players/matches/7/Friis
#def extract_id(part_url, key_word = 'teams'):
#    if key_word in part_url:
#        init = part_url.find(key_word) + len(key_word) + 1
#    else:
#        print(part_url)
#    id = '0'
#    for i in range(init, 1000):
#        if part_url[i].isdigit():
#            id += part_url[i]
#        else:
#            break
#    id = id[1:]
#    return id
#df = pd.read_csv('data\player_url.csv')
#import numpy as np
#df1 = np.array(df)
#for i in df1:
#    if extract_id(i[0], key_word = 'matches') == '7':
#        print(i)

#df = pd.read_csv('data\matches.csv')

#