# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 11:01:27 2023

@author: hp
"""

#------------------------------------------SET-UP
import pandas as pd
import requests
from bs4 import BeautifulSoup 
import datetime
from datetime import timedelta
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import re

PATH = "D:/pruebas/portalesOfertadeEmplep/"
pathInput = PATH + "2-data/"
pathInterm = PATH + "3-intermediate/"
pathOutput = PATH + "4-output/"

#-----------------------------------------FUNCTIONS
def findicador(y):
  if pd.isna(y)==True:
    return(0)
  else:
    if type(re.match( string=y , pattern="/empleos/" ))==type(None):
      return(0)
    else:
      return(1)

## import
##### realizar la especifiacion en esta seccion
fecha_descarga = "2023_12_28"

## import
pathfile = pathInterm + fecha_descarga + "_dia_bumeran_Links.csv"
df_links = pd.read_csv( pathfile , header=None )

##input
list_fecha_descarga = fecha_descarga.split( "_" ) 
today = datetime.date( int(list_fecha_descarga[0]) , int(list_fecha_descarga[1]) , int(list_fecha_descarga[2]) )

#-----------------------------------------MAIN
df_links["indicador"] = df_links[0].apply( lambda x: findicador(x) )
df_links = df_links[df_links["indicador"]==1]
list_links = df_links[0].to_list()
## Definition of web driver
pathdriver = pathInput + "chromedriver.exe"
user_agent = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
option = webdriver.ChromeOptions()          ### Define las caracteristicas que tendrá el buscador.
chrome_prefs = {}                           ### DEfinicion de un diccionario.      
option.experimental_options["prefs"] = chrome_prefs ### Funcion que define las caracteristicas del buscador Chrome.
chrome_prefs["profile.default_content_settings"] = {"images": 2} 
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
#option.add_argument('--headless')
option.add_argument('user-agent={user_agent}')
driver = webdriver.Chrome(options=option, executable_path=pathdriver ) ### Definicion del WebDriver
driver.implicitly_wait(10)
#driver.quit()

##------------------------------------------------FUNCTION
from selenium.common.exceptions import NoSuchElementException
def check_exists_by_xpath(sselect):
    try:
        driver.find_element(by=By.CSS_SELECTOR , value=sselect)
    except NoSuchElementException:
        return False
    return True

#section-detalle > div:nth-child(2) > div > div.sc-hzXNXc.hzPFCc

#j = 0
#url ='https://www.bumeran.com.pe' + list_links[j]
#r = requests.get( url , headers = headers )
#web_content_soup =  BeautifulSoup( r.text , 'html.parser' )

headers = {
'authority': 'www.bumeran.com.pe',
'method': 'GET',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language': 'es,es-ES;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
'Cache-Control': 'max-age=0',
'cookie': '__gads=ID=1db5e9d412dd69b2-2279e976a0b400b1:T=1685993014:RT=1685993014:S=ALNI_MaOBVluwYH8mWKftDcDDV0D-isxwg; __gpi=UID=000009f4d249f26f:T=1685993014:RT=1685993014:S=ALNI_MaqQpOcWcaVtNv80GUnZn8DUpb9RA; _gu=36f0cc42-f707-4731-a495-033ba9868b07; _hjSessionUser_245448=eyJpZCI6IjM2M2E5ZWFiLTE4OWQtNTM0OC1iZjE2LTUzYzZjZmY5MzEwMyIsImNyZWF0ZWQiOjE2ODU5OTMwMjQxMDcsImV4aXN0aW5nIjp0cnVlfQ==; _gcl_au=1.1.1703958477.1693948578; _fbp=fb.2.1693948578613.2013361841; _clck=1o0hy93|2|ffc|0|1251; _gid=GA1.3.1992061376.1695703286; _hjSession_245448=eyJpZCI6IjBjZTA0ZGU3LTE0ZmUtNGIwMS1hZWQ0LWFhMWIxYjcwNjUzOCIsImNyZWF0ZWQiOjE2OTU3MDMyODY3NzIsImluU2FtcGxlIjpmYWxzZX0=; _gs=2.s(); _ga_K7K8FVBZVB=GS1.1.1695703286.5.1.1695703481.38.0.0; _ga=GA1.3.1341034611.1685993016; _gw=2.500971(sc~6%2Cs~s1kt6i)509869(sc~1%2Cs~s0j7mv)511265(sc~1%2Cs~s1kt18)u%5B%2C%2C%2C%2C%5Dv%5B~gtqvw%2C~2%2C~1%5Da(); _clsk=153e6f|1695704561231|4|1|p.clarity.ms/collect; g_state={"i_p":1695711763550,"i_l":1}; __cf_bm=wSCAcv0vUEmnfFvBzRINDhjmLN9e3so4M7mAPwlLi5o-1695704577-0-Ad5U6AN66O/sklvtSGB30L/78z27SOmkgX7JNBCwtBu0kVc58AOtk++R9eqIZHIwzeTjSlO3eEaqCHVpPjlQPOg=',
'Sec-Ch-Ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
'Sec-Ch-Ua-Mobile': '?0',
'Sec-Ch-Ua-Platform': 'Windows',
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-User': '?1',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41'}


#--------------------------------------DONWLOAD
for j in range( 0 , len(list_links) ):
  url ='https://www.bumeran.com.pe' + list_links[j]
  driver.get( url )
  ## contenido
  web_content = driver.find_element(by=By.CSS_SELECTOR , value="#ficha-detalle > div:nth-child(2) > div > div")
  web_content = web_content.get_attribute("innerHTML")
  web_content_soup =  BeautifulSoup( web_content , 'html.parser' )
  ## titulo y nombre de firma
  web_titulo = driver.find_element(by=By.CSS_SELECTOR , value="#header-component")
  web_titulo = web_titulo.get_attribute("innerHTML")
  web_titulo_soup =  BeautifulSoup( web_titulo , 'html.parser' )
  ## Edicion de titulo y firma
  titulo = web_titulo_soup.findChildren('h1')[0].get_text()
  firma = web_titulo_soup.findChildren( name="div" , attrs="sc-lbihag cvOoLI" )[0].get_text()
  #firma = web_titulo_soup.findChildren( name="div" , attrs="sc-eUqAvv THvxr" )[0].get_text()
  ## Edicion de contenido
  list_children = [ i for i in web_content_soup.children ]
  list_contenido = list()
  for i in range(1, len(list_children)-1 ):
    list_contenido.append(list_children[i].get_text(' '))
  contenido = ' '.join(list_contenido)
  ##Edicion de fecha
  str_dia = list_children[ 0 ].get_text('|')
  locacion = str_dia.split('|')[1]
  fechapublicacion = str_dia.split('|')[0]
  ##Guardar en dataframe
  df_loop = pd.DataFrame({'titulo': titulo, 'firma': firma, 'locacion':locacion,
            'fechaPublicacion':fechapublicacion,'fechaDescarga':today.isoformat(),
            'contenido':contenido}, index=[j])
  ##Save
  if j==0:
    df_Contenido = df_loop
  else:
    df_Contenido = pd.concat( [df_Contenido , df_loop] )

#df_Contenido.drop_duplicates(inplace=True)
## save
#pathfile = pathOutput + "bumeran_semana_23_06_24.csv"
#df_Contenido.to_csv( pathfile , header=False , index = False )

##
df_Contenido.reset_index( inplace=True )
df_Contenido.drop( ["index"] , axis=1 , inplace=True)
##
pathfile = pathOutput + "bumeran_dia_"+ fecha_descarga +".pkl"
df_Contenido.to_pickle( pathfile )
