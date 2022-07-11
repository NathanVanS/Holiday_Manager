from datetime import date, datetime
from config import holidayloc
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass

# file = open(holidayloc)
# HolidayList  = json.load(file)
# print(type(HolidayList))
# for a in HolidayList['holidays']:
#         print(a)

# file.close
@dataclass
class Holiday:
    theHoliday: str
    theDate: date

    def __str__(self, holiday, date):
        print("appended string") 
        return '(%s, %s, %s)' % (self, holiday, date)

@dataclass
class HolidayList:
    innerHolidays: list

def getHTML(url):
    response = requests.get(url)
    return response.text

def addHoliday(holidayObj):
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday
    print(type(holidayObj))
    
html = getHTML("https://www.timeanddate.com/holidays/us/2022")
soup = BeautifulSoup(html,'html.parser')
table = soup.find('table',attrs = {'class':'table table--left table--inner-borders-rows table--full-width table--sticky table--holidaycountry'})
holidays = []
finaldate = []
onedict = {}
year = 2022
for row in table.find_all('tr', id=lambda x: x and 'tr' in x):
    cells = row.find_all_next('td') 
    holiday = {}
    holiday['name'] = cells[1]
    holidays.append(holiday)
    day = row.find_all_next('th')
    thedate = {}
    daystring = day[0].string
    thedate['year'] = year
    thedate['month'] = datetime.strptime(daystring.split(' ')[0], '%b').month
    thedate['day'] = int(daystring.split(' ')[1])
    megasuperdate = date(thedate['year'],thedate['month'],thedate['day'])
    finaldate.append(megasuperdate)
for a in range(0, len(holidays)):  
    print(a)
    print(holidays[a], finaldate[a])
    print(Holiday(holidays[a], finaldate[a]))
            