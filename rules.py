#!/usr/bin/python

import sys
import json
import sqlite3
from sqlite3 import Error
import re

commands = ['file_search','url_search','download_search','key_search','value_search','subkey_search']

def check_rules(rules):
	try:
		f = open(rules)
	except:
		print('Error opening the rule file')
		sys.exit(1)

	for line in f:
		matchObj = re.search('^(#|\n$)',line)
		if matchObj: # La linea es un comentario
			continue
		rule = line.split(',')
		try:
			# Comprobar que la regla termina con un entero
			end = int(rule[-1])
			if end != 0 and end != 1:
				print('Wrong rule -- > ' + line + '// last field must be integer with value 1 or 0')
				sys.exit(1)
		except:
			print('Wrong rule -- > ' + line + '// last field must be integer with value 1 or 0')
			sys.exit(1)

		if rule[0] not in commands:
			print('Wrong rule --> ' + line + '// Command not supported')
			sys.exit(1)

		command = rule[0]
		l = len(line.split(','))
		if command == 'file_search':
			if l != 4:
				print('Wrong rule --> ' + rule + '//Invalid number of arguments')
				sys.exit(1)
		elif command == 'url_search':
			if l != 4:
				print('Wrong rule --> ' + rule + '//Invalid number of arguments')
				sys.exit(1)
		elif command == 'download_search':
			if l != 4:
				print('Wrong rule --> ' + rule + '//Invalid number of arguments')
				sys.exit(1)
		elif command == 'key_search':
			if l != 4:
				print('Wrong rule --> ' + rule + '//Invalid number of arguments')
				sys.exit(1)
		elif command == 'url_search':
			if l != 6:
				print('Wrong rule --> ' + rule + '//Invalid number of arguments')
				sys.exit(1)

	# Comprobar que al menos el ultimo valor tiene un 1 como end
	if end != 1:
		print('Wrong rule //Last end field must be 1')
		sys.exit(1)

	print('Archivo de reglas correcto')
	f.close()
			

def parse_rules(rules):

	ruleset = list()

	with open(rules) as f:
		for line in f:
			matchObj = re.search('^(#|\n$)',line)
			if matchObj: # La linea es un comentario
				continue
			rule = line.split(',')
			try:
				end = int(rule[-1])
				if end != 0 and end != 1:
					print('Wrong rule --> ' + line + '//Invalid value as end')
					sys.exit(1)
			except:
				print('Wrong rule --> ' + str(rule) + ' // last field must be integer')
				sys.exit(1)
			if rule[0] not in commands:
				print('Wrong command --> ' + rule[0])
				sys.exit(1)

			# Comprobacion de los argumentos de cada funcion
			command = rule[0]
			l = len(rule)
			if command == 'file_search':
				if l != 4:
					print('Wrong rule --> ' + str(rule) + '//Invalid number of arguments')
					sys.exit(1)
			elif command == 'url_search':
				if l != 4:
					print('Wrong rule --> ' + str(rule) + '//Invalid number of arguments')
					sys.exit(1)
			elif command == 'download_search':
				if l != 4:
					print('Wrong rule --> ' + str(rule) + '//Invalid number of arguments')
					sys.exit(1)
			elif command == 'key_search':
				if l != 4:
					print('Wrong rule --> ' + str(rule) + '//Invalid number of arguments')
					sys.exit(1)
			elif command == 'value_search':
				if l != 6:
					print('Wrong rule --> ' + str(rule) + '//Invalid number of arguments')
					sys.exit(1)

			# Regla correcta	
			ruleset.append(rule)

			# Comprobar que al menos el ultimo valor tiene un 1 como end
		if end != 1:
			print('Wrong rule //Last end field must be 1')
			sys.exit(1)

	# Cerramos el archivo de reglas y trabajamos a partir de ahora con la lista en memoria
	f.close()
	return ruleset
			
