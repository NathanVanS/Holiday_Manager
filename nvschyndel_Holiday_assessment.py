from datetime import date, datetime
import json
# from pandas import read_json # what the?
from config import holidayloc
from config import finalholidaysloc
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass

#these are my add ons
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

@dataclass
class Holiday:
    # -------------------------------------------
    # Modify the holiday class to 
    # 1. Only accept Datetime objects for date.
    # 2. You may need to add additional functions
    # 3. You may drop the init if you are using @dataclasses
    # --------------------------------------------
    theHoliday: str
    theDate: date

    def __str__ (self):
        return f'{self.theHoliday}, ({self.theDate})'

@dataclass
class HolidayList: #
    # -------------------------------------------
    # The HolidayList class acts as a wrapper and container
    # For the list of holidays
    # Each method has pseudo-code instructions
    # --------------------------------------------
    innerHolidays: list

    def __contains__(self, anotherholiday):
        if anotherholiday in self:
            return True 

    def scrapeHolidays(self): # DONE 560ish/year gets every holiday in a year, prevents duplicates and writes it to innerHolidays
        # DONE Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # DONE Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # DONE Check to see if name and date of holiday is in innerHolidays array
        # DONE Add non-duplicates to innerHolidays
        # Handle any exceptions.
        year = 2022
        thedate = {}

        for d in range(-2, 3):
            currentyear = year + d
            html = getHTML("https://www.timeanddate.com/holidays/us/{}".format(currentyear))
            soup = BeautifulSoup(html,'html.parser')
            table = soup.find('table',attrs = {'class':'table table--left table--inner-borders-rows table--full-width table--sticky table--holidaycountry'})

            for row in table.find_all('tr', id=lambda x: x and 'tr' in x):
                cells = row.find('a') 
                holiday= cells.text
                day = row.find_all_next('th')
                daystring = day[0].string
                thedate['year'] = currentyear
                thedate['month'] = datetime.strptime(daystring.split(' ')[0], '%b').month
                thedate['day'] = int(daystring.split(' ')[1])
                megasuperdate = date(thedate['year'],thedate['month'],thedate['day'])
                holidayobject = Holiday(holiday, megasuperdate)
                if holidayobject not in self.innerHolidays:
                    self.addHoliday(holidayobject) #may need another self
        #at the end currentlist contains all objects created from scraping and innerlist has been written to  

    def read_json(self, filelocation): #takes from passed filelocation and adds to list
                # Read in things from json file location
                # Use addHoliday function to add holidays to inner list.
        with open(filelocation) as json_file: 
            holidaydict = json.load(json_file)
            for a in holidaydict['holidays']:
                thename = a['name']
                thedate = a['date']
                thedate = datetime.strptime(thedate, "%Y-%m-%d")
                self.addHoliday(Holiday(thename, thedate))

    def finaljson(self, filelocation):
        with open(filelocation) as json_file: #doesnt finish with adding to innerlist errors
            holidaydict = json.load(json_file)
            for a in holidaydict:
                thename = a['theHoliday']
                thedate = a['theDate']
                thedate = datetime.strptime(thedate, "%Y-%m-%d")
                self.addHoliday(Holiday(thename, thedate))

    def readclean(self): #take in the JSONS to inner list remove duplicates empty the final_holiday.json rewrite to it
        holidaylist.read_json(holidayloc)
        holidaylist.finaljson(finalholidaysloc)
        holidaylist.scrapeHolidays()
        #open(finalholidaysloc, "w").close() This should clear final_holidays.json if needed
        self.innerHolidays = [i for n, i in enumerate(self.innerHolidays) if i not in self.innerHolidays[n + 1:]] # eliminate dupes

    def writetojson(self):
        listodictionaryholidays = [holidaylist.__dict__ for holidaylist in self.innerHolidays] 
        with open (finalholidaysloc, "w") as file: #should create it if does not exist
            json.dump(listodictionaryholidays, file, default=str)
            file.close     

    def removeHoliday(self, HolidayName, Date): #DONE
            # Done Find Holiday in innerHolidays by searching the name and date combination. use find holiday
            # DONE remove the Holiday from innerHolidays
            # DONE inform user you deleted the holiday
        result = self.findHoliday(HolidayName, Date)
        if result in self.innerHolidays:
            self.innerHolidays.remove(result)
            print("Success:\n{} ({}) has been removed from the holiday list." .format(HolidayName, Date))
        else:
            print("No matching holiday found.")

    def addHoliday(self, holidayObj): #DONE
        # DONE Make sure holidayObj is an Holiday Object by checking the type
        # DONE Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday
        if isinstance(holidayObj, Holiday):
                self.innerHolidays.append(holidayObj)
                print("Success:\n{} has been added to the holiday list." .format(holidayObj)) # print isnt happening
        else:
            print("Not the correct object type.")

    def findHoliday(self, HolidayName, Date):#DONE
            #find Holiday in innerHolidays
            #return Holiday
            #result = list(filter(lambda x: (x.theHoliday == HolidayName and x.theDate == Date), self.innerHolidays))
        if self.innerHolidays.__contains__(Holiday(HolidayName,Date)):
            for x in self.innerHolidays:
                if x.theHoliday == HolidayName and x.theDate == Date:
                    found_holiday = x
            print(found_holiday)
            return(found_holiday)
  
    def numHolidays(self): #DONE
        # Return the total number of holidays in innerHolidays
        return len(self.innerHolidays)
        
    def filter_holidays_by_week(self, year, week_number): #Done needs testing with populated list
            # DONE Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
            # Done Week number is part of the the Datetime object
            # DONE Cast filter results as list
            # DONE return your holidays
        if (year == int and week_number == int): # shouldnt be necessary will error in input should move the conversion?
            holidays = list(filter(lambda x : x.date.isocalendar()[1] == week_number and x.date.isocalendar()[0] == year, self.innerHolidays))
        else:
            print("Input numbers only.")
            holidaylist.filter_holidays_by_week(int(get_input("Which year? YYYY:")), int(get_input("Which number? ## 1-52 blank for this week:")))
        #holidays = list(filter(lambda x: (x.datetime.strptime("%Y") == year and x.datetime.strftime("%W") == week_number), self.innerHolidays)) 
        return holidays

    def displayHolidaysInWeek(self, theholidaylist): #Done needs testing with populated list
            # DONE Use your filter_holidays_by_week to get list of holidays within a week as a parameter
            # DONE formating leaves something to be desiredOutput formated holidays in the week. 
            # DONE * Remember to use the holiday __str__ method.
        #map(lambda x: print(x), holidayList)
        if len(theholidaylist)> 0:
            print(f"These are the holidays for {holidaylist[0].date.isocalendar()[0]} week {holidaylist[0].date.isocalendar()[1]}")
            for x in theholidaylist:
                print(x) #weather if possible
        else:
            print("no holidays met the specifications")
    # functionality example displayHolidaysInWeek(filter_holidays_by_week(gettheyear, gettheweek))

    #def getWeather(weekNum): opting out
            # Convert weekNum to range between two days
            # Use Try / Except to catch problems
            # Query API for weather in that week range
            # Format weather information and return weather string.
        
    def viewCurrentWeek(self): #may not be necesary
        # DONE Use the Datetime Module to look up current week and year
        # DONE Use your filter_holidays_by_week function to get the list of holidays 
        # DONE for the current week/year
        # DONE Use your displayHolidaysInWeek function to display the holidays in the week
        # Opted Out Ask user if they want to get the weather
        # Opted OutIf yes, use your getWeather function and display results
        # Opted Outif weather == "These are the holidays for this week with weather:":

        current = datetime.datetime.now()
        holidaylist.displayHolidaysInWeek(holidaylist.filter_holidays_by_week(current.strftime("%Y"), current.strftime("%U")))

