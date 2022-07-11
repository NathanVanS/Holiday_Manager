from datetime import date, datetime
import json
from config import holidayloc
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass

holidaylist = []
def display_main_menu():
    print("""
1.) Add a Holiday
2.) Remove a Holiday
3.) Save Holiday List
4.) View Holidays
5.) Exit""")

def get_input(display): # take display phrase (string) displays it and returns input
    the_input = input(display)
    return the_input

def confirm_deny(input, confirm, deny): # checks for y/n anything else reprimand and repeat
    if input == "y":
        return confirm
    if input == "n":
        return deny
    else:
        print("Not a valid entry!")
        return confirm_deny(input,confirm, deny)

def display_title(title): #title plus = signs
    print(title)
    for i in title:
        print("=", end="")

def getHTML(url):
    response = requests.get(url)
    return response.text

def initialize():
    read_json(holidayloc)
    scrapeHolidays()
# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
@dataclass
class Holiday:
    theHoliday: str
    theDate: date

    def __str__(self, holiday, date):
        print("appended string") 
        return '(%s, %s, %s)' % (self, holiday, date)
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
@dataclass
class HolidayList:
    innerHolidays: list
   
def addHoliday(holidayObj): #needs objectype check
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday
    try:
        print(type(holidayObj))
        HolidayList.innerHolidays.append(holidayObj)
        print("Success:\n{} has been added to the holiday list." .format(holidayObj))
    except:
        print("Incorrent object reference.")

def scrapeHolidays(): # 560ish/year gets every holiday in a year, and writes it to holidays list, gets and formats into finaldate list for 5 total years
    # DONE Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
    # DONE Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
    # Check to see if name and date of holiday is in innerHolidays array
    # Add non-duplicates to innerHolidays
    # Handle any exceptions.
    year = 2022
    holidays = []
    finaldate = []
    thedate = {}
    holiday = {}
    for d in range(-2, 3):
        currentyear = year + d
        html = getHTML("https://www.timeanddate.com/holidays/us/{}".format(currentyear))
        soup = BeautifulSoup(html,'html.parser')
        table = soup.find('table',attrs = {'class':'table table--left table--inner-borders-rows table--full-width table--sticky table--holidaycountry'})
        for row in table.find_all('tr', id=lambda x: x and 'tr' in x):
            cells = row.find_all_next('td') 
            holiday['name'] = cells[1]
            holidays.append(holiday)
            day = row.find_all_next('th')
            daystring = day[0].string
            thedate['year'] = currentyear
            thedate['month'] = datetime.strptime(daystring.split(' ')[0], '%b').month
            thedate['day'] = int(daystring.split(' ')[1])
            megasuperdate = date(thedate['year'],thedate['month'],thedate['day'])
            finaldate.append(megasuperdate)
            
def removeHoliday(HolidayName, Date):
        # Find Holiday in innerHolidays by searching the name and date combination. use find holiday
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday
    print("Success:\n{} ({}) has been removed from the holiday list." .format(HolidayName, Date))

def read_json(filelocation): #reads to json into dictionary holidaydict
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.
    file = open(filelocation)
    holidaydict  = json.load(file)
    # for a in holidaydict['holidays']:
    #     print(a) should be addholiday when completed
    file.close

def findHoliday(HolidayName, Date):
    #find Holiday in innerHolidays
    #return Holiday
    print('stuff')

    return(Holiday)
           
def numHolidays():
        # Return the total number of holidays in innerHolidays
    print('stuff')   
    
def filter_holidays_by_week(year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays
        filter(lambda year, week_number, )
    print('stuff')

def displayHolidaysInWeek(holidayList):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.
    print('stuff')

def getWeather(weekNum):
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.
    print('stuff')

def viewCurrentWeek():
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
    print('stuff')

def main():
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. DONE Display User Menu (Print the menu)
    # 5. DONE Take user input for their action based on Menu and check the user input for errors
    # 6. DONE Run appropriate method from the HolidayList object depending on what the user input is
    # 7. DONE Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 
    display_title("Holiday Menu")
    x = get_input(display_main_menu())
    
    holidaylist = HolidayList()
    holiday = []
    theDate = []
    leave = None
    weather = None

    if x == "1":
        display_title("Add a Holiday")
        holiday = Holiday(get_input("\nHoliday:"),get_input("Date:"))
        addHoliday(holiday)
    elif x == "2":
        display_title("Remove a Holiday")
        removeHoliday(get_input("Holiday Name:"), get_input("Participant Name:"))
    elif x == "3":
        display_title("Save Holidays")
        save = confirm_deny(get_input("Are you sure you want to save your changes? [y/n]:"), "Changes have been saved.", "Changes have not been saved")
        main()
    elif x == "4":
        display_title("View Holidays")
        theDate = get_input("Which year?:")
        theWeek = get_input("Which Week?")
        weather = confirm_deny(get_input("Would you like to see this week's weather? [y/n]:"), "Goodbye!", "Going back to main menu.")  #needs adjusting
    elif x == "5":
        display_title("Exit")
        leave = confirm_deny(get_input("Any unsaved changes will be lost.\nAre you sure you want to exit? [y/n]"), "Goodbye!", "Going back to main menu.")
        if leave == "Going back to main menu.":
            main()
        else:
            # file.close()
            quit()
    else:
        print("Incorrect Value.")
        main()
    

if __name__ == "__main__":
    main();
# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code