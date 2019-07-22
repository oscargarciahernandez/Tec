#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 13:40:08 2019

@author: oscar
"""

from libraries_script import DOWNLOAD_ZIP, get_user_agents, set_user_agents, GET_COSMOBOX_URL, GET_ELECTROBUZZ_URLS, GET_ELECTROBUZZ_URLS_BY_SEARCH
import os
import csv
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
import shutil


def main(inputlist):

    #DESCARGAMOS USER AGENTS 
    users_list= get_user_agents()

    PATH_RUN= 'Run/' 

    if not os.path.exists(PATH_RUN):
        os.mkdir(PATH_RUN)
    #MERGE INPUTS2 FUNCION SEARCH
    for busqueda in inputlist:
        
        
        print('BUSQUEDA ELECTROBUZZ PARA ', busqueda.replace(",", "").replace("_", " ").upper())
        busqueda= busqueda.replace(",", "").replace("_", " ")
        merge_list2= [users_list, busqueda]
        
        results_merge= GET_ELECTROBUZZ_URLS_BY_SEARCH(merge_list2, REMOVE_VA_and_BEATPORT=True, EXTRICT_ARTIST=True)
        file= PATH_RUN + "/urls_electrobuzz_" + busqueda.replace(" ", "_") + ".csv"
        with open(file, 'wt') as myfile:
             wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
             for x in np.arange(0,len(results_merge)):
                 wr.writerow([results_merge[x]])
                 

    ### LEEMOS URL'S DE ELECTROBUZZ
    
    LISTA_ARTISTAS= os.listdir('Run/')
    
    for files in LISTA_ARTISTAS:
        
        read_urls= []
        file=PATH_RUN + files 
        with open(file, 'rt') as myfile:
             wx = csv.reader(myfile)
             for x in wx:
                 read_urls.append(x)
    
        merge_list= []
        for i in np.arange(0, len(read_urls)):
            merge_list.append([users_list, read_urls[i]])   
        
        print('\n BUSCANDO LINK COSMOBOX PARA ', files.replace("urls_electrobuzz_", "").replace(".csv", "").upper())
        #PARALELIZAMOS EMPLEANDO POLL.STARMAP CON TODOS LOS NÚCLUES -1        
        pool = mp.Pool(mp.cpu_count()-1)
       
        results=[]
        for _ in tqdm.tqdm(pool.imap_unordered(GET_COSMOBOX_URL, merge_list), total=len(read_urls)):
            results.append(_)
            pass
        #MATAMOS SUBPROCESOS 
        pool.close()
        pool.terminate()
        pool.join()
        
        #GUARDAMOS RESULTADOS EN UN CSV
        file= PATH_RUN + files.replace('electrobuzz', 'cosmobox')
        with open(file, 'wt') as myfile:
             wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
             for x in np.arange(0,len(results)):
                 wr.writerow([results[x]])
        
        os.remove(PATH_RUN + files)
                 
       
    LISTA_COSMOBOX= os.listdir('Run/')
    for cosmobox in LISTA_COSMOBOX: 

    # DOWNLOAD COSMOBOX
        cosmo_url= []
        file=PATH_RUN + cosmobox
        with open(file, 'rt') as myfile:
             wx = csv.reader(myfile)
             for x in wx:
                 cosmo_url.append(x)
                 
        DOWNLOAD_ZIP(cosmo_url[0][1])

             
             

if __name__ == "__main__":
    shutil.rmtree('Run/' )
    main(sys.argv[1:])
    