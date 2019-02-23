# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 04:24:31 2019

@author: Oscar
"""

import requests 

from bs4 import BeautifulSoup

import shutil

import numpy as np

import os


first_req= requests.get('https://www.electrobuzz.net')

soup = BeautifulSoup(first_req.content, 'html.parser')
soup1=soup.find_all('div', {'class': 'listing listing-blog listing-blog-1 clearfix columns-1 columns-1'})
soup2=soup1[0].find_all('article')





#a get_total_pags se le da tipo soup
def get_total_pags(bs4_elmn):  
    soup_pages=bs4_elmn.find_all('a', {'class': 'page-numbers'})
    pages=int(soup_pages[2].text.replace(',',''))
    vector_pages= np.arange(1,pages+1)  
    return vector_pages


#a get_total_pags se le da tipo soup2
    
def obtn_link_title_img(bs4_element):
    list_link_title= []
    for i in np.arange(0,len(soup2)):
        title= soup2[i].find('a')['title']
        link= soup2[i].find('a')['href']
        
        
        
        link_img= soup2[0].find('a')['data-src']
        ext=link_img[-3:]
        filename= title.replace(' ','').replace('/','').replace('\\','') + '.' + ext
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
    
def get_info(vector_dado)    
    url_base= 'https://www.electrobuzz.net/page'
        
    list_info=[]
    for i in vector_dado:
        url_page= url_base + '/' + str(i)+ '/'
        
        req= requests.get(url_page)
        soup = BeautifulSoup(req.content, 'html.parser')
        soup1=soup.find_all('div', {'class': 'listing listing-blog listing-blog-1 clearfix  columns-1'})
        soup2=soup1[0].find_all('article')
        
        list_info.append(obtn_link_title_img(soup2))
        









        
        
obtn_link_title_img(soup2)