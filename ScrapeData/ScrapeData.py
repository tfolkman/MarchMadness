#BRING IN LIBRARIES

import re
import datetime
import csv
import logging
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


def processdate(month, day, year):
    daysoup = getsoup("http://www.sports-reference.com/cbb/boxscores/index.cgi?month={m}&day={d}&year={y}".format(
        m=month, d=day, y=year))
    boxlinks = getboxlinks(daysoup)
    allrows = []
    logger.info('{0}_{1}_{2}'.format(year, month, day))
    for link in boxlinks:
        logger.info('\t{0}'.format(link))
        datarow = []
        boxsoup = getsoup(link)
        fourfactors = getfourfactors(boxsoup)
        for factor in fourfactors:
            datarow.append(factor)
        teamstats = getteamstats(boxsoup)
        for stat in teamstats:
            datarow.append(stat)
        allrows.append(datarow)
    return allrows

#SET UP LOG

# create logger with 'spam_application'
logger = logging.getLogger("ScrapeData")
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
ch = logging.FileHandler('ScrapeData.log')
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(ch)

#LOOP OVER ALL DATES

f = open('./Output/test.csv', 'w')
a = csv.writer(f)
a.writerow(colHeaders)

listOfDates = dateseries(startdate=datetime.datetime(2013, 11, 12))
for date in listOfDates:
    rowsFromDate = processdate(date[0], date[1], date[2])
    for row in rowsFromDate:
        a.writerow(row)
    logger.info('Written to File!')

f.close()
