# import datetime
import datetime
# from datetime import datetime
# from datetime import date
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass



# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
@dataclass
class Holiday:
    name: str
    date: datetime.date

    # def __init__(self,name, date):
    #     #Your Code Here
    #     pass        
    
    def __str__ (self):
        return f"{self.name} ({self.date})"
        # String output
        # Holiday output when printed.
        pass
          
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class HolidayList:
    def __init__(self):
        self.innerHolidays = []

    def addHoliday(self, holidayObj):
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday
        self.innerHolidays.append(holidayObj)
#         print(hday_list.innerHolidays)

    def findHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays
        # Return Holiday
        pass
    
    def removeHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        rem = {}
        rem["name"] = HolidayName
        rem["date"] = Date
        rem = Holiday(rem["name"], rem["date"])
        
        for i in range(len(self.innerHolidays)):
            if self.innerHolidays[i]==rem:
                print("You deleted " + HolidayName + " successfully!")
                self.innerHolidays.pop(i)
        if rem not in self.innerHolidays:
            print("Invalid holiday.\nIts possible we don't have that holiday or you input the information incorrectly.\nPlease double check the name and date and try again.")

        
        # inform user you deleted the holiday

    
    def read_json(self, filelocation):
        global holidayjson
        global hday
#         global holiday
        # Read in things from json file location
        with open(filelocation, 'r') as f:
#             self.innerHolidays = json.load(f)
#         return self.innerHolidays
            holidayjson = json.load(f)
            for holiday in holidayjson["holidays"]:
                hday = Holiday(holiday["name"], holiday["date"])
                self.addHoliday(hday)
        # Use addHoliday function to add holidays to inner list.
        


    def save_to_json(self, filelocation):
        fn = 'allholidays.json'
        dict_translate = {"holidays":[{"name": h.name, "date": h.date} for h in self.innerHolidays]}
        with open(fn, 'w') as f:
            json.dump(dict_translate, f, indent=4, default=str)
        # Write out json file to selected file.

        
    def scrapeHolidays(self):
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        days = []
        dates = []
        years = ['2020', '2021', '2022', '2023', '2024']
        for year in years:
            url_list = [f'https://www.timeanddate.com/holidays/us/{year}']
            for i in range(len(url_list)):
                r = requests.get(url_list[i])
                soup = BeautifulSoup(r.text, 'html.parser')
                table = soup.find('table', attrs = {'id':'holidays-table'})
                body = table.find('tbody')
                rows = body.find_all('tr')
                for row in rows:
                    daywrappers = row.find_all('td')
                    datewrappers = row.find_all('th')
                    if datewrappers != []:
                        date = datewrappers[0].get_text()
                        date_string = f"{date}, {year}"
                        fdatetime = datetime.datetime.strptime(date_string, "%b %d, %Y")
                        fdate = fdatetime.date()
                        dates.append(fdate)
        #                 print(fdate)
                    if daywrappers != []:
                        dayname = daywrappers[1].get_text()
        #                 print(dayname)
                        days.append(dayname)

        scraped = zip(days, dates)
        scrapedlist = (list(scraped))
        for i in scrapedlist:
            hday_list.addHoliday(Holiday(i[0], i[1]))





        # hday_list.addHoliday(day)
                # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
                # Check to see if name and date of holiday is in innerHolidays array
                # Add non-duplicates to innerHolidays
                # Handle any exceptions.


    def numHolidays(self):
        global lenHolidays
        # Return the total number of holidays in innerHolidays
        lenHolidays = len(self.innerHolidays) 
        return lenHolidays
    
    def filter_holidays_by_week(self, year, week_number):
        global holidayList
        global weekdateList
        weekdateList = []
        holidayList = []
        for i in self.innerHolidays:
            idate = i.date
            try:
                weekdate = idate.isocalendar()
            except:
                exceptYear = (i.date[0:4])
                exceptMonth = (i.date[5:7])
                exceptDay = (i.date[8:10])
                exceptDate = datetime.date(int(exceptYear),int(exceptMonth),int(exceptDay))
                weekdate = exceptDate.isocalendar()
            weekdateList.append(weekdate)
            yr, wk, wkday = weekdate
            if yr == int(year) and wk == int(week_number) and wkday in range(1,8):
                holidayList.append(i)
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays
        self.displayHolidaysInWeek(holidayList)

        
# for i in range(len(hday_list.innerHolidays)):
#     print(hday_list.innerHolidays[i])
    

    def displayHolidaysInWeek(self, holidayList):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.
        for holiday in holidayList:
            print(str(holiday))


    def viewCurrentWeek(self):
        # Use the Datetime Module to look up current week and year
        today = datetime.date.today().isocalendar()
        tyr, twk, twkday = today
        self.filter_holidays_by_week(tyr, twk)

        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
        pass
 

import datetime

