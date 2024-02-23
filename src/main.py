# Simon Ogorek
# 2/22/24
# Find available room times given NJIT .scv file(s)

import os
import csv

def findFiles():
    rootDirectoryItems = os.listdir(os.path.dirname(os.path.realpath(__file__)))
    rootDirectory = os.path.dirname(os.path.realpath(__file__))

    listOfSheets = []
    if rootDirectoryItems.__contains__("csvs"):
        #print("Directory found!")
        csvsDirectory = rootDirectoryItems.__getitem__(rootDirectoryItems.index("csvs"))
        for csvFile in os.listdir(csvsDirectory):
            #print("Loading: " + csvFile)
            listOfSheets.append(csv.reader(open(rootDirectory + "/" + csvsDirectory + "/" + csvFile)))

        #print("\nAll csv files loaded!")

        return listOfSheets

    else:
        print("Directory was not found, please ensure that the file with the .csv(s) is named csvs")

spreadSheets = findFiles()

print("~~~~~~~ Find a empty room ~~~~~~~")

# Monday    M | 0
# Tuesday   T | 1
# Wednesday W | 2
# Thursday  R | 3
# Friday    F | 4

weekdayRange = ""

while (len(weekdayRange) < 1 or len(weekdayRange) > 5):
    weekdayRange = input("\nType any amount of weekdays you would like to search for as MTWRF\n")
    weekdayRange = weekdayRange.upper()

weekdaysToCheck = ["M" if weekdayRange.__contains__("M") else "X", "T" if weekdayRange.__contains__("T") else "X",
                   "W" if weekdayRange.__contains__("W") else "X", "R" if weekdayRange.__contains__("R") else "X",
                   "F" if weekdayRange.__contains__("F") else "X"]

startTimeH = -1
startTimeM = -1
startTimeAM = True

endTimeH = -1
endTimeM = -1
endTimeAM = True

while (startTimeH < 1 or startTimeH > 12 or startTimeM < 0 or startTimeM > 59):
    startTimeAM = input("\nIs this in the morning (Y/N)\n")
    startTimeH  = int(input("\nWhat hour does the event start\n")) #fix plz so the input is defended against words
    startTimeM  = int(input("\nWhat minute does the event start (30 minute increments work best)\n"))

    if (startTimeAM.upper() == "Y"):
        startTimeAM = True
    elif (startTimeAM.upper() == "N"):
        startTimeAM = False
    else:
        startTimeH = -1; #Force a reset


while (endTimeH < 1 or endTimeH > 12 or endTimeM < 0 or endTimeM > 59):
    endTimeAM = input("\nIs this in the morning (Y/N)\n")
    endTimeH = int(input("\nWhat hour does the event end\n"))  # fix so the input is defended against words
    endTimeM = int(input("\nWhat minute does the event end (30 minute increments work best)\n"))

    if (endTimeAM.upper() == "Y"):
        endTimeAM = True
    elif (endTimeAM.upper() == "N"):
        endTimeAM = False
    else:
        endTimeH = -1;

locationIndex = 7

listOfRooms = []
listOfClassesOccuring = []*1
# First pass to get all the rooms
for workspaces in spreadSheets:
    for rows in workspaces:
        if rows[7] != " " and rows[7] != "" and not (listOfRooms.__contains__(rows[7])):
            listOfRooms.append(rows[7])

#Refresh the readers
spreadSheets = findFiles()

# second pass to grab classes that occur on the days needed
for workspaces in spreadSheets:
    for rows in workspaces:
        for days in rows[5]:
            if weekdaysToCheck.__contains__(days):
                listOfClassesOccuring.append(rows)

listOfClassesOccuring.pop(0)

for i in range(len(listOfClassesOccuring)):
    classTimeString = str(listOfClassesOccuring[i][6])

    classStartH = classTimeString[0:classTimeString.index(':')]
    classStartM = classTimeString[classTimeString.index(':')+1:classTimeString.index(' ')]
    classStartAM = True if (classTimeString[classTimeString.index(' ')+1:classTimeString.index(' ', classTimeString.index(' ') + 1)] == "AM") else False

    classEndH = classTimeString[classTimeString.index('-')+2:classTimeString.index(':',classTimeString.index('-'))]
    classEndM = classTimeString[classTimeString.index(':', classTimeString.index('-'))+1:classTimeString.index(' ', classTimeString.index(':', classTimeString.index('-')))]
    classEndAM = True if classTimeString.find("AM", classTimeString.index('-')) != -1 else False










