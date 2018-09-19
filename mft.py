#!/usr/bin/python

import sys
import re

def ads_detect(m):
	with open(m) as mft:
		for line in mft:
			matchObj = re.match('Y$',line)
			if matchObj:
				line = line.split(',')
				print(line[0])
	mft.close()

#def timestomping_detect(m):
#	with open(m) as mft:
		
