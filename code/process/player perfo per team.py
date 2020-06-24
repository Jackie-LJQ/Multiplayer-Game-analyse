# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 15:21:26 2020

@author: liu
"""

# =============================================================================
# find player performance in each team
# =============================================================================
from collections import defaultdict
import pandas as pd
from matplotlib import pyplot as plt
df = pd.read_csv('data/player_team_Datesplit.csv')

## filt player plays less than 20 matches in one team
df1 = df.groupby(['player_id','team_id'])['Date'].nunique().reset_index(name='Count') 
df2 = df1.where(df1.Count>20).dropna()

### merge df1 and df2 name new dataframe as 'df1'
df1 = df.merge(df2, on = ['player_id','team_id'])
df1 = df1.sort_values(['player_id','team_id'])

# find the corresponding match id for each date
df2 = pd.read_csv('data/matches.csv')
df3 = pd.DataFrame( {'Date':df2['Date'],'match_id':df2['Match ID'], 'team_id':df2['Team 1 ID']}) #match id based on Team 1
df4 = pd.DataFrame( {'Date':df2['Date'],'match_id':df2['Match ID'], 'team_id':df2['Team 2 ID']}) #match id based on Team 1
df5 = pd.concat([df3,df4]).drop_duplicates().reset_index(drop=True)
df6 = df1.merge(df5, on = ['Date','team_id']).drop_duplicates()

#find player performance in each team
df7 = pd.read_csv('data/player_match.csv')
df8 = df6.merge(df7, on = ['player_id','match_id'])
df8.to_csv('F:\grid\data\player_team_perf.csv')

