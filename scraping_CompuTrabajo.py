# -*- coding: utf-8 -*-
"""
Created on Wed May 31 17:02:25 2023
Modified: Nov 3 2023
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

## ubicaciones
list_ubicaciones= ["/empleos-en-lima", "/empleos-en-arequipa", "/empleos-en-la-libertad","/empleos-en-piura",
"/empleos-en-lambayeque", "/empleos-en-ica", "/empleos-en-junin",
"/empleos-en-cusco", "/empleos-en-ancash", "/empleos-en-cajamarca", "/empleos-en-san-martin",
"/empleos-en-moquegua", "/empleos-en-puno", "/empleos-en-loreto", "/empleos-en-huanuco",
"/empleos-en-tacna", "/empleos-en-ucayali", "/empleos-en-ayacucho", "/empleos-en-pasco"]

## Get number of pages in each departmanto
user_agent = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
list_pages = dict()
for k in list_ubicaciones:
    url =  "https://pe.computrabajo.com"+ k + "?pubdate=3"
    r = requests.get( url , headers = {"user-agent": user_agent}  )
    if r.status_code==200:
        content =  BeautifulSoup( r.text , 'html.parser' )
        web_content = content.find_all( "div" , {"id":"offersGridOfferContainer" , "class":"box_grid parrilla_oferta" } )
        if len(web_content)>0:
            web_content_text = web_content[0].find_all( "h1" ,  class_="title_page" )
            find_n = re.findall(pattern="\d", string=web_content_text[0].get_text())
            number_pages = int(''.join( find_n ))
            if number_pages<=20:
                list_pages[k] = 1
            else:
                list_pages[k]= int(number_pages/20) + 2

## Get Urls of Each Anounce
list_all_links = list()
for depart in list_ubicaciones:
    if depart in list_pages:
        for i in range(1 , list_pages[depart] ):
            url =  "https://pe.computrabajo.com" + depart +"?pubdate=1&p=" + str( i )
            r = requests.get( url , headers = {"user-agent": user_agent} )
            if r.status_code == 200:
                content =  BeautifulSoup( r.text , 'html.parser' )
                job_Ads = content.find_all('h2', class_="fs18 fwB")
                for ii in job_Ads:
                    job_ads_link = ii.find_all( "a" , class_="fc_base" )[0].get('href')
                    list_all_links.append(job_ads_link )

## to dataframe
df_all_links = pd.DataFrame( list_all_links )
## Export
pathfile = pathInterm + "2023_12_28_dia_Computrabajo_Links.csv"
df_all_links.to_csv( pathfile , header=False , index=False )