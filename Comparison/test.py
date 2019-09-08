import requests, csv, os, time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import cv2


# file with additional functions
import functions


# Importing URLs
URLs = ['https://www.faa.gov']
varients = ["","/index55.html","/index60.html"]

for link in URLs:
    folderName = '-'.join(link.split('.')[-2:])
    for proxyVarient in varients:

        # makes callable url
        URL = link + proxyVarient

        #################################
        ### 1. Extracting Source code ###
        #################################
        options = Options()
        profile = webdriver.FirefoxProfile('/Users/waleed/Library/Application Support/Firefox/Profiles/dmopb59z.default-release')
        driver = webdriver.Firefox(profile, options=options, executable_path="/Users/waleed/Desktop/JS-Reseach/Comparison/driver/geckodriver")
        # driver = webdriver.Firefox(options=options, executable_path="/Users/waleed/Desktop/JS-Reseach/Comparison/driver/geckodriver")
        driver.get(URL)

        soup = bs(driver.page_source.encode("utf-8"),"lxml")

        output = open('unedited.txt', mode='w')
        # output = csv.writer(restaurant_output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        output.write(str(soup))

        IDs = []
        classes = []

        for tag in ["nav","li","ul","div","p","span","h1","h2","h3","h4","h5","h6","p","button"]:
            tags = soup.findAll (tag)
            for t in tags:
                # storing all div's IDs
                try:
                    id = t.get('id')
                    # print (id)
                    if id != None and (not id in IDs) and (type(id)==type('str') or (type(id)==type(['list']) and len(id)==1)):
                        if type(id) == type([]):id = id[0]
                        IDs.append([tag,id])
                except:
                    pass
                # storing all div's classes
                try:
                    cl = t.get('class')
                    # print (cl,type(cl))
                    if cl != None and (not cl in classes) and (type(cl)==type('str') or (type(cl)==type(['list']) and len(cl)==1)) :
                        if type(cl) == type([]):cl = cl[0]
                        classes.append([tag,cl])
                except:
                    pass

        #######################################
        ### 2. Find elements and Screenshot ###
        #######################################
        for id in IDs:
            try:
                # find element in the code
                elem = driver.find_element_by_id(id[1])

                # get y position and scroll to that location
                location = elem.location.get('y')
                scrollScript = "setTimeout(function(){window.scrollTo(0," + str(location) + ");}, 2000);"
                driver.execute_script(scrollScript)
                time.sleep(.5)

                # hover over that element
                actions = ActionChains(driver)
                driver.execute_script("arguments[0].scrollIntoView();", elem)
                actions.move_to_element(elem)
                actions.perform()

                # take a screenshot and store it
                if not os.path.exists("ss/" + folderName):
                    os.mkdir("ss/" + folderName)
                    os.mkdir("ss/" + folderName + "/0")
                    os.mkdir("ss/" + folderName + "/1")
                    os.mkdir("ss/" + folderName + "/2")
                ssPath = "ss/" + folderName + "/" + str(varients.index(proxyVarient)) + "/screenshot{}.png".format(id[1])
                driver.save_screenshot(ssPath)
                print ("Capturing Screenshot for ID =", id[1])
                time.sleep(.5)
            except:
                print ("Error parsing ID =", id[1])


        for cl in classes:
            try:
                # find element in the code
                elem = driver.find_element_by_class_name(cl[1])

                # get y position and scroll to that location
                location = elem.location.get('y')
                scrollScript = "setTimeout(function(){window.scrollTo(0," + str(location) + ");}, 2000);"
                driver.execute_script(scrollScript)
                time.sleep(.5)

                # hover over that element
                actions = ActionChains(driver)
                driver.execute_script("arguments[0].scrollIntoView();", elem)
                actions.move_to_element(elem)
                actions.perform()

                # take a screenshot and store it
                if not os.path.exists("ss/" + folderName):
                    os.mkdir("ss/" + folderName)
                    os.mkdir("ss/" + folderName + "/0")
                    os.mkdir("ss/" + folderName + "/1")
                    os.mkdir("ss/" + folderName + "/2")
                ssPath = "ss/" + folderName + "/" + str(varients.index(proxyVarient)) + "/screenshot{}.png".format(id[1])
                driver.save_screenshot(ssPath)
                print ("Capturing Screenshot for Class =", cl[1])
                time.sleep(.5)
            except:
                print ("Error parsing Class =", cl[1])

        driver.close()
