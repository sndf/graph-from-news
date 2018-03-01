"""
Trabajo de fin de master - Universidad Internacional de La Rioja

Clase para el tratamiento de noticias

@author: Sandra Fresnillo Velasco
@license: MIT
"""

from pymongo import MongoClient

class Noticia:
	def __init__(self, source, id, title, tags, meta_keywords, summary, content, published):
		self.source = source
		self.id = id
		self.title = title
		self.tags = tags
		self.meta_keywords = meta_keywords
		self.summary = summary
		self.content = content
		self.published = published

	def toDBDocument(self):
		return {
			"source":self.source,
			"_id":self.id,
			"title":self.title,		
			"tags":self.tags,
			"meta_keywords":self.meta_keywords,
			"summary":self.summary,
			"published":self.published,
			"content":self.content
		}
		
	def insert(self, collection):
		try:
			if self.content != '':
				collection.insert_one(self.toDBDocument())
		except:
			print("Error al insertar la noticia "+self.id)
			