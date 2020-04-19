import bs4
from urllib.request import urlopen as uReq
from urllib.request import Request,urlopen
from bs4 import BeautifulSoup as soup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random
import time
import pandas as pd


'''
****set up
###
This part of the code starts a webdriver with settings we want for us to connect to it later on.
###


from selenium import webdriver

options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options, executable_path=r'/Users/limbangjin/Downloads/chromedriver_2')
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})
driver.execute_cdp_cmd("Network.enable", {})
driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browser1"}})
driver.command_executor._url
driver.session_id


'''


page =  1

#connect remotely using obtained session id and ip address
driver = webdriver.Remote('IP Address Here',{})
driver.session_id = 'Session ID Here'

#website to scrap , continue from page
my_url = "https://www.propertyguru.com.sg/property-for-sale/" + str(page)
driver.get(my_url)


while True:

    dataFrame = pd.read_json("/Users/limbangjin/Documents/property_raw_data.JSON")
    
    html = driver.execute_script("return document.documentElement.outerHTML")
    sel_soup= soup(html,"html.parser")
    container = sel_soup.findAll("div",{"class":"col-xs-12 col-sm-7 listing-description"})
    #container contains our listing description
    for x in container:
            
            Building = x.find("h3",{"class":"ellipsis"}).text
            Address = x.find("p",{"class":"listing-location ellipsis"}).text
            
            
            Price = x.find("li",{"class":"list-price pull-left"}).text
            
            #to check if is a normal house with bedroom and bathroom
            BedBath = x.find("li",{"class":"listing-rooms pull-left"}).text.split()
            if len(BedBath) != 2 :
                continue
            else:
                for z in BedBath:
                    if z.isdigit():
                        pass
                    else:
                        continue
            Bedroom = BedBath[0]
            Bathroom = BedBath[1]
            #
            if len((x.findAll("li",{"class":"pull-left"}))) != 7:
                continue
            Sqft = x.find("li",{"class":"listing-floorarea pull-left"}).text
            PSF = x.findAll("li",{"class":"listing-floorarea pull-left"})[1].text.replace('\xa0',' ')
            Type = x.findAll("li",{"class":"pull-left"})[4].text 
            Tenure = x.findAll("li",{"class":"pull-left"})[5].text
            
            BuiltOn = x.findAll("li",{"class":"pull-left"})[6].text.replace('Built: ','')
            
            toAdd = pd.Series({"Building Name":Building,
                               "Address":Address,
                               "Price":Price,
                               "Number of Bedroom":Bedroom,
                               "Number of Bathroom":Bathroom,
                               "Land Area":Sqft,
                               "Price per sqft":PSF,
                               "Type":Type,
                               "Tenure":Tenure,
                               "Built On":BuiltOn})

            dataFrame = dataFrame.append(toAdd,ignore_index = True)
                               
            

    #save data to our propertyguru file
    print(dataFrame)
    dataFrame.to_json("/Users/limbangjin/Documents/property_raw_data.JSON")
    print("Saved successfully page:",page)
    
    #go to next page
    page+=1
    #since next page button can be identified by page number from html
    python_button = driver.find_element_by_link_text(str(page))
    python_button.click()
    time.sleep(3)
    #my_url = "https://www.propertyguru.com.sg/property-for-sale/" + str(count)
    #driver.get(my_url)
    #count+=1
    print ("Went to next page")
    




