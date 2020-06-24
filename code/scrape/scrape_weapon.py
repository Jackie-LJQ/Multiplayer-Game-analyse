# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 12:33:26 2020

@author: liu
"""


import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import csv


csv_file = open('weapon stats.csv',"w")
writer = csv.writer(csv_file, delimiter=',')
writer.writerow(['player_id', 'player_name', 'weapon', 'freq'])

df = pd.read_csv('F:\grid\data\weapon_url.csv')
for url in df['weapon_url']:
    response = requests.get(url)
    weapon_page = BeautifulSoup(response.content, 'html')
    player_id, player_name = url[42:].split('/')
#    print(url)
    for weapons in weapon_page.find_all("div",{"class":"stats-row"}):
        weapon = weapons.div.contents[1].string
        freq = weapons.div.next_sibling.next_sibling.string
        writer.writerow([player_id, player_name, weapon, freq])
    time.sleep(0.3)
csv_file.close()
