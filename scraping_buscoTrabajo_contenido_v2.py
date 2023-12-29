# -*- coding: utf-8 -*-
"""
Created on Wed Oct 04 2023

@author: hp (colgado2666@gmail.com)
"""
#------------------------------------------SET-UP
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
from datetime import timedelta
import re
import os

## "Settear" directorio de trabajo
PATH = "D:/pruebas/portalesOfertadeEmplep/"
pathInput = "2-data/"
pathInterm = "3-intermediate/"
pathOutput = "4-output/"

##### realizar la especifiacion en esta seccion
fecha_descarga = "2023_12_28"

## Importa base de datos 
pathfile = pathInterm + fecha_descarga + "_dia_buscotrabajo_Links.csv"
df_links = pd.read_csv( pathfile , header=None )

def IdentificadorNULL(x):
    if re.search( string=x , pattern="fechainicio=" ):
        return(0)
    elif re.match( string=x , pattern="/ofertas" ):
        return(0)
    else:
        return(1)

##
df_links["identificador"] = df_links[0].apply( lambda x : IdentificadorNULL(x) )
df_links = df_links[df_links["identificador"]==1]
list_links = df_links[0].to_list()

##input
list_fecha_descarga = fecha_descarga.split( "_" ) 
today = datetime.date( int(list_fecha_descarga[0]) , int(list_fecha_descarga[1]) , int(list_fecha_descarga[2]) )
## headers
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41'}

### MAIN

for j in range(0, len(list_links)):
    url = 'https://www.buscojobs.pe' + list_links[j]
    r = requests.get( url , headers = headers )
    if r.status_code==200:
        source_html = BeautifulSoup( r.text , "html.parser" )
        ## Titulo
        web_titulo_soup = source_html.find_all( "div" , class_="row title-heading no-margin-top" )
        titulo = web_titulo_soup[0].get_text("|")
        titulo = titulo.split("|")[0]
        ##Contenido
        web_content_soup = source_html.find_all( "div" , class_="OfertaDetalle_oferta_tabs_content___CTuq" )
        web_content_soup = web_content_soup[0].find_all( "div" , class_="text-container" )
        list_children = [ i.get_text(' ') for i in web_content_soup[0].children ] 
        contenido = ' '.join(list_children)
        contenido = contenido.replace("\n", "")
        contenido = contenido.replace("\t", "")
        ## Requerimientos
        requer = web_content_soup[1].find_all( "div" , style="margin-bottom:10px" )
        requerimientos = ". ".join([i.get_text(" ") for i in requer ])
        requerimientos = requerimientos.replace( "\n", "" )
        requerimientos = requerimientos.replace( "\t", "" )
        ## Unir con contenido
        contenido = contenido + ". Requerimientos: " + requerimientos
        ## Firma
        web_firma_soup = source_html.find_all( "div" , class_="OfertaDetalle_oferta_main_top__eYT07" )
        nombre_firma = web_firma_soup[0].find_all( "div" , class_="col-sm-12 no-padding-right")
        nombre_firma = nombre_firma[1].get_text("")
        ## Locacion
        web_locacion = web_firma_soup[0].find_all( "div" , class_="col-sm-12 detalles")
        list_result = [i.get_text(" ") for i in web_locacion[0].children]
        locacion = list_result[0].replace( "Lugar :" , "" )
        locacion = locacion.strip()
        ## fecha:
        fechapublicacion = today.isoformat()
        ## save
        df_loop = pd.DataFrame({'titulo': titulo, 'firma': nombre_firma, 'locacion':locacion,
                        'fechaDescarga':today.isoformat(),
                        'contenido':contenido}, index=[j])
        ##
        if ('df_Contenido' in globals())==False:
            df_Contenido = df_loop
        else:
            df_Contenido = pd.concat( [df_Contenido , df_loop] )

## save
df_Contenido.drop_duplicates(inplace=True)
##
pathfile = pathOutput + "buscotrabajo_dia_" + fecha_descarga + ".pkl"
df_Contenido.to_pickle( pathfile ) 