def file_search(mft,rule):
	alert = {}
	with open(mft) as mft_file:
		for line in mft_file:
			filename = line.split(',')[0]
			pattern = rule[2] 
			matchObject = re.search( pattern, filename, re.I)
			if matchObject:
				alert['command'] = rule[0]
				alert['criticality'] = rule[1]
				alert['argument1'] = rule[2]
				alert['end'] = int(rule[3])
				if 'result' not in alert:
					alert['result'] = list()
				alert['result'].append(filename)
		mft_file.close()
		if bool(alert):
			results = ''
			for result in alert['result']:
				results += result + ','
			results = results[:-1]
			alert['result'] = results
			return alert
		return -1

def url_search(database_name,rule):
	try:
		alert = {}
		db = sqlite3.connect(database_name)
		cursor = db.cursor()

		str_query = "SELECT json FROM browser_activity" 

		cursor.execute(str_query)
		all_jsons = cursor.fetchall()

		for json_object in all_jsons:
			json_object = eval(json_object[0])
			if json_object['type'] != 'visit':
				continue
			pattern = rule[2]
			url = json_object['url']
			matchObject = re.search(pattern,url,re.I)
			if matchObject:
				alert['command'] = rule[0]
				alert['criticality'] = rule[1]
				alert['argument1'] = rule[2]
				alert['end'] = int(rule[3])
				if 'result' not in alert:
					alert['result'] = list()
				alert['result'].append(url)

		if bool(alert):
			results = ''
			for result in alert['result']:
				results += result + ','
			results = results[:-1]
			alert['result'] = results
			return alert
		return -1
	except:
		print(e)
	finally:
		db.close()

def download_search(database_name,rule):
	try:
		alert = {}
		db = sqlite3.connect(database_name)
		cursor = db.cursor()

		str_query = "SELECT json FROM browser_activity" 

		# Extraemos el campo de interes de la regla
		pattern = rule[2]

		cursor.execute(str_query)
		all_jsons = cursor.fetchall()

		for json_object in all_jsons:
			json_object = eval(json_object[0])
			if json_object['type'] != 'download':
				continue
			filename = json_object['url']
			matchObject = re.search(pattern,filename,re.I)
			if matchObject:
				alert['command'] = rule[0]
				alert['criticality'] = rule[1]
				alert['argument1'] = rule[2]
				alert['end'] = int(rule[3])
				if 'result' not in alert:
					alert['result'] = list()
				alert['result'].append(filename)

		if bool(alert):
			results = ''
			for result in alert['result']:
				results += result + ','
			results = results[:-1]
			alert['result'] = results
			return alert
		return -1
	except:
		print(e)
	finally:
		db.close()

def key_search(database_name,rule):
	try:
		alert = {}
		db = sqlite3.connect(database_name)
		cursor = db.cursor()

		# Extraemos el campo de interes de la regla
		key = rule[2]

		str_query = "SELECT json FROM registry"

		cursor.execute(str_query)
		all_jsons = cursor.fetchall()

		for json_object in all_jsons:
			json_object = eval(json_object[0])


			if json_object['key'] == key:
				alert['command'] = rule[0]
				alert['criticality'] = rule[1]
				alert['argument1'] = rule[2]
				alert['end'] = int(rule[3])
				if 'result' not in alert:
					alert['result'] = list()
				alert['result'].append(key)
		
		if bool(alert):
			results = ''
			for result in alert['result']:
				results += result + ','

			# Linea para eliminar la ultima coma
			results = results[:-1]
			alert['result'] = results
			return alert
		return -1

	except Error as e:
		print(e)
	finally:
		db.close()

