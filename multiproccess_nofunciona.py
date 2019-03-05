# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 17:18:30 2019

@author: Oscar
"""

### numero aleatorio para elegir el proxii
list_random=[]
for i in np.arange(0,len(vec_pags_div)):
     n=random.randrange(0, len(proxies))
     list_random.append(n)
    
vec_pags_proxi= []
for i in range(0,len(vec_pags_div)):
    vec_pags_proxi.append(list([vec_pags_div[i],set_proxi_for_req(proxies,list_random[i])]))
    
    

from multiprocessing import Pool

if __name__ == '__main__':
    p = Pool(5)
    print(p.map(srch_info_chg_ua, list(vec_pags_div[:5],users_list)))
    
    
    

#####Multiproccess cambiando user-agents    
import multiprocessing
from functools import partial
from contextlib import contextmanager

@contextmanager
def poolcontext(*args, **kwargs):
    pool = multiprocessing.Pool(*args, **kwargs)
    yield pool
    pool.terminate()


if __name__ == '__main__':
    with poolcontext(processes=3) as pool:
        results = pool.map(partial(srch_info_chg_ua, ua=users_list),vec_pags_div[:5])
    print(results)




import itertools
from multiprocessing import Pool, freeze_support


def func_star(a_b):
    """Convert `f([1,2])` to `f(1,2)` call."""
    return srch_info_chg_ua(*a_b)

def main():
    pool = Pool()
    a_args = vec_pags_div[:3]
    second_arg = users_list
    pool.map(func_star, itertools.izip(a_args, itertools.repeat(second_arg)))

if __name__=="__main__":
    freeze_support()
    main()
    
    
    