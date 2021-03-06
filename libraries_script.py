#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 13:40:08 2019

@author: oscar
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import csv
import numpy as np
import time
import requests
from bs4 import BeautifulSoup
import random
import re
import shutil
from difflib import SequenceMatcher
import rarfile
import zipfile




# SIN USO AKI PERO NECESARIOS EN MAIN_SCRIPT
# ERÁ NECESARIO HACER MÁS FUNCIONES Y QUE EL MAIN SCRIPT ESTÉ MÁS LIMPIO
import sys
from datetime import date
import csv    
import tqdm
import multiprocessing as mp
from  itertools import chain
#DESCARGAR PEDAZO DE LISTA DE USER AGENTS 

def get_user_agents2():
    
    session = requests.Session()
    session.trust_env = False
    url='https://developers.whatismybrowser.com/useragents/explore/software_type_specific/web-browser/'       
    user_agents= session.get(url)
    soup= BeautifulSoup(user_agents.content, 'html.parser')
    soup2= soup.find_all('td')
    soup3=[]     
    for item2 in soup2:
        if item2.find_all('a'):
            soup3.append(item2.find_all('a')[0].text)
    return soup3




def get_user_agents():
    session = requests.Session()
    session.trust_env = False
    user_agents= session.get('http://www.useragentstring.com/pages/useragentstring.php?typ=Browser')
    user_soup = BeautifulSoup(user_agents.content, 'html.parser')
    user_soup1=user_soup.find_all('ul')
    
    users_list=[]
    for i in np.arange(0,len(user_soup1)):
        user_soup2= user_soup1[i].find_all('a')
        for j in np.arange(0,len(user_soup2)):
            users_list.append(user_soup2[j].text)
            
    return users_list

#PONER USER AGENTS EN FORMATO PARA HEADERS
def set_user_agents(users_list, n):
    headers = {'User-Agent': str(users_list[n])}
    return headers



def GET_ELECTROBUZZ_URLS(merge_inputs):
    users_list= merge_inputs[0]
    k= merge_inputs[1]
    
    
    fail=1
    while True:
            try:
                ua=set_user_agents(users_list,random.randrange(0, len(users_list)))
                url='https://www.electrobuzz.net/page/' + str(k) +'/'
                req= requests.get(url,
                                  headers=ua)
                
                if req.status_code == requests.codes.ok:
                    break
            except:
                pass
            #print('invalid UserAgent')
            fail=fail+1
            if fail>10:
                break
    
    lista_nombres= []
    for nombres in lista_busquedaF:
        lista_nombres.append(nombres.split('/')[-2])   
           

            
            
    primary= re.search('primary(.*)',req.text.replace("\n","")).group(1)
    m = re.findall('https://www.electrobuzz.net/[0-9]'
               '[^\"]+' , primary)
    m1 = list(set(m))
    return m1

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
    
