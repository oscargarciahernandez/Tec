#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 06:55:15 2019

@author: oscar
"""

'''
TODO
MUCHAS MUCHISIMAS COSAS

- CREAR UN TXT QUE VAYA GUARDANDO LAS URLS DE BANDCAMP QUE VA ENCONTRANDO
 O HACER UN BARRIDO PRELIMINAR.... ESTO TIENEN SENTIDO EN PLAYLIST 
 DE PAGINAS QUE SUBAN POPURRI...HATE. JAELOS Y POCO MAS
 
- MODIFICAR FUNCION ANDONI PARA QUE GUARDE EN LA CARPETA QUE YO QUIERO Y ASI 
PODER LELVAR UN CONTROL Y NO GUARDAR REPETIDAMENTE COSAS, COMO AHORA ME PASA

- JOTAKE

'''

from pytube import YouTube
from pytube import Playlist
import re
import os
from  itertools import chain
import tqdm
import multiprocessing as mp
import subprocess   
  
def COMMANDO_POR_CONSOLA(COMMANDO, PATH_COMANDO):
    '''
    FUNCION PARA EJECUTAR UN COMMANDO POR CONSOLA
    HAY QUE DECIR EL COMMANDO QUE QUEREMOS Y EL PATH DONDE SE VA A 
    EJECUTAR DE ESTA MANERA ELIMINAMOS LAS NECESIDAD DE cd /home/ ....
    '''
    #EJECUTAMOS EL MODELO 
    procces= subprocess.Popen(COMMANDO,stdout= subprocess.PIPE, cwd= PATH_COMANDO, shell=True)
    output, error = procces.communicate()
    print('Done')        
    

'''
LO DE DESCARGAR UNA LISTA DE REPRODUCCION SUENA PRECIOSO
PERO FALLA CON ALGUN VIDEO DEFECTUOSO Y PETA.
MEJOR SACAMOS LAS URLS Y LUEGO DESCARGAMOS VIDEO A VIDEO 
ASI PODEMOS PONER UN TRY CATCH.
'''
'''
SELLOS O PAGINAS SIN PLAYLISTS

jaelos
ninja tune ------------- https://ninjatune.bandcamp.com/
shallnotfade ----------- https://shallnotfade.co.uk/
lobstertheremin - ------ https://lobstertheremin.com/
sincopatmusic ---------- https://sincopat.bandcamp.com/music
hivern discs ----------- https://hiverndiscs.bandcamp.com/  
Analogica Force -------- https://analogicalforce.bandcamp.com/
involve (REGAL) -------- https://involve-records.bandcamp.com/music
modern obscure music ---- https://modernobscuremusic.bandcamp.com/
forbiden colours -------- https://forbiddencolours.bandcamp.com/
 Musexindustries -------- https://musexindustries.bandcamp.com/
perc traxxx ------------- https://perctrax.bandcamp.com/
token
Ostgut Ton --------------- https://ostgut.bandcamp.com/
Stroboscopic Artefacts
blueprint (JAMES RUSKIN)---https://blueprintrecords.bandcamp.com/
'''


'''
SELLOS QUE NO TIENEN PAGINA OFICIAL EN YT
O ESO CREO

giegling
northernelectronics -------- https://northernelectronics.bandcamp.com/
hemlock --------------------- https://hemlockrecordings.bandcamp.com/
afterlife
semantica records ----------- https://semanticarecords.bandcamp.com/
'''



DRUMCODE_RELEASES_PL= 'https://www.youtube.com/playlist?list=PLhkZrfli9PCoSk-8w4ANUS3WgNG2gQ4aB'
RUNNING_BACK_TRAXX= 'https://www.youtube.com/playlist?list=PLow8O9Lc3srTrX1L6ruPRVukMd4vCPL8a'
NINBA_KRAVIZ_LABEL= 'https://www.youtube.com/playlist?list=PLMWPOVFOonzVjauhhjtvMUO8F1OBOCZfJ'
POLE_GROUP_RELEASES= 'https://www.youtube.com/playlist?list=PLkjr3p36P2PDpg38L-J2oZ4Cs3NHCtbRs'
POLE_GROUP_AINE_RELEASES= 'https://www.youtube.com/watch?v=X_zqXa1MSbY&list=PLkjr3p36P2PD_zE7V9AlUuPmNOkW-4AaU'
SUARA_TEHCNO_BACK_CATS= 'https://www.youtube.com/playlist?list=PLx0AxQYjLjbTwjEE1pinP4ohmYm47Uqiz'
MORD_CATALOGUE= 'https://www.youtube.com/playlist?list=PLxNHCMcVaEYKlTdtWbgb_uueArYJ-llzl'
INDUSTRIAL_TECHNO_UNITED= 'https://www.youtube.com/playlist?list=PL1Ia8igkNbxfrjNvI0zjXI-NS5yiiTX2E'
HATE_TRACKS= 'https://www.youtube.com/playlist?list=PL1ntfXx-b2MyxKr-kRkpe0xxcqwB4fRLz'

DICTIONARY_YT= {'HATE':HATE_TRACKS,
                'DRUMCODE':DRUMCODE_RELEASES_PL,
                'RUNNING_BACK': RUNNING_BACK_TRAXX,
                'NINA_KRAVIZ_LAB': NINBA_KRAVIZ_LABEL,
                'POLE_GROUP_RELEASES': POLE_GROUP_RELEASES,
                'POLE_GROUP_AINE':POLE_GROUP_AINE_RELEASES,
                'SUARA': SUARA_TEHCNO_BACK_CATS,
                'MORD': MORD_CATALOGUE,
                'IND_TEC_UNIT':INDUSTRIAL_TECHNO_UNITED}

def GET_BANDCAMP_LINK(url):
    '''
    FUNCION PARA BUSCAR LINKS DE BANDCAMP EN LA DESCRIPCION DE UN VIDEO DE YOUTUBE
    DEVUELVE UN STRING CON LA URL DEL VIDEO Y EL RESULTADO.
    URL__LINKBANDCAMP
    URL__EMPTY
    URL_ERROR_TIPO_ERROR
    '''
    try:
        yt= YouTube(url)
        print('BUSCANDO LINK BANDCAMP EN ------------' + yt.title)
    
        
        LINK_BANDCAMP=[item.split('.com')[0] + '.com' for item in re.findall("(?P<url>https?://[^\s]+)", yt.watch_html) if 'bandcamp' in item]
        if LINK_BANDCAMP:
            return([url + '__' + item for item in LINK_BANDCAMP])
        else:
            return(url + '__EMPTY')
    except Exception as e:
        return(url+ '__ERROR__' + str(e))
        
    
    

if True:
    try:
        FILE_PATH= os.path.join(os.path.dirname(__file__))
        print(FILE_PATH)
    except:
        FILE_PATH= '/home/oscar/Tec/'
        pass

for INDEX in range(len(DICTIONARY_YT)):
    YT_NAME= list(DICTIONARY_YT.keys())[INDEX]
    YT_PLAYLIST=  list(DICTIONARY_YT.values())[INDEX]
    
    
    PATH_DONWLOAD= FILE_PATH + '/YT/' + YT_NAME + '/'
    if not os.path.exists(PATH_DONWLOAD):
        os.makedirs(PATH_DONWLOAD, exist_ok=True)
    
    print('BUSCANDO URLS EN PLAYLIST')
    playlist = Playlist(YT_PLAYLIST)
    playlist.populate_video_urls()
    VIDEOS_PLAYLIST= playlist.video_urls
    
    try:
        with open(PATH_DONWLOAD + 'URLS_CHECKED.txt', 'r') as file:
            URLS_CHECKED= file.read().splitlines()
    except:
        URLS_CHECKED= []
        print('TODAVÍA NO EXISTE URLS_CHECKED.txt')
    
    NEW_URLS= [item for item in VIDEOS_PLAYLIST if item not in URLS_CHECKED]
       
    BUSCAR_LINKS_BANDCAMP= True
    if BUSCAR_LINKS_BANDCAMP: 
        LINKS_bandcamp= []
        VIDEOS_WITHOUT_BANDCAMP= []
        URLS_CHECKED= []
        for url in NEW_URLS:
        
            try:
                pool = mp.Pool(mp.cpu_count()-6)
                results=[]
                for _ in tqdm.tqdm(pool.imap_unordered(GET_BANDCAMP_LINK, NEW_URLS[1:10]), total=len(NEW_URLS)):
                    results.append(_)
                    pass
                #MATAMOS SUBPROCESOS 
                pool.close()
                pool.terminate()
                pool.join()
                results_merge= list(chain.from_iterable(results))
                
                yt= YouTube(url)
                print('BUSCANDO LINK BANDCAMP EN ------------' + yt.title)
                
                LINK_BANDCAMP=[item for item in re.findall("(?P<url>https?://[^\s]+)", yt.watch_html) if 'bandcamp' in item]
                if LINK_BANDCAMP:
                    LINKS_bandcamp.append(LINK_BANDCAMP)
                else:
                    VIDEOS_WITHOUT_BANDCAMP.append(url)
                
                URLS_CHECKED.append(url)
                
                
            except:
                print('ERROR BUSCANDO LINKS BANDCAMP')
                
        SET_LINKS_BANDCAMP= set(list(chain(*LINKS_bandcamp)))
       
            
        with open(PATH_DONWLOAD + 'BANDCAMP_LINKS.txt', 'a') as file:
            for link in [item.split('.com')[0] + '.com' for item in SET_LINKS_BANDCAMP]:
                file.writelines(link + '\n')
       
            
        with open(PATH_DONWLOAD + 'VIDEOS_WITHOUT_BANDCAMP.txt', 'a') as file:
            for link in VIDEOS_WITHOUT_BANDCAMP:
                file.writelines(link+ '\n')
           
        with open(PATH_DONWLOAD + 'URLS_CHECKED.txt', 'a') as file:
            for link in URLS_CHECKED:
                file.writelines(link + '\n')
           










         
DOWNLOAD_SONG= False
if DOWNLOAD_SONG:
    os.chdir(PATH_DONWLOAD)
    
    with open('DOWNLOADED_LINKS.txt', 'r') as file:
        LINKS_DOWNLOADED= file.readlines()
    
    LINKS_DOWNLOADED= [item.replace('\n','') for item in LINKS_DOWNLOADED]
    
    VIDEOS_POR_DESCARGAR= [item for item in VIDEOS_PLAYLIST if item not in LINKS_DOWNLOADED]
    
    for url in VIDEOS_POR_DESCARGAR:
        DOWNLOADED_FILES= [item.replace('.webm','').replace('.mp4','') for item in os.listdir()]
    
        try:
            yt= YouTube(url)
            if 'podcast' in yt.title.lower():
                print('IGNORAMOS PODCAST')
            else:
                if yt.title in DOWNLOADED_FILES:
                    print(str(yt.title) + '  YA HA SIDO DESCARGADA ANTES')
                    with open(PATH_DONWLOAD + 'DOWNLOADED_LINKS.txt', 'a') as file:                    
                            file.writelines(url+ '\n')
                            
                else:
                    print('DESCARGANDO ----- ' + str(yt.title))
                    
                    '''
                     ORDENAMOS LAS OPCIONES PARA DESCARGAR EL AUDIO CON MEJOR CALIDAD
                     Y DESCARGAMOS LA MEJOR. 
                     HAY QUE DAR UNA VUELTA A LO DE ENCONTRAR LAS URLS QUE QUERAMOS Y 
                     TAMBIEN HABRÁ QUE HACER ALGUNA COSITA PARA ELEGIR UN PATH
                     DE DESCARGA... EN FUNCION DEL NOMBRE DEL AUTOR, NOMBRE DEL ALBUM O VETE A SABER.
                     
                     ESTE DESC, ES PARA CAMBIAR EL ORDEN, DE MAYOR A MENOR O DE MENOR A MAYOR.
                     POCO MAS. 
                     
                     ES RARO PORQUE TODAVIA CUANDO USO FILTER SOLO AUDIO DESCARGA UN VIDEO. 
                     '''
                    yt.streams.filter(only_audio= True).order_by('bitrate').desc().first().download(PATH_DONWLOAD)
                    with open(PATH_DONWLOAD + 'DOWNLOADED_LINKS.txt', 'a') as file:                    
                            file.writelines(url + '\n')
                            
        except:
            
            print('ERROR DESCARGANDO VIDEO')
            
            with open(PATH_DONWLOAD + 'DOWNLOADED_LINKS.txt', 'a') as file:
                file.writelines(url + ' (ERROR)' + '\n')
    
    
    
    CONVERT_TO_MP3= False
    
    if CONVERT_TO_MP3:
        DOWNLOADED_FILES= os.listdir()
        for file in DOWNLOADED_FILES:    
            COMANDO_CONVERSION= 'ffmpeg -i "{0}" "{1}"'.format(file,file.replace('.webm','.mp3').replace('.mp4','.mp3'))
            COMMANDO_POR_CONSOLA(COMANDO_CONVERSION, os.getcwd())
        
    else:
        print('CONVERSION A MP3 DESACTIVADA')
    
    
    
    
    
    
    
    
    '''
    from bs4 import BeautifulSoup
    import requests
    
    
    
    HATE_videos= 'https://www.youtube.com/channel/UC6qQOTx9LuKMC5p2dbjmSRg/videos'
    
    session = requests.Session()
    session.trust_env = False
    user_agents= session.get(HATE_videos)
    user_soup = BeautifulSoup(user_agents.content, 'html.parser')
                            
    x= user_soup.find('div', {'class':'style-scope ytd-item-section-renderer'})
    
    COMO NO SE PUEDE HACER SCROLL DE MANERA SENCILLA USANDO REQUESTS
    CAMBIAMOS DE PLAN. VAMOS A DESCARGAR LA LISTA DE REPRODUCCION 
    USANDO PLAYLIIST DE LA LIBRERIA PYTUBE
    
    
    
    
    PARA TRANSFORMAR DE MP4 A MP3
    
    ffmpeg -i downloaded_filename.mp4 new_filename.mp3
    
    '''
          