### Libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
from datetime import timedelta

PATH = "D:/pruebas/portalesOfertadeEmplep/"
#PATH = "/accounts/projects/pkline/peru-educ/Documents/__Labor/6_siaf/"
pathInput = PATH + "2-data/"
pathInterm = PATH + "3-intermediate/"
pathOutput = PATH + "4-output/"

## import
##### realizar la especifiacion en esta seccion
fecha_descarga = "2023_12_28"

## Importa base de datos 
pathfile = pathInterm + fecha_descarga + "_dia_mipleo_Links.csv"
df_links = pd.read_csv( pathfile )
list_links = df_links["0"].to_list()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41'}

##input
list_fecha_descarga = fecha_descarga.split( "_" ) 
today = datetime.date( int(list_fecha_descarga[0]) , int(list_fecha_descarga[1]) , int(list_fecha_descarga[2]) )

###
for idx in range(0, len(list_links)):
    url = list_links[idx]
    r = requests.get( url=url , headers=headers )
    content_html = BeautifulSoup( r.text , "html.parser")
    ###
    descripcion = content_html.find_all( "ul" , class_="info_item" )
    descripcion_str = "|".join([i.get_text() for i in descripcion[0].find_all("li") ])
    ###
    localidad_html = content_html.find_all("h2" , class_="subtitle_item")
    localidad = localidad_html[0].get_text()
    localidad = localidad.split( "en" )[1]
    localidad = localidad.strip() 
    ###
    titulo_html = content_html.find_all("div" , class_="header_item")
    titulo = titulo_html[0].findChildren("h1")
    titulo = titulo[0].get_text()
    ###
    lateral_box_html = content_html.find_all("div" , class_="col_rt small")
    firma_html = lateral_box_html[0].find_all( "span" , class_="title_box" )
    firma = firma_html[0].get_text()
    ###
    contenido_html = content_html( "div" , style="font-size:1.2em;color:#474747;font-weight:400;padding:20px 0px 20px 0px;" )
    contenido = "|".join([i.get_text() for i in contenido_html[0].find_all( "p" )])
    ##Guardar en dataframe
    df_loop = pd.DataFrame( {'titulo': titulo, 'firma': firma, 'locacion':localidad, 'fechaDescarga':today.isoformat(),
                'contenido':contenido, 'descripcion':descripcion_str } , index=[idx] )
    ##Save
    if idx == 0:
        df_Contenido = df_loop
    else:
        df_Contenido = pd.concat( [df_Contenido , df_loop] )

## save
df_Contenido.reset_index( inplace=True )
##
pathfile = pathOutput + "mipleo_dia_" + fecha_descarga + ".pkl"
df_Contenido.to_pickle( pathfile )