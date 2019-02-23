# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 04:24:31 2019

@author: Oscar
"""

def abestia_jaitsi(url):
       import os
       from mutagen import File        
       from mutagen.id3 import TPE1, TIT2, TRCK, TALB, APIC, TYER
       import re
       import requests
       import html
       
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
       import re
       import requests
       import os
       import html

       
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
       path_abuma=path_hasierakoa + '\\' + albuma
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
              
def artista_jaitsi(url):
       import re
       import requests
       import os
       import html

       
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
       import re
       pattern=re.compile('[?\\\/|<>():*]')
       path=re.sub(pattern, '', path)
       return(path)