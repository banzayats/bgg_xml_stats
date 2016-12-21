# -*- coding: utf-8 -*-
import csv
import operator
import xml.etree.cElementTree as ET
import urllib2

end = False
api_link = 'https://boardgamegeek.com/xmlapi2/plays'
user = 'banzayats'
mindate='2016-01-01'
maxdate='2016-12-31'
page = 1
result = []
summary = {}

while not end:
    url = '{0}?username={1}&mindate={2}&maxdate={3}&page={4}'.format(api_link, user, mindate, maxdate, page)
    tree = ET.ElementTree(file=urllib2.urlopen(url))
    plays = tree.getroot()
    if len(plays) < 100:
        end = True
    for play in plays.findall(".//play[@quantity='1']"):
        length = play.attrib['length']
        date = play.attrib['date']
        location = play.attrib['location']
        name = play[0].attrib['name'].encode("utf-8")
        players = len(play.find('players').findall('player'))
        if name in summary.keys():
            summary[name] += int(length)
        else:
            summary[name] = int(length)
        result.append([name, length, date, location, players])
    page += 1

sorted_summary = sorted(summary.items(), key=operator.itemgetter(1))

with open('result.csv', 'wb') as f:
    wr = csv.writer(f)
    wr.writerow(["Game title", "Length", "Date", "Location", "Players"])
    for row in result:
        wr.writerow(row)

with open('summary.csv', 'wb') as f:
    wr = csv.writer(f)
    wr.writerow(["Game title", "Plays"])
    for row in sorted_summary:
       wr.writerow(row)


