# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 23:58:11 2019

@author: Oscar
"""

from bs4 import BeautifulSoup
import requests
import numpy as np
import os
import random
import re
import csv    
import tqdm
import multiprocessing as mp
from  itertools import chain
from datetime import date




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


#BUSCAMOS PARALELIZACIÓN DE LA MOVIDA      
         
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

            
            
    primary= re.search('primary(.*)',req.text.replace("\n","")).group(1)
    m = re.findall('https://www.electrobuzz.net/[0-9]'
               '[^\"]+' , primary)
    m1 = list(set(m))
    return m1
    
    
 



def main():

    #DESCARGAMOS USER AGENTS 
    users_list= get_user_agents()  
    
    merge_list= []
    for i in np.arange(1, 8000):
        merge_list.append([users_list,i])  
    
    #PARALELIZAMOS EMPLEANDO POLL.STARMAP CON TODOS LOS NÚCLUES -1        
    pool = mp.Pool(mp.cpu_count()-6)
    results=[]
    for _ in tqdm.tqdm(pool.imap_unordered(GET_ELECTROBUZZ_URLS, merge_list), total=len(merge_list)):
        results.append(_)
        pass
    #MATAMOS SUBPROCESOS 
    pool.close()
    pool.terminate()
    pool.join()
    results_merge= list(chain.from_iterable(results))
    #GUARDAMOS RESULTADOS EN UN CSV
    file= os.getcwd() + "/urls_electrobuzz_" + str(date.today()) + ".csv"
    with open(file, 'wt') as myfile:
         wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
         for x in np.arange(0,len(results_merge)):
             wr.writerow([results_merge[x]])
             
             

#AL ATAQUE        
if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
