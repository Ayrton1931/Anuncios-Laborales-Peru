

### Libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup

PATH = "D:/pruebas/portalesOfertadeEmplep/"
#PATH = "/accounts/projects/pkline/peru-educ/Documents/__Labor/6_siaf/"
pathInput = PATH + "2-data/"
pathInterm = PATH + "3-intermediate/"
pathOutput = PATH + "4-output/"

###
list_Depart = [  "amazonas","ancash","apurimac","arequipa","ayacucho","cajamarca","callao","cusco",
                    "extranjero","huancavelica","huanuco","ica","junin","la-libertad","lambayeque",
                    "lima","loreto","madre-de-dios","moquegua","pasco","piura","puno","san-martin","tacna",
                    "tumbes","ucayali"]
list_depart_path =  [ "https://www.mipleo.com.pe/ofertas-de-trabajo/empleos-" + i + "/?q=&range=1" for i in list_Depart ]

## headers
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41'}

###
list_links = list()
for link in list_depart_path:
    r = requests.get( link , headers = headers )
    if r.status_code==200:
        source_html = BeautifulSoup( r.text , "html.parser" )
        ## numeros de anuncios publicados hoy.
        n_anun_html = source_html.find_all( "div" , class_="head_list" )
        n_anun = n_anun_html[0].findChildren( name="h2" )[0].get_text()
        n_anun = n_anun.replace("Ofertas de trabajo" , "")
        n_anun = int( n_anun.replace(",","").strip() )
        if n_anun>0:
            if n_anun/20 < 1:
                list_anun = source_html.find_all( "div" , class_="item_list" )
                for anun in list_anun:
                    anun_child = anun.find_all( "span" , class_="titleAd" )
                    href = anun_child[0].find_all('a', href=True)
                    list_links.append(href[0]["href"])
            else:
                for j in range(1 , int(n_anun/20) + 2 ):
                    r = requests.get( link + "&pag=" + str(j) , headers = headers )
                    if r.status_code==200:
                        source_html = BeautifulSoup( r.text , "html.parser" )
                        list_anun = source_html.find_all( "div" , class_="item_list" )
                        for anun in list_anun:
                            anun_child = anun.find_all( "span" , class_="titleAd" )
                            href = anun_child[0].find_all('a', href=True)
                            list_links.append(href[0]["href"])

### save
df_links =pd.DataFrame( list_links )
pathfile = pathInterm + "2023_12_28_dia_mipleo_Links.csv"
df_links.to_csv( pathfile , index=False )