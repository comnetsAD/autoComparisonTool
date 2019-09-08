#####
#####  1. Aim:
#####           a/ Normalise -> Set background as 0 and everything else in their primary colors
#####           b/ find disconnected components
#####

# import the necessary packages
import cv2, os
import numpy as np
import skimage
import scipy.misc
from matplotlib import pyplot as plt

def makeFolders():
    websites = os.listdir("ss")
    websites = RemoveTempFolders(websites)
    for website in websites:
        if website == "faa-gov": continue
        print (website)
        varients = os.listdir("ss/"+website)
        varients = RemoveTempFolders(varients)
        imageMatrix = []
        for varient in varients:
            imageMatrix.append([])
            images = os.listdir("ss/"+website+"/"+varient)
            images = RemoveTempFolders(images)
            for image in images:
                imageMatrix[int(varient)].append(image)

        for image in imageMatrix[0]:
                paths = ["ss/" + website + "/0/" + image,
                         "ss/" + website + "/1/" + image,
                         "ss/" + website + "/2/" + image]

                for loc in paths:
                        try:
                            os.mkdir("components/" + loc.split("/")[1])
                        except:
                            pass
                        try:
                            os.mkdir("components/" + loc.split("/")[1] + "/" + loc.split("/")[-1].split(".")[0])
                        except:
                            pass
                        try:
                            os.mkdir("components/" + loc.split("/")[1] + "/" + loc.split("/")[-1].split(".")[0] + "/" + loc.split("/")[-2])
                        except:
                            pass

def RemoveTempFolders(someList):
    for item in someList:
        if item[0] == ".":
            someList.remove(item)
    return someList

def normalise(img, background = [255,255,255]):
    # change background to black(0)
    # transorm the rest of the pixels to
    # monotone for easier comparison later
    black = 0
    white = 255
    k = 0
    l=0
    for i in range(len(img)):
        for j in range(len(img[0])):
            if list(img[i][j]) == background:
                img[i][j] = black
                l+=1
            else:
                img[i][j] = white
                k+=1
    print (k,l)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


def breakIntoComponents (img0):
    # print ("Normalising Image \t")
    img0_norm = normalise(img0)

    save_dir = ("components/" + loc.split("/")[1] + "/" +  loc.split("/")[-1].split(".")[0] + "/" + loc.split("/")[-2] + "/")
    cv2.imwrite(save_dir+"normalised.jpg" , img0_norm)

    # img0_norm = cv2.adaptiveThreshold(img0,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,115,1)
    # _, img0_norm = cv2.threshold(img0, 155, 255, cv2.THRESH_TOZERO_INV)
    # cv2.imwrite("123.jpg", img0_norm)

    # dilate components: this will join the nearby components for them to be grouped
    img0_dil = cv2.dilate (img0_norm,np.ones((20,20)))

    labels, markers = cv2.connectedComponents(img0_dil.astype(np.uint8),connectivity=8)

    # print (labels)

    img0_mask = skimage.measure.label(markers, background = 0).flatten()

    for i in range (1,labels,1):
        component = np.where(img0_mask==i)[0]
        # print ("Saving Comp #", i)
        saveComponent(component,markers.shape,i)

def crop(mask):
    cv2.imwrite ('temp.jpg', mask)
    img = cv2.imread('temp.jpg')
    os.remove('temp.jpg')

    # print (img.shape,img1.shape)

    # img = cv2.cvtColor(img1,cv2.COLOR_GRAY2BGR)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,1,255,cv2.THRESH_BINARY)

    contours = [cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)]
    cnt = contours[0][0]
    x,y,w,h = cv2.boundingRect(cnt)

    crop = (cv2.imread (loc))[y:y+h,x:x+w]

    # cv2.imwrite("1.jpg",imgOrg)

    return crop

def saveComponent (comp,shape,label):
    nChannels = 3 #RGB
    sizeForFlatten = shape[0]*shape[1]
    originalImage = imgOrg.flatten().reshape(sizeForFlatten , nChannels)

    mask = np.zeros(sizeForFlatten * nChannels).reshape(sizeForFlatten , nChannels)
    for c in comp:
        mask[c] = originalImage[c]

    # mask = cv2.erode(mask, np.ones((50, 50)))

    mask = mask.reshape(shape[0],shape[1],nChannels)

    mask = crop(mask)

    if len(mask.flatten()) < 20:
        print ("component too small")
    else:
        # print ("writing image")
        save_dir = ("cmp2/")
        cv2.imwrite(save_dir + str(label) + ".jpg" , mask)

# websites = os.listdir("ss")
# imageMatrix = []
#
# websites = RemoveTempFolders(websites)
# makeFolders()
# i=0
#
# for website in websites:
#     # List and Normalise
#     varients = os.listdir("ss/"+website)
#     varients = RemoveTempFolders(varients)
#     for varient in varients:
#
#         imageMatrix.append([])
#         # List and Normalise
#         images = os.listdir("ss/"+website+"/"+varient)
#         images = RemoveTempFolders(images)
#
#         for image in images:
#             imageMatrix[int(varient)].append(image)
#
#     diffMatrix = [imageMatrix[0],[],[]]
#
#     j = 0
#     for image in imageMatrix[0]:
#
#         # i += 1
#         # print (i)
#         # if i < 9: continue
#
#         paths = ["ss/" + website + "/0/" + image,
#                  "ss/" + website + "/1/" + image,
#                  "ss/" + website + "/2/" + image]
#
#         # print (paths)
#
#         for loc in paths:
#                 print (loc.split("/")[1] + "\t" +  loc.split("/")[-1].split(".")[0])
#                 if os.path.isfile(loc):

loc = "/Users/waleed/Desktop/JS-Reseach/Comparison/ss/faa-gov/2/screenshotdiv-id-faaModal.png"
imgOrg = cv2.imread (loc)

cv2.imwrite ("cmp2/nor.jpg",imgOrg)
# a = input ("s")

breakIntoComponents(imgOrg)
