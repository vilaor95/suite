#!/usr/bin/python

import json
import sqlite3
from sqlite3 import Error
import sys
import re

#def store(json_data):
#	global db
#	cursor = db.cursor()
#	table_name = json_data['artifact']  
#	str_columns = '('
#	str_values = '('
#	keys = list(json_data.keys())
#	for key in keys[:-1]:
#		if key == 'artifact':
#			continue
#		str_columns += str(key) + ','
#		str_values += "'" + str(json_data[key]) + "',"
#	if keys[-1] != 'artifact':
#		str_columns += str(keys[-1])
#		str_values += "'" + str(json_data[keys[-1]])
#	str_columns += ')'
#	str_values += "')"
#	str_query = 'INSERT INTO ' + table_name + str_columns + ' VALUES' + str_values
#	cursor.execute(str_query)
#	db.commit() 

def store(json_data):
	try:
		global db
		cursor = db.cursor()
		table_name = json_data['artifact'] 
		str_columns = "(json)"
		str_values = '("' + str(json_data) + '")'
		str_query = 'INSERT INTO ' + table_name + str_columns + ' VALUES' + str_values
		cursor.execute(str_query)
		db.commit()
	except Error as e:
		print(json_data)
		print(e)
	finally:
		cursor.close()


if __name__ == '__main__':

	json_file = sys.argv[1]
	database = sys.argv[2]

	try:
		db = sqlite3.connect(database) 
		cursor = db.cursor() 
		#cursor.execute('CREATE TABLE browser_activity(id INTEGER PRIMARY KEY, date TEXT, url TEXT, host TEXT, file TEXT, title TEXT)')
		cursor.execute('CREATE TABLE browser_activity(id INTEGER PRIMARY KEY, type TEXT, json TEXT)')
		db.commit()
		cursor.execute('CREATE TABLE registry(id INTEGER PRIMARY KEY, json TEXT)')
		db.commit()
		cursor.execute('CREATE TABLE alerts(id INTEGER PRIMARY KEY, criticality TEXT, command TEXT, argument1 TEXT, argument2 TEXT, argument3 TEXT, end TEXT, result TEXT, last_id TEXT, rule TEXT)')
		db.commit() 
		print('Tables created')

	except Error as e:
		print(e) 
	finally:
		db.close()

	# Movemos la informacion del JSON a la base de datos
	with open(json_file) as f:
		db = sqlite3.connect(database)
		cursor = db.cursor()
		for line in f:
			try:
				line = re.sub('"','',line)
				store(eval(line))
			except Error as e:
				print(e)
				continue
		db.close() 
		f.close()

