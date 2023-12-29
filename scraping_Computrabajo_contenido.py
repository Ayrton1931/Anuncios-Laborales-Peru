# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 23:13:10 2023

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

### SET UP working Directory
PATH = "D:/pruebas/portalesOfertadeEmplep/"
os.chdir(PATH)
pathInput = "2-data/"
pathInterm = "3-intermediate/"
pathOutput = "4-output/"

## import
fecha_descarga = "2023_12_28"
pathfile = pathInterm + fecha_descarga + "_dia_Computrabajo_Links.csv"
df_links = pd.read_csv( pathfile , header=None )
list_links = df_links[0].to_list()
#
list_fecha_descarga = fecha_descarga.split( "_" )
today = datetime.date( int(list_fecha_descarga[0]) , int(list_fecha_descarga[1]), int(list_fecha_descarga[2]))


#-----------------------------------------MAIN
list_links = df_links[0].to_list()

user_agent = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
for j in range(0 , len(list_links) ):
    url = 'https://pe.computrabajo.com' + list_links[j]
    r = requests.get( url , headers = {"user-agent": user_agent} )
    if r.status_code == 200:
        web_titulo_soup =  BeautifulSoup( r.text , 'html.parser' )
        web_titulo_soup = web_titulo_soup.find_all( "div" , class_="container" )
        titulo = web_titulo_soup[1].findChildren('h1')[0].get_text()
        firma_locacion = web_titulo_soup[1].findChildren('p')[0].get_text()
        firma = firma_locacion.split("-")[0]
        locacion = firma_locacion.split("-")[1]
        ### Contenido
        web_content = BeautifulSoup( r.text , 'html.parser' )
        web_content = web_content.find_all( "p" , class_="mbB" )
        list_children = [ i.get_text(' ') for i in web_content[0].children ]
        contenido = ' '.join(list_children)
        ## Requerimiento
        web_reque = BeautifulSoup( r.text , 'html.parser' )
        web_reque = web_reque.find_all( "ul" , class_="disc mbB" )
        requerimientos = '. '.join([ i.get_text('') for i in web_reque[0].children ])
        requerimientos = requerimientos.replace( "\n", "" )
        ## union contenido y requerimientos
        contenido = contenido + ". Requerimientos:" + requerimientos
        df_loop = pd.DataFrame({'titulo': titulo, 'firma': firma, 'locacion':locacion,
                                'fechaDescarga':today.isoformat(),
                                'contenido':contenido}, index=[j])
        ## save
        if ('df_Contenido' in globals())==False:
            df_Contenido = df_loop
        else:
            df_Contenido = pd.concat( [ df_Contenido , df_loop ] )

##
df_Contenido.drop_duplicates(inplace=True)
#df_Contenido.reset_index( inplace=True )
#df_Contenido.drop( ["index"] , axis=1 , inplace=True)
##
pathfile = pathOutput + "computrabajo_dia_" + fecha_descarga + ".pkl"
df_Contenido.to_pickle( pathfile )