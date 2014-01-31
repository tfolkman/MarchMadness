#BRING IN LIBRARIES

import re, csv, datetime
from urllib2 import urlopen
import pandas as pd
from bs4 import BeautifulSoup

#FUNCTION TO GET SOUP FROM WEBSITE

def getSoup(website):
    r = urlopen(website)
    return BeautifulSoup(r)

#FUNCTION TO EXTRACT FOUR FACTORS FROM A SOUP

def getFourFactors(soupIn):
    dataRow = []
    table = soupIn.find('table', {'id': 'four_factors'})
    date = soupIn.find('a', {'href': re.compile('/cbb/boxscores/index.cgi?.*')})
    tableRows = table.findAll('td')
    dataRow.append(date.text)
    for value in tableRows:
        dataRow.append(value.text)
    return dataRow

#FUNCTION TO GET LIST OF BOX SCORES ON A PAGE

def getBoxLinks(soupIn):
    allLinks = soupIn.findAll('a')
    gameLinks = []
    for link in allLinks:
        if link.text == "Final":
            gameLinks.append("http://www.sports-reference.com{0}".format(link['href']))
    return gameLinks

#FOR A GIVEN DATE GET ALL FOUR FACTORS FROM EACH BOX SCORE

def processDate(linkIn):
    soup = getSoup(linkIn)
    boxScores = getBoxScores(soup)
    with open('./Output/FourFactors.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(colHeaders)
        for score in boxScores:
            scoreLink = "http://www.sports-reference.com{0}".format(score)
            print scoreLink
            scoreSoup = getSoup(scoreLink)
            fourFactors = getFourFactors(scoreSoup)
            writer.writerow(fourFactors)

#CREATE SERIES OF DATES

def dateSeries(startDate=datetime.datetime(2010,11,12),endDate=datetime.datetime.today() - datetime.timedelta(days=1)):
    timeDelta = datetime.timedelta(days=1)
    days = []
    while startDate < endDate:
        days.append([startDate.strftime('%m'),startDate.strftime('%d'),startDate.strftime('%Y')])
        startDate += timeDelta
    return days

#GET TEAM STATS

def getTeamStats(soupIn):
    teamTables = soupIn.findAll('tr', {'class': 'bold_text stat_total'})
    otherStats = []
    for table in teamTables:
        stats = table.findAll('td')
        for stat in stats:
            otherStats.append(stat.renderContents().strip())
    return otherStats

#COLUMN HEADERS

colHeaders = ['Date','School1','School1_Pace','School1_eFG%','School1_TOV%','School1_ORB%','School1_FT/FGA',
              'School1_ORTG','School2','School2_Pace','School2_eFG%','School2_TOV%','School2_ORB%',
              'School2_FT/FGA','School2_ORTG','School1_Type','School1_MP','School1_FG','School1_FGA','School1_FG%',
              'School1_2P',
              'School1_2PA','School1_2P%','School1_3P','School1_3PA','School1_3P%','School1_FT','School1_FTA',
              'School1_FT%','School1_ORB','School1_DRB','School1_TRB','School1_AST','School1_STL','School1_BLK',
              'School1_TOV','School1_PF','School1_PTS','School2_Type','School2_MP','School2_FG','School2_FGA','School2_FG%',
              'School2_2P',
              'School2_2PA','School2_2P%','School2_3P','School2_3PA','School2_3P%','School2_FT','School2_FTA',
              'School2_FT%','School2_ORB','School2_DRB','School2_TRB','School2_AST','School2_STL','School2_BLK',
              'School2_TOV','School2_PF','School2_PTS']

#PROCESS A DATE

month = 1
year = 2014
day = 29

fileOut = open("./Output/{y}_{m}_{d}.csv".format(y=year,m=month,d=day),'w')
writeFileOut = csv.writer(fileOut)
writeFileOut.writerow(colHeaders)
daySoup = getSoup("http://www.sports-reference.com/cbb/boxscores/index.cgi?month={m}&day={d}&year={y}".format(m=month,d=day,y=year))
boxLinks = getBoxLinks(daySoup)
for link in boxLinks[:2]:
    dataRow = []
    boxSoup = getSoup(link)
    fourFactors = getFourFactors(boxSoup)
    for factor in fourFactors:
        dataRow.append(factor)
    teamStats = getTeamStats(boxSoup)
    for stat in teamStats:
        dataRow.append(stat)
    print link
    writeFileOut.writerow(dataRow)
fileOut.close()
