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


def getboxscores(soupin):
    alllinks = soupin.findAll('a')
    gamelinks = []
    for link in alllinks:
        if link.text == "Final":
            gamelinks.append(link['href'])
    return gamelinks

#FOR A GIVEN DATE GET ALL FOUR FACTORS FROM EACH BOX SCORE


def processdate(linkin):
    soup = getsoup(linkin)
    boxscores = getboxscores(soup)
    with open('./Output/FourFactors.csv', 'w') as f:
        writer = csv.writer(f)
        colheaders = ['Date', 'School1', 'School1_Pace', 'School1_eFG', 'School1_TOV', 'School1_ORB', 'School1_FT/FGA',
                      'School1_ORTG', 'School2', 'School2_Pace', 'School2_eFG', 'School2_TOV', 'School2_ORB',
                      'School2_FT/FGA', 'School2_ORTG']
        writer.writerow(colheaders)
        for score in boxscores:
            scorelink = "http://www.sports-reference.com{0}".format(score)
            print scorelink
            scoresoup = getsoup(scorelink)
            fourfactors = getfourfactors(scoresoup)
            writer.writerow(fourfactors)

#CREATE SERIES OF DATES


def dateseries(startdate=datetime.datetime(2010, 11, 12),
               enddate=datetime.datetime.today() - datetime.timedelta(days=1)):
    timedelta = datetime.timedelta(days=1)
    days = []
    while startdate < enddate:
        days.append([startdate.strftime('%m'), startdate.strftime('%d'), startdate.strftime('%Y')])
        startdate += timedelta
    return days

#####

#WORK ON GETTING THE OTHER TABLES

soup1 = getsoup("http://www.sports-reference.com/cbb/boxscores/2014-01-29-stanford.html")
teamTables = soup1.findAll('tr', {'class': 'bold_text stat_total'})
for table1 in teamTables:
    stats = table1.findAll('td')
    for stat in stats:
        print stat.renderContents().strip()

