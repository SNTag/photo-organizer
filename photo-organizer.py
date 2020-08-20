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
from PIL import Image
import cv2
import numpy as np
import imutils


### required variables: final_dir, search_dir
stuff = arg[1].split(',')
for item in stuff:
    exec(item)


#----------|Functions|----------#
##### get_date_taken #####
def get_date_taken(path):
    """ gets the date a photo was taken
    Variables: path

Parameters
----------
path : where to look for the photo


Returns
-------
out : image date

    """
    return Image.open(path)._getexif()[36867]


##### photo_cataloger #####
def photo_cataloger(path):
    """ Generates a csv of photos in a directory
Generates a csv file of all photo filenames and creation date in a directory. This information is used downstream, enabling faster search functions.
    """
    data = []
    for file in sorted(os.listdir(path)):
        photo_date = get_date_taken(path+file) #### This line should do it. !!!! Need to append creation-date metadata !!!!
        data.append((file, photo_date))

    data = pd.DataFrame(data = data)
    data.columns = ["file","date"]
    return(data)


##### photo_finder #####
def photo_finder(image_name, in_data, out_data):
    """ when given a photo, looks for similar in final dir
looks for:
- same name
- creation date
    """
    #! search for images with the same name.
    file_names = []
    for i in range(len(in_data)):
        tmpVar=in_data.iloc[i][0]

        #! looks up tmpVar in output for exact string match
        boolean_finding = out_data["file"].str.contains(tmpVar).any()
        if boolean_finding:
            file_names.append(tmpVar)
            break

    #! search for images with the same creation date
    #for i in range(len(in_data)):

    return(file_names)


##### photo_rotator #####
def photo_rotator(image_name):
    #! loop over rotation angles.
    image_file = cv2.imread(stuff[1]+image_name)
    for angle in np.arange(0, 360, 90):
        rotated = imutils.rotate(image_file, angle)
        if (image_file == rotated).all():
            return(rotated)

    #! if files are slightly different due to photoediting
    #im = Image.open(stuff[1]+image_name)
    #for angle in np.arange(0, 360, 90):
    #    rotated = imutils.rotate(image_file, angle)
 


##### compare_photos #####
def compare_photos(image_name, in_data, out_data):
    """ Organizes the photo comparison
The goal is to rapidly dismiss dismiss disimilar photos through a rough analysis. If it is worth looking further, a harsh analysis will decide how to handle the photos.

steps:
1. determines which files to compare.
2. determine optimal rotation
3. rough analysis
4. harsh analysis

    Variables:

    """
    #! step 1
    to_compare = photo_finder(image_name, in_data,out_data)

    #! step 2
    optimal_rotation = photo_rotator(image_name)

    #! step 3

    #! step 4




#----------|program|----------#


in_data =photo_cataloger(stuff[0])
out_data=photo_cataloger(stuff[1])

for (i in range(in_data)):
    image_name = in_data.iloc[i][0]
    compare_photos(image_name)









#----------|archived process|----------#



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
