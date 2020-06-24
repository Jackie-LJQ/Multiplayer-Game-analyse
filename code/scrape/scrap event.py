# -*- coding: utf-8 -*-
"""
Created on Sun Apr 01 13:20:31 2020

@author: liu
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
#
def one_page(url):
    result = requests.get(url)
    #print(result.status_code)
    events = BeautifulSoup(result.content)
    for event in events.find_all("div", {"class": "table-holder"}):
        event_name.append(event.find("div", {"class": "text-ellipsis"}).text)
        location.append(event.find("span", {"class" : "smallCountry"}).select('.col-desc')[0].text)
        prize.append(event.find("td", {"class" : "col-value small-col prizePoolEllipsis"}).text)
#        time.sleep(1)
    for event in events.find_all("a", class_="a-reset small-event standard-box"):
        event_url = 'https://www.hltv.org/' + event['href']
        event_id.append(int(extract_id(event_url, 'events')))
        print(event_url)
        team_in_event, event_date = get_teams_date(event_url)
        teams.append(team_in_event)
        date.append(event_date)
        time.sleep(1)
#
def get_url(n):
    url1 = url
    return url1 + str('?offset={0}'.format(n))    

def get_teams_date(url):
    team_result, date_result = [], []
    res = requests.get(url)
    src = res.content
    team_doc = BeautifulSoup(src)
    teams = team_doc.find("div", {"class":"teams-attending grid"})
    if teams == None:
        team_result = 'Other'
    else:
        for team in teams.find_all("div", {"class":"team-name"}):
            team_url = team.find("a")['href']
            team_result.append(extract_id(team_url, 'team'))
    dates = team_doc.find("td", {"class":"eventdate"})
    date_result.append(dates.text)
    return team_result, date_result
#
def extract_id(part_url, key_word):
    if key_word in part_url:
        init = part_url.find(key_word) + len(key_word) + 1
    else:
        print('The url is invalid')
    id = '0'
    for i in range(init, 1000):
        if part_url[i].isdigit():
            id += part_url[i]
        else:
            break
    id = int(id[1:])
    return id
##
##
##
event_name = []
location = []
date = []
prize = []
teams = []
event_id = []
#
url = 'https://www.hltv.org/events/archive'
one_page(url)
#
##4050 is the num of total events web page
##you need to see the last page in hltv website to find the iterate time
##eg 'https://www.hltv.org/events/archive?offset=4050'
for i in range(50,4050,50): #4050 50
    url1 = get_url(i)
    one_page(url1)
    print(len(date)) # track how many dataset has been pulled
#
with open('eventsdata.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    for i in range(len(location)):
        row = [event_id[i], event_name[i], date[i], location[i], prize[i], teams[i]]
        writer.writerow(row)