#MERGE INPUTS2 NECESITA USER AGENTS Y LA BUSQUEDA
def GET_ELECTROBUZZ_URLS_BY_SEARCH(merge_inputs2, REMOVE_VA_and_BEATPORT= True, EXTRICT_ARTIST= True):
    users_list= merge_inputs2[0]
    busqueda= merge_inputs2[1].replace(" ", "+")
    
    lista_busqueda= []
    k=1
    fail=1
    while True:
            try:
                ua=set_user_agents(users_list,random.randrange(0, len(users_list)))
                url='https://www.electrobuzz.net/page/' + str(k) +'/?s=' + busqueda 
                req= requests.get(url,
                                  headers=ua)
                
                if req.status_code == requests.codes.ok:
                                
                    primary= re.search('primary(.*)',req.text.replace("\n","")).group(1)
                    m = re.findall('https://www.electrobuzz.net/[0-9]'
                               '[^\"]+' , primary)
                    m1 = list(set(m))
                    lista_busqueda.append(m1)
                    k= k+1
            except:
                pass
            #print('invalid UserAgent')
            fail=fail+1
            if fail>10:
                break
            
    lista_busquedaF = []
    for sublist in lista_busqueda:
        for item in sublist:
            lista_busquedaF.append(item)
                
    lista_nombres= []
    for nombres in lista_busquedaF:
        lista_nombres.append(nombres.split('/')[-2])   
    
    if REMOVE_VA_and_BEATPORT:
        remove_list= [item for item in lista_nombres for item2 in item.split("-") if item2=='va' or item2=='beatport']
        if len(remove_list)>0: 
            for item in remove_list:
                if item in lista_nombres:
                    lista_nombres.remove(item)
    
    if EXTRICT_ARTIST:
        '''
        METODO 1
        
        BUSCA SIMILARIDAD ENTRE EN EL INPUT Y EL NOMBRE DEL ALBUM
        '''
        
        #LISTA_SOLO_BUSQUEDA= [item for item in lista_nombres for item2 in item.split("-") for item3 in merge_inputs2[1].split(" ") if similar(item3.lower(), item2)> 0.8]
        
        '''
        METODO 2
        
        MIRA QUE NUESTRA BUSQUEDA SE ENCUENTRE EXTRICTAMENTE DENTRO DEL NOMBRE DEL ALBUM
        
        '''
        LISTA_SOLO_BUSQUEDA= [item for item in lista_nombres if busqueda.replace(' ', "-").lower() in item ]

        
        
    else:
        LISTA_SOLO_BUSQUEDA=lista_nombres
        
    LISTA_SOLO_BUSQUEDA= list(set(LISTA_SOLO_BUSQUEDA))
    LISTA_URLS= [item for item in lista_busquedaF for item2 in item.split("/") if item2 in LISTA_SOLO_BUSQUEDA]
    
        
     
            

    return LISTA_URLS
    
  
    


      
def GET_COSMOBOX_URL(merge_inputs):
    users_list= merge_inputs[0]
    read_url= merge_inputs[1]
    
    #SI FALLA VUELVE A INTENTARLO CAMBIANDO EL USER-AGENT--- ASI HASTA 10 VECES
    fail=1
    while True:
        try:
            #SETEAMOS USER AGENTS Y LA URL PARA QUE REQUESTS NO FALLE
            ua=set_user_agents(users_list,random.randrange(0, len(users_list)))
            url1= read_url
            url=str(url1).replace('[\'', '' ).replace('\']', '')
            
            #CREAMOS SESION E IGNORAMOS ENV... PROBLEMA PROXY
            session = requests.Session()
            session.trust_env = False
            req= session.get(url,headers=ua)
            
            if req.status_code == requests.codes.ok:
                break
        except:
            pass
        #print('invalid UserAgent')
        
        fail=fail+1
        if fail>10:
            break
        '''
        with lock:
            progress= tqdm.tqdm(total= Ntotal, position= pos)
        for _ in range(0, Ntotal, 5):
            with lock:
                progress.update(5)
                time.sleep(0.1)
        with lock:
            progress.close()
        '''
    Contenido=[]
    #CONSEGUIR ARTISTA 
    '''
    ARTISTA= re.search(r'ARTIST\(S\):</span>(.*?)</p>', req.text).group(1)
    SONGS=  re.search(r'greyf12(.*?)</ol>', req.text.replace("\n","")).group(1)
    SONG_ART= re.findall(r'<strong>(.*?)</strong>',SONGS)
    SONG_NAME= re.findall(r'\;(.*?)</li>',SONGS)
    
    Contenido.extend([read_url, m1, ARTISTA, list(zip(SONG_ART, SONG_NAME))])

    '''
    #TRATAMOS EL REQUESTS COMO TEXTO Y BUSCAMOS LA URL DE COSMOBOX
    m = re.findall('https://cosmobox.org/' \
               '[^\"]+' , req.text)
    m1 = list(set(m))
    Contenido.extend([read_url, m1])
    #print(m1)
    return Contenido