def main():
    global done
    global lenlist
    global hday_list
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    hday_list = HolidayList()
    
    
#     lenlist = hday_list.numHolidays()
#     lenlist = str(len(hday_list.innerHolidays))
    
    # 2. Load JSON file via HolidayList read_json function
    hday_list.read_json('holidays.json') 
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    hday_list.scrapeHolidays() 
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    done = False
    while done == False:
        done = Title()

    
    
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 
    pass

def Title():
    global done
    global lenlist
    greeting = print(f"\nWelcome to the Holidays App!\n==============\nThere are {(len(hday_list.innerHolidays))} holidays currently stored.")
    greeting
    uinput = input("\nHoliday Menu\n===============\n1. Add a Holiday\n2. Remove a Holiday\n3. Save Holiday List\n4. View Holidays\n5. Exit\nPlease input an option from 1-5.\n")
    if uinput == "1":
        addHday()
    elif uinput == "2":
        remHday()
    elif uinput == "3":
        saveList()
    elif uinput == "4":
        viewHolidays()
    elif uinput == "5":
        leave = input("Are you sure you want to exit? All unsaved changes will be lost!\n1. Yes\n2. No\n")
        if leave == "1":
            print("Goodbye!")
            done = True
            return True
        elif leave == "2":
            Title()
        else:
            print("Not a valid input.")
            Title()
    else:
        print("Not a valid input.")
        Title()


def addHday():
    print("\n1. Add a Holiday\n===============")
    validDate = False
    addHolidayName = input("Please input the Holiday's name.\n")
    while validDate == False:
        addHolidayDateYear = input(f"Please input the year of the Holiday in yyyy format.\n(Eg. For Dec 3, 2022 this input would be '2022')\n")
        addHolidayDateMonth = input(f"Please input the month of the Holiday in number format.\n(Eg. For Dec 3, 2022 this input would be '12' and for January 12, 2022, this input would be '1')\n")
        addHolidayDateDay = input(f"Please input the day of the Holiday in number format.\n(Eg. For Dec 3, 2022 this input would be '3' and for January 12, 2022, this input would be '12')\n")
        try:
            addHolidayDate = datetime.date(int(addHolidayDateYear), int(addHolidayDateMonth), int(addHolidayDateDay))           
            validDate = True
            break
        except:
            print("That didn't work. Please check the format instructions and try again.")
            continue
    addHolidayObj = Holiday(addHolidayName, addHolidayDate)
    hday_list.addHoliday(addHolidayObj)
    print(f"Successfully added {addHolidayName}.")
    contaddHday = input("Would you like to add another holiday?\n1. Yes\n2. No\n")
    if contaddHday == "1":
        addHday()
    elif contaddHday == "2":
        Title()
        
        
        
def remHday():
    print("\n2. Remove a Holiday\n===============")
    validDate = False
    remHolidayName = input("Please input the Holiday's name.\n")
    while validDate == False:
        remHolidayDateYear = input(f"Please input the year of the Holiday in yyyy format.\n(Eg. For Dec 3, 2022 this input would be '2022')\n")
        remHolidayDateMonth = input(f"Please input the month of the Holiday in number format.\n(Eg. For Dec 3, 2022 this input would be '12' and for January 12, 2022, this input would be '1')\n")
        remHolidayDateDay = input(f"Please input the day of the Holiday in number format.\n(Eg. For Dec 3, 2022 this input would be '3' and for January 12, 2022, this input would be '12')\n")
        try:
            remHolidayDate = datetime.date(int(remHolidayDateYear), int(remHolidayDateMonth), int(remHolidayDateDay))           
            break
        except:
            print("That didn't work. Please check the format instructions and try again.")
            pass
    hday_list.removeHoliday(remHolidayName, remHolidayDate)
    contremHday = input("Would you like to remove another holiday?\n1. Yes\n2. No\n")
    if contremHday == "1":
        remHday()
    elif contremHday == "2":
        Title()
        
        
        
def saveList():
    print("\n3. Save Holiday List\n===============")
    print("Saving...")
    hday_list.save_to_json('allholidays.json')
    print("Saved successfully!\nLocation: allholidays.json")
    Title()
    

    

    
    
def viewHolidays():
    valid = False
    viewYear = int(input("What year?\n"))
    while viewYear not in range(2020,2025):
        viewYear = int(input("Not in range, please input year from 2020 to 2024.\n"))
    while valid == False:
        viewWeek = input("What week? (1-52, leave blank for the current week)\n")
        if viewWeek == "":
            print("Showing the current week's holidays.\n")
            valid = True
            hday_list.viewCurrentWeek()
        elif int(viewWeek) in (range(1,53)):  
            print(f"Showing week {viewWeek}'s holidays.\n")
            valid = True
            hday_list.filter_holidays_by_week(viewYear, viewWeek)
        else:
            print("Not a valid input. Input a week from 1-52 or leave blank for the current week.")
    contviewHday = input("Would you like to view another week?\n1. Yes\n2. No\n")
    if contviewHday == "1":
        viewHolidays()
    elif contviewHday == "2":
        Title()


if __name__ == "__main__":
    main();