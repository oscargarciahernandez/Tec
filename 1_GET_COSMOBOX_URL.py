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





### De esta manera se lee corretamente
read_urls= []
file=os.getcwd() + "/urls_190619.csv"
with open(file, 'rt') as myfile:
     wx = csv.reader(myfile)
     for x in wx:
         read_urls.append(x)


users_list= get_user_agents()  


COSMO_list= []
k=0
while True:
    fail=1
    while True:
            try:
                ua=set_user_agents(users_list,random.randrange(0, len(users_list)))
                url1= read_urls[k]
                url=str(url1).replace('[\'', '' ).replace('\']', '')
                ession = requests.Session()
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
    if fail>10:
        break
            
            
           
    m = re.findall('https://cosmobox.org/' \
               '[^\"]+' , req.text)
    m1 = list(set(m))
    
    COSMO_list.append(m1)
    time.sleep(random.random()/50)
    print(str(k))
    k+=1
    
    
    
    
    
file=os.getcwd()+'\urls_cosmo.csv'
with open(file, 'wb') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     for x in np.arange(0,len(prueba)):
         wr.writerow([str(prueba[x])])



## PARALELIZAMOS
         
         #USANDO APPLY
         
         
def GET_COSMOBOX_URL(users_list, read_url):
    fail=1
    while True:
        try:
            ua=set_user_agents(users_list,random.randrange(0, len(users_list)))
            url1= read_url
            url=str(url1).replace('[\'', '' ).replace('\']', '')
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
        
           
    m = re.findall('https://cosmobox.org/' \
               '[^\"]+' , req.text)
    m1 = list(set(m))
    print(m1)
    return m1
    
# POOL.STARMAP SI QUE CONSIGUE ACELERAR EL PROCESO, LA VIDA

def main():
    pool = mp.Pool(mp.cpu_count()-1)
    results = pool.starmap(GET_COSMOBOX_URL, [(users_list,read_urls[k]) for k in np.arange(0,len(read_urls))])
    pool.terminate()
    pool.join()
    file= os.getcwd() + "/urls_cosmo_multi.csv"
    with open(file, 'wt') as myfile:
         wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
         for x in np.arange(0,len(results)):
             wr.writerow([results[x]])
        
if __name__ == '__main__':
    main()
    