def subkey_search(databse_name,rule):
	try:
		alert = {}
		db = sqlite3.connect(database_name)
		cursor = db.cursor()

		key = rule[2]
		value_name = rule[3]
		value = rule[4]

		str_query = 'SELECT json FROM registry GROUP BY json'

		cursor.execute(str_query)
		all_jsons = cursor.fetchall()

		for json_object in all_jsons:
			json_object = json_object[0]
			json_object = eval(json_object)
			if key in json_object['key']:
				if value_name == '':
					for v in json_object['values'].values():
						matchObj = re.search(value,v,re.I)
						if matchObj:
							alert['command'] = rule[0]
							alert['criticality'] = rule[1]
							alert['argument1'] = rule[2]
							alert['argument2'] = rule[3]
							alert['argument3'] = rule[4]
							alert['end'] = int(rule[5])
							if 'result' not in alert:
								alert['result'] = list()
							alert['result'].append(v)
				elif value == '':
					for k in json_object['values'].keys():
						matchObj = re.search(value_name,k,re.I)
						if matchObj:
							alert['command'] = rule[0]
							alert['criticality'] = rule[1]
							alert['argument1'] = rule[2]
							alert['argument2'] = rule[3]
							alert['argument3'] = rule[4]
							alert['end'] = int(rule[5])
							if 'result' not in alert:
								alert['result'] = list()
							alert['result'].append(k)
				else:
					for k in json_object['values'].keys():
						matchObj1 = re.search(value_name,k,re.I)
						matchObj2 = re.search(value,json_object['values'][k],re.I)
						if matchObj1 and matchObj2:
							alert['command'] = rule[0]
							alert['criticality'] = rule[1]
							alert['argument1'] = rule[2]
							alert['argument2'] = rule[3]
							alert['argument3'] = rule[4]
							alert['end'] = int(rule[5])
							if 'result' not in alert:
								alert['result'] = list()
							#alert['result'].append(k)	
							#alert['result'].append(json_object['values'][k])	
							alert['result'].append(str(k) + ': ' + str(json_object['values'][k]))

		if bool(alert):
			results = ''
			for result in alert['result']:
				results += result + ','
			results = results[:-1] # Linea para eliminar la ultima coma
			alert['result'] = results
			return alert
		return -1		

	except Error as e:
		print(e)
	finally:
		db.close()

def value_search(database_name,rule):
	try:
		alert = {}
		db = sqlite3.connect(database_name)
		cursor = db.cursor()

		value_name = rule[3]
		value = rule[4]

		str_query = 'SELECT json FROM registry GROUP BY json'	

		cursor.execute(str_query)
		all_jsons = cursor.fetchall()

		for json_object in all_jsons:
			json_object = eval(json_object[0])
			
			if rule[2] == json_object['key']:
				if value_name == '':
					for v in json_object['values'].values():
						matchObj = re.search(value,v,re.I)
						if matchObj:
							alert['command'] = rule[0]
							alert['criticality'] = rule[1]
							alert['argument1'] = rule[2]
							alert['argument2'] = rule[3]
							alert['argument3'] = rule[4]
							alert['end'] = int(rule[5])
							if 'result' not in alert:
								alert['result'] = list()
							alert['result'].append(v)
				elif value == '':
					for k in json_object['values'].keys():
						matchObj = re.search(value_name,k,re.I)
						if matchObj:
							alert['command'] = rule[0]
							alert['criticality'] = rule[1]
							alert['argument1'] = rule[2]
							alert['argument2'] = rule[3]
							alert['argument3'] = rule[4]
							alert['end'] = int(rule[5])
							if 'result' not in alert:
								alert['result'] = list()
							alert['result'].append(k)
				else:
					for k in json_object['values'].keys():
						matchObj1 = re.search(value_name,k,re.I)
						matchObj2 = re.search(value,json_object['values'][k],re.I)
						if matchObj1 and matchObj2:
							alert['command'] = rule[0]
							alert['criticality'] = rule[1]
							alert['argument1'] = rule[2]
							alert['argument2'] = rule[3]
							alert['argument3'] = rule[4]
							alert['end'] = int(rule[5])
							if 'result' not in alert:
								alert['result'] = list()
							#alert['result'].append(k)	
							#alert['result'].append(json_object['values'][k])	
							alert['result'].append(str(k) + ': ' + str(json_object['values'][k]))

		if bool(alert):
			results = ''
			for result in alert['result']:
				results += result + ','
			results = results[:-1] # Linea para eliminar la ultima coma
			alert['result'] = results
			return alert
		return -1		

	except Error as e:
		print(e)
	finally:
		db.close()


