#!/usr/bin/python

'''
Para cualquier problema, contactar 
vicente.lahoz@s2grupo.es
erik.martinez@s2grupo.es
'''

import sys
import requests
import xmltodict
import datetime
import time
from bs4 import BeautifulSoup
#import bluecoat
import threatcrowd

ua= 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'
head = {'User-agent': ua}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def urlvoid(domain):
	UV_APIKEY="26a2fdb7339a463f94b00e6bb04482b6961fedd3"
	url="http://api.urlvoid.com/api1000/"+UV_APIKEY+"/host/"+domain+'/'	
	d = xmltodict.parse(str(requests.get(url, headers = head).text))
	d = d['response']

	if 'details' not in d: 
		# No hay registro previo del dominio
		url_scan = url + 'scan/'
		d = xmltodict.parse(str(requests.get(url_scan, headers = head).text))
		d = d['response']
	else: # El registro se encuentra registrado
		details = d['details']

		# Comprobamos ultima fecha de actualizacion
		updated = float(details['updated'])
		current = time.time()

		actual = current - updated
        # 14*24*3600 = 1209600 Segundos correspondientes a 2 semanas
	
		if actual > 1209600: # Reescaneamos el dominio
			url_rescan = url + 'rescan/'
			d = xmltodict.parse(str(requests.get(url_rescan, headers = head).text))
			d = d['response']
			
	details = d['details']
	ip = details['ip']
	print("---------------URLVOID----------------\n")
	if 'addr' in ip:
		print('IP: ' + str(ip['addr']))
	if 'hostname' in ip:
		print('Hostname: ' + str(ip['hostname']))
	if 'asname' in ip:
		print('As Name: ' + str(ip['asname']))
	if 'country_name' in ip:
		print('Country: ' + str(ip['country_name']))
	if 'region_name' in ip:
		print('Region: ' + str(ip['region_name']))
	if 'city_name' in ip:
		print('City name: ' + str(ip['city_name']))
	if 'country_name' in ip:
		print('Country: ' + str(ip['country_name']))
	print('First Registered: ' + datetime.datetime.fromtimestamp(int(details['domain_age'])).strftime('%Y-%m-%d %H:%M:%S'))
	print("\n--------------------------------------\n")
    #print('Last Checked: ' + datetime.datetime.fromtimestamp(int(details['updated'])).strftime('%Y-%m-%d %H:%M:%S'))
    #detected = int(detections['count'])
	if 'detections' not in d.keys():
		print(bcolors.OKGREEN + ' Not blacklisted \n')
	else:
		detections = d['detections']
		detected = int(detections['count'])
		print(bcolors.FAIL + 'Detections: ' + str(detected)+'\n')



def fortiguard(domain):
    url = 'https://fortiguard.com/webfilter?q='+domain
    soup = BeautifulSoup(requests.get(url, headers = head).content, 'html.parser')
    #html = list(soup.children)[2]
    #body = list(html.children)[3]
    category =soup.find_all('h4')[1]
    print(bcolors.ENDC +"---------------FORTIGUARD----------------\n")
	
    print(category.get_text())

    print("\n-----------------------------------------")

def bluecoatf(domain):

    bluecoat.main(domain)
    #head = {'User-agent': ua, 'Content-Type':'application/json'}
    #r = requests.post("https://sitereview.bluecoat.com/lookup", headers = head,data={'captcha': '', 'url': domain})
    #print(r.content)

def virustotal(domain): 
	VT_APIKEY = 'a89c4170c2f76d776e7111ec02a6a3caa20dff1526e8955713f9b5fa30f2cbf7'
	
	params = {'apikey': VT_APIKEY, 'url':domain}
	response = requests.post('https://www.virustotal.com/vtapi/v2/url/scan', data=params)
	json_response = response.json()
	headers = {
	"Accept-Encoding": "gzip, deflate",
	"User-Agent" : ua
	}
	params = {'apikey': VT_APIKEY, 'resource':domain}
	response = requests.post('https://www.virustotal.com/vtapi/v2/url/report',
	params=params, headers=headers)
	json_response = response.json()
	print("---------------VIRUSTOTAL----------------\n")
	if 'positives' in json_response:
		if str(json_response['positives']) == '0':
			print(bcolors.OKGREEN +"Detections: "+str(json_response['positives'])+'/'+str(json_response['total']))
		else:
			print(bcolors.FAIL+"Detections: "+str(json_response['positives'])+'/'+str(json_response['total']))
		print(bcolors.ENDC+"\n-----------------------------------------")

def threatcrowd_check(domain):
	print('---------------THREATCROWD----------------\n')
	result = threatcrowd.domain_report(domain)
	votes = 100
	if result['response_code'] == '1':
		votes = result['votes']
	if votes == -1:
		print('Dominio calificado potencialmente como malicioso')
	elif votes == 0:
		print('Dominio con similitud de votos negativos y positivos')
	elif votes == 1:
		print("Dominio no calificado como malicioso")
	elif votes == 100:
		print('Dominio no indexado')
	print()

def main(domain):

	threatcrowd_check(domain)
	urlvoid(domain)	
	fortiguard(domain) 
	bluecoatf(domain)
	virustotal(domain)
	


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("Solo puede haber un argumento")
		sys.exit(1)

	domain=sys.argv[1]
	
	print('Checking ' + domain+'\n')

	threatcrowd_check(domain)
	urlvoid(domain)	
	fortiguard(domain) 
	#bluecoatf(domain)
	virustotal(domain)
	
	

	

