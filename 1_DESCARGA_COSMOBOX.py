from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import csv
import datetime
import os
import numpy as np
import zipfile
import re


profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2) 
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', os.getcwd())
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip')
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/download')
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream')

def LOGIN_COSMOBOX():
    
    driver=webdriver.Firefox(profile)
    url= "https://cosmobox.org"
    driver.get(url)
    
    ### Login attr sin necesidad de que esten en la nube.. xd
    login= []
    file=os.getcwd()+'/login.txt'
    with open(file, 'rt') as myfile:
         wx = csv.reader(myfile)
         for x in wx:
             login.append(x)
    
    usr=str(re.search('usr= (.*)',str(login[0])).group(1).replace('\']', ""))
    password=re.search('pass= (.*)',str(login[1])).group(1).replace('\']', "")
    
    #HEMOS AÑADIDO COSITAS PARA QUE NO DE ERRORES A LA HORA DE ENCONTRAR ELEMENTOS... WEBDRIVERWAIT
    #PULSAR BOTON DE REGISTRASE
    css_login= "#topnav > div.topbar-main > div > div.menu-extras > ul > li:nth-child(6)"
    log_open = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_login)))
    log_open.click()
    
    
    #SUBIR USUARIO
    css_caja_login= '#login > div > div > div.account-bg > div > div.m-t-10.p-20 > form > div:nth-child(5) > div > input'
    caja_user = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_caja_login)))
    caja_user.send_keys(Keys.CONTROL + "a")
    caja_user.send_keys(Keys.DELETE)
    caja_user.send_keys(usr)
    
    
    #SUBIR CONTRASEÑA
    css_caja_pass= '#login > div > div > div.account-bg > div > div.m-t-10.p-20 > form > div:nth-child(6) > div > input'
    caja_pass = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_caja_pass)))
    caja_pass.send_keys(Keys.CONTROL + "a")
    caja_pass.send_keys(Keys.DELETE)
    caja_pass.send_keys(password)
    
    #PULSAR BOTON DE LOGIN 
    css_pushlog='#login > div > div > div.account-bg > div > div.m-t-10.p-20 > form > div.form-group.text-center.row.m-t-10 > div > button'
    log = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_pushlog)))
    log.click()
    return driver

def DOWNLOAD_ZIP(LISTA_COSMO_URL):    
    driver= LOGIN_COSMOBOX()
    ###TRAS REGISTRARNOS ABRIMOS UNA VENTANA NUEVA, PARA EMPEZAR A DESCARBGAR MOVIDAS
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    for i in np.arange(0, len(LISTA_COSMO_URL)):
        p=re.sub('[\[\]\'\"]','', str(LISTA_COSMO_URL[i]))
        driver.get(p)
        
        try: 
            WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.text-danger')))
            print('ERROR 404: YA NO EXISTE EL ARCHIVO')
        except TimeoutException:
            css_DOWNLOAD= 'div.col-md-12:nth-child(10) > button:nth-child(1)'
            DOWN = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_DOWNLOAD)))
            DOWN.click()
            print('Descargando ' + str(LISTA_COSMO_URL[i]))
            
    driver.close()
    driver.quit()
        
    
def main(): 
    cosmo_url= []
    file=os.getcwd()+'/urls_cosmo_multi.csv'
    with open(file, 'rt') as myfile:
         wx = csv.reader(myfile)
         for x in wx:
             cosmo_url.append(x)
             
    DOWNLOAD_ZIP(cosmo_url[0:20])
    


#AL ATAQUE        
if __name__ == '__main__':
    main()
