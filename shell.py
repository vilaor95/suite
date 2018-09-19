#!/usr/bin/python

import sys
import sqlite3
from sqlite3 import Error
import re
from show_alerts import *
import domains_check

def alerts(database):
	PS = 'alerts--> '
	while True:
		try:
			line = input(PS)			
		except EOFError:
			break
		if not line:
			continue
			
		#try:
		line = line.split()	
		command = line[0]


		if command == 'quit' or command =='q':
			break
		elif command == 'h' or command == 'help':
			help_alerts()
		elif command == 'show' and line[1] == 'all':
			show_alarms(database)
		elif command == 'show' and len(line) == 2 and type(int(line[1])) == int:
			show_alarms(database,int(line[1]))
		else:
			print('Wrong command. Type h or help')

		#except:
			#continue


def browser(database):
	PS='browser--> '	
	try:
		db = sqlite3.connect(database)
		cursor =  db.cursor()

		str_query = "SELECT json FROM browser_activity"
		cursor.execute(str_query)
		all_jsons = cursor.fetchall()

		urls = list()
		domains = list()
		downloads = list()
		set_domains = list()
		set_downloads = list()

		for json_object in all_jsons:
			json_object = eval(json_object[0])
			if json_object['type'] == 'visit':
				domain = re.sub('http[s]*://(www\.|)','',json_object['url'])
				domain = re.sub('/.*$','',domain)
				if domain not in domains:
					domains.append(domain)
			else:
				download = re.sub('file:/','',json_object['file'])
				if download not in downloads:
					downloads.append(download)
			
			if json_object['url'] not in urls:
				urls.append(json_object['url'])

		while True:
			try:
				line = input(PS)			
			except EOFError:
				break
			if not line:
				continue

			line = line.split()
			command = line[0]

			#try:
			if command == 'quit' or command =='q':
				break
			elif command == 'h' or command =='help':
				help_browser()
			elif command == 'urls':
				for i in range(1,len(urls)+1):
					print(str(i) + ': ' + urls[i-1])
			elif command == 'domains':
				for i in range(1,len(domains)+1):
					print(str(i) + ': ' + domains[i-1])
			elif command == 'downloads':
				for i in range(1,len(downloads)+1):
					print(str(i) + ': ' + downloads[i-1])
			elif command == 'set':
				l = len(line)
				if l >= 3:
					if line[1] == 'domains':
						set_domains = line[2:]	
						print(set_domains)
					elif line[1] == 'downloads':
						set_downloads = line[2:]	
						print(set_downloads)
					else: 
						print('Wrong command. Type h or help')
				else:
					print('Not enough arguments. Type h or help')
			elif command == 'check':
				if line[1] == 'domains':
					for i in set_domains:
						print('Checking ' + domains[int(i)-1] + '\n')
						domains_check.main(domains[int(i)-1])	

				elif type(int(line[1])) == int:
					print('Checking ' + domains[int(i)-1] + '\n')
					domains_check.main(domains[int(line[1])-1])
				else:
					print('Wrong command. Type h or help')

			#except:
				#continue

	except Error as e:
		print(e)

	finally:
		db.close()

def help_shell():
	print('Commands:')
	print('%s --> for %s mode' % ('alerts','alerts'))
	print('%s --> for %s mode' % ('browser','browser'))
	print('%s --> for %s mode' % ('mft','mft'))
	print('%s --> for %s mode' % ('email','email'))

def help_browser():
	print('Commands:')
	print('%s --> for list %s visited' % ('urls','urls'))
	print('%s --> for list %s visited' % ('domains','domains'))
	print('%s --> for list %s visited' % ('downloads','downloads'))
	print()
	print('%s %s [1 2 .. N] --> select [1 2 .. N] domains' % ('set','domains'))
	print('%s %s --> check selected domains' % ('check','domains'))
	print('%s %s --> check third domain' % ('check','3'))

def help_alerts():
	print('Commands:')
	print('%s %s --> show all alerts' % ('show','all'))
	print('%s %s --> show alerts with criticality 5' % ('show','5'))

if __name__ == '__main__':

	# Args
	database = sys.argv[1]

	# Start shell
	while True:
		PS = '--> '
		try:
			line = input(PS)
		except EOFError:
			break
		if not line:
			continue

		line = line.split()
		command = line[0]

		if command == 'quit' or command == 'q':
			break
		elif command == 'h' or command == 'help':
			help_shell()
		elif command == 'alerts':
			alerts(database)
		elif command == 'browser':
			browser(database)	
		else:
			print('Command error. Type h or help')
