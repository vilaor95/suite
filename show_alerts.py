#!/usr/bin/python

import sys
import sqlite3
from sqlite3 import Error

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def show_alarms(database_name,c=0):
	try:
		db = sqlite3.connect(database_name)
		cursor = db.cursor()

		cursor.execute('SELECT * FROM alerts WHERE criticality >= ' + str(c) +' ORDER BY criticality DESC;')
		all_rows = cursor.fetchall()

		criticality = 0 # Variable para llevar la cuenta de la criticidad de la alerta
		count = 0 # Variable para llevar la cuenta de las alertas generadas
		# Variable diccionario para almacenar informacion del set de reglas
		alert = {'commands':list(), 'results':list()}
		for row in all_rows:
		# Actualizamos la criticidad de la alerta
			if row[1] != None:
				if int(row[1]) > criticality:
					criticality = int(row[1])

			# Extraemos informacion de la alerta
			alert['commands'].append(row[2])
			alert['results'].append(row[7])
			alert['rule'] = row[9]

            # Chequeamos si se trata de la ultima regla en el set
			if row[6] == '1': # row[6] = end
				count += 1 # Actualizamos el numero de alertas generadas
				print_alert(alert,criticality,count,c)

				# Reseteamos valores para la siguiente alerta
				criticality = 0
				alert = {'commands':list(), 'results':list()}

	except Error as e:
		print('Error')
		print(e)

	finally:
		db.close()

def print_alert(alert,criticality,count,c):
	rules = ''
	r = alert['rule'].split('-')
	for rule in r:
		rules += rule + '\n'

	print(bcolors.BOLD + bcolors.UNDERLINE + 'Rule ' + str(count) +':' + '\n' + bcolors.ENDC + bcolors.BOLD + str(rules) + bcolors.ENDC)
	commands = alert['commands']
	results = alert['results']

	if criticality >= c and criticality == 1: # Criticidad baja
		str_alert = alert_info(commands,results) 
		print( bcolors.WARNING + str_alert + bcolors.ENDC)
	elif criticality >= c and criticality == 2: # Criticidad media
		str_alert = alert_info(commands,results) 
		print( bcolors.WARNING + str_alert + bcolors.ENDC)
	elif criticality >= c and criticality == 3: # Criticidad alta
		str_alert = alert_info(commands,results) 
		print( bcolors.FAIL + str_alert + bcolors.ENDC)
	elif criticality >= c and criticality >= 4: # Criticidad critica
		str_alert = alert_info(commands,results) 
		print( bcolors.FAIL + str_alert + bcolors.ENDC)

def alert_info(commands,results):
	str_alert = ''

	r = list()
	for result in results:
		temp = ''
		result = result.split(',')
		for res in result:
			temp += res + '\n'	
		r.append(temp)

	for i in range(0,len(commands)):
		str_alert +=  commands[i] + '--> ' + r[i] + '\n'
	return str_alert

if __name__ == '__main__':
    
	print('In show alerts')

	database_name = sys.argv[1]
	if len(sys.argv) == 3:
		c = sys.argv[2]
		show_alarms(database_name,c)		
	else:	
		show_alarms(database_name)
