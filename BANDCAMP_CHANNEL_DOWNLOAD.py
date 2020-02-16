#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 13:49:29 2019

@author: oscar
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
import os
from mutagen import File        
from mutagen.id3 import TPE1, TIT2, TRCK, TALB, APIC, TYER
import re
import requests
import html
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

    
def LOOK_FOR_TRACKS_AND_ALBUMS_IN_URL(url):
    
    session = requests.Session()
    session.trust_env = False
    user_agents= session.get(url)
    BS4_ELEMENT = BeautifulSoup(user_agents.content, 'html.parser')
    '''
    INTROUDCIMOS UN ELEMENTO BS4 Y DEVUELVE 
    LOS LINKS DE ALBUMES Y LAS CANCIONES
    '''
    try:
        BS4_ELEMENT.find('div',  {'class':'recommendations-container'}).decompose()
    except:
        pass

    LINKS_BS4= []
    for a in BS4_ELEMENT.find_all(href=True):
        LINKS_BS4.append(a['href'])
    
    URL_CANAL = url.split('.com')[0] + '.com'
    ALBUMS= [link if 'https://' in link else URL_CANAL + link for link in LINKS_BS4 if '/album/' in link]
    ALBUMS= list(dict.fromkeys(ALBUMS))
    
    
    SONGS= [link if 'https://' in link else URL_CANAL + link for link in LINKS_BS4 if '/track/' in link]
    SONGS= [item for item in SONGS if '?action=download' not in item]
    SONGS= list(dict.fromkeys(SONGS))
    
    try:
        PATRON_STREAM = re.compile('https://t4.bcbits.com/stream/'   
                                '[^\"]+' )                        
        AUDIO_URL=re.findall(PATRON_STREAM,user_agents.text)[0]
    except: 
        AUDIO_URL= []
   
    try:
        PATRON_IMG = re.compile('<img src="(https://f4.bcbits.com/img/.[^\.]+.jpg)')
                                     
        IMG_URL=re.findall(PATRON_IMG,user_agents.text)[0]
    except: 
        IMG_URL= []
        
    return {'ALBUMS': ALBUMS, 'TRACKS': SONGS, 'AUDIO':AUDIO_URL, 'IMG':IMG_URL}

'''
EL PLAN ES REHACER LAS FUNCIONES DE ANDONI. PARA ELLO VOY A EMPLEAR 
LOOK FOR TRACKS AND ALBUMS ANTES DE ABESTIA JAITSI, DESPUES DE AI
TODACARA REHACER ABESTIA JAITSI
HAY QUE DAR CAÑA A REGES ESTOY VERDE


'''                      





       
        


def main():
    

                

#AL ATAQUE        
if __name__ == '__main__':
    main()
        



try:
    FILE_PATH= os.path.join(os.path.dirname(__file__))
except:
    FILE_PATH= os.getcwd()
   
with open(FILE_PATH + '/YT/HATE/BANDCAMP_LINKS.txt', 'r') as file:
        
        LINKS_BANDCAMP= file.readlines()

LABELS= [item.split('.com')[0] + '.com' for item in LINKS_BANDCAMP]
   
for CHANNEL in LABELS:
    
    session = requests.Session()
    session.trust_env = False
    user_agents= session.get(CHANNEL)
        
    user_soup = BeautifulSoup(user_agents.content, 'html.parser')
    CHANNEL_NAME= user_soup.find('head').find('title').text.replace('\n','').strip()
    

        
    
    HREFS= LOOK_FOR_TRACKS_AND_ALBUMS_IN_URL(CHANNEL)

    
    
    for ALBUMS in HREFS['ALBUMS']:
        session = requests.Session()
        session.trust_env = False
        user_agents= session.get(ALBUMS)
        
        #PARSEANDO HTML
        user_soup = BeautifulSoup(user_agents.content, 'html.parser')
            
        NAME_SECTION= [item for item in user_soup.find_all('div', { "id" : "name-section" })][0]
        ALBUMA_NAME= NAME_SECTION.find('', {'class':'trackTitle'}).text.replace('\n','').strip()
        ARTIST_NAME= NAME_SECTION.find('', {'itemprop':'byArtist'}).text.replace('\n','').strip()
        HREF_ARTIST= [item['href'] for item in NAME_SECTION.find('', {'itemprop':'byArtist'}).find_all(href= True)]
        INFO_ARTISTA= '--------'.join(list(chain(*[[ARTIST_NAME], HREF_ARTIST])))        
             
        
        TRACKS_IN_ALBUM= LOOK_FOR_TRACKS_AND_ALBUMS_IN_URL(ALBUMS)['TRACKS']
        
        for TRACKS in TRACKS_IN_ALBUM:
            session = requests.Session()
            session.trust_env = False
            user_agents= session.get(TRACKS)
                
            #PARSEANDO HTML
            user_soup = BeautifulSoup(user_agents.content, 'html.parser')
            NAME_SECTION= [item for item in user_soup.find_all('div', { "id" : "name-section" })][0]
            SONG_NAME= NAME_SECTION.find('', {'class':'trackTitle'}).text.replace('\n','').strip()
            ARTIST_NAME= NAME_SECTION.find('', {'itemprop':'byArtist'}).text.replace('\n','').strip()
            HREF_ARTIST= [item['href'] for item in NAME_SECTION.find('', {'itemprop':'byArtist'}).find_all(href= True)]
            INFO_ARTISTA= '--------'.join(list(chain(*[[ARTIST_NAME], HREF_ARTIST])))        
            
            
            
            IMG_AUDIO= LOOK_FOR_TRACKS_AND_ALBUMS_IN_URL(TRACKS)
            HREF_AUDIO= IMG_AUDIO['AUDIO']
            HREF_IMG= IMG_AUDIO['IMG']
            
            PATH_DONWLOAD=  os.path.join(FILE_PATH, CHANNEL_NAME, ALBUMA_NAME)
            
            if not os.path.exists(PATH_DONWLOAD):
                os.makedirs(PATH_DONWLOAD, exist_ok=True)
            os.chdir(PATH_DONWLOAD)
            
    
            IMG = requests.get(HREF_IMG, allow_redirects=True)
            open('cover.jpg', 'wb').write(IMG.content)  #Karatula jaitsi
        
            SONG_FILE= SONG_NAME + '.mp3'
        
            SONG = requests.get(HREF_AUDIO, allow_redirects=True)
            if not os.path.exists(SONG_FILE):
                  open(SONG_FILE, 'wb').write(SONG.content)        #Fitxategiari izen generikoa jarriko diogu amaierako izenaren ordez komando hau karaktere batzuekin moskeatu egiten delako

           #Metadatuak gehitu
            audio=File(SONG_FILE)
            audio['TPE1'] = TPE1(encoding=3, text=ARTIST_NAME)
            audio['TIT2'] = TIT2(encoding=3, text=SONG_NAME)
           #audio['TRCK'] = TRCK(encoding=3, text=zenbakia)
            audio['TALB'] = TALB(encoding=3, text=ALBUMA_NAME)
           #Karatula jarri
            with open('cover.jpg', 'rb') as albumart:
                  audio['APIC'] = APIC(
                                encoding=3,
                                mime='image/jpeg',
                                type=3, desc=u'Cover',
                                data=albumart.read()
                                )       
            audio.save()
      
     