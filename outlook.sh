#!/bin/bash

IFS=$'\n'
PWD=`pwd`

for file in $(ls $EMAIL)
do
    # Tomamos precauciones
    rm -r $OUTPUTDIR$file 2> /dev/null

    # Directorios interesantes
    INCOMING="Bandeja de entrada/"
    SENDED="Elementos enviados/"
    DELETED="Elementos eliminados/"

    # Extraemos informacion del archivo
    readpst -S -o $OUTPUTDIR $EMAIL$file 1> /dev/null
    [ $? -eq 1 ] && exit(1)

    cd $OUTPUTDIR$file
    
    if [ -d $INCOMING ]
    then
        cd $INCOMING
            INTERNALDOMAIN=$(grep -e ^To * | sed 's/[0-9]*://' | sort | uniq -c | sort -r | head -n 1 | cut -d@ -f2) 
            #EMAILS=($(grep -e ^From * | grep -v $INTERNALDOMAIN | sed 's/.*<\(.*\)>.*/\1/' | sort | uniq))
            FILES=($(ls | grep -))
            HASHES=()
            for file in ${FILES[@]}
            do
                HASH=$(md5sum $file | awk '{print $1}')
                threatcrowdCheck.py $HASH -j $JSONFILE
            done
            #for email in ${EMAILS[@]}
            #do
            #    threatcrowdCheck.py $email -j $JSONFILE
                # Hay que meter una pausa de 10 segundos entre peticiony peticion
            #done
            for file in ${HASHES[@]}
            do
                threatcrowdCheck.py $file -j $JSONFILE
                # Pausa da 10 segundos
            done
            # Comprobar urls dentro de los propios correos
            URLS=($(grep -P "/((?:https?\:\/\/|www\.)(?:[-a-z0-9]+\.)*[-a-z0-9]+.*)/i" * | awk -F: '{print $2}')) 
            for url in ${URLS[@]}
            do
                # Extraer el dominio de la url
                threatcrowdCheck.py $url -j $JSONFILE
            done
        cd ..
    fi
    #if [ ! -z $SENDED ]
    #    then
    #        echo "Not empty"    
    #    fi
    if [ ! -z $DELETED ]
    then
        cd $DELETED
            INTERNALDOMAIN=$(grep -e ^To * | sed 's/[0-9]*://' | sort | uniq -c | sort -r | head -n 1 | cut -d@ -f2) 
            #EMAILS=($(grep -e ^From * | grep -v $INTERNALDOMAIN | sed 's/.*<\(.*\)>.*/\1/' | sort | uniq))
            FILES=($(ls | grep -))
            HASHES=()
            for file in ${FILES[@]}
            do
                HASHES+=($(md5sum $file | awk '{print $1}'))
            done
            #for email in ${EMAILS[@]}
            #do
            #    threatcrowdCheck.py $email -j $JSONFILE
            #done
            for file in ${HASHES[@]}
            do
                threatcrowdCheck.py $file -j $JSONFILE
            done
            # Comprobar urls dentro de los propios correos
            URLS=($(grep -P "/((?:https?\:\/\/|www\.)(?:[-a-z0-9]+\.)*[-a-z0-9]+.*)/i" * | awk -F: '{print $2}')) 
            for url in ${URLS[@]}
            do
                threatcrowdCheck.py $url -j $JSONFILE
            done
        cd ..
    fi
    cd $PWD
done

cd $PWD
