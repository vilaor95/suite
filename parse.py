#!/usr/bin/python

import sys
import json
import re

def parsefiles(t):
    try:
        for line in t:
            d={}
            l=line.split(',')
            d['artifact'] = 'systemfile'
            d['file'] = l[0]
            d['md5'] = l[1]
            d['sha1'] = l[2]
            d['path'] = l[3]
            json_data = json.dumps(d)
            print(json_data)
            # guardar datos para posterior utilizacion
    except:
        pass

def parseusers(t):
    try:    
        for line in t:
            l=line.split(':')
            if l[0].strip() == 'Username':
                d={}
                d['artifact'] = 'user'
                d['username'] = l[1].strip()
            elif l[0].strip() == 'Account Type':
                d['account'] = l[1].strip()
            elif l[0].strip() == 'Account Created':
                d['created'] = l[1].strip()
            elif l[0].strip() == 'Last Login Date':
                d['last'] = l[1].strip()
            elif l[0].strip() == 'Login Count':
                d['count'] = l[1].strip()
                json_data = json.dumps(d)
                print(json_data)
    except:
        print('Error parseusers')
        pass

def parseprogramexecution(t):
    try:
        for line in t:
            d={}
            l=line.split('|')
            d['artifact'] = 'program_execution'
            d['timestamp'] = l[0]
            d['execution'] = l[4]
            json_data = json.dumps(d)
            print(json_data)
    except:
        pass

def parseatjobs(t):
    try:
        for line in t:
            d={}
            l=line.split('|')
            d['artifact'] = 'at_job'
            d['timestamp'] = l[0]
            d['job'] = l[4]
            json_data = json.dumps(d)
            print(json_data)
    except:
        pass

def parsedirectaccesses(t):
    try:
        for line in t:
            d={}
            d['artifact'] = 'direct_access'
            d['timestamp'] = l[0]
            d['shortcut'] = l[4]
            json_data = json.dumps(d)
            print(json_data)
    except:
        pass

def parseautorun(t):
    try:
        d={}
        for line in t:
            if 'soft_run' in line or '[Autostart]' in line or '.........' in line or 'has no values' in line or 'has no subkeys' in line:
                continue
            elif line == '\n':
                if len(d) > 0:
                    json_data = json.dumps(d)
                    print(json_data)
                d={}
                d['artifact'] = 'run_key'
            elif len(d) == 1:
                d['key'] = line
            elif len(d) == 2:
                d['lastwrite'] = line
            elif len(d) == 3:
                d['subkey_value'] = {}
                d['subkey/value'][len(d) - 3] = line
            elif len(d) > 3:
                d['subkey/value'][len(d) -3] = line
    except:
        print('Error in autorun')
        pass
            
def parseuserrunkey(t):
    try:
        d={}
        for line in t:
            if 'user_run' in line or '[Autostart]' in line:
                continue
            elif 'User:' in line:
                user = line.split(':')[1].strip()
            elif line == '\n':
                if len(d) > 0:
                    json_data = json.dumps(d)
                    print(json_data)
                d={}
                d['artifact'] = 'auto_run'
            elif len(d) == 1:
                d['key'] = line
            elif len(d) == 2:
                d['lastwrite'] = line
            elif len(d) == 3:
                d['subkey/value'] = {}
                d['subkey/value'][len(d) - 3] = line
            elif len(d) > 3:
                d['subkey/value'][len(d) -3] = line
    except:
        pass

def parseservices(t):
    for line in t:
        d={}
        if 'svc' in line or '(System)' in line or 'DisplayName' in line or line == '\n':
            continue
        else:
            l=line.split(',')
            if l[0] != '':
                d['artifact'] = 'services'
                d['timestamp'] = l[0]
            if l[1] != '':
                d['name'] = l[1]
            if l[2] != '':
                d['displayname'] = l[2]
            if l[3] != '':
                d['imagepath'] = l[3]
            if l[4] != '':
                d['type'] = l[4]
            if l[5] != '':
                d['start'] = l[5]
            if l[6] != '':
                d['object_name'] = l[6]
            json_data = json.dumps(d)
            print(json_data)

