# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 23:58:11 2019

@author: Oscar
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


#DESCARGAR PEDAZO DE LISTA DE USER AGENTS        
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






users_list= get_user_agents()        

while True:
            try:
                ua=set_user_agents(users_list,random.randrange(0, len(users_list)))
                req= requests.get('https://www.electrobuzz.net/',
                                  headers=ua)
                
                if req.status_code == requests.codes.ok:
                    break
            except:
                pass
            print('invalid UserAgent')


req.content          



m = re.findall('https://www.electrobuzz.net/[0-9]'
               '[^\"]+' , req.text)

m1 = list(set(m))


mp = re.findall('https://www.electrobuzz.net/page/([0-9]+)' , req.text)

pages=int(mp[2])


link_list= []
k=2
while True:
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
            print('invalid UserAgent')
            fail=fail+1
            if fail>10:
                break
    if fail>10:
        break
            
            
           
    m = re.findall('https://www.electrobuzz.net/[0-9]'
               '[^\"]+' , req.text)
    m1 = list(set(m))
    
    if(len(m1)==0):
        break
    link_list.append(m1)
    time.sleep(random.random()/20)
    print(str(k))
    k=k+1
    
    
# Esto lo que hace es comvertir la lista de listas en 
    # 1 única lista
prueba= list(chain.from_iterable(link_list))

##GUARDAMOS
file= os.getcwd() + "/urls_190619.csv"
with open(file, 'wt') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     for x in np.arange(0,len(prueba)):
         wr.writerow([prueba[x]])




#BUSCAMOS PARALELIZACIÓN DE LA MOVIDA 
         
         
def GET_ELECTROBUZZ_URLS(users_list, k):
    
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
            print('invalid UserAgent')
            fail=fail+1
            if fail>10:
                break

            
            
           
    m = re.findall('https://www.electrobuzz.net/[0-9]'
               '[^\"]+' , req.text)
    m1 = list(set(m))
    print(str(k))
    return m1
    
    
# Esto lo que hace es comvertir la lista de listas en 
    # 1 única lista
prueba= list(chain.from_iterable(link_list))

##GUARDAMOS
file= os.getcwd() + "/urls_190619.csv"
with open(file, 'wt') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     for x in np.arange(0,len(prueba)):
         wr.writerow([prueba[x]])



def main():

    #DESCARGAMOS USER AGENTS 
    users_list= get_user_agents()  
    
    #PARALELIZAMOS EMPLEANDO POLL.STARMAP CON TODOS LOS NÚCLUES -1        
    pool = mp.Pool(mp.cpu_count()-1)
    results = pool.starmap(GET_ELECTROBUZZ_URLS, [(users_list,k) for k in np.arange(0,100000)])
    
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
    
