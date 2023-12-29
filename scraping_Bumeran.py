# -*- coding: utf-8 -*-
"""
Created on Mon May 29 18:58:14 2023

@author: hp
"""
#------------------------------------------SET-UP
import pandas as pd
import requests
from bs4 import BeautifulSoup 
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

PATH = "D:/pruebas/portalesOfertadeEmplep/"
pathInput = PATH + "2-data/"
pathInterm = PATH + "3-intermediate/"
pathOutput = PATH + "4-output/"

# definition of chromedriver
pathdriver = pathInput + "chromedriver.exe"
# definition of options of in chromedriver
option = webdriver.ChromeOptions()          ### Define las caracteristicas que tendrá el buscador.
user_agent = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
chrome_prefs = {}                           ### DEfinicion de un diccionario.      
option.experimental_options["prefs"] = chrome_prefs ### Funcion que define las caracteristicas del buscador Chrome.
chrome_prefs["profile.default_content_settings"] = {"images": 2} 
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
#option.add_argument( "--headless" )
option.add_argument('user-agent={user_agent}')
# Open driver
driver = webdriver.Chrome(options=option, executable_path=pathdriver ) ### Definicion del WebDriver.

#listado-avisos

## Get links for each anunce**
list_pages_links = list()
for j in range( 1, 24):
  url = 'https://www.bumeran.com.pe/empleos-publicacion-hoy.html?page=' + str( j )
  driver.get( url )
  web_content = driver.find_element(by=By.CSS_SELECTOR , value="#listado-avisos")
  web_content = web_content.get_attribute("innerHTML")
  web_content_soup =  BeautifulSoup( web_content , 'html.parser' )
  links = [child.a.get("href") for child in web_content_soup.children]
  list_pages_links.append(links)


list_links = list()
for i in list_pages_links:
  for j in i:
    list_links.append(j)

## save
pathfile = pathInterm + "2023_12_28_dia_bumeran_Links.csv"
df_jobads = pd.DataFrame( list_links )
df_jobads.to_csv( pathfile , index=False , header=False )