from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import os
import csv
import datetime
import os
import numpy as np
import zipfile


profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2) 
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', 'C:\titititit\Descargas')
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip')

path=os.getcwd()
driver=webdriver.Firefox(profile)
url= "https://www.electrobuzz.net/category/techno/"
driver.get(url)

pre_links= driver.find_elements_by_css_selector("div:nth-child(1) > h2:nth-child(2) > a:nth-child(1)")
total_pags=driver.find_element_by_css_selector("a.page-numbers:nth-child(5)").get_attribute('text').replace(',','')

pags=np.arange(0,4,step=1)
links=['urls']

for j in np.arange(0,len(pre_links),step=1):
  
  links.append(pre_links[j].get_attribute('href')) 


for i in pags:
  url_loop= 'https://www.electrobuzz.net/category/techno/page/' + str(i) + '/'
  driver.get(url_loop)
  pre_links= driver.find_elements_by_css_selector("div:nth-child(1) > h2:nth-child(2) > a:nth-child(1)")
  
  for j in np.arange(0,len(pre_links),step=1):
    
    links.append(pre_links[j].get_attribute('href')) 


file=os.getcwd()+'\urls.csv'

with open(file, 'wb') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerow(links)


