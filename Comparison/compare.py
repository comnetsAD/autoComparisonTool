#########################################################
#########################################################
#####                                               #####
#####   Compares screenshots in a pixel by          #####
#####   pixel  comparison and can not be used       #####
#####   with the cloner as different versions of    #####
#####   the page have slight movements that marsks  #####
#####   seemingly similar images as different.      #####
#####                                               #####
#########################################################
#########################################################

import cv2, os, numpy


def imageCompare(p1,p2):
    # print (img1,img2)

    print (p1.split("/")[-1:][0])
    print (p1)
    print (p2)

    try:
        img1 = cv2.imread(p1)
        img2 = cv2.imread(p2)

        diff = cv2.subtract(img1,img2)

        r,g,b = cv2.split(diff)

        print (cv2.countNonZero(r))

        if cv2.countNonZero(r)==cv2.countNonZero(g)==cv2.countNonZero(b)==0:
            return True
        else:
            return False

        print ("works")

    except:
        print ("Error handling: ", p1)



def RemoveTempFolders(someList):
    for item in someList:
        if item[0] == ".":
            someList.remove(item)
    return someList

# extract the list of websites to compare
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

    for image in imageMatrix[0]:

        paths = ["ss/" + website + "/0/" + image,
                 "ss/" + website + "/1/" + image,
                 "ss/" + website + "/2/" + image]

        for i in varients[1:]:
            i = int(i)
            if image in imageMatrix[i]:
                if imageCompare(paths[0],paths[i]):
                    diffMatrix[i].append("SAME")
                else:
                    diffMatrix[i].append("DIFFERENT")
            else:
                diffMatrix[i].append("NOT FOUND")


for i in range(len(diffMatrix[1])):
    print (diffMatrix[1][i],"\t",diffMatrix[2][i],"\t",diffMatrix[0][i])
    print ()
