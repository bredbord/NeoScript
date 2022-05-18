# Cape Parsing Interface
# Larson Rivera
# 2019

from tkinter import *  # Get the Tkinter Class
from RGBParser import RGBParse
import os.path
import cv2
from time import sleep


class Interface:
    def __init__(self, master):  # CONSTRUCTOR==========================================================================

        self.master = master
        self.leftInterface = Frame(master)
        self.leftInterface.pack(fill=Y)

        # Source Files
        self.source = Label(self.leftInterface, text="Source:")
        self.sourceBox = Entry(self.leftInterface, width=70)
        self.source.pack()
        self.sourceBox.pack(fill=X)

        # Output File
        self.output = Label(self.leftInterface, text="Output:")
        self.outputBox = Entry(self.leftInterface, width=70)
        self.output.pack()
        self.outputBox.pack(fill=X)

        self.outputName = Label(self.leftInterface, text="Output File Name")
        self.outputNameBox = Entry(self.leftInterface, width=70)
        self.outputName.pack()
        self.outputNameBox.pack(fill=X)

        #Operational Definitions
        self.current = Label(self.leftInterface, text="Maximum Circuit Current (A)")
        self.currentBox = Entry(self.leftInterface, width=70)
        self.current.pack()
        self.currentBox.pack(fill=X)

        # Status
        self.status = Label(self.leftInterface, text=" ", fg="red")
        self.status.pack()

        # Buttons
        self.run = Button(self.leftInterface, text="Run RGB Parsing Script", command=self.prepRGBCycler)
        self.run.pack()

        # Configurattion for program launch
        self.startupConfig("r")  # configure the program for launch


    def startupConfig(self, type):
        if (type == "r"):  # Read the contents of the file
            config = open("config.txt", "rt")  # Read text file

            self.sourceBox.insert(0, config.readline().strip())  # Read the config file
            self.outputBox.insert(0, config.readline().strip())
            self.currentBox.insert(0, config.readline().strip())

            config.close()  # Close the file to prevent corruption

        elif (type == "w"):  # If the type asks to write to the config file

            os.remove("config.txt")  # First, destroy the old
            newConfig = open("config.txt", "a+")  # Make a new one

            newConfig.write(self.sourceBox.get().strip() + "\n")  # Add the neccesary data
            newConfig.write(self.outputBox.get().strip() + "\n")
            newConfig.write(self.currentBox.get().strip() + "\n")

            newConfig.close()  # Close to prevent corruption


    def checkInput(self, input):  # Check for valid inputs==============================================================

        if input.strip() != "":
            return True

        else:
            return False

    def checkPath(self, source):  # Check for valid out path============================================================

        try:
            cv2.imread(source + "0001.png", 1)  # open image
            return True

        except TypeError:
            print("OOPS!")
            return False


    def constantChecking(self):
        source = self.sourceBox.get()  # Get the Source File
        out = self.outputBox.get()  # Get the output File
        name = self.outputNameBox.get()  # Get the name
        current = self.currentBox.get()  # Get the Maximum Current Parameter

        # Boolean Tracking
        sourceIsGo = False
        outIsGo = False
        nameIsGo = False
        currentIsGo = False

        if self.checkInput(current):  # Is the output not blank?
            currentIsGo = True
        else:
            self.status['text'] = "PLEASE ENTER A MAXIMUM CURRENT RATING"
            self.status['fg'] = "red"

        if self.checkInput(name):  # Is the output not blank?
            nameIsGo = True
        else:
            self.status['text'] = "PLEASE ENTER A VALID OUTPUT NAME"
            self.status['fg'] = "red"

        if self.checkInput(out):  # Is the output not blank?
            outIsGo = True
        else:
            self.status['text'] = "PLEASE ENTER A VALID OUTPUT PATH"
            self.status['fg'] = "red"

        if self.checkInput(source) and self.checkPath(
                source):  # Is the source not blank and contains valid starting image?
            sourceIsGo = True
        else:
            self.status['text'] = "PLEASE ENTER A VALID SOURCE PATH"
            self.status['fg'] = "red"

        if sourceIsGo and outIsGo and nameIsGo and currentIsGo:  # Is everything ready?
            self.status['text'] = "Ready"
            self.status['fg'] = "green"

            return True

        return False  # Otherwise, probably not


    def prepRGBCycler(self):  # PREP PARSER ============================================================================

        if self.constantChecking():  # If all checks are ready, run the parser
            self.status['text'] = "Parsing"
            self.status['fg'] = "blue"
            self.master.update()

            #Main Parsing Call
            Parser = RGBParse(self.sourceBox.get(), self.outputBox.get(), self.outputNameBox.get(), self.currentBox.get())
            tempStatus = Parser.parseRGB()

            if tempStatus:
                self.startupConfig("w")  # Write the new config file

                self.status['text'] = "Parsing Completed"
                self.status['fg'] = "green"



root = Tk(screenName="RGB Parsing Interface Version 1.0")  # Make the Window

application = Interface(root)

root.mainloop()
