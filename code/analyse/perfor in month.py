# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 11:32:49 2020

@author: liu
"""
# =============================================================================
# player performance per team per month 
# want to see if player performance change when he stays in a team for long time
# =============================================================================
from collections import defaultdict
import pandas as pd
from matplotlib import pyplot as plt
df8 = pd.read_csv('F:\grid\data\player_team_perf.csv')
param = 'kills'
kills = df8[['player_id', 'team_id', 'Date', 'year', 'month', 'day', param]]
kills = kills.groupby(['player_id', 'team_id', 'year', 'month'])[param].mean().reset_index()
dic = defaultdict(list)
for i in range(len(kills)):
    dic[(kills.player_id[i],kills.team_id[i])].append(kills[param][i])
test1 = pd.DataFrame.from_dict(dic, orient='index')
test2 = test1.isnull().sum(axis=1)
m = len(test2.columns) - test2.median() 
test2 = test1.loc[:,0:m]
avg = test2.mean()
print(avg)
plt.plot(avg, label=param)
plt.ylabel(param)
plt.legend()
plt.show()