def LOGIN_COSMOBOX_AND_DOWNLOAD(LISTA_COSMO_URL, PATH_DOWNLOAD):
    
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2) 
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', PATH_DOWNLOAD)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip')
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/download')
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream')
    
        
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
    

    ###TRAS REGISTRARNOS ABRIMOS UNA VENTANA NUEVA, PARA EMPEZAR A DESCARBGAR MOVIDAS
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    
    for i in range(len(LISTA_COSMO_URL)):
        p=re.sub('[\[\]\'\"]','', str(LISTA_COSMO_URL[i]))
        driver.get(p)
        
        
        #TRY PARA ASEGURARNOS DE QUE EXISTE EL ARCHIVO
        # EN COSMOBOX HAY MUCHOS ARCHIVOS CAIDOS QUE YA NO EXISTEN
        try: 
            
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.text-danger')))
            print('ERROR 404: YA NO EXISTE EL ARCHIVO')
        except TimeoutException:
            
            #SI EL ARCHIVO EXISTE LO DESCARGAMOS Y LISTO
            css_DOWNLOAD= 'div.col-md-12:nth-child(10) > button:nth-child(1)'
            DOWN = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_DOWNLOAD)))
            DOWN.click()
            print('Descargando ' + str(LISTA_COSMO_URL[i]))
            
            
     
    time.sleep(10)
    while True:
        FILES= os.listdir(PATH_DOWNLOAD)
        if '.part' in str(FILES):
            time.sleep(5)
        else: 
            break
    driver.close()
    driver.quit()
    BORRAR_ARCHIVOS_REPETIDOS(PATH_DOWNLOAD)
    

        
def LIMPIAR_CARPETA(PATH_CARPETA):
    shutil.rmtree(PATH_CARPETA)
    
    
def BORRAR_ARCHIVOS_REPETIDOS(PATH_DOWNLOAD):
    
    #BORRAMOS LAS DESCARGAS REPETIDAS
    REPEATED_FILES= [item for item in os.listdir(PATH_DOWNLOAD) if '(1).' in item or '(2).' in item or '(3).' in item ]
    for i in REPEATED_FILES:
        os.remove(PATH_DOWNLOAD + '/' + i)






#UNZIPINGGGG
        
def FLASH_DRIVE_PATH_DOWNLOAD():
    PATH_MEDIA= '/media/oscar/'
    pen_drive= os.listdir(PATH_MEDIA)
    
    if pen_drive:
        PATH_DOWNLOAD= PATH_MEDIA + pen_drive[0] + '/DESCARGAS_COSMOBOX'
    else: 
        PATH_DOWNLOAD= os.getcwd() + '/DESCARGAS_COSMOBOX'
    
    return PATH_DOWNLOAD



def BORRAR_ARCHIVOS_CORRUPTOS(PATH):  
    '''
    ELIMINAMOS .part POR POSIBLES ERRORES DE EJECUCIONES PASADAS
    QUE VAYAN A AFECTAR A LA FUNCION DE DESCARGA.... QUE ESPERA 
    HASTA QUE NO EXISTAN .PARTS... ES DECIR HASTA QUE TODAS LAS DESCARGAS
    ESTEN COMPLETAS
    
    '''
    FILES= os.listdir(PATH)
    PART_FILES = [item for item in FILES if '.part' in item]
    for i in PART_FILES:
        os.remove(PATH + '/'+i)
            

def UNZIP(PATH_ZIP): 
    
    for i in [item for item in os.listdir(PATH_ZIP) if '.zip' in item]:
        PATH_TO_ZIP_FILE= PATH_ZIP + i
        with zipfile.ZipFile(PATH_TO_ZIP_FILE, 'r') as zip_ref:
            zip_ref.extractall(PATH_ZIP)



def UNRAR(PATH_RAR):
    for rar in [item for item in os.listdir(PATH_RAR) if '.rar' in item]:
        filepath = os.path.join(PATH_RAR, rar)
        opened_rar = rarfile.RarFile(filepath)
        
        '''
        # POR SI QUEREMOS SACAR INFORMACION CONTENIDAD EN EL RAR
        # NOMBRE DE FICHEROS Y TAMAINO
        for f in opened_rar.infolist():
            print (f.filename, f.file_size)
            
        '''
        opened_rar.extractall(filepath.replace('.rar', ''))
