#!/bin/bash

PWD=`pwd`
IFS=$'\n'

OUTPUT=$EMAIL"output"
mkdir $OUTPUT 2> /dev/null

for file in $(ls $EMAIL)
do
    readpst -S -o $OUTPUT 1> /dev/null
done

# Directorios interesantes
ENTRADA='Bandeja de entrada/'
BORRADOS='Elementos eliminados/'

for file in $(ls $OUTPUT)
do
    cd $OUTPUT$file
        if [ -d $ENTRADA ]
        then
            # Buscar archivos adjuntos
            for attached in $(ls | grep -)
            do
				TYPE=$(file --mime-type $attached | cut -d: -f2)
				grep -i "macro" $attached > /dev/null
				if [ $? -eq 0 ]
				then
					MACRO='yes'
				else
					MACRO='no'
				fi
				echo "{'artifact':'email','type':'attached','file':'$attached','macro':'$MACRO'}" >> $JSONFILE
            done
            # Extraer URLs en los correos
			for $mail in $(ls | grep -v "-")
			do
				
			done
        fi    
    cd $PWD
done
