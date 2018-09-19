#!/bin/bash

# Directorio donde se encuentran los archivos del registro
#DIR=/home/vlo/TFG/registry/
DIR="$1"
SYSTEMDIR="$DIR"System/

USERDIR="$DIR"Users/
USERDIRS=()
for d in $(ls $USERDIR)
do
    USERDIRS+=("$USERDIR$d/")
done

# Nombres de los archivos del registro
SYSTEM=$(ls $SYSTEMDIR | grep -i system)
SOFTWARE=$(ls $SYSTEMDIR | grep -i software)
SAM=$(ls $SYSTEMDIR | grep -i sam)
SECURITY=$(ls $SYSTEMDIR | grep -i security)
NTUSER=()
n=0
for i in ${USERDIRS[@]}
do
    NTUSER+=(${USERDIRS[n]}$(ls $i | grep -i "ntuser.dat"))
    n=$((n+1))
done
n=0
USRCLASS=()
for i in ${USERDIRS[@]}
do
    USRCLASS+=(${USERDIRS[n]}$(ls $i | grep -i "usrclass.dat"))
    n=$((n+1))
done

# Conocer usuarios en el sistema, fecha de creacion de la cuenta, ultimo loggeo y veces que han sido loggeados
USERLIST=user_list
rip.pl -r $SYSTEMDIR$SAM -f sam | grep -i 'Username\|Account Type\|Account Created\|Last Login Date\|Login Count' > $RAW$USERLIST
cat $RAW$USERLIST | sed 's/\[//g' | sed 's/\]//g' | parse.py -u > $JSONFILE

# Ejecucion de programas
PROGRAMEXECUTION=program_execution
ATJOBS=at_jobs
DIRECT=direct_accesses
rip.pl -r $SYSTEMDIR$SYSTEM -p appcompatcache_tln > $RAW$PROGRAMEXECUTION
rip.pl -r $SYSTEMDIR$SYSTEM -p legacy_tln >> $RAW$PROGRAMEXECUTION
rip.pl -r $SYSTEMDIR$SOFTWARE -p at_tln >> $RAW$ATJOBS
rip.pl -r $SYSTEMDIR$SOFTWARE -p direct_tln >> $RAW$DIRECT
for file in ${NTUSER[@]}
do
    USER=$(echo $file | awk -F'/' '{printf $(NF-1)}')
    rip.pl -r $file -p muicache_tln -u $USER >> $RAW$PROGRAMEXECUTION
done
for file in ${USRCLASS[@]}
do
    USER=$(echo $file | awk -F'/' '{printf $(NF-1)}')
    rip.pl -r $file -p muicache_tln -u $USER >> $RAW$PROGRAMEXECUTION
done
# Ordenamos los timestamps y preparamos el informe para ser presentado
cat -s $RAW$PROGRAMEXECUTION | sort -nr | uniq -u | sed 's/\\//g' > "$RAW"new && mv "$RAW"new $RAW$PROGRAMEXECUTION
cat -s $RAW$ATJOBS | sort -nr | uniq  > "$RAW"new && mv "$RAW"new $RAW$ATJOBS
cat -s $RAW$DIRECT| sort -nr | uniq  > "$RAW"new && mv "$RAW"new $RAW$DIRECT

cat $RAW$PROGRAMEXECUTION | parse.py -p >> $JSONFILE
cat $RAW$DIRECT | parse.py -da >> $JSONFILE
cat $RAW$ATJOBS | parse.py -aj >> $JSONFILE

# Autoruns
RUNKEY=run_key
URUNKEY=user_run_key
SERVICES=services
APPINIT=appinit
rip.pl -r $SYSTEMDIR$SOFTWARE -p soft_run > $RAW$RUNKEY
echo "................................................................" >> $RAW$URUNKEY
for file in ${NTUSER[@]}
do
    USER=$(echo $file | awk -F'/' '{printf $(NF-1)}')
    echo "User: $USER" >> $RAW$URUNKEY
    rip.pl -r $file -p user_run  >> $RAW$URUNKEY
    echo "................................................................" >> $RAW$URUNKEY
done
cat $RAW$RUNKEY | parse.py -a | grep -v "not found" | sed 's/\\n//g' | sed 's:\\:/:g' >> $JSONFILE
cat $RAW$URUNKEY | sed 's/\\n//g' | sed 's:\\:/:g' | parse.py -ua >> $JSONFILE

# Listado de servicios
rip.pl -r $SYSTEMDIR$SYSTEM -p svc > $RAW$SERVICES
tounixtime.sh $RAW$SERVICES
cat $RAW$SERVICES | parse.py -s >> $JSONFILE

# AppInitdlls
rip.pl -r $SYSTEMDIR$SOFTWARE -p appinitdlls > $RAW$APPINIT
cat $RAW$APPINIT | parse.py -id | sed 's:\\:/:g' >> $JSONFILE

# Start up
STARTUP=startup
cat $RAW$STARTUP > $RAW$STARTUP # limpiamos el archivo para cada prueba
for file in ${NTUSER[@]}
do
    USER=$(echo $file | awk -F'/' '{printf $(NF-1)}')
    echo "User: $USER" >> $RAW$STARTUP
    rip.pl -r $file -p startup >> $RAW$STARTUP
done
cat $RAW$STARTUP | sed 's:\\:/:g' | parse.py -sf >> $JSONFILE

# Start Registry Keys
SRUNKEY=srun_keys
rip.pl -r $SYSTEMDIR$SOFTWARE -p srun_tln > $RAW$SRUNKEY
# Falta completar la funcion en parse.py
cat $RAW$SRUNKEY | sed 's:\\:/:g' | parse.py -sr >> $JSONFILE

# Spawn programs
SPAWNPROGRAMS=spawn_programs
rip.pl -r $SYSTEMDIR$SYSTEM -p cmd_shell_tln > $RAW$SPAWNPROGRAMS
cat $RAW$SPAWNPROGRAMS | parse.py -sp

# Installed components
INSCOMP=installed_components
rip.pl -r $SYSTEMDIR$SOFTWARE -p installedcomp > $RAW$INSCOMP

# Winlogon
WINLOGON=winlogon
rip.pl -r $SYSTEMDIR$SOFTWARE -p winlogon > $RAW$WINLOGON
cat $RAW$WINLOGON | sed 's:\\:/:g' | parse.py -w >> $JSONFILE

# Limpiar la salida json
cat $JSONFILE |  sed 's/\\n//g' | sed 's/\\\\/\\/g' | sed 's:/n::g' > /tmp/json_file &&mv /tmp/json_file $JSONFILE
