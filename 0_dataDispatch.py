#!/usr/bin/python3
# -*- coding: utf-8 -*-

import glob, os
import os.path
import time
from shutil import copyfile
import cv2
from xml.dom import minidom
from os.path import basename

#--------------------------------------------------------------------
#classList = { "Mask":0, "No_Mask":1 }
classList = { "with_mask":0, "without_mask":1,"mask_weared_incorrect":2  }
workFolder  = os.getcwd()
dataFolder  = workFolder+"/dataset"
labelFolder = workFolder+"/dataset"
backupFolder = workFolder+"/backup"
trainList 	= "train.txt"
testList  	= "test.txt"

negFolder 	= ""

#---------------------------------------------------------------------
if not os.path.exists(backupFolder):	# if no "labels" folder, create it!
    os.makedirs(backupFolder)

def transferYolo( xmlFilepath, imgFilepath):
    global dataFolder

    img_file, img_file_extension = os.path.splitext(imgFilepath)
    img_filename = basename(img_file)

    if(xmlFilepath is not None):
        img = cv2.imread(imgFilepath)
        imgShape = img.shape
        img_h = imgShape[0]
        img_w = imgShape[1]

        labelXML = minidom.parse(xmlFilepath)
        labelName = []
        labelXmin = []
        labelYmin = []
        labelXmax = []
        labelYmax = []
        totalW = 0
        totalH = 0
        countLabels = 0

        tmpArrays = labelXML.getElementsByTagName("filename")
        for elem in tmpArrays:
            filenameImage = elem.firstChild.data

        tmpArrays = (labelXML.getElementsByTagName("name"))
        for elem in tmpArrays:
            labelName.append(str(elem.firstChild.data))

        tmpArrays = labelXML.getElementsByTagName("xmin")
        for elem in tmpArrays:
            labelXmin.append(int(elem.firstChild.data))

        tmpArrays = labelXML.getElementsByTagName("ymin")
        for elem in tmpArrays:
            labelYmin.append(int(elem.firstChild.data))

        tmpArrays = labelXML.getElementsByTagName("xmax")
        for elem in tmpArrays:
            labelXmax.append(int(elem.firstChild.data))

        tmpArrays = labelXML.getElementsByTagName("ymax")
        for elem in tmpArrays:
            labelYmax.append(int(elem.firstChild.data))

        yoloLabel = os.path.join(labelFolder, img_filename + ".txt")
#        print("writing to {}".format(yoloLabel))

        with open(yoloLabel, 'a') as the_file:
            i = 0
            for className in labelName:
                if(className in classList):
                    classID = classList[className]
                    x = (labelXmin[i] + (labelXmax[i]-labelXmin[i])/2) * 1.0 / img_w 
                    y = (labelYmin[i] + (labelYmax[i]-labelYmin[i])/2) * 1.0 / img_h
                    w = (labelXmax[i]-labelXmin[i]) * 1.0 / img_w
                    h = (labelYmax[i]-labelYmin[i]) * 1.0 / img_h
                    the_file.write(str(classID) + ' ' + str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h) + '\n')
                    i += 1

    else:
        yoloLabel = os.path.join(labelFolder ,img_filename + ".txt")
#        print("writing negative file to {}".format(yoloLabel))

        with open(yoloLabel, 'a') as the_file:
            the_file.write(' ')

    the_file.close()

#---------------------------------------------------------------
fileCount = 0

trainListFile = open(trainList, 'w')
testListFile = open(testList, 'w')

for file in os.listdir(dataFolder):
    filename, file_extension = os.path.splitext(file)
    file_extension = file_extension.lower()

    if(file_extension == ".jpg" or file_extension==".png" or file_extension==".jpeg" or file_extension==".bmp"):
        imgfile = os.path.join(dataFolder, file)
        xmlfile = os.path.join(dataFolder ,filename + ".xml")
        if(os.path.isfile(xmlfile)):
            if( fileCount % 5 == 0 ):
#                copyfile(imgfile, os.path.join(testFolder ,file))
                testListFile.write(imgfile+'\n')
#            else:
#            copyfile(imgfile, os.path.join(trainFolder ,file))
            trainListFile.write(imgfile+'\n')

            transferYolo( xmlfile, imgfile)
            fileCount += 1

if(os.path.exists(negFolder)):
    for file in os.listdir(negFolder):
        filename, file_extension = os.path.splitext(file)
        file_extension = file_extension.lower()
        imgfile = os.path.join(negFolder ,file)

        if(file_extension == ".jpg" or file_extension==".png" or file_extension==".jpeg" or file_extension==".bmp"):
            transferYolo( None, imgfile, "")
            copyfile(imgfile, os.path.join(dataFolder ,file))

trainListFile.close()
testListFile.close()
