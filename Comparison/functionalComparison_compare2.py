# import the necessary packages
from skimage.measure import compare_ssim as ssim
import cv2, os
import numpy as np
from subImageSearch import find_image
from PIL import Image


def RemoveTempFolders(someList):
    for item in someList:
        if item[0] == ".":
            someList.remove(item)
        if item == "normalised.jpg" or item == "ref_mask.jpg":
            someList.remove(item)

    return someList

def imageCompare(imageA, imageB):
    if imageA.shape != imageB.shape:
        return False
    try:
        return ssim(imageA, imageB, multichannel=True)
    except:
        return False


websites = os.listdir("components")
imageMatrix = []
websites = RemoveTempFolders(websites)

for website in ['faa-gov']: #in websites:
    classes = os.listdir("components/"+website)
    classes = RemoveTempFolders(classes)

    for cls in classes:
        varients = os.listdir("components/"+website+"/"+cls)
        varients = RemoveTempFolders(varients)

        imageMatrix = []
        for varient in ["/0","/1","/2"]:
            reference = cv2.imread ("components/"+website+"/"+cls+"/0/normalised.jpg",0)
            reference_mask = cv2.imread ("components/"+website+"/"+cls+"/0/normalised.jpg")

            components = os.listdir("components/"+website+"/"+cls+"/"+varient)
            components = RemoveTempFolders(components)
            imageMatrix.append(components)
            notFound=0
            found = 0

            output = open("scores/" + website + "_" + cls + "_varient" + varient[-1] + ".csv", "a+")

            for c in components:
                if varient == "/0": continue
                comp = cv2.imread ("components/"+website+"/"+cls+"/"+varient+"/"+c,0)
                result = find_image (reference,comp)

                cropCount = 0
                cropped = comp

                while result==False and cropCount<5:
                    cropCount+=1
                    cropped = cropped [cropped.shape[0]//10:(cropped.shape[0]-cropped.shape[0]//10),cropped.shape[1]//10:(cropped.shape[1]-cropped.shape[1]//10)]
                    result = find_image (reference,cropped)
                if result == False:
                    notFound+=1
                    resultMatrix = []
                    for originalComponent in imageMatrix[0]:
                        originalComponent = cv2.imread ("components/"+website+"/"+cls+"/0/"+originalComponent,0)
                        resultMatrix.append(imageCompare(originalComponent,comp))
                    result = max(resultMatrix)
                else:
                    found +=1
                    cv2.rectangle(reference_mask, (result[1],result[0]), (result[1]+comp.shape[1], result[0]+comp.shape[0]), (255,0,0), 2)
                    result = True

                output.write (("original: "+c) + "," + ("matched: "+ str(result)))
                output.write("\n")

            cv2.imwrite("components/"+website+"/"+cls+"/"+varient+"/ref_mask.jpg", reference_mask)
            print (notFound,found)
