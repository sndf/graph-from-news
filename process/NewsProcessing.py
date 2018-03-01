"""
Trabajo de fin de master - Universidad Internacional de La Rioja

Selecciona las noticias de la base de datos MongoDB, las procesa
con NLP para extraer las entidades y genera el fichero con las
relaciones entre entidades

@author: Sandra Fresnillo Velasco
@license: MIT
"""
import sys
from pymongo import MongoClient
import spacy
import re
from collections import defaultdict
import pickle

mongoClient = MongoClient('localhost', 27017)
db = mongoClient.DBNews
collection = db.News

nlp=spacy.load('es_core_news_sm')

d=defaultdict(list)
cursor=collection.find({"$or":[{"content" : {"$regex":"/.*corrup.*","$options":"si"}}]},{"_id":"1", "source":"1", "title":"1", "content":"1"}, no_cursor_timeout=True)
for document in cursor:
	source=document['source']
	if ("galego" not in source) and ("naciodigital" not in source) and ("brasil" not in source):
		text=re.sub(' +', ' ',document['content'].replace('\n',' '))
		doc=nlp(text)
		
		for i in range(len(doc.ents)):
			ent1=doc.ents[i]
			if ent1.label_=='PER' or ent1.label_=='ORG':
				for ent2 in doc.ents[i+1:]:
					if ent2.label_=='PER' or ent2.label_=='ORG':
						if ent1.end!=ent2.start:
							if ent2.text<ent1.text:
								d[(ent2.text, ent2.label_, ent2.text, ent2.label_)].append(1/(ent2.start-ent1.end))
							else:
								d[(ent1.text, ent1.label_, ent2.text, ent2.label_)].append(1/(ent2.start-ent1.end))
						else:
							d[(ent1.text, ent1.label_, ent2.text, ent2.label_)].append(1)
						
		for k in d.keys():
			d[k]=[sum(d[k])] 
		
cursor.close()
for k in d.keys():
	d[k]=sum(d[k])
with open('relaciones.pkl','wb') as f:
    pickle.dump(d, f, pickle.HIGHEST_PROTOCOL)