#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 13:51:44 2019

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
import zipfile
import requests
from bs4 import BeautifulSoup
import requests
import numpy as np
import random
import re
import csv    
import tqdm
import multiprocessing as mp
from  itertools import chain
from datetime import date
import sys
from libraries_script import get_user_agents, set_user_agents, GET_COSMOBOX_URL, GET_ELECTROBUZZ_URLS, GET_ELECTROBUZZ_URLS_BY_SEARCH

'''
def main(): 
    cosmo_url= []
    file=os.getcwd()+'/urls_cosmo_multi.csv'
    with open(file, 'rt') as myfile:
         wx = csv.reader(myfile)
         for x in wx:
             cosmo_url.append(x)
             
    DOWNLOAD_ZIP(cosmo_url[0:20])
    
    
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
    
    merge_list= []
    for i in np.arange(0, len(read_urls)):
        merge_list.append([users_list, read_urls[i]])   
        
    
    #PARALELIZAMOS EMPLEANDO POLL.STARMAP CON TODOS LOS NÚCLUES -1        
    pool = mp.Pool(mp.cpu_count()-1)
    #results = pool.starmap(GET_COSMOBOX_URL, [(users_list,read_urls[k], k, 100) for k in np.arange(0,100)])
    #resuLts= pool.map([GET_COSMOBOX_URL(users_list, read_urls[k]) for k in np.arange(100)])

    #results = pool.map(GET_COSMOBOX_URL, merge_list)    
    results=[]
    for _ in tqdm.tqdm(pool.imap_unordered(GET_COSMOBOX_URL, merge_list), total=len(read_urls)):
        results.append(_)
        pass
    #MATAMOS SUBPROCESOS 
    pool.close()
    pool.terminate()
    pool.join()
    #GUARDAMOS RESULTADOS EN UN CSV
    file= os.getcwd() + "/urls_cosmo_multi.csv"
    with open(file, 'wt') as myfile:
         wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
         for x in np.arange(0,len(results)):
             wr.writerow([results[x]])

'''


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
                 
        
    
    onlyfiles = [f for f in os.listdir(PATH_RUN) if os.path.isfile(os.path.join(PATH_RUN, f))]
    
    for electrobuzz_file in onlyfiles: 
        file=PATH_RUN+ electrobuzz_file
    
        read_urls= []
        with open(file, 'rt') as myfile:
             wx = csv.reader(myfile)
             for x in wx:
                 read_urls.append(x)
        merge_list= []
        for i in np.arange(0, len(read_urls)):
            merge_list.append([users_list, read_urls[i]])   
            
        
        #PARALELIZAMOS EMPLEANDO POLL.STARMAP CON TODOS LOS NÚCLUES -1        
        pool = mp.Pool(mp.cpu_count()-1)
        #results = pool.starmap(GET_COSMOBOX_URL, [(users_list,read_urls[k], k, 100) for k in np.arange(0,100)])
        #resuLts= pool.map([GET_COSMOBOX_URL(users_list, read_urls[k]) for k in np.arange(100)])
    
        #results = pool.map(GET_COSMOBOX_URL, merge_list)    
        results=[]
        for _ in tqdm.tqdm(pool.imap_unordered(GET_COSMOBOX_URL, merge_list), total=len(read_urls)):
            results.append(_)
            pass
        #MATAMOS SUBPROCESOS 
        pool.close()
        pool.terminate()
        pool.join()
        
        
        #GUARDAMOS RESULTADOS EN UN CSV
        file= PATH_RUN + electrobuzz_file.replace('urls_electrobuzz_', "urls_cosmobox_")
        with open(file, 'wt') as myfile:
             wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
             for x in np.arange(0,len(results)):
                 wr.writerow([results[x]])


        
        
if __name__ == "__main__":
   
    main(sys.argv[1:])
    