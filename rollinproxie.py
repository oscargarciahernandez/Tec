# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 01:36:23 2019

@author: Oscar
"""

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random


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
    






ua = UserAgent() # From here we generate a random user agent
proxies = [] # Will contain proxies [ip, port]

# Main function
def main():
  # Retrieve latest proxies
  proxies_req = requests.get('https://www.sslproxies.org/')
  proxies_req.add_header('User-Agent', ua.random)
  
  headers = {'user-agent': 'ua.random'}
   
  proxies_req = requests.get('https://www.sslproxies.org/', headers=headers)

  proxies_doc = urlopen(proxies_req).read().decode('utf8')

  soup = BeautifulSoup(proxies_req.content, 'html.parser')
  proxies_table = soup.find(id='proxylisttable')
  
  proxies=[]

  # Save proxies in the array
  for row in proxies_table.tbody.find_all('tr'):
    proxies.append({
      'ip':   row.find_all('td')[0].string,
      'port': row.find_all('td')[1].string
    })

  # Choose a random proxy
  #proxy_index = random_proxy()
  #proxy = proxies[proxy_index]

  total_info=[]
  for n in range(1, 100):
    
    
    proxi='http://' + str(proxies[n]['ip'])+ ':' +proxies[n]['port']
    
    proxi1 = {'http': str(proxi)}
    
    
    
    url_base= 'https://www.electrobuzz.net/page'
        
    list_info=[]
    for i in vector_dado:
        url_page= url_base + '/' + str(i)+ '/'
        
        req= requests.get(url_page, proxies= proxi1)
        soup = BeautifulSoup(req.content, 'html.parser')
        soup2=soup.find_all('article')

        
        list_info.append(obtn_link_title_img(soup2))
        
    total_info.append(list_info)

# Every 10 requests, generate a new proxy
if n % 10 == 0:
  proxy_index = random_proxy()
  proxy = proxies[proxy_index]

# Make the call
try:
  my_ip = urlopen(req).read().decode('utf8')
  print('#' + str(n) + ': ' + my_ip)
except: # If error, delete this proxy and find another one
  del proxies[proxy_index]
  print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
  proxy_index = random_proxy()
  proxy = proxies[proxy_index]

# Retrieve a random index proxy (we need the index to delete it if not working)
def random_proxy():
  return random.randint(0, len(proxies) - 1)

if __name__ == '__main__':
  main()