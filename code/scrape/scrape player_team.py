# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 17:05:32 2020

@author: liu
"""

import requests
from bs4 import BeautifulSoup
import numpy as np
import csv
import time
#
url = 'https://www.hltv.org/stats/players?minMapCount=1000'
result = requests.get(url)
src = result.content
player_page = BeautifulSoup(src, 'html')
players = player_page.find_all("td", {"class": "playerCol"})

player_url = []

for player in players:
    part_text = player.find("a")["href"]
    text = 'https://www.hltv.org'+ part_text[:15]+'matches/'+part_text[15:]
    print(text)
    player_url.append(text)

with open('player_url.csv', 'w', newline = '') as csvfile:
    writer = csv.writer(csvfile)
    for row in player_url:
        writer.writerow(row)

def extract_id(part_url, key_word = 'teams'):
    if key_word in part_url:
        init = part_url.find(key_word) + len(key_word) + 1
    else:
        print(part_url)
    id = '0'
    for i in range(init, 1000):
        if part_url[i].isdigit():
            id += part_url[i]
        else:
            break
    id = id[1:]
    return id
#
date_save = ['match_date']
team_save = ['team_id']
player_save = ['player_id']

#
#
for i in range(len(player_url)):
    url = player_url[i]
    player_id = extract_id(url, key_word = 'matches')
    result = requests.get(url)
    src = result.content
    player_page = BeautifulSoup(src,'html')
    matches = player_page.find_all("tr" , {"class":"group-1 first"})
    for t in matches:
        date = t.find("div", {"class":"time"}).text
        date_save.append(date)
        team_text = t.find("div", {"class":"gtSmartphone-only"}).find("a")["href"]
        team_save.append(extract_id(team_text,key_word = 'teams'))
        player_save.append(player_id)
#        print(date)
#        print(team_text)
    matches = player_page.find_all("tr" , {"class":"group-2 first"})
    for t in matches:
        date = t.find("div", {"class":"time"}).text
        date_save.append(date)
        team_text = t.find("div", {"class":"gtSmartphone-only"}).find("a")["href"]
        team_save.append(extract_id(team_text))
        player_save.append(player_id)
#        print(date)
#        print(player_id)
    print(url)
    time.sleep(0.5)

date_save = np.array(date_save)
player_save = np.array(player_save)
team_save = np.array(team_save)
save = np.vstack((player_save, team_save, date_save))
save = save.T

with open('player_team.csv', 'w', newline = '') as csvfile:
    writer = csv.writer(csvfile)
    for row in save:
        writer.writerow(row)