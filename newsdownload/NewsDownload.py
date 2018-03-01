"""
Trabajo de fin de master - Universidad Internacional de La Rioja

Descarga noticias a partir de enlaces e inserta los datos en 
una base de datos mongoDB

@author: Sandra Fresnillo Velasco
@license: MIT
"""

import pandas as pd
import newspaper
import os
from newspaper import Article, Config
import sys
import shutil
from pymongo import MongoClient
from noticia import Noticia
import logging

logger = logging.getLogger('newsdownload')
hdlr = logging.FileHandler('newsdownload.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)

datapath = "urls"
processed = "processed"
files = [f for f in os.listdir(datapath) if os.path.isfile(os.path.join(datapath, f))]

config = Config()
config.fetch_images = False
config.language = 'es'
config.browser_user_agent = 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0'

mongoClient = MongoClient('localhost', 27017)
db = mongoClient.DBNews
collection = db.News

for f in sorted(files, reverse=True):
	print(f)
	urls=pd.read_csv(os.path.join(datapath, f), delimiter=',', error_bad_lines=False, warn_bad_lines=True)
	urls.columns=['URL','TIPO']
	print(urls.head())
	
	for url in urls['URL']:
		print(url)
		a = Article(url, config)
		try:
			a.download()
			a.parse()
		except:
			logger.warning("Error al descargar la noticia "+url)
			
		try:
		 	noticia = Noticia(a.source_url, a.url, a.title, list(a.tags), a.meta_keywords, a.summary, a.text, a.publish_date)
		except:
			logger.warning("Error al crear la noticia "+url)

		noticia.insert(collection)
				
	if not os.path.exists(os.path.join(datapath, processed)):
		os.makedirs(os.path.join(datapath, processed))	
	shutil.move(os.path.join(datapath, f), os.path.join(datapath, processed, f))
	