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

def BAND_CAMP_SEARCH(INPUT, MODO=1):
    '''
    INPUT es un string para introducir en la busqueda
    MODO=1 : BUSCA ALBUMS, ARTISTAS/LABELS Y CANCIONES
    MODO=2 : SOLO ARTISTAS. EN BANDCAMP NO HAY DISTINCION ENTRE LABELS Y ARTISTAS
    MODO=3= SOLO ALBUMS
    MODO=4 : SOLO CANCIONES
    
    '''
    
    LIST_album= []
    LIST_track= []
    LIST_artist= []

    pages= 1
    while True:
        BUSQUEDA='https://bandcamp.com/search?page={}&q='.format(pages) + INPUT
        
        
        #INICIAMOS SESION REQUEST
        session = requests.Session()
        session.trust_env = False
        user_agents= session.get(BUSQUEDA)
        
        #PARSEANDO HTML
        user_soup = BeautifulSoup(user_agents.content, 'html.parser')
        
        #OBTENEMOS GRUPOS DISPONIBLES
        soup_album= user_soup.find_all('li' , class_='searchresult album')
        soup_track=user_soup.find_all('li' , class_='searchresult track')
        soup_band=user_soup.find_all('li' , class_='searchresult band')
        
        

        if len(soup_album)+len(soup_track)+len(soup_band)==0:
            break
        
        LIST_album.append(soup_album)
        LIST_track.append(soup_track)
        LIST_artist.append(soup_band)
        pages += 1
    
    
    
    TRACKS= list(chain(*LIST_track))
    ALBUMS= list(chain(*LIST_album))
    ARTISTS_LABELS= list(chain(*LIST_artist))

    print('Se han encontrado ' + str(len(TRACKS)) + ' canciones, ' + str(len(ALBUMS)) + ' Albums y ', str(len(ARTISTS_LABELS)) + ' Artistas o labels')
    
    if MODO==1:
        LISTA_RETURN= [TRACKS, ALBUMS, ARTISTS_LABELS]
    elif MODO==2:
        LISTA_RETURN = ARTISTS_LABELS
    elif MODO== 3:
        LISTA_RETURN= ALBUMS
    elif MODO== 4:
        LISTA_RETURN= TRACKS
    else:
        LISTA_RETURN= []
        print('MODO INCORRECTO')
    
    return LISTA_RETURN

def FIND_INFO_BANDCAMP_ELEMENT(LISTA_TODO, DISPLAY_IMG= False):
    '''
    A ESTA FUNCION SE LE METE DIRECTAMENTE LA LISTA PROPORCIONADA POR
    BANDCAMP_SEARCH Y LO QUE HACE ES BUSCAR INFORMACION DE CADA ELEMENTO
    DEVUELVE UN DICCIONARIO CON LA INFO DE CADA ELEMENTO
    
    PODEMOS ELEGIR SI QUEREMOS SACAR POR CONSOLA LLA IMAGEN DE LA CARATULA
    '''
    

    GROUPS= []
    if isinstance(LISTA_TODO, list):
        if isinstance(LISTA_TODO[0], list):
            LISTA_ITER =  list(chain(*LISTA_TODO))
        else:
            LISTA_ITER= LISTA_TODO
    else:
        LISTA_ITER= [LISTA_TODO]

    for ELEMENT in LISTA_ITER:
        
        ATTRS_DICT= [item.attrs for item in ELEMENT.find_all('div')]
        INFO_DICT= {}
        for j in range(len(ATTRS_DICT)):
            CLASE= ATTRS_DICT[j]['class']
            if CLASE:
                try:
                    INFO= ELEMENT.find_all('div', class_= CLASE[0])[0].contents[0].replace("\n", "").strip()
                    if not INFO:
                        try:
                            INFO= ELEMENT.find_all('div', class_= CLASE[0])[0].find('a').contents[0].replace("\n", "").strip()
                        except:
                            pass
                            if not INFO:
                                try:
                                    INFO= ELEMENT.find_all('div', class_= CLASE[0])[0].find('img').attrs['src']
                                except:
                                    pass
                    INFO_DICT[CLASE[0]]= INFO
                except:
                    pass
                                                
        if DISPLAY_IMG:
            for dicts in INFO_DICT.keys():
                JPG= INFO_DICT[dicts]
                if '/img/' in JPG:
                    r = requests.get(JPG, allow_redirects=True)
                    open('cover.jpg', 'wb').write(r.content) 
                    img=mpimg.imread('cover.jpg')
                    plt.imshow(img)
                    plt.axis('off')
                    plt.show()
                if re.match(r'(itemtype|heading|itemurl)', dicts):
                    print(INFO_DICT[dicts])

        

        GROUPS.append(INFO_DICT)
    return GROUPS
            
