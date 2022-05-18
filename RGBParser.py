# Main Cape Parser
# Larson Rivera
# 2019

import cv2
import os.path
from tkinter import *
#from matplotlib import pyplot as plot

class RGBParse:

    def __init__(self, i, o, n, c):

        #Define the Operational Variables for the Parser
        self.inputPath = i
        self.outputPath = o
        self.outputName = n
        self.maximumCurrent = c

        #Path Tracking
        self.numFrames = len(os.listdir(self.inputPath))  # get the number of files in the directory

        #Graphing
        self.graphFrame = [self.numFrames]
        self.red = []
        self.green = []
        self.blue = []
        self.total = []


    def launch(self):

        '''leftWindow = Frame(self.rootParse)
        rightWindow = Frame(self.rootParse)

        #Left frame
        position = Label(leftWindow, text=("Frame %s of %s" % (0, 0)), font="Times 16 bold")
        position.pack()

        #Current Draw
        redCurrent = Label(leftWindow, text=("Red: %s Amps" % 0), fg="red", font="Times 12 bold")
        blueCurrent = Label(leftWindow, text=("Blue: %s Amps" % 0), fg="blue", font="Times 12 bold")
        greenCurrent = Label(leftWindow, text=("Green: %s Amps" % 0), fg="green", font="Times 12 bold")
        redCurrent.pack()
        blueCurrent.pack()
        greenCurrent.pack()


        #Right Frame
        totalCurrent = Label(rightWindow, text="Total: %s" % 0, font="Times 16 bold")
        totalCurrent.pack()

        leftWindow.pack(side=LEFT)
        rightWindow.pack(side=RIGHT)
        '''


    def parseRGBImage(self, sourceF, out, frame):  # PARSE INDIVIDUAL========================================================

        # get image
        img = cv2.imread(sourceF + frame + ".png", 1)  # open image

        # shaping
        imgShape = img.shape
        x = imgShape[1]  # get x pixels by number of columns
        y = imgShape[0]  # get y pixles by number of rows

        #print("Picture width is: %s, %s" % (x, y))

        for xpos in range(0, x):  # for each column

            posTest = xpos % 2

            if posTest == 0:  # If the column is an even number, it writes down, so parse from top down
                for ypos in range(0, y):  # for each pixel (column) in thr row
                    pixel = img[ypos, xpos]  # get pixel BGR
                    out.write(str(pixel[2]) + "\n" + str(pixel[1]) + "\n" + str(pixel[0]) + "\n")

            if posTest == 1:  # Otherwise the strip is odd, it writes up, so parse from bottom up
                for ypos in range((y-1), -1, -1):  # for each pixel (column) in thr row
                    pixel = img[ypos, xpos]  # get pixel BGR
                    out.write(str(pixel[2]) + "\n" + str(pixel[1]) + "\n" + str(pixel[0]) + "\n")
        out.write("-1\n")


    def parseRGB(self):  # CYCLE THE PARSER==========================================================
        file = open(self.outputPath + self.outputName+".txt", "a+")  # Open the file in the destination
        file.write(self.outputName.upper() + "\n")
        file.write("BEGIN" + "\n")

        for f in range(3061, 4132): # 1, (self.numFrames + 1)
            bufferFrame = str(f)

            # buffering
            if f < 1000:
                bufferFrame = "0" + bufferFrame

                if f < 100:
                    bufferFrame = "0" + bufferFrame

                    if f < 10:
                        bufferFrame = "0" + bufferFrame
            self.parseRGBImage(self.inputPath, file, bufferFrame)

        file.write("-2\n")  # signal end of animation
        file.write(self.outputName.upper() + "\n")
        file.close()  # close the file

        return True
