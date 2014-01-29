#BRING IN LIBRARIES

import re, csv
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

def getBoxScores(soupIn):
    allLinks = soupIn.findAll('a')
    gameLinks = []
    for link in allLinks:
        if link.text == "Final":
            gameLinks.append(link['href'])
    return gameLinks

#FOR A GIVEN DATE GET ALL FOUR FACTORS FROM EACH BOX SCORE

soup = getSoup("http://www.sports-reference.com/cbb/boxscores/index.cgi?month=11&day=12&year=2010")
boxScores = getBoxScores(soup)
with open('./Output/FourFactors.csv','w') as f:
    writer = csv.writer(f)
    colHeaders = ['Date','School1','School1_Pace','School1_eFG','School1_TOV','School1_ORB','School1_FT/FGA',
                  'School1_ORTG','School2','School2_Pace','School2_eFG','School2_TOV','School2_ORB',
                  'School2_FT/FGA','School2_ORTG']
    writer.writerow(colHeaders)
    for score in boxScores[:2]:
        scoreLink = "http://www.sports-reference.com{0}".format(score)
        print scoreLink
        scoreSoup = getSoup(scoreLink)
        fourFactors = getFourFactors(scoreSoup)
        writer.writerow(fourFactors)
