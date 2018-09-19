#!/bin/bash

rm -r ../myreport/* 2> /dev/null

PROGRAM=$0
#function usage{
#    echo "usage:" 
#}

POSITIONAL=()
while [[ $# -gt 0 ]]
do
    KEY="$1"
    case $KEY in
        -r|--registry)
        export REGISTRY="$2"
        shift
        shift
        ;;
        -b|--browser)
        export BROWSER="$2"
        shift
        shift
        ;;
        -m|--mft)
        export MFT="$2"
        shift
        shift
        ;;
        -e|--email)
        export EMAIL="$2"
        shift
        shift
        ;;
       --output)
        export OUTPUTDIR=$2
        shift
        shift
        ;;
        -d|--database)
        export DATABASE="$2"
        shift
        shift
        ;;
		-i|--interactive)
		export SHELL='yes'
		shift
		;;
		--rules)
		export RULES="$2"
		shift
		shift
		;;
        *)
        POSITIONAL+=("$1")
        shift
        ;;
    esac
done

# Directorios para almacenar la salida de informacion de diferentes herramientas
export RAW=$OUTPUTDIR"raw/"
export JSON=$OUTPUTDIR"json/"
export JSONFILE=$JSON"json_file"
mkdir $RAW 2> /dev/null
mkdir $JSON 2> /dev/null
touch $JSONFILE

# Extraccion de informacion

# Registro de Windows
if [[ ! -z $REGISTRY &&  -d $REGISTRY ]]
then
#	echo "Parsing registry"
#    registry.sh $REGISTRY
	registry.py $REGISTRY $RULES $JSONFILE
fi


# Navegacion de los usuarios
if [[ ! -z $BROWSER && -d $BROWSER ]]
then
	echo "Parsing browser activity"
    for file in $(ls $BROWSER)
    do
        browser_activity.py $BROWSER$file $JSONFILE
    done
fi

# Correo electronico
#if [[ ! -z $EMAIL && -d $EMAIL ]]
#then
    

# $MFT
if [[ ! -z $MFT && -f $MFT ]]
then
	echo "Parsing MFT"
    python2 ~/build/analyzeMFT/analyzeMFT.py -f $MFT -o $OUTPUTDIR"mftparsed"
    mft_parse.sh $OUTPUTDIR"mftparsed"  > /tmp/mfttemp && mv /tmp/mfttemp $OUTPUTDIR"mftparsed"
    export MFT=$OUTPUTDIR"mftparsed"
fi

# Almacenamiento de datos
if [[ -z $DATABSE ]] 
then
    export DATABASE=$OUTPUTDIR`date "+%F"`.sqlite
fi
echo "Storing data in DB"
to_db.py $JSONFILE $DATABASE
	
# Tratamiento de los datos
echo "Starting rules"
if [[ -f $MFT ]]
then
	rules.py $RULES $DATABASE $MFT
else
	rules.py $RULES $DATABASE
fi

if [ "$SHELL" = "yes" ]
then
	# Inicio de la shell interactiva
	shell.py $DATABASE
else
	# Generacion de alertas
	show_alerts.py $DATABASE
fi
