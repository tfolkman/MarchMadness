#BRING IN LIBRARIES

import requests, re
import pandas as pd
from bs4 import BeautifulSoup

#FUNCTION TO GET SOUP FROM WEBSITE

def getSoup(website):
    r = requests.get(website)
    return BeautifulSoup(r.text)

#FUNCTION TO EXTRACT FOUR FACTORS FROM A SOUP

def getFourFactors(soupIn):
    dataRow = []
    colHeaders = ['Date','School1','School1_Pace','School1_eFG','School1_TOV','School1_ORB','School1_FT/FGA',
                  'School1_ORTG','School2','School2_Pace','School2_eFG','School2_TOV','School2_ORB',
                  'School2_FT/FGA','School2_ORTG']
    table = soupIn.find('table', {'id': 'four_factors'})
    date = soupIn.find('a', {'href': re.compile('/cbb/boxscores/index.cgi?.*')})
    tableRows = table.findAll('td')
    dataRow.append(date.text)
    for value in tableRows:
        dataRow.append(value.text)
    return dataRow

def getBoxScores(soupIn):
    allLinks = soupIn.findAll('a')
    gameLinks = []
    for link in allLinks:
        if link.text == "Final":
            gameLinks.append(link['href'])
    return gameLinks

soup = getSoup("http://www.sports-reference.com/cbb/boxscores/index.cgi?month=11&day=12&year=2010")
boxScores = getBoxScores(soup)
for i in boxScores:
    print i
