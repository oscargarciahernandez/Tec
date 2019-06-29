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



def abestia_jaitsi(url):       
       html_kodea=requests.get(url).text
       
       patroia = re.compile('https://t4.bcbits.com/stream/'   
                            '[^\"]+' )                        
       esteka=re.findall(patroia,html_kodea)[0]
       
       #Metadatuak lortu
       patroia = re.compile('<meta property="og:title" content="'
                            '.+'
                            ' by ')
       izena=re.findall(patroia,html_kodea)[0][35:-5]
       izena=html.unescape(izena)
       
       patroia = re.compile('<meta property="og:title" content="'
                            '.+, by [^\"]+')
       artista=re.findall(patroia,html_kodea)[0][(35+len(izena)+5):]
       artista=html.unescape(artista)
       
       patroia = re.compile('<meta name="Description" content="\n'
                            '.+')
       urtea=re.findall(patroia,html_kodea)[0]
       urtea=urtea[len(urtea)-4:len(urtea)]
       
       patroia = re.compile('from the album'
                            '[^>]+')
       try:
              albuma=re.findall(patroia,html_kodea)[0][15:-2]
              albuma=html.unescape(albuma)
       except:
              print("Ezin izan da hurrengo abestiko albuma lortu:\n"+url)
              albuma=""
       
       patroia = re.compile('"track_number":'
                            '\d+')
       try:
              zenbakia=re.findall(patroia,html_kodea)[0][15:]
       except:
              print("Ezin izan da hurrengo abestiko zenbakia lortu:\n"+url)
              zenbakia=""
       
       patroia = re.compile('<img src="https://f4.bcbits.com/img/'
                            '.[^\.]+'
                            '.jpg')
       karatularen_esteka=re.findall(patroia,html_kodea)[0][10:]
       r = requests.get(karatularen_esteka, allow_redirects=True)
       open('cover.jpg', 'wb').write(r.content)  #Karatula jaitsi

       fitxategiaren_izena=zenbakia + ' ' + izena + '.mp3'
       #Badaude fitxategien izenek eduki ezin ditzazketen karaktereak, kendu egingo ditugu
       fitxategiaren_izena = karaktereak_filtratu(fitxategiaren_izena)       
                   
       #Abestia jaitsi
       r = requests.get(esteka, allow_redirects=True)
       if not os.path.exists(fitxategiaren_izena):
              open(fitxategiaren_izena, 'wb').write(r.content)        #Fitxategiari izen generikoa jarriko diogu amaierako izenaren ordez komando hau karaktere batzuekin moskeatu egiten delako

       #Metadatuak gehitu
       audio=File(fitxategiaren_izena)
       audio['TPE1'] = TPE1(encoding=3, text=artista)
       audio['TIT2'] = TIT2(encoding=3, text=izena)
       audio['TRCK'] = TRCK(encoding=3, text=zenbakia)
       audio['TALB'] = TALB(encoding=3, text=albuma)
       audio['TYER'] = TYER(encoding=3, text=urtea)
       #Karatula jarri
       with open('cover.jpg', 'rb') as albumart:
              audio['APIC'] = APIC(
                            encoding=3,
                            mime='image/jpeg',
                            type=3, desc=u'Cover',
                            data=albumart.read()
                            )       
       audio.save()
       

def albuma_jaitsi(url):
       
       html_kodea=requests.get(url).text
       
       patroia=re.compile('href=\"/track/'
                          '.+'
                          'itemprop="url"')
       esteken_amaierak=re.findall(patroia,html_kodea)
       for i in range(0,len(esteken_amaierak)):
              esteken_amaierak[i]=esteken_amaierak[i][6:-16]
              
       patroia=re.compile('.+'
                          '/album/')
       esteken_hasiera=re.findall(patroia,url)[0][:-7]
       
       estekak=[None] * len(esteken_amaierak)
       for i in range(0,len(esteken_amaierak)):
              estekak[i]=esteken_hasiera + esteken_amaierak[i]

       #Albumaren izena lortu (karpetaren izenerako)
       patroia = re.compile('<meta name="title" content="'
                            '.+'
                            ', by ')
       try:
              albuma=re.findall(patroia,html_kodea)[0][28:-5]
              albuma=html.unescape(albuma)
       except:
              albuma=""
              print("Ezin izan da hurrengo abestiko albuma lortu:\n"+url)
       
       path_hasierakoa=os.getcwd()
       albuma=karaktereak_filtratu(albuma)
       path_abuma=path_hasierakoa + '//' + url.replace('https://', '').split(".")[0] + '//' + albuma
       if not os.path.exists(path_abuma):
              os.makedirs(path_abuma)
       os.chdir(path_abuma)
       
       #Behin karpeta barruan egonda, abestiak jaits ditzakegu
       for i in range(0,len(estekak)):
              try:
                     abestia_jaitsi(estekak[i])
              except:
                     print("abestia_jaitsi funtzioak ezin izan du hurrengo esteka jaitsi:\n"+estekak[i])
              
       os.chdir(path_hasierakoa)
       return path_abuma


