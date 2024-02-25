# Simon Ogorek & Mia Schultz 
# 2/22/24 (.csvs last updated 2/22/24)
# Find available room times given NJIT .scv file(s)

import os
import csv

#5:30PM = 17.3
def convertTo24Hour(hour,minute,AM):
    return float(int(hour) + (int(minute)*0.01) + (0 if AM or int(hour) == 12 else 12))

def findFiles(verbose):
    rootDirectoryItems = os.listdir(os.path.dirname(os.path.realpath(__file__)))
    rootDirectory = os.path.dirname(os.path.realpath(__file__))

    listOfSheets = []
    if rootDirectoryItems.__contains__("csvs"):
        if verbose:
            print("Directory found!\n")
        csvsDirectory = os.path.join(rootDirectory, "csvs")
        for csvFile in os.listdir(csvsDirectory):
            if verbose:
                print("Loading: " + csvFile)
            if csvFile[-4:] == '.csv':
                listOfSheets.append(csv.reader(open(os.path.join(csvsDirectory, csvFile)))) # encoding='cp1252'))) might be necessary, idk
        if verbose:
            print("\nAll csv files loaded!")

        return listOfSheets

    else:
        print("Directory was not found, please ensure that the file with the .csv(s) is named csvs")


spreadSheets = findFiles(True)

print("\n~~~~~~~ Find a empty room ~~~~~~~")

# Monday    M | 0
# Tuesday   T | 1
# Wednesday W | 2
# Thursday  R | 3
# Friday    F | 4

weekdayRange = ""

while (len(weekdayRange) < 1):
    weekdayRange = input("\nType a weekday you would like to search for as MTWRF\n")
    weekdayRange = weekdayRange.upper()

weekdaysToCheck = ["M" if weekdayRange.__contains__("M") else "X", "T" if weekdayRange.__contains__("T") else "X",
                   "W" if weekdayRange.__contains__("W") else "X", "R" if weekdayRange.__contains__("R") else "X",
                   "F" if weekdayRange.__contains__("F") else "X"]

startTimeH  = -1
startTimeM  = -1
startTimeAM = True

endTimeH  = -1
endTimeM  = -1
endTimeAM = True

while (startTimeH < 1 or startTimeH > 12 or startTimeM < 0 or startTimeM > 59):
    startTimeAM = input("\nIs the starting time in the morning (Y/N)\n")
    startTimeH  = int(input("\nWhat hour does the event start\n")) #fix plz so the input is defended against words
    startTimeM  = int(input("\nWhat minute does the event start (30 minute increments work best)\n"))

    if (startTimeAM.upper() == "Y"):
        startTimeAM = True
    elif (startTimeAM.upper() == "N"):
        startTimeAM = False
    else:
        startTimeH = -1; #Force a reset


while (endTimeH < 1 or endTimeH > 12 or endTimeM < 0 or endTimeM > 59):
    endTimeAM = input("\nIs the ending time in the morning (Y/N)\n")
    endTimeH  = int(input("\nWhat hour does the event end\n"))  # fix so the input is defended against words
    endTimeM  = int(input("\nWhat minute does the event end (30 minute increments work best)\n"))

    if (endTimeAM.upper() == "Y"):
        endTimeAM = True
    elif (endTimeAM.upper() == "N"):
        endTimeAM = False
    else:
        endTimeH = -1;

startTime = convertTo24Hour(startTimeH, startTimeM, startTimeAM)
endTime   = convertTo24Hour(endTimeH, endTimeM, endTimeAM)

#Catch a reverse order of start/ end times
if startTime > endTime:
    temp = startTime
    startTime = endTime
    endTime = temp

locationIndex = 7

listOfRooms = []
listOfClassesOccuring = []*1
# First pass to get all the rooms
for workspaces in spreadSheets:
    for rows in workspaces:
        if rows[7] != " " and rows[7] != "" and not (listOfRooms.__contains__(rows[7])):
            listOfRooms.append(rows[7])

# Refresh the readers
spreadSheets = findFiles(False)

# second pass to grab classes that occur on the days needed
for workspaces in spreadSheets:
    for rows in workspaces:
        for days in rows[5]:
            if weekdaysToCheck.__contains__(days):
                listOfClassesOccuring.append(rows)

listOfClassesOccuring.pop(0)

# another pass to remove courses markes as closed
for course in reversed(listOfClassesOccuring):
    if course[8].capitalize().__contains__("Cancelled") or course[8].capitalize().__contains__("Closed"):
        listOfClassesOccuring.remove(course)

for course in reversed(listOfClassesOccuring):

    classTimeString = str(course[6])

    classStartH  = classTimeString[0:classTimeString.index(':')]
    classStartM  = classTimeString[classTimeString.index(':')+1:classTimeString.index(' ')]
    classStartAM = True if (classTimeString[classTimeString.index(' ')+1:classTimeString.index(' ', classTimeString.index(' ') + 1)] == "AM") else False

    classEndH  = classTimeString[classTimeString.index('-')+2:classTimeString.index(':',classTimeString.index('-'))]
    classEndM  = classTimeString[classTimeString.index(':', classTimeString.index('-'))+1:classTimeString.index(' ', classTimeString.index(':', classTimeString.index('-')))]
    classEndAM = True if classTimeString.find("AM", classTimeString.index('-')) != -1 else False

    classStart = convertTo24Hour(classStartH, classStartM, classStartAM)
    classEnd   = convertTo24Hour(classEndH, classEndM, classEndAM)

    #Check if the start of the event clashes with the bounds of the class

    if startTime >= classStart and startTime <= classEnd:
        #listOfClassesOccuring.remove(course)
        if listOfRooms.__contains__(course[7]):
            listOfRooms.remove(course[7])
        continue

    #Check if the end of the event clashesd with the bounds of the class
        
    if endTime >= classStart and endTime <= classEnd:
        #listOfClassesOccuring.remove(course)
        if listOfRooms.__contains__(course[7]):
            listOfRooms.remove(course[7])
        continue

listOfRooms.remove("Location")
listOfRooms.sort()

print("\nThe list of rooms that are empty at your given time is: \n")
for room in listOfRooms:
    print(room)

print("End of program.")