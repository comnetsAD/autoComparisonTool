# import the necessary packages
from skimage.measure import compare_ssim as ssim
import cv2, os
import numpy as np
from subImageSearch import find_image
from PIL import Image
import sys

def RemoveTempFolders(someList):
    for item in someList:
        if item[0] == ".":
            someList.remove(item)
        if item == "normalised.jpg" or item == "ref_mask.jpg":
            someList.remove(item)

    return someList

def count (src):
    f = open("scores/"+src, "r")
    text = f.read()
    return ([text.count("True"),text.count("False")])

filebyWesbsite = []

websites = os.listdir("components")
websites = RemoveTempFolders(websites)
for website in websites: filebyWesbsite.append([])

files = os.listdir("scores")
files = RemoveTempFolders(files)


for file in files:
    ind = websites.index(file.split("_")[0])
    filebyWesbsite[ind].append(file)


varients = "varient1.csv","varient2.csv","varient3.csv"
scores = []
# scores = [["website","/",["index50 (found)","index50 (not found)"],["index55 (found)","index55 (not found)"],["index60 (found)","index60 (not found)"]]]
for website in websites:
    scores.append ([website,[0,0],[0,0],[0,0]])
    # website, [true, false], [true, false], [true, false]

for x in filebyWesbsite:
    for file in x:
        ind = websites.index(file.split("_")[0])
        if (file.split("_")[-1]) == "varient1.csv":
            cnt = count(file)
            scores[ind][1][0] += cnt[0]
            scores[ind][1][1] += cnt[1]
        if (file.split("_")[-1]) == "varient2.csv":
            cnt = count(file)
            scores[ind][2][0] += cnt[0]
            scores[ind][2][1] += cnt[1]
        if (file.split("_")[-1]) == "varient3.csv":
            cnt = count(file)
            scores[ind][3][0] += cnt[0]
            scores[ind][3][1] += cnt[1]


for s in scores:
    print (s)

output = open("scores.csv", "a+")

for s in scores:
    output.write (str(s[0]) + "," + str(s[1][0]) + "," + str(s[1][1]) + "," + str(s[2][0]) + "," + str(s[2][1]) + "," + str(s[3][0]) + "," + str(s[3][1]) +  "\n")