def song_jaitsi(url):
    
       path_hasierakoa=os.getcwd()
       path_abuma=path_hasierakoa + '//' + url.replace('https://', '').split(".")[0] 
       if not os.path.exists(path_abuma):
              os.makedirs(path_abuma)
       os.chdir(path_abuma)
       abestia_jaitsi(url)              
       os.chdir(path_hasierakoa)
       return path_abuma

def artista_jaitsi(url):
       
       html_kodea=requests.get(url).text
       
       patroia = re.compile('/album/'
                            '.[\w|-]+')
       esteken_amaierak=re.findall(patroia,html_kodea)
       patroia = re.compile('.+'
                            '\.com')
       esteken_hasiera=re.findall(patroia,url)[0]
              
       patroia=re.compile('.+'
                          '/album/')       
       estekak=[None] * len(esteken_amaierak)
       for i in range(0,len(esteken_amaierak)):
              estekak[i]=esteken_hasiera + esteken_amaierak[i]
       
       #Artista lortu (karpeta izendatzeko)
       patroia = re.compile('<title>Music | '
                            '.+'
                            '</title>')
       artista=re.findall(patroia,html_kodea)[0][19:-8]
       artista=html.unescape(artista)
              
       path_hasierakoa=os.getcwd()
       artista=karaktereak_filtratu(artista)
       path_artista=path_hasierakoa + '\\' + artista
       if not os.path.exists(path_artista):
              os.makedirs(path_artista)
       os.chdir(path_artista)
       
       for i in range(0,len(estekak)):
              try:
                     albuma_jaitsi(estekak[i])
              except:
                     print("abestia_jaitsi funtzioak ezin izan du hurrengo esteka jaitsi:\n"+estekak[i])
       
       #Goiko parteak albuma aurkitzen ditu, baina singleak ez. Konponbidea:
       patroia=re.compile('/track/'
                          '[^\"]+')
       esteken_amaierak=re.findall(patroia,html_kodea)
            
       estekak=[None] * len(esteken_amaierak)
       for i in range(0,len(esteken_amaierak)):
              estekak[i]=url + esteken_amaierak[i]
              
       for i in range(0,len(estekak)):
              try:
                     abestia_jaitsi(estekak[i])
              except:
                     print("abestia_jaitsi funtzioak ezin izan du hurrengo esteka jaitsi:\n"+estekak[i])
              
              
       os.chdir(path_hasierakoa)

#def bandcamp_jaitsi(url)    #Bandcampeko esteka bat emanda zer den detektatu (artistaren orria, albuma, abesti soltea..) eta beharrezko funtzioak deitzen ditu.

def karaktereak_filtratu(path):
       #Programa honek string bat hartu eta windowsek karpeten izenetan
       #onartzen ez dituen karaktereak kendu egiten ditu
       pattern=re.compile('[?\\\/|<>():*]')
       path=re.sub(pattern, '', path)
       return(path)





