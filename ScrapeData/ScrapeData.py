#BRING IN LIBRARIES

import re
import csv
import datetime
from urllib2 import urlopen
from bs4 import BeautifulSoup

#FUNCTION TO GET SOUP FROM WEBSITE


def getsoup(website):
    r = urlopen(website)
    return BeautifulSoup(r)

#FUNCTION TO EXTRACT FOUR FACTORS FROM A SOUP


def getfourfactors(soupin):
    datarow = []
    table = soupin.find('table', {'id': 'four_factors'})
    date = soupin.find('a', {'href': re.compile('/cbb/boxscores/index.cgi?.*')})
    tablerows = table.findAll('td')
    datarow.append(date.text)
    for value in tablerows:
        datarow.append(value.text)
    return datarow

#FUNCTION TO GET LIST OF BOX SCORES ON A PAGE


def getboxlinks(soupin):
    alllinks = soupin.findAll('a')
    gamelinks = []
    for link1 in alllinks:
        if link1.text == "Final":
            gamelinks.append("http://www.sports-reference.com{0}".format(link1['href']))
    return gamelinks


#CREATE SERIES OF DATES


def dateseries(startdate=datetime.datetime(2010, 11, 12),
               enddate=datetime.datetime.today() - datetime.timedelta(days=1)):
    timedelta = datetime.timedelta(days=1)
    days = []
    while startdate < enddate:
        days.append([startdate.strftime('%m'), startdate.strftime('%d'), startdate.strftime('%Y')])
        startdate += timedelta
    return days

#GET TEAM STATS


def getteamstats(soupin):
    teamtables = soupin.findAll('tr', {'class': 'bold_text stat_total'})
    otherstats = []
    for table in teamtables:
        stats = table.findAll('td')
        for stat1 in stats:
            otherstats.append(stat1.renderContents().strip())
    return otherstats

#COLUMN HEADERS

colHeaders = ['Date', 'School1', 'School1_Pace', 'School1_eFG%', 'School1_TOV%', 'School1_ORB%', 'School1_FT/FGA',
              'School1_ORTG', 'School2', 'School2_Pace', 'School2_eFG%', 'School2_TOV%', 'School2_ORB%',
              'School2_FT/FGA', 'School2_ORTG', 'School1_Type', 'School1_MP', 'School1_FG', 'School1_FGA',
              'School1_FG%', 'School1_2P', 'School1_2PA', 'School1_2P%', 'School1_3P', 'School1_3PA', 'School1_3P%',
              'School1_FT', 'School1_FTA', 'School1_FT%', 'School1_ORB', 'School1_DRB', 'School1_TRB', 'School1_AST',
              'School1_STL', 'School1_BLK', 'School1_TOV', 'School1_PF', 'School1_PTS', 'School2_Type', 'School2_MP',
              'School2_FG', 'School2_FGA', 'School2_FG%', 'School2_2P', 'School2_2PA', 'School2_2P%', 'School2_3P',
              'School2_3PA', 'School2_3P%', 'School2_FT', 'School2_FTA', 'School2_FT%', 'School2_ORB', 'School2_DRB',
              'School2_TRB', 'School2_AST', 'School2_STL', 'School2_BLK', 'School2_TOV', 'School2_PF', 'School2_PTS']

#PROCESS A DATE

month = 1
year = 2014
day = 29

fileOut = open("./Output/{y}_{m}_{d}.csv".format(y=year, m=month, d=day), 'w')
writeFileOut = csv.writer(fileOut)
writeFileOut.writerow(colHeaders)
daySoup = getsoup("http://www.sports-reference.com/cbb/boxscores/index.cgi?month={m}&day={d}&year={y}".format(m=month,
                                                                                                              d=day,
                                                                                                              y=year))
boxLinks = getboxlinks(daySoup)
for link in boxLinks[:2]:
    dataRow = []
    boxSoup = getsoup(link)
    fourFactors = getfourfactors(boxSoup)
    for factor in fourFactors:
        dataRow.append(factor)
    teamStats = getteamstats(boxSoup)
    for stat in teamStats:
        dataRow.append(stat)
    print link
    writeFileOut.writerow(dataRow)
fileOut.close()
