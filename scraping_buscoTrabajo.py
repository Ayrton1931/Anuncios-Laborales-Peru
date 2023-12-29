# -*- coding: utf-8 -*-
"""
Created on Wed May 31 18:33:20 2023
Modified: Nov 3 2023s
@author: hp
"""
#------------------------------------------SET-UP
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
from datetime import timedelta
import re
import os

PATH = "D:/pruebas/portalesOfertadeEmplep/"
pathInput = PATH + "2-data/"
pathInterm = PATH + "3-intermediate/"
pathOutput = PATH + "4-output/"

##
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41'}
list_pages_links = list()
for i in range(1,167):
    url = "https://www.buscojobs.pe/ofertas/" + str(i) + "?fechainicio=1"
    r = requests.get( url, headers = headers )
    if r.status_code==200:
        source_html = BeautifulSoup( r.text , "html.parser" )
        anounces = source_html.find_all( "div" , class_ = "row ListadoOfertas_result__vlmRK click undefined" )
        for i in anounces:
            element_link = i.find_all( "a" ,class_ = "ListadoOfertas_containerLink__NlwJU" )
            if len(element_link)>0:
                list_pages_links.append( element_link[0]["href"] )

## save
df_links = pd.DataFrame( list_pages_links )
pathfile = pathInterm + "2023_12_28_dia_buscotrabajo_Links.csv"
df_links.to_csv( pathfile , header=False , index=False )
df_links.shape
