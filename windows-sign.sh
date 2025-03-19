#!/bin/bash

INPUT_PATH=""
CERT_FILE=""
CERT_PSSW=""

#checking for parameters
for i in "$@"
do
case $i in
    -i=*|--input_path=*)
        INPUT_PATH="${i#*=}"
        shift # past argument=value
        ;;
    -cf=*|--cert_file=*)
        CERT_FILE="${i#*=}"
        shift # past argument=value
        ;;
    -cp=*|--cert_pssw=*)
        CERT_PSSW="${i#*=}"
        shift # past argument=value
        ;;
    *)
        # unknown option
        echo "WARNING: Unknown parameter not processed: $i"
        ;;
esac
done

cd $INSTALL_PATH

if [ -z "$INPUT_PATH" ]; then
    echo "Input path is required. Exiting..."
    exit 1
fi

# if cert file does not exist, exit
if [ ! -f "$CERT_FILE" ]; then
then
    echo "Certificate file not found. Exiting..."
    exit 1
fi

CERT_WIN=$(echo "$CERT_FILE" | sed 's/^\///' | sed 's/\//\\/g') # get windows relative path (with backslashes) of the cert

# if INPUT_PATH is a file, sign it
if [ -f $INPUT_PATH ]
then
    FILE_WIN=$(echo "$INPUT_PATH" | sed 's/^\///' | sed 's/\//\\/g')  # win relative path
    signtool.exe sign //fd SHA256 //f $CERT_WIN //p $CERT_PSSW //t http://timestamp.comodoca.com/authenticode $FILE_WIN
elif [ -d $INPUT_PATH ]
then
    # will sign all dll and exe files inside INSTALL_PATH, recursively
    for file in $(find $INPUT_PATH -name '*.dll' -or -name '*.exe');
    do
        FILE_WIN=$(echo "$file" | sed 's/^\///' | sed 's/\//\\/g')  # win relative path
        signtool.exe sign //debug //fd SHA256 //f $CERT_WIN //p $CERT_PSSW //t http://timestamp.comodoca.com/authenticode $FILE_WIN
    done
else
    echo "Input path not found. Exiting..."
    exit 1
fi

exit 0