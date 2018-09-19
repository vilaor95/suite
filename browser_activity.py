#!/usr/bin/python

import sys
import json
import sqlite3
from sqlite3 import Error
import re

def browser_activity(browser_file,output_json):
    try:

        if 'places.sqlite' in browser_file or 'History' in browser_file:
            conn = sqlite3.connect(browser_file)
            cursor = conn.cursor()
    except:
        print('Error abriendo archivo sqlite')

    try:
        json_file = open(output_json,'a')

        if 'places.sqlite' in browser_file:
            # Registramos las visitas a diferentes sitios
            str_query = "SELECT datetime(moz_historyvisits.visit_date/1000000, 'unixepoch', 'localtime'), moz_places.url, moz_places.rev_host, moz_places.title FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id;"
            cursor.execute(str_query)
            all_rows = cursor.fetchall()
            for row in all_rows:
                parse_firefox_visits(row,json_file)
        
            # Registramos las descargas
            str_query = "SELECT datetime(moz_historyvisits.visit_date/1000000, 'unixepoch', 'localtime'), moz_annos.content, moz_places.url FROM moz_historyvisits, moz_annos INNER JOIN moz_places ON moz_places.id = moz_annos.place_id WHERE moz_annos.place_id = moz_historyvisits.place_id AND moz_annos.anno_attribute_id = 3;"
            cursor.execute(str_query)
            all_rows = cursor.fetchall()
            for row in all_rows:
                parse_firefox_downloads(row,json_file)

        elif 'History' in browser_file:
            # Registramos las visitas a diferentes sitios
            str_query = 'SELECT datetime(((visits.visit_time/1000000)-11644473600), "unixepoch"), urls.url, urls.title FROM urls, visits WHERE urls.id = visits.url;'
            cursor.execute(str_query)
            all_rows = cursor.fetchall()
            for row in all_rows:
                parse_chrome_visits(row,json_file)
                
            str_query = 'SELECT datetime((downloads.start_time/1000000)-11644473600, "unixepoch"), downloads.site_url, downloads.current_path FROM downloads;' 
            cursor.execute(str_query)
            all_rows = cursor.fetchall()
            for row in all_rows:
                parse_chrome_downloads(row,json_file)

        elif 'ie' in browser_file:
            pass

    except Error as e:
        print(e)

    finally:
        conn.close()
        json_file.close()

        
def parse_firefox_visits(row,json_file):
	d={}
	d['artifact'] = 'browser_activity'
	d['type'] = 'visit'
	d['date'] = row[0]
	d['url'] = row[1]
	d['host'] = row[2]
	json_data = json.dumps(d)
	json_data = re.sub('"',"'",json_data)
	json_file.write(json_data + '\n')

def parse_chrome_visits(row,json_file):
	d={}
	d['artifact'] = 'browser_activity'
	d['type'] = 'visit'
	d['date'] = row[0]
	d['url'] = row[1]
	json_data = json.dumps(d)
	json_data = re.sub('"',"'",json_data)
	json_file.write(json_data + '\n')

def parse_firefox_downloads(row,json_file):
	d={}
	d['artifact'] = 'browser_activity'
	d['type'] = 'download'
	d['date'] = row[0]
	d['file'] = row[1]
	d['url'] = row[2]
	json_data = json.dumps(d)
	json_data = re.sub('"',"'",json_data)
	json_file.write(json_data + '\n')

def parse_chrome_downloads(row,json_file):
	d={}
	d['artifact'] = 'browser_activity'
	d['type'] = 'download'
	d['date'] = row[0]
	d['file'] = row[1]
	d['url'] = row[2]
	json_data = json.dumps(d)
	json_data = re.sub('"',"'",json_data)
	json_file.write(json_data + '\n')


if __name__ == '__main__':

    f = sys.argv[1]
    o = sys.argv[2]

    browser_activity(f,o)