def generate_alert(correlation,rules):
	global database_name
	try:
		# Codigo para generar la alerta
		d = {}
		last_id = -1

		r = ''
		for rule in rules:
			rule = re.sub("'",'"',rule)
			r = r + str(rule) + '-' 
		r = r[:-1]

		for alert in correlation: # correlation = lista de diccionarios
			str_columns = "(rule,"
			str_values = "('" + r +"',"
			#str_columns = "(rules,"
			#str_values = "('" + str(r) + "',"
			keys = list(alert.keys())
			for key in keys[:-1]:
				str_columns += str(key) + ','
				str_values += "'" + str(alert[key]) + "',"
			if last_id != -1:
				str_columns += 'last_id,'
				str_values += "'" + str(last_id) + "',"
			str_columns += str(keys[-1]) + ')'
			str_values += "'" + str(alert[keys[-1]]) + "')"

			str_query = 'INSERT INTO alerts ' + str_columns + ' VALUES' + str_values
			#print(str_query)

			# Almacenar la alerta en la BD
			db = sqlite3.connect(database_name)
			cursor = db.cursor()
			cursor.execute(str_query)
			db.commit()
			last_id = cursor.lastrowid

	except Error as e:
		print(e)
	finally:
		db.close()

if __name__ == '__main__':

	# Chequear si el archivo de reglas tiene una sintaxis correcta
	if len(sys.argv) == 3 and sys.argv[1] == '--check':
		check_rules(sys.argv[2])
		sys.exit(0)

	# Argumentos de entrada
	rules = sys.argv[1]
	database_name = sys.argv[2]
	mft = ''
	if len(sys.argv) == 4:
		mft = sys.argv[3]

	# Parseamos el archivo de reglas y lo pasamos a una lista en memoria
	ruleset = parse_rules(rules)
	#print('Ruleset ' + str(ruleset))

	n = 0 # llevar cuenta de que se cumple la correlacion(0 Correcta/ 1 Incorrecta)
	correlation = list() # variable de lista para almacenar las reglas que saltan
	rules = list()

	for rule in ruleset:
		#print('n --> ' + str(n))
		#print('Rule' + str(rule))
		# Extraemos la informacion de la regla
		command = rule[0]
		arguments = rule[1:-1]
		end = int(rule[-1])

		alert = {} # diccionario para almacenar las alertas
		rules.append(str(rule))	

		if n == 1: # No se cumple la correlacion
			if end == 1: # Final de reglas de correlacion
				n = 0 # Empezamos otro conjunto de reglas
				correlation = list()
				rules = list()
			continue
		
		# Funciones de la herramienta / Devuelven un diccionario con la regla y el resultado obtenido o -1 en caso erroneo
		if command == 'file_search' and mft != '':
			alert = file_search(mft,rule)
			if alert == -1:
				n = 1 
			else:
				correlation.append(alert)
				if end == 1:
					# Generar alerta en la base de datos
					generate_alert(correlation,rules)
		elif command == 'url_search':
			alert = url_search(database_name,rule)
			if alert == -1:
				n = 1
			else:
				correlation.append(alert)
				if end == 1:
					generate_alert(correlation,rules)
		elif command == 'download_search':
			alert = download_search(database_name,rule)
			if alert == -1:
				n = 1
			else:
				correlation.append(alert)
				if end == 1:
					generate_alert(correlation,rules)
		elif command == 'key_search':
			alert = key_search(database_name,rule)		
			if alert == -1:
				n=1
			else:
				correlation.append(alert)
				if end == 1:
					generate_alert(correlation,rules)
		elif command == 'value_search':
			alert = value_search(database_name,rule)		
			if alert == -1:
				n=1
			else:
				correlation.append(alert)
				if end == 1:
					#print('Rule --> ' + str(rule))
					generate_alert(correlation,rules)
		elif command == 'subkey_search':
			alert = subkey_search(database_name,rule)
			if alert == -1:
				n=1
			else:
				correlation.append(alert)
				if end == 1:
					generate_alert(correlation,rules)

		# Comprobamos si se trata de una regla simple o del final de un conjunto de estas
		if n ==1 and end == 1:
			n = 0 # Empezamos otro conjunto de reglas
			correlation = list()
			rules = list()
		elif end == 1:
			correlation = list()
			rules = list()
			



