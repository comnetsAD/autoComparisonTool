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
    return someList

def imageCompare(imageA, imageB):
    if imageA.shape != imageB.shape:
        return 0
    try:
        return ssim(imageA, imageB, multichannel=True)
    except:
        return 0

reference = np.asarray(Image.open('components/faa-gov/screenshotdiv-class-twoColumn/0/normalised.jpg').convert('RGB'))
# reference = cv2.imread ("components/faa-gov/screenshotdiv-class-twoColumn/0/normalised.jpg")
# reference = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)
# reference = cv2.cvtColor(reference, cv2.COLOR_GRAY2BGR)
reference_mask = reference
print (reference[1][1])

components = os.listdir("components/faa-gov/screenshotdiv-class-twoColumn/0/")
components = RemoveTempFolders(components)

notFound=0
found = 0


for c in components:
    # comp = cv2.imread ("components/faa-gov/screenshotdiv-class-twoColumn/0/" + c)
    comp = np.asarray(Image.open("components/faa-gov/screenshotdiv-class-twoColumn/0/" + c).convert('RGB'))
    print (comp[1][1])
    result = find_image (reference,comp)
    if result == False:
        notFound +=1
    else:
        found +=1
        cv2.rectangle(reference_mask, (result[1],result[0]), (result[1]+comp.shape[1], result[0]+comp.shape[0]), (255,0,0), 2)

cv2.imwrite("1.jpg", reference_mask)
print (notFound,found)


# img0 = cv2.imread ("components/faa-gov/screenshotdiv-class-twoColumn/0/normalised.jpg", 0)
#
# img1 = cv2.imread ("components/faa-gov/screenshotdiv-class-twoColumn/0/42.jpg", 0)
#
# img0 = cv2.cvtColor(img0,cv2.COLOR_GRAY2RGB)
#
# result = find_image (img0,img1)
# print (result)
# # cv2.rectangle(img0, (result[0],result[1]), (result[0]+img1.shape[0], result[1]+img1.shape[1]), (255,0,0), 2)
#
# cv2.rectangle(img0, (result[1],result[0]),(result[1]+img1.shape[1],result[0]+img1.shape[0]) , (255,0,0), 2)
#
# cv2.imwrite("1.jpg", img0)









# def score(website,cls,imageMatrix):
#     root = "components/" + website + "/" + cls + "/"
#
#     for var in [1]:
#         output = open("scores/" + website + "_" + cls + "varient_" + str(var) + ".csv", "a+")
#
#         for img0 in imageMatrix[0]:
#             img0_ = cv2.imread(root + "0/" + img0)
#             highest = [0,"None"]
#             if highest[0]==1: continue
#
#             for img1 in imageMatrix[var]:
#                 img1_ = cv2.imread(root + str(var) + "/" + img1)
#                 s = imageCompare(img0_,img1_)
#
#                 if s>highest[0]:
#                     highest = [s,img1]
#
#             # print (highest)
#
#
#             output.write (("original: "+img0) + "," + ("matched: "+highest[1])+ "," +("score: "+str(highest[0])))
#             output.write("\n")
#
#
# websites = os.listdir("components")
# imageMatrix = []
# websites = RemoveTempFolders(websites)
#
# for website in websites:
#     classes = os.listdir("components/"+website)
#     classes = RemoveTempFolders(classes)
#
#     for cls in classes:
#         varients = os.listdir("components/"+website+"/"+cls)
#         varients = RemoveTempFolders(varients)
#
#         imageMatrix = []
#
#         for varient in ["/0","/1","/2"]:
#             images = os.listdir("components/"+website+"/"+cls+varient)
#             images = RemoveTempFolders(images)
#             imageMatrix.append(images)
#
#         print ("scoring", cls)
#         score (website, cls, imageMatrix)
