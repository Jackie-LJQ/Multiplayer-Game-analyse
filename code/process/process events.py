# -*- coding: utf-8 -*-
"""
Created on Sun Apr 03 13:20:31 2020

@author: liu
"""


import csv
from dateutil import parser


event_id, event_name, date, location, prize, teams = ['event_id'], ['event_name'], ['date'], ['location'], ['prize'], ['teams']
with open('eventsdata.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        event_id.append(row[0])
        event_name.append(row[1])
        date.append(row[2])
        location.append(row[3])
        prize.append(row[4])
        teams.append(row[5])

   
## convert the prize format from string to decimal
## delete the last 3 meaningless characters in location
for i in range(1,len(prize)):
    if prize[i] != 'Other': # eg $3,456,789
        temp = ''
        for x in prize[i][1:].split(','):
            temp += x
        prize[i] = int(temp)
    location[i] = location[i][:-3]


## modify the data type
## convert the type of events date to 'datetime', then store again
start_date = [0] * 4050
end_date = [0] *4050
for i in range(1,4050):#4050
    temp = date[i][1:-1][1:-1] #eg 'Jun 19th - Jun 21st 2020'
    if '-' in temp:
        pos = temp.find('-') 
        start_date[i] = parser.parse(temp[:pos]+ temp[-4:])
        end_date[i] = parser.parse(temp[pos+2:])
    else:
        start_date[i] = parser.parse(temp)
        end_date[i] = parser.parse(temp)
        
start_date[0] = 'start_date'
end_date[0] = 'end_date'

with open('eventsdata.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    for i in range(len(location)):
        row = [event_id[i], event_name[i], start_date[i], end_date[i], location[i], prize[i], teams[i]]
        writer.writerow(row)