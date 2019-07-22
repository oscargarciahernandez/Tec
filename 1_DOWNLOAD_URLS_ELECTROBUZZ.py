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
import sys
from libraries_script import get_user_agents, set_user_agents
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

from difflib import SequenceMatcher
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
        for item in remove_list:
            lista_nombres.remove(item)
    
    if EXTRICT_ARTIST:
        LISTA_SOLO_BUSQUEDA= [item for item in lista_nombres for item2 in item.split("-") for item3 in merge_inputs2[1].split(" ") if similar(item3.lower(), item2)> 0.8]
    else:
        LISTA_SOLO_BUSQUEDA=lista_nombres
        
    LISTA_SOLO_BUSQUEDA= list(set(LISTA_SOLO_BUSQUEDA))
    LISTA_URLS= [item for item in lista_busquedaF for item2 in item.split("/") if item2 in LISTA_SOLO_BUSQUEDA]
    
        
     
            

    return LISTA_URLS
    
  
    




# DEFINICION DE VARIABLES
PATH_RUN= 'Run/' 


def main(inputlist):

    #DESCARGAMOS USER AGENTS 
    users_list= get_user_agents()

    
    if not os.path.exists(PATH_RUN):
        os.mkdir(PATH_RUN)
    #MERGE INPUTS2 FUNCION SEARCH
    for busqueda in inputlist:
        
        busqueda= busqueda.replace(",", "").replace("_", " ")
        merge_list2= [users_list, busqueda]
        
        results_merge= GET_ELECTROBUZZ_URLS_BY_SEARCH(merge_list2, REMOVE_VA_and_BEATPORT=True, EXTRICT_ARTIST=False)
        file= PATH_RUN + "/urls_electrobuzz_" + busqueda.replace(" ", "_") + ".csv"
        with open(file, 'wt') as myfile:
             wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
             for x in np.arange(0,len(results_merge)):
                 wr.writerow([results_merge[x]])
                 
        
    SCRAP_ALL=False
    
    if SCRAP_ALL:
        
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
             
             

if __name__ == "__main__":
   
    main(sys.argv[1:])
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
