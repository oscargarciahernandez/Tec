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



url_base= 'https://www.electrobuzz.net/page/2'
req= requests.get(url_base)                
            


m = re.findall(r'<article(.*)<\article>', req.content)

m = re.findall(r'\"href(.*)\"', req.content)

if m:
    found = m.group(1)


        

    
    
    soup = BeautifulSoup(req.content, 'html.parser')
    soup2=soup.find_all('article')

    
    list_info.append(obtn_link_title(soup2))
    
    



    


users_list= get_user_agents()        

## obtenemos las proxies
#proxies=get_proxies()

# Hacemos el primer request para obtener los releases de la pagina  principal y el numero total de páginas
#first_req_conproxi= requests.get('https://www.electrobuzz.net/',proxies= set_proxi_for_req(proxies,10),headers=set_user_agents(users_list,random.randrange(0, len(users_list))))

first_req= requests.get('https://www.electrobuzz.net/',
                        headers=set_user_agents(users_list,
                                                 random.randrange(0, 
                                                                  len(users_list))))


soup = BeautifulSoup(first_req.content, 'html.parser')
soup1=soup.find_all('div', 
                    {'class': 'listing listing-blog listing-blog-1 clearfix columns-1 columns-1'})
soup2=soup1[0].find_all('article')


##vector de pags
total_pags_vec= get_vector_pags(soup)

#Info de la página principal
info_pag_1= obtn_link_title(soup2)