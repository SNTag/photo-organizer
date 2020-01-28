#!/usr/bin/env python3
# File: photo manager
# Author: SNTagore (agenttiny@gmail.com)
# Date: 28/12/2019
# Description: To manage my photo library.  Will sort photos by country into the appropiate category.  Tested on photos from 2019 onwards
# Usage: Simply call this program FROM THE DIRECTORY WITH UNSORTED PHOTOS.  It will read the 'config.csv' file, generate the appropiate folders under ./output/sorted (IF THEY AREN'T THERE ALREADY) and sort the photos in here into them (IF THEY AREN'T IN THERE ALREADY).  Keep note, it does not duplicate files but creates symlinks so as to reduce space consumption.
# Version: 1.0.2


# CSV file used to dictate this program need to have the following 1st line:
# City, Year, file identifier, Beginning, Ending


## modify the following line to set the output folder name
#TODO: [C] Add a user prompt for the following line?
userPath = "photostorage-sorted"

#TODO: [C] make the system robust to unknown values in CSV file.
#TODO: [C] make the system robust to files from multiple cameras (different naming conventions)


import pandas as pd
import os
import subprocess
from os import walk


## background processes like prepping config.csv, setting up paths, making userPath directory
class PhotoOrganizer:
    def __init__(self):
        #TODO: [A] need to make all the following variables global/accesable by the function
        ## Will load & format data
        self.dataMain = pd.read_csv('./config.csv', delimiter=', ', engine="python")
        #TODO: [C] can I use this as a security check for a properly configured config?
        self.dataMain['Beginning'] = self.dataMain['Beginning'].astype(int)
        self.dataMain['Ending'] = self.dataMain['Ending'].astype(int)
        self.dataMain['Ignore'] = self.dataMain['Ignore'].astype(bool)

        ## sets up the paths
        self.pathHomeOrig = os.getcwd()
        os.chdir("../")
        self.pathHome = os.getcwd()
        self.pathSorted = self.pathHome+'/'+userPath+'/'

        if os.path.isdir(self.pathSorted) == False:
            os.makedirs(self.pathSorted)

    # #TODO: [A] need to make all the following variables global/accesable by the function
    # ## Will load & format data
    # dataMain = pd.read_csv('./config.csv', delimiter=', ', engine="python")
    # #TODO: [C] can I use this as a security check for a properly configured config?
    # self.dataMain['Beginning'] = self.dataMain['Beginning'].astype(int)
    # self.dataMain['Ending'] = self.dataMain['Ending'].astype(int)
    # self.dataMain['Ignore'] = self.dataMain['Ignore'].astype(bool)

    # ## sets up the paths
    # self.pathHomeOrig = os.getcwd()
    # os.chdir("../")
    # self.pathHome = os.getcwd()
    # self.pathSorted = self.pathHome+'/'+userPath+'/'

    # if os.path.isdir(self.pathSorted) == False:
    #     os.makedirs(self.pathSorted)


    ## does the photo sorting/removing, making sorted folder directories
    def photoSorting(self):
        for i in range(len(self.dataMain["City"])):
            #TODO: [C] make this section reliant on column name, not number
            print(self.dataMain)
            dataNomen = self.dataMain.iloc[i, 2]
            dataNomen = dataNomen.replace(" ", "")
            dataStart = int(self.dataMain.iloc[i, 3])
            dataEnd = int(self.dataMain.iloc[i, 4])
            strCity = self.dataMain.loc[i,"City"]
            strCity = strCity.replace(" ","_")
            strYear = self.dataMain.iloc[i,1]
            fileName = strCity + '-' + strYear
            self.pathHomeFiles = self.pathSorted + fileName

            ## handles the directories
            ## makes new dir named as described in the config.csv
            if os.path.isdir(self.pathHomeFiles) == False:
                os.makedirs(self.pathHomeFiles)

            ## Sorts/removes photos by making symlinks into the appropiate folder as described by config.csv
            #TODO: [A] needs to remove all broken symlinks too!
            #TODO: [C] This approach will most likely only work on linux.  Try to make it universal?
            for d in range(dataStart, dataEnd+1):
                something1 = self.pathHomeOrig+'/'+dataNomen+str(d)+"*"
                something2 = self.pathHomeFiles+'/'
                bashString = str('ln -s ' + something1 + ' ' + something2)
                subprocess.call(bashString, shell = True)

                # ## Will remove unwanted files
                # if self.dataMain["Ignore"]==True:
                #     os.chdir(self.pathSorted+'/'+i)
                #     tempString = "rm -r * " + d
                #     subprocess.call([tempString], shell = True)

            ## Cleans up the directories and removes possible broken links
            f = []
            for (dirpath, dirnames, filenames) in walk(self.pathSorted):  # Can made more efficient.
                f.extend(dirnames)
                break
            for i in f:
                os.chdir(self.pathSorted+'/'+i)
                subprocess.call(["find -L . -name . -o -type d -prune -o -type l -exec rm {} +"], shell = True)

tmp=PhotoOrganizer()
tmp.photoSorting()