def parseappinitdlls(t):
    d={}
    for line in t:
        if 'appinitdlls' in line or '(Software)' in line or line == '\n' or 'disabled' in line or '....' in line:
            continue
        elif 'CurrentVersion\Windows' in line:
            d={}
            d['artifact'] = 'appinitdlls'
            d['key'] = line
        elif 'LastWrite' in line:
            d['lastwrite'] = line
        elif 'LoadAppInit_DLLs :' in line:
            d['enabled'] = line.split(':')[1].strip()
            json_data = json.dumps(d)
            print(json_data)
        elif 'AppInit_DLLs :' in line:
            d['AppInit_DLLs'] = line.split(':')[1].strip()

def parsestartupfolders(t):
    for line in t:
        if 'startup' in line or 'Startup Folder' in line or line == '\n':
            continue
        elif 'User:' in line:
            user=line.split(':')[1].strip()
        elif 'Software\Microsoft\Windows' in line:
            d={}
            d['artifact'] = 'startup_folder'
            d['user'] = user
            d['key'] = line
        elif 'LastWrite' in line:
            d['lastwrite'] = line
        elif 'StartUp folder :' in line:
            d['location'] = line.split(':')[1].strip()
            json_data = json.dumps(d)
            print(json_data)

#def parsesoftwarerunkeys(t):
#    for line in t:
#        l = line.split('|')                

#def parsespawnprograms(t):
#    for line in t:
#        l = line.split('|')

def parsewinlogon(t):
    for line in t:
        if 'Microsoft\Windows NT\CurrentVersion' in line:
            d = {}
            d['artifact'] = 'winlogon'
            d['key'] = line
        elif 'LastWrite Time' in line:
            d['lastwrite'] = line
        elif 'Shell' in line:
            d['shell'] = line.split('=')[1].strip()
        elif 'Userinit' in line:
            d['userinit'] = line.split('=')[1].strip()
            json_data = json.dumps(d)
            print(json_data)

def parseemailattached(t):
    for line in t:
        d = {}
        l = line.strip('-')
        d['artifact'] = 'attached'
        d['file'] = str(l[0])
        d['attach'] = l[1]
        json_data = json.dumps(d)
        print(json_data)

def parsemft(t):
    for line in t:
        d = {}
        l = line.split(',')    
        d['artifact'] = 'mft'
        d['file'] = l[0]
        d['std_creation'] = l[1]
        d['std_modification'] = l[2]
        d['std_access'] = l[3]
        d['std_entry'] = l[4]
        d['fn_creation'] = l[5]
        d['fn_modification'] = l[6]
        d['fn_access'] = l[7]
        d['fn_entry'] = l[8]
        d['ads'] = l[9]
        json_data = json.dumps(d)
        print(json_data)
        

if __name__ == '__main__':
    
    f = sys.argv[1]

    if f == '-f':
        parsefiles(sys.stdin)
    elif f == '-u':
        parseusers(sys.stdin)
    elif f == '-p':
        parseprogramexecution(sys.stdin)
    elif f == '-aj':
        parseatjobs(sys.stdin)
    elif f == '-da':
        parsedirectaccesses(sys.stdin)
    elif f == '-a':
        parseautorun(sys.stdin)
    elif f == '-ua':
        parseuserrunkey(sys.stdin)
    elif f == '-s':
        parseservices(sys.stdin)
    elif f == '-id':
        parseappinitdlls(sys.stdin)
    elif f == '-sf':
        parsestartupfolders(sys.stdin)
    elif f == '-rk':
        parserunkeys(sys.stdin)
    elif f == '-sr':
        parsesoftwarerunkeys(sys.stdin)
    elif f == '-sp':
        parsespawnprograms(sys.stdin)
    elif f == '-w':
        parsewinlogon(sys.stdin)
    elif f == '-ea':
        parseemailattached(sys.stdin)
