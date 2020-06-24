# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 15:44:41 2020

@author: liu
"""

# =============================================================================
# See if player performance change after they change team 
# Apply discontitinuity regression
# =============================================================================
import pandas as pd
from collections import defaultdict
from rdd import rdd
from matplotlib import pyplot as plt
import statsmodels.formula.api as smf


df = pd.read_csv('F:\grid\data\player_team_perf.csv')
param = 'kills'
df1 = df[['player_id', 'team_id', 'Date', 'year', 'month', 'day', param]]
df1 = df1.groupby(['player_id', 'team_id', 'year', 'month'])[param].mean().reset_index()
dic = defaultdict(list)
for i in range(len(df1)):
    dic[(df1.player_id[i],df1.team_id[i])].append(df1[param][i])
df2 = pd.DataFrame.from_dict(dic, orient='index')
df2.index = pd.MultiIndex.from_tuples(df2.index, names=['player_id', 'team_id'])
df2 = df2.reset_index()
helpdf = df2.groupby('player_id')['team_id'].count().reset_index()
helpdf = helpdf.rename(columns = {'team_id':'team count'})
helpdf = helpdf.where(helpdf['team count'] > 1).dropna()
df3 = df2.merge(helpdf, on=['player_id'])

y = list(df3.iloc[0][2:15]) + list(df3.iloc[1][2:12])
threshold = 0
data = pd.DataFrame({'y':y,'x':range(-12,11)})
bandwidth_opt = rdd.optimal_bandwidth(data['y'], data['x'], cut=threshold)
print("Optimal bandwidth:", bandwidth_opt)

window = rdd.truncated_data(data, 'x', bandwidth_opt, cut=threshold)
def small(size):
    if(size>=0):
        return 1
    return 0

window['small'] = window['x'].map(small)

result = smf.ols(formula = "y ~ x+small", 
                 data = window).fit()



plt.figure(num=None, figsize=(8, 3), dpi=80, facecolor='w', edgecolor='k')
plt.scatter(window.x,window.y, color="blue")
l=window[window.x<0].x.count()
plt.plot(window.x[0:l], result.predict()[0:l], '-', color="r")
plt.plot(window.x[l:], result.predict()[l:], '-', color="r")
plt.axvline(x=0,color="black", linestyle="--")
plt.title("Regression Discontinuity: Kills Before and After change team", fontsize="9")