def main():
    #URL DE LA DE BUSQUEDA
    while True: 
        print('INTRODUCE NOMBRE DEL ARTISTA: \n')
        INPUT = str(input())
        URL_BUSQUEDA= 'https://bandcamp.com/search?q='
        BUSQUEDA=URL_BUSQUEDA +  INPUT
        
        
        #INICIAMOS SESION REQUEST
        session = requests.Session()
        session.trust_env = False
        user_agents= session.get(BUSQUEDA)
        
        #PARSEANDO HTML
        user_soup = BeautifulSoup(user_agents.content, 'html.parser')
        
        
        #OBTENEMOS GRUPOS DISPONIBLES
        user_soup1=user_soup.find_all('li' , class_='searchresult band')
        GROUPS= []
        for i in range(len(user_soup1)):        
            GROUP_NAME=  user_soup1[i].find_all('div', class_= 'heading')[0].find('a').contents[0].replace("\n", "").strip()
            GENRE= user_soup1[i].find_all('div', class_= 'genre')[0].contents[0].replace("\n", "").strip()
            LINK= user_soup1[i].find_all('div', class_= 'itemurl')[0].find_all('a')[0].contents[0].replace("\n", "").strip()
    
            GROUPS.append([GROUP_NAME, LINK, GENRE])
            
        
        
            
        #SELECIONAMOS GRUPOS QUE QUEREMOS
        
        print('SELECCIONA GRUPO INTRODUCIENDO EL NUMERO A SU IZQUIERDA: \n')
            
        k=0
        for sublist in GROUPS:
            
            print(str(k) + ') ' + sublist[0] + "------>" + sublist[2])
            k=k+1
        print(str(k) + ') CAMBIAR BUSQUEDA')
        GRUPO_SELECT = int(input('Enter numbers: '))

        if GRUPO_SELECT==int(k):
            pass
        else: 
            break
               
           
           
           
           
    
           
     
    url= GROUPS[GRUPO_SELECT][1]
    #MIRAMOS LOS ALBUMES DE ESE ARTISTA 
    user_agents= session.get(url)
    user_soup = BeautifulSoup(user_agents.content, 'html.parser')
    
    ALL_LINKS= []
    for a in user_soup.find_all('a', href=True):
        ALL_LINKS.append(a['href'])
        
    ALBUMS = [s for s in ALL_LINKS if not "https://" in s]
    ALBUMS = [s for s in ALBUMS if "/album/" in s]
    ALBUMS= list(dict.fromkeys(ALBUMS))
    
    if len(ALBUMS)==0:
        print("NO HAY ALBUMES DISPONIBLES...")
        SONGS = [s for s in ALL_LINKS if not "https://" in s]
        SONGS = [s for s in SONGS if "/track/" in s]
        SONGS= list(dict.fromkeys(SONGS))
        print('HAY DISP0NIBLE: ' + str(len(SONGS)) + " cancion(es)")
        print('¿DESCARGAR CANCION(ES) DISPONIBLE(S)?(y/n): \n')
        
        GRUPO_SELECT = str(input(' '))
        if GRUPO_SELECT=='y':
            for i in range(len(SONGS)):
                print("DESCARGANDO CACION: " + SONGS[i].replace('/track/', ""))
                path= song_jaitsi((url + str(SONGS[i])))
                print("CANCION DESCARGADA EN : " +  path)

                
        else: None
    else: 
    
        print('SELECCIONA ALBUM INTRODUCIENDO EL NUMERO A SEGUIR DESCARGANDOSU IZQUIERDA: \n')
        k=0
        for sublist in ALBUMS:
            nombre_album= sublist.replace('/album/', "")
            print(str(k) + ') ' + nombre_album )
            k=k+1
        print(str(k) + ') TODOS LOS ALBUMS')
        GRUPO_SELECT = list(map(int, input('Enter numbers: ').split()))
        
        if GRUPO_SELECT[0]==int(k):     
            for i in range(len(ALBUMS)):
                url_ALBUM= url.split("?")[0] + ALBUMS[i]
                print("DESCARGANDO ALBUM: ", ALBUMS[i].replace('/album/', ""))
    
                path_descarga= albuma_jaitsi(url_ALBUM)
                print("ALBUM DESCARGADO EN : " +  path_descarga)
    
        else:     
            for i in GRUPO_SELECT:
                url_ALBUM= url.split("?")[0] + ALBUMS[i]
                print("DESCARGANDO ALBUM: " + ALBUMS[i].replace('/album/', ""))
    
                path_descarga= albuma_jaitsi(url_ALBUM)
                print("ALBUM DESCARGADO EN : " +  path_descarga)

    
    
                

#AL ATAQUE        
if __name__ == '__main__':
    while True: 
        clear = lambda: os.system('clear')
        clear()
        main()
        print('¿SEGUIR DESCARGANDO?(y/n): \n')
        GRUPO_SELECT = str(input(' '))
        if GRUPO_SELECT=='y':
            pass
        else: 
            break
        
    