#####
#####  1. Aim:
#####           Newer approach to solve the issues from compare.py
#####           This script should be able to give a score on similarity
#####           of the page visually, not taking in view the entire
#####           functionality of the page
#####
#####  2. Refrences:
#####           https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/
#####

# import the necessary packages
from skimage.measure import compare_ssim as ssim
import cv2, os
import numpy as np

def RemoveTempFolders(someList):
    for item in someList:
        if item[0] == ".":
            someList.remove(item)
    return someList

def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err

def imageCompare(imageA, imageB):
    imageA = cv2.imread(imageA)
    imageB = cv2.imread(imageB)
    m = mse(imageA, imageB)
    s = ssim(imageA, imageB, multichannel=True)
    return [m,s]

websites = os.listdir("ss")
imageMatrix = []

websites = RemoveTempFolders(websites)


for website in websites:
    # List and Normalise
    varients = os.listdir("ss/"+website)
    varients = RemoveTempFolders(varients)

    for varient in varients:
        imageMatrix.append([])
        # List and Normalise
        images = os.listdir("ss/"+website+"/"+varient)
        images = RemoveTempFolders(images)

        for image in images:
            imageMatrix[int(varient)].append(image)

    diffMatrix = [imageMatrix[0],[],[]]

    j = 0
    for image in imageMatrix[0]:

        paths = ["ss/" + website + "/0/" + image,
                 "ss/" + website + "/1/" + image,
                 "ss/" + website + "/2/" + image]

        for i in varients[1:]:
            i = int(i)
            if image in imageMatrix[i]:
                diffMatrix[i].append(imageCompare(paths[0],paths[i])[1])
            else:
                diffMatrix[i].append("NOT FOUND")

        print (diffMatrix[1][j],"\t",diffMatrix[2][j],"\t",diffMatrix[0][j])
        j+=1

for i in range(len(diffMatrix[1])):
    print (diffMatrix[1][i],"\t",diffMatrix[2][i],"\t",diffMatrix[0][i])
    print ()