def LOOK_FOR_TRACKS_AND_ALBUMS(BS4_ELEMENT):
    '''
    INTROUDCIMOS UN ELEMENTO BS4 Y DEVUELVE 
    LOS LINKS DE ALBUMES Y LAS CANCIONES
    '''
    LINKS_BS4= []
    for a in BS4_ELEMENT.find_all('a', href=True):
        LINKS_BS4.append(a['href'])
        
    ALBUMS =[s for s in LINKS_BS4 if "/album/" in s]
    #ALBUMS = [s for s in ALBUMS if "/album/" in s]
    ALBUMS= list(dict.fromkeys(ALBUMS))
    SONGS = [s for s in LINKS_BS4 if "/track/" in s] #[s for s in LINKS_BS4 if not "https://" in s]
    #SONGS = [s for s in SONGS if "/track/" in s]
    SONGS= list(dict.fromkeys(SONGS))
    
    return {'ALBUMS': ALBUMS, 'TRACKS': SONGS}

                                
        

def main():
    #URL DE LA DE BUSQUEDA
    while True: 
        print('INTRODUCE NOMBRE DEL ARTISTA: \n')
        INPUT = str(input())
       
        LISTA_TODO= BAND_CAMP_SEARCH(INPUT, MODO=1)
                

        #SELECIONAMOS GRUPOS QUE QUEREMOS
        GROUPS= FIND_INFO_BANDCAMP_ELEMENT(LISTA_TODO)
       
        
        '''
        AHORA HACEMOS UN DISPLAY Y SELECCION DE LO ENCOTRADO EN LA 
        BUSQUEDA BANDCAMP
        '''
        print('SELECCIONA GRUPO INTRODUCIENDO EL NUMERO A SU IZQUIERDA: \n')
            
        k=0
        for sublist in GROUPS:
            
            REST_OF_DESCRIPTIOIN= '---'.join([sublist[item].replace('  ','') for item in sublist.keys() if item in ['result-info', 'heading', 'genre'] ])
            LEN_DES= len(REST_OF_DESCRIPTIOIN) + len(sublist['itemtype'])
            if LEN_DES>79:
                NEXO= '-'
            else:
                NEXO= ''.join(np.tile('-', 80-LEN_DES))
            
            print(str(k) + ')--' + sublist['itemtype'] +NEXO +REST_OF_DESCRIPTIOIN)
            k=k+1
        print(str(k) + ') CAMBIAR BUSQUEDA')
        #GRUPO_SELECT = (input('INTRODUCE LOS NUMEROS SEPARADOS POR 1 ESPACIO: '))
        
        GRUPO_SELECT= list(map(int, input('Enter numbers: ').split()))
        
        
        if int(k) in GRUPO_SELECT:
            SELECTION= False
            pass
        else:
            SELECTION= True
            break
    
    '''
     EN BASE A LA SELECCION REALIZAMOS LA DESCARGA
    '''
    if SELECTION:
        SELECIONES= GRUPO_SELECT       
        
        for SELECT in SELECIONES:
            url= GROUPS[SELECT]['itemurl']
            
            if '/track/' in url:
                print("DESCARGANDO CACION: " + url.replace('/track/', ""))
                path= song_jaitsi(url)
                print("CANCION DESCARGADA EN : " +  path)
            elif '/album/' in url:
                print("DESCARGANDO ALBUM: " + url.replace('/track/', ""))
                path=albuma_jaitsi(url)
                print("ALBUM DESCARGADA EN : " +  path)
                    
            else:          
                while url:
                    '''
                    SI LA URL ES DE UN ARTISTA O LABEL
                    MIRAMOS DENTRO A VER QUE ENCONTRAMOS                    
                    
                    '''
                    
                    CANALES_EXTERNOS= []
                    url = url if isinstance(url, list) else [url]
                    for url_artista in url:
                        #MIRAMOS LOS ALBUMES DE ESE ARTISTA 
                        session = requests.Session()
                        session.trust_env = False
                        user_agents= session.get(url_artista)
                        user_soup = BeautifulSoup(user_agents.content, 'html.parser')
                        
                        
                        '''
                        SEPARAMOS EL APARTADO DE RECOMENDACIONES DEL RESTO DE 
                        ALBUMS DE LA PAGINA. 
                        '''
                        try:
                            
                            RECOMENDACIONES= LOOK_FOR_TRACKS_AND_ALBUMS(user_soup.find('div',  {'class':'recommendations-container'}))
                            user_soup.find('div',  {'class':'recommendations-container'}).decompose()
                        except:
                            print('NO HAY RECOMENDACIONES')
      
                        
                        '''
                        AKI SACAMOS ALBUMES Y CANCIONES DEL ARTISTA EN CUESTION 
                        '''
                        
                        ALBUMS_TRACKS= LOOK_FOR_TRACKS_AND_ALBUMS(user_soup)
                        ALBUMS= ALBUMS_TRACKS['ALBUMS']
                        SONGS= ALBUMS_TRACKS['TRACKS']
                        
                        '''
                        DESPUES DE MIRAR DENTRO DEL CANAL VEMOS SI EXISTEN ALBUMES
                        SI NO EXISTEN ALBUMES MIRAMOS A VER QUE CANCIONES HAY
                        
                        '''
                        
                        if len(ALBUMS)==0:
                            print("NO HAY ALBUMES DISPONIBLES...")
                            if len(SONGS)==0:
                                print('TAMPOCO HAY CANCIONES DISPONIBLES')
                            else:
                                print('HAY DISP0NIBLE: ' + str(len(SONGS)) + " cancion(es)")
                                print('¿DESCARGAR CANCION(ES) DISPONIBLE(S)?(y/n): \n')
                            
                                GRUPO_SELECT = str(input(' '))
                                if GRUPO_SELECT=='y':
                                    for i in range(len(SONGS)):
                                        print("DESCARGANDO CACION: " + SONGS[i].replace('/track/', ""))
                                        path= song_jaitsi((url_artista + str(SONGS[i])))
                                        print("CANCION DESCARGADA EN : " +  path)
                    
                                    
                                else: None
                        else: 
                            
                            print('SELECCIONA ALBUM INTRODUCIENDO EL NUMERO A SU IZQUIERDA: \n')
                            k=0
                            for sublist in ALBUMS:
                                nombre_album= sublist.replace('/album/', "")
                                print(str(k) + ') ' + nombre_album )
                                k=k+1
                            print(str(k) + ') TODOS LOS ALBUMS')
                            print(str(k+1) + ') NINGUNO')
                            GRUPO_SELECT = list(map(int, input('Enter numbers: ').split()))
                           
                            if GRUPO_SELECT[0]==int(k)+1:
                                break
                                
                            if GRUPO_SELECT[0]==int(k):     
                                for i in range(len(ALBUMS)):
                                    if 'https://' in ALBUMS[i]:
                                        url_ALBUM= ALBUMS[i]
                                        print("DESCARGANDO ALBUM: ", ALBUMS[i].replace('/album/', ""))
                                    else:
                                        url_ALBUM= url_artista.split("?")[0] + ALBUMS[i]
                                        print("DESCARGANDO ALBUM: ", ALBUMS[i].replace('/album/', ""))
                            
                                    path_descarga= albuma_jaitsi(url_ALBUM)
                                    print("ALBUM DESCARGADO EN : " +  path_descarga)
                        
                            else:     
                                for i in GRUPO_SELECT:
                                    if 'https://' in ALBUMS[i]:
                                        url_ALBUM= ALBUMS[i]
                                        print("DESCARGANDO ALBUM: ", ALBUMS[i].replace('/album/', ""))
                                    else:
                                        url_ALBUM= url_artista.split("?")[0] + ALBUMS[i]
                                        print("DESCARGANDO ALBUM: ", ALBUMS[i].replace('/album/', ""))
                            
                                    path_descarga= albuma_jaitsi(url_ALBUM)
                                    print("ALBUM DESCARGADO EN : " +  path_descarga)
                            
                            
                            for i in range(len(ALBUMS)):
                                if 'https://' in ALBUMS[i]:
                                    CANALES_EXTERNOS.append(ALBUMS[i])
                            
                    url= None     
                            
                    if not len(CANALES_EXTERNOS)==0:
                        print('EN ESTE/OS CANAL/ES HAY REFERENCIAS A CANALES EXTERNOS')
                        print('¿INVESTIGAMOS ESOS CANALES?(y/n): \n')

                        GRUPO_SELECT = str(input(' '))
                        if GRUPO_SELECT=='y':
                            url= [item.split('bandcamp.com')[0] + 'bandcamp.com'  for item in CANALES_EXTERNOS]
                        else: 
                            break
                        


                             

                

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
        
    