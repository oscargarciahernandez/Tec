#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 18:51:01 2019

@author: oscar
"""


from bs4 import BeautifulSoup
import requests
import shutil
import numpy as np
import os
import random
from random import choice
import re
import time
import csv
from itertools import chain
import multiprocessing as mp


#DESCARGAR PEDAZO DE LISTA DE USER AGENTS        
def get_user_agents():
    #INICIAMOS SESSIOIN REQUESTS Y DECIMOS QUE PASE DEL ENV... PROBLEMAS CON PROXY
    session = requests.Session()
    session.trust_env = False
    
    #DESCARGAMOS LISTA Y PARSEAMOS CON BS4
    user_agents= session.get('http://www.useragentstring.com/pages/useragentstring.php?typ=Browser')
    user_soup = BeautifulSoup(user_agents.content, 'html.parser')
    user_soup1=user_soup.find_all('ul')
    
    #EXTRAEMOS LA INFO DE USER-AGENTS
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



         
def GET_COSMOBOX_URL(users_list, read_url):
    
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
            req= session.get(url,
                              headers=ua)
            
            if req.status_code == requests.codes.ok:
                break
        except:
            pass
        print('invalid UserAgent')
        fail=fail+1
        if fail>10:
            break
        
    #TRATAMOS EL REQUESTS COMO TEXTO Y BUSCAMOS LA URL DE COSMOBOX
    m = re.findall('https://cosmobox.org/' \
               '[^\"]+' , req.text)
    m1 = list(set(m))
    print(m1)
    return m1
    

#FUNCIÓN MAIN... AKI SE ABORDA LA PARALELIZACIÓN DE LA MOVIDA
def main():
    ### LEEMOS URL'S DE ELECTROBUZZ
    read_urls= []
    file=os.getcwd() + "/urls_190619.csv"
    with open(file, 'rt') as myfile:
         wx = csv.reader(myfile)
         for x in wx:
             read_urls.append(x)
    
    #DESCARGAMOS USER AGENTS 
    users_list= get_user_agents()  
    
    #PARALELIZAMOS EMPLEANDO POLL.STARMAP CON TODOS LOS NÚCLUES -1        
    pool = mp.Pool(mp.cpu_count()-1)
    results = pool.starmap(GET_COSMOBOX_URL, [(users_list,read_urls[k]) for k in np.arange(0,len(read_urls))])
    
    #MATAMOS SUBPROCESOS 
    pool.terminate()
    pool.join()
    #GUARDAMOS RESULTADOS EN UN CSV
    file= os.getcwd() + "/urls_cosmo_multi.csv"
    with open(file, 'wt') as myfile:
         wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
         for x in np.arange(0,len(results)):
             wr.writerow([results[x]])
             
             

#AL ATAQUE        
if __name__ == '__main__':
    main()
    


