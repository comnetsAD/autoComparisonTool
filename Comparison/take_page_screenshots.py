import requests, csv, os, time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import cv2

# Importing URLs
# URLs = ["https://www.head-fi.org",
#         "https://www.military.com",
#         "https://www.metafilter.com",
#         "https://www.nrl.com",
#         "https://www.prevention.com,"
#         "https://www.nascar.,com"
#         "https://www.elle.com",
#         "https://phys.org",
#         "https://www.dslrepor,ts.com"
#         "https://www.abc.net.au"
#         "https://www.voanews.com",
#         "https://www.ted.com",
#         "https://uncrate.com",]
URLs = []
with open('URLs.txt', 'r') as f:
    URLs = f.read().split()

# varients = ["","/index55.html","/index60.html"]
options = Options()

fp1 = webdriver.FirefoxProfile("/Users/Jacinta/Library/Application Support/Firefox/Profiles/kciui8dl.default")
fp2 = webdriver.FirefoxProfile("/Users/Jacinta/Library/Application Support/Firefox/Profiles/7irvo3ii.Simplified")
driver1 = webdriver.Firefox(options=options, firefox_profile=fp1)
driver2 = webdriver.Firefox(options=options, firefox_profile=fp2)
driver1.set_window_size(1400, 900)
driver2.set_window_size(1400, 900)
drivers = [driver1, driver2]

for link in URLs:
    folderName = '-'.join(link[8:].split('.')[-2:])
    for i, driver in enumerate(drivers):

        #################################
        ### 1. Extracting Source code ###
        #################################
        # if os.path.exists("ss/" + folderName + "/" + str(i)):
        #     continue
        if i == 0:
            driver.get(link)
        elif link[-1] == "/":
            driver.get(link + "JSCleaner.html")
        else:
            driver.get(link + "/JSCleaner.html")

        try:

            soup = bs(driver.page_source.encode("utf-8"),"lxml")

            output = open('unedited.txt', mode='w')
            # output = csv.writer(restaurant_output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            output.write(str(soup))

            #######################################
            ### 2. Screenshot ###
            #######################################
            j = 1
            lastHeight = -1
            while j < 5 and lastHeight != driver.execute_script("return window.scrollY"):
                try:
                    # take a screenshot and store it
                    if not os.path.exists("ss/" + folderName):
                        os.mkdir("ss/" + folderName)
                        os.mkdir("ss/" + folderName + "/0")
                        os.mkdir("ss/" + folderName + "/1")
                    ssPath = "ss/" + folderName + "/" + str(i) + "/screenshot{}.png".format(j)
                    driver.save_screenshot(ssPath)
                    print ("Capturing Screenshot #", j, "for", link)
                    lastHeight = driver.execute_script("return window.scrollY")

                    # scroll down
                    scrollScript = "setTimeout(function(){window.scrollBy(0," + str(driver1.get_window_size()['height']) + ");}, 2000);"
                    driver.execute_script(scrollScript)
                    time.sleep(2)
                    j = j + 1
                except Exception as e:
                    print (str(e))

        except Exception as e:
            print(str(e))
            pass
driver1.close()
driver2.close()
