from tkinter import *
import re
import ctypes
import time
from datetime import date
import pickle

#global variable to save data
DataDict = {}

#for saving DataDict in Pickle File
def save_object(obj):
    try:
        with open("data.pickle", "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported):", ex)

#Load pickle file data into DataDict
def load_object(filename):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except Exception as ex:
        print("Error during unpickling object (Possibly unsupported):", ex)


#a = date, x = number of days to add
def addonDays(a, x):
    ret = time.strftime("%Y-%m-%d", time.localtime(time.mktime(time.strptime(a, "%Y-%m-%d")) + x * 3600 * 24 + 3600))
    return ret

#return days of week for the monday given
def daysofWeek(MondayDate):
    dowList = []
    dowList.append(MondayDate)
    for x in range(1, 7):
        xtime = time.strptime(addonDays(str(MondayDate), x), "%Y-%m-%d")
        dowList.append(date(xtime.tm_year,xtime.tm_mon,xtime.tm_mday))
    return dowList

class MyGUI:
    def __init__(self, root, dowList, MondayDate):
        self.currentMonday = MondayDate
        self.dowList = dowList
        self.master = root
        self.master.title("MySimplePlanner")

        Grid.columnconfigure(root, 0, weight=1)
        Grid.columnconfigure(root, 1, weight=1)
        Grid.columnconfigure(root, 2, weight=1)
        Grid.columnconfigure(root, 3, weight=1)
        Grid.columnconfigure(root, 4, weight=1)
        Grid.columnconfigure(root, 5, weight=1)
        Grid.columnconfigure(root, 6, weight=1)
        Grid.columnconfigure(root, 7, weight=1)

        def on_closing():
            self.master.destroy()  # close Gui

        root.protocol("WM_DELETE_WINDOW", on_closing)

        #Year
        self.yearLabel = Label(self.master, text="Year: " + str(dowList[6].year), width = 22, anchor = CENTER)
        self.yearLabel.grid(row=0, column=3, sticky='NS')

        #Monday
        self.MLabel = Label(self.master, text=str(dowList[0].month) + "/" + str(dowList[0].day) + "\nMonday", width=22, anchor=CENTER)
        self.MLabel.grid(row=1, column=0, sticky='ns')
        self.MTextBox = Text(self.master, width=22, height=10)
        self.MTextBox.grid(row=2, column=0, sticky=E)
        #Tuesday
        self.TuLabel = Label(self.master, text=str(dowList[1].month) + "/" + str(dowList[1].day) + "\nTuesday", width=22, anchor=CENTER)
        self.TuLabel.grid(row=1, column=1, sticky='ns')
        self.TuTextBox = Text(self.master, width=22, height=10)
        self.TuTextBox.grid(row=2, column=1, sticky=E)
        #Wednesday
        self.WLabel = Label(self.master, text=str(dowList[2].month) + "/" + str(dowList[2].day) + "\nWednesday", width=22, anchor=CENTER)
        self.WLabel.grid(row=1, column=2, sticky='ns')
        self.WTextBox = Text(self.master, width=22, height=10)
        self.WTextBox.grid(row=2, column=2, sticky=E)
        #Thursday
        self.ThLabel = Label(self.master, text=str(dowList[3].month) + "/" + str(dowList[3].day) + "\nThursday", width=22, anchor=CENTER)
        self.ThLabel.grid(row=1, column=3, sticky='ns')
        self.ThTextBox = Text(self.master, width=22, height=10)
        self.ThTextBox.grid(row=2, column=3, sticky=E)
        #Friday
        self.FLabel = Label(self.master, text=str(dowList[4].month) + "/" + str(dowList[4].day) + "\nFriday", width=22, anchor=CENTER)
        self.FLabel.grid(row=1, column=4, sticky='ns')
        self.FTextBox = Text(self.master, width=22, height=10)
        self.FTextBox.grid(row=2, column=4, sticky=E)
        #Saturday
        self.SatLabel = Label(self.master, text=str(dowList[5].month) + "/" + str(dowList[5].day) + "\nSaturday", width=22, anchor=CENTER)
        self.SatLabel.grid(row=1, column=5, sticky='ns')
        self.SatTextBox = Text(self.master, width=22, height=10)
        self.SatTextBox.grid(row=2, column=5, sticky=E)
        #Sunday
        self.SunLabel = Label(self.master, text=str(dowList[6].month) + "/" + str(dowList[6].day) + "\nSunday", width=22, anchor=CENTER)
        self.SunLabel.grid(row=1, column=6, sticky='ns')
        self.SunTextBox = Text(self.master, width=22, height=10)
        self.SunTextBox.grid(row=2, column=6, sticky=E)

        self.textBoxes = [self.MTextBox, self.TuTextBox, self.WTextBox, self.ThTextBox, self.FTextBox, self.SatTextBox, self.SunTextBox]

        self.updateWeek()  # load data

        #Back button
        self.backButton = Button(self.master, text="Back", command=self.Back, width=8, bg = "#00ccff")
        self.backButton.grid(row=4, column=0, sticky=E, padx=40)
        #Next button
        self.nextButton = Button(self.master, text="Next", command=self.Next, width=8, bg = "#00ccff")
        self.nextButton.grid(row=4, column=1, sticky=E, padx=40)

        #save button
        self.saveButton = Button(self.master, text="Save", command=self.permSave, width=8, bg = "#00ffff")
        self.saveButton.grid(row=4, column=2, sticky=E, padx=40)

    def Back(self):
        self.Save()
        mondayTime = time.strptime(addonDays(str(self.currentMonday), -7), "%Y-%m-%d")  # last monday time
        self.currentMonday = date(mondayTime.tm_year,mondayTime.tm_mon,mondayTime.tm_mday)  # last monday date
        self.dowList = daysofWeek(self.currentMonday)  # last week days
        self.updateWeek()  # update week

    def Next(self):
        self.Save()
        mondayTime = time.strptime(addonDays(str(self.currentMonday), 7), "%Y-%m-%d")  # next monday time
        self.currentMonday = date(mondayTime.tm_year, mondayTime.tm_mon, mondayTime.tm_mday)  # next monday date
        self.dowList = daysofWeek(self.currentMonday) #next week days
        self.updateWeek() #update week

    def updateWeek(self):
        self.yearLabel.configure(text="Year: " + str(self.dowList[6].year))
        self.MLabel.configure(text=str(self.dowList[0].month) + "/" + str(self.dowList[0].day) + "\nMonday", width=22, anchor=CENTER)
        self.TuLabel.configure(text=str(self.dowList[1].month) + "/" + str(self.dowList[1].day) + "\nTuesday", width=22, anchor=CENTER)
        self.WLabel.configure(text=str(self.dowList[2].month) + "/" + str(self.dowList[2].day) + "\nWednesday", width=22, anchor=CENTER)
        self.ThLabel.configure(text=str(self.dowList[3].month) + "/" + str(self.dowList[3].day) + "\nThursday", width=22, anchor=CENTER)
        self.FLabel.configure(text=str(self.dowList[4].month) + "/" + str(self.dowList[4].day) + "\nFriday", width=22, anchor=CENTER)
        self.SatLabel.configure(text=str(self.dowList[5].month) + "/" + str(self.dowList[5].day) + "\nSaturday", width=22, anchor=CENTER)
        self.SunLabel.configure(text=str(self.dowList[6].month) + "/" + str(self.dowList[6].day) + "\nSunday", width=22, anchor=CENTER)

        for x in range(0, 7):
            if str(self.dowList[x]) in DataDict:
                self.textBoxes[x].delete("1.0", END)
                self.textBoxes[x].insert(END, DataDict[str(self.dowList[x])])
            else:
                self.textBoxes[x].delete("1.0", END)


    #save to DataDict
    def Save(self):
        for x in range(0, 7):
            if (str(self.dowList[x]) in DataDict) or self.textBoxes[x].get('1.0', "end-1c") != "":
                if self.textBoxes[x].get('1.0', "end-1c") == "": #if already saved data is empty now, remove from data
                    DataDict.pop(str(self.dowList[x]))
                else:
                    DataDict[str(self.dowList[x])] = self.textBoxes[x].get('1.0', "end-1c") #save data to dictionary

    #save DataDict to pickle file
    def permSave(self):
        for x in range(0, 7):
            if (str(self.dowList[x]) in DataDict) or self.textBoxes[x].get('1.0', "end-1c") != "":
                if self.textBoxes[x].get('1.0', "end-1c") == "": #if already saved data is empty now, remove from data
                    DataDict.pop(str(self.dowList[x]))
                else:
                    DataDict[str(self.dowList[x])] = self.textBoxes[x].get('1.0', "end-1c") #save data to dictionary
                    #print(DataDict[str(self.dowList[x])])
        save_object(DataDict)



if __name__ == '__main__':
    DataDict = load_object("data.pickle")
    todays_date = date.today()
    weekDay = todays_date.weekday()  # days from this monday
    thisMonday = time.strptime(addonDays(str(date.today()), -weekDay), "%Y-%m-%d")
    MondayDate = date(thisMonday.tm_year,thisMonday.tm_mon,thisMonday.tm_mday) #convert to date object
    dowList = daysofWeek(MondayDate)  #get list of days in the current week

    ctypes.windll.shcore.SetProcessDpiAwareness(1) #for sharper resoulution
    myTkRoot = Tk()
    my_gui = MyGUI(myTkRoot, dowList, MondayDate)
    myTkRoot.mainloop()
