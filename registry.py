#!/usr/bin/python

import sys
from os import listdir
from os.path import isfile, join
from Registry import *
import json
import re

#TODO 
# Implementar metodo para recuperar subclaves de una clave
# Renombrar las funciones y el main acorde
commands = ['key_search','subkey_search','value_search']

def check_key(registry_file,key):
	# Abrimos el archivo del registro
	reg = Registry.Registry(registry_file)

	try:
		reg_key = reg.open(key)
	except Registry.RegistryKeyNotFoundException:
		# No se ha encontrado la clave
		#print("Key not found")
		return -1 
	
	d = {} # Diccionario con claves artifact, key y values
	d['artifact'] = 'registry'
	d['key'] = key
	d['values'] = ''

	values = {}
	for value in [v for v in reg_key.values() \
				if v.value_type() == Registry.RegSZ or \
				v.value_type() == Registry.RegExpandSZ]:
		values[value.name()] = value.value()
	d['values'] = values	
	return d

def check_subkeys(registry_file,key):
	# Abrimos el archivo del registro
	reg = Registry.Registry(registry_file)

	try:
		reg_key = reg.open(key)
	except:
		return -1
	
	l = list()

	for subkey in reg_key.subkeys():
		d = {}

		d['artifact'] = 'registry'
		d['key'] = subkey.path()
		d['values'] = ''

		values = {}
		for value in [v for v in subkey.values() \
					if v.value_type() == Registry.RegSZ or \
					v.value_type() == Registry.RegExpandSZ]:
			values[value.name()] = value.value()
		d['values'] = values

		l.append(d)
	
	return l

def check_name_value(d,value):
	for k in d['values'].keys():
		matchObj = re.search(value,k,re.I)
		if matchObj:
			return d
		return -1
	

def check_value_value(d,value):
	for v in d['values'].values():
		matchObj = re.search(value,v,re.I)
		if matchObj:
			return d
		return -1

def to_json(json_file,d):
	f = open(json_file,'a')
	f.write(str(d) + '\n')
	f.close()
		

if __name__ == '__main__':
	#Directorio con los archivos del registro
	registry_dir = sys.argv[1]
	registry_files = [registry_dir + f for f in listdir(registry_dir) if isfile(join(registry_dir, f))]
	# Archivo de reglas
	rule_file = sys.argv[2]
	# Archivo con los jsons
	json_file = sys.argv[3]

	rules = open(rule_file)
	#print('Rules opened')

	for rule in rules:
		matchObj = re.match('^(#|\n$)',rule)
		if matchObj: # La linea es un comentario
			continue
		rule = rule.split(',')
		command = rule[0]
		key = rule[2]
		if command in commands :
			if command == 'subkey_search':
				for f in registry_files:
					#print(f)
					d = check_subkeys(f,key)
					if d != -1:
						for subkey in d:
							to_json(json_file,subkey)
			else:
				for f in registry_files:
					#print(f)
					d = check_key(f,key)
					if d != -1:
						to_json(json_file,d)					
						to_json(json_file,d)
	
	rules.close()
