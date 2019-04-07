# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 13:04:34 2019

@author: Oscar
"""

import requests
import shutil
import numpy as np
import os
import random
from random import choice
import re
import time
import csv
from itertools import chain


#EL ROLLO AKI SERÍA ELABORAR UN SISTEMA QUE SEA CAPAZ
# DE IR A BUSCAR SOLAMENTE LAS URLS QUE FALTAN
#CREO QUE LO MEJOR VAS A SER BUSCAR POR FECHAS
# LAS URLS DE LOS ALBUMES ESTAN ORGANIZADOS DE ESTA MANERA...
# MIRAR QUE FECHA ES LA ULTIMA Y BUSCAR HASTA AHÍ... 



read_urls= []
file=os.getcwd()+'\urls.csv'
with open(file, 'rb') as myfile:
     wx = csv.reader(myfile)
     for x in wx:
         read_urls.append(x)