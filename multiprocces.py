import multiprocessing
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

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2) 
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', 'C:\titititit\Descargas')
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip')

os.chdir('C:\\Users\\Oscar\\Documents\\Tec')
path=os.getcwd()
driver=webdriver.Firefox(profile)
url= "https://www.electrobuzz.net/"
driver.get(url)

pre_links= driver.find_elements_by_css_selector("div:nth-child(1) > h2:nth-child(2) > a:nth-child(1)")
total_pags=driver.find_element_by_css_selector("a.page-numbers:nth-child(5)").get_attribute('text').replace(',','')

pags=np.arange(2,int(total_pags),step=1)
links=['urls']

for j in np.arange(0,len(pre_links),step=1):
  
  links.append(pre_links[j].get_attribute('href')) 




file=os.getcwd()+'\\1.csv'
with open(file, 'wb') as myfile:
       wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
       wr.writerow(links)
       
       
vectores_pags=list(chunks(pags, 1000))



#Abrimos ventanas en blanco, tantas como vectores halla  
for i in np.arange(1,len(vectores_pags)): 
   driver.execute_script("window.open('');")



a=driver.window_handles
b=np.arange(0,len(a))

listas_multi=zip(vectores_pags,b)

def electrobuzz(vector_pags, num):
    
  current= driver.switch_to_window(num)
  links=['urls']
  
  for i in vector_pags:
    url_loop= 'https://www.electrobuzz.net/page/' + str(i) + '/'
    current.get(url_loop)
    pre_links=  current.find_elements_by_css_selector("div:nth-child(1) > h2:nth-child(2) > a:nth-child(1)")
      
  for j in np.arange(0,len(pre_links),step=1):

    links.append(pre_links[j].get_attribute('href')) 

  name= str(vector_pags[0])
  file=os.getcwd()+'\\' + name + 'csv'
  
  with open(file, 'wb') as myfile:
       wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
       wr.writerow(links)

  
  





from multiprocessing import Pool (8) as pool

if __name__ == "__main__":
    resutl=pool.apply_async(electrobuzz,listas_multi)
