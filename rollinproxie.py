# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 01:36:23 2019

@author: Oscar
"""

from bs4 import BeautifulSoup
import requests
import shutil
import numpy as np
import os
import random
from random import choice


################funciones


#####funcion para obtener link titulo e imagen del album
#### hay que introducir soup2 (ver electrobuzz.py)
def obtn_link_title_img(bs4_element):
    list_link_title= []
    for i in np.arange(0,len(soup2)):
        title= soup2[i].find('a')['title']
        link= soup2[i].find('a')['href']
        
        
        
        link_img= soup2[0].find('a')['data-src']
        ext=link_img[-3:]
        filename_0=''.join(e for e in title if e.isalnum())
        filename= filename_0 + '.' + ext
        path='C:/Users/Oscar/Desktop/img/'
        file_ext= path + filename
        
        r = requests.get(link_img, stream=True)
        
        
        if r.status_code == 200:
            with open(file_ext, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
                
        if os.path.isfile(file_ext):
            link_title= list([link,title,file_ext])
            list_link_title.append(link_title)
        else: 
            link_title= list([link, title,str('NO')])
            list_link_title.append(link_title)
            
    return list_link_title
    


def obtn_link_title(bs4_element):
    list_link_title= []
    for i in np.arange(0,len(soup2)):
        title= soup2[i].find('a')['title']
        link= soup2[i].find('a')['href']

        link_title= list([link, title])
        list_link_title.append(link_title)
        
    return list_link_title




####funcion para obtener proxies de una página web
def get_proxies():   
   
  proxies_req = requests.get('https://www.sslproxies.org/')


  soup = BeautifulSoup(proxies_req.content, 'html.parser')
  proxies_table = soup.find(id='proxylisttable')
  
  proxies=[]

  # Save proxies in the array
  for row in proxies_table.tbody.find_all('tr'):
    proxies.append({
      'ip':   row.find_all('td')[0].string,
      'port': row.find_all('td')[1].string
    })

  return proxies








### funcion para poner en un formato guay para usar requests.get
## hay que incluir el array de proxies y la posición n (se podría llegar a generar de manera aleatoria)
def set_proxi_for_req(proxies,n):
    proxi_http='http://' + str(proxies[n]['ip'])+ ':' +proxies[n]['port']
    proxi_https='https://' + str(proxies[n]['ip'])+ ':' +proxies[n]['port']
    proxi1 = {'http': str(proxi_http), "https": str(proxi_https)}
    return proxi1







########Funcion que busca la informaxcion de electrobuz
    ##### hay que setear el vector de páginas y el proxi a utilizar empleando la funcion set_proxi_for_req

#### OBSOLETO    
def srch_info(vector_paginas, proxi1):
    
    url_base= 'https://www.electrobuzz.net/page'
        
    list_info=[]
    for i in vector_paginas:
        url_page= url_base + '/' + str(i)+ '/'
        
        req= requests.get(url_page, proxies= proxi1)
        soup = BeautifulSoup(req.content, 'html.parser')
        soup2=soup.find_all('article')
    
        
        list_info.append(obtn_link_title_img(soup2))
        
    
    return list_info


#a get_total_pags se le da tipo soup
def get_vector_pags(bs4_elmn):  
    soup_pages=bs4_elmn.find_all('a', {'class': 'page-numbers'})
    pages=int(soup_pages[2].text.replace(',',''))
    vector_pages= np.arange(2,pages+1)  
    return vector_pages

### OBSOLETO
def div_vector_pags(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
        
#DESCARGAR PEDAZO DE LISTA DE USER AGENTS        
def get_user_agents():
    user_agents= requests.get('http://www.useragentstring.com/pages/useragentstring.php?typ=Browser')
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

#FUNCION GUAY, MUY GUAY.
def srch_info_chg_ua(vector_paginas, ua):
    
    url_base= 'https://www.electrobuzz.net/page'
        
    list_info=[]
    for i in vector_paginas:     
        while True:
            try:
                url_page= url_base + '/' + str(i)+ '/'
                headers=set_user_agents(ua,random.randrange(0,len(ua)))
                req= requests.get(url_page, headers= headers)                
                if req.status_code == requests.codes.ok:
                    break
            except:
                pass
            print('invalid user_agent')


            

        
        
        soup = BeautifulSoup(req.content, 'html.parser')
        soup2=soup.find_all('article')
    
        
        list_info.append(obtn_link_title(soup2))
        
    
    return list_info



    


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


#prueba=srch_info_chg_ua(total_pags_vec, users_list)






##### MULTIPROCCESSS AUN EN ESTAND-BY 
### divide el vector de pags. en grupos del tamaño que queramos
### nos sirve para aplicar multiproccessign en paralelo. 
### cada proceso contara con un vector diferente
vec_pags_div=list(div_vector_pags(total_pags_vec,5))

import time

links_list=[]
for i in np.arange(0,len(vec_pags_div)):
    links_list.append(srch_info_chg_ua(vec_pags_div[i],users_list))
    time.sleep(0.5)
    print(str(i))

