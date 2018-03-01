"""
Trabajo de fin de master - Universidad Internacional de La Rioja

Genera el grafo para analizar con networkX a partir de las 
relaciones obtenidas con NewsProcessing

@author: Sandra Fresnillo Velasco
@license: MIT
"""
import pickle
import networkx as nx
import re

def check_entity(entity):
	if re.match("[\W]+", entity) is None and \
        re.match("^[\d|Y |A ]",entity) is None and \
        "?" not in entity and "¿" not in entity and "¡" not in entity and "!" not in entity and \
        "@" not in entity and len(entity.split(" "))>1:
			return True
	return False	

with open('relaciones.pkl','rb') as f:
	d=pickle.load(f)
	
G=nx.Graph()	
		
f=open('pesos.txt','w')
i=0
for k in d.keys():
	ent1, ent1_type, ent2, ent2_type=k
    	
	if ent1_type=='PER' and ent2_type=='PER' and ent1!=ent2:	
		if check_entity(ent1)==True and check_entity(ent2)==True:
			G.add_edge(ent1, ent2, weight=d[k])
			f.write(str(d[k])+"\n")
	
nx.write_gpickle(G, 'GrafoRelaciones.pkl', pickle.HIGHEST_PROTOCOL)
f.close()	