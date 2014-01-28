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
    table = soupIn.find('table', {'id': 'four_factors'})
    date = soupIn.find('a', {'href': re.compile('/cbb/boxscores/index.cgi?.*')})
    tableRows = table.findAll('td')
    d = {'Date' : [date.text], 'School1': [tableRows[0].text], 'School1_Pace' : [tableRows[1].text],
         'School1_eFG' : [tableRows[2].text],'School1_TOV' : [tableRows[3].text], 'School1_ORB' : [tableRows[4].text],
         'School1_FT/FGA' : [tableRows[5].text],'School1_ORTG' : [tableRows[6].text], 'School2': [tableRows[7].text],
         'School2_Pace' : [tableRows[8].text], 'School2_eFG' : [tableRows[9].text],'School2_TOV' : [tableRows[10].text],
         'School2_ORB' : [tableRows[11].text], 'School2_FT/FGA' : [tableRows[12].text],'School2_ORTG' : [tableRows[13].text]}
    return d


soup = getSoup("http://www.sports-reference.com/cbb/boxscores/2014-01-26-arizona.html")
fourFactors = getFourFactors(soup)
print(pd.DataFrame(fourFactors))