def main():
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Done global Initialize HolidayList Object 
    # 2. Done Load JSON file via HolidayList read_json function
    # 3. Done Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. DONE?Create while loop for user to keep adding or working with the Calender
    # 4. DONE Display User Menu (Print the menu)
    # 5. DONE Take user input for their action based on Menu and check the user input for errors
    # 6. DONE Run appropriate method from the HolidayList object depending on what the user input is
    # 7. DONE Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 
    display_title("Holiday Menu")
    x = get_input(display_main_menu())
    #holidaylist = HolidayList([]) #instanciates variable holidaylist of the Holidaylistclass since I recur main I cant do this
    saved = False
    
    if x == "1": #DONE
        display_title("Add a Holiday")   
        holidaylist.addHoliday(Holiday(get_input("\nHoliday:"),datetime.strptime(get_input("Date YYYY-MM-DD:"), "%Y-%m-%d")))
        main()
    elif x == "2": #DONE
        display_title("Remove a Holiday")
        holidaylist.removeHoliday(get_input("\nHoliday Name:"), datetime.strptime(get_input("Date YYYY-MM-DD:"), "%Y-%m-%d"))
        main()
    elif x == "3":#Done needs checking
        display_title("Save Holidays")
        save = confirm_deny(get_input("Are you sure you want to save your changes? [y/n]:"), "Changes have been saved.", "Changes have not been saved")
        if save == "Changes have been saved.":
            saved = True
            holidaylist.writetojson()
        print(save)
        main()
    elif x == "4": #DONE int checking in filter
        display_title("View Holidays") #x.strftime("%Y")
        weather = confirm_deny(get_input("\nWould you like to see this week's weather? [y/n]: Weather currently unavailable select [n]"), "These will be the holidays for this week with weather:", "These will be the holidays for this week without the weather:")
        print(weather)
        currentweekornot = confirm_deny(get_input("\nWould you like to see this week's weather? [y/n]: Weather currently unavailable select [n]"), "These will be the holidays for this week:", "These will be the holidays for the selected year and week:")
        print(currentweekornot)
        if currentweekornot =="These will be the holidays for the selected year and week:":
            holidaylist.displayHolidaysInWeek(holidaylist.filter_holidays_by_week(int(get_input("Which year? YYYY:")), int(get_input("Which number? ## 1-52 blank for this week:"))))
        # if weather == "These are the holidays for this week with weather:":
        #     print('stuff')
            #do API weather schinanigans
    elif x == "5": #DONE
        display_title("Exit")
        leave = confirm_deny(get_input("\nAre you sure you want to exit? [y/n]"), "Goodbye!", "Going back to main menu.")
        if saved == False and leave == "Goodbye!":
            leave = confirm_deny(get_input("\nYour changes will be lost [y/n]"), "Goodbye!", "Going back to main menu.")
        else: #saved or 
            if leave == "Going back to main menu.":
                print(leave)
                main()
            else: #leave = Goodbye!
                print(leave)
                quit()
    else:
        print("Incorrect Value.")
        main()
    
if __name__ == "__main__":
    holidaylist = HolidayList([]) #instantiate
    holidaylist.readclean() # this reads both files into the list removes dupes emtpies fina_holidays and rewrites 
    main();