from datetime import date, datetime
from time import strptime
from typing_extensions import Self
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

# @dataclass
# class Holiday:
#     theHoliday: str
#     theDate: date

#     def __str__(self, holiday, date):
#         print("appended string") 
#         return '(%s, %s, %s)' % (self, holiday, date)

# @dataclass
# class HolidayList:
#     innerHolidays: list

# holidaylist = HolidayList(Holiday)

# def getHTML(url):
#     response = requests.get(url)
#     return response.text

# def remove_dups_list(items):# removes duplicates from the list sent in by changing to set then back
#     return list(set(items))

# def addHoliday(holidayObj): #DONE?
#         # Make sure holidayObj is an Holiday Object by checking the type
#         # Use innerHolidays.append(holidayObj) to add holiday
#         # print to the user that you added a holiday
#     try:
#         print(type(holidayObj))
#         holidaylist.append(holidayObj)
#         print("Success:\n{} has been added to the holiday list." .format(holidayObj)) # printisnt happening
#     except:
#         print("Incorrent object reference.")
    
# html = getHTML("https://www.timeanddate.com/holidays/us/2022")
# soup = BeautifulSoup(html,'html.parser')
# table = soup.find('table',attrs = {'class':'table table--left table--inner-borders-rows table--full-width table--sticky table--holidaycountry'})
# def scrapeHolidays():
#     year = 2022
#     thedate = {}
#     currentlist = []
#     for d in range(-2, 3):
#         currentyear = year + d
#         html = getHTML("https://www.timeanddate.com/holidays/us/{}".format(currentyear))
#         soup = BeautifulSoup(html,'html.parser')
#         table = soup.find('table',attrs = {'class':'table table--left table--inner-borders-rows table--full-width table--sticky table--holidaycountry'})

#         for row in table.find_all('tr', id=lambda x: x and 'tr' in x):
#             cells = row.find('a') 
#             holiday= cells.text
#             day = row.find_all_next('th')
#             daystring = day[0].string
#             thedate['year'] = currentyear
#             thedate['month'] = datetime.strptime(daystring.split(' ')[0], '%b').month
#             thedate['day'] = int(daystring.split(' ')[1])
#             megasuperdate = date(thedate['year'],thedate['month'],thedate['day'])
#             holidayobject = Holiday(holiday, megasuperdate)
#             if holidayobject not in currentlist:
#                 currentlist.append(holidayobject)
#     holidaylist.innerHolidays.extend(currentlist)