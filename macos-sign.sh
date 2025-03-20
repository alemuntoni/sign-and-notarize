#!/bin/bash

INPUT_PATH=""
CERT_ID=""

#checking for parameters
for i in "$@"
do
case $i in
    -i=*|--input_path=*)
        INPUT_PATH="${i#*=}"
        shift # past argument=value
        ;;
    -ci=*|--cert_id=*)
        CERT_ID="${i#*=}"
        shift # past argument=value
        ;;
    *)
        # unknown option
        echo "WARNING: Unknown parameter not processed: $i"
        ;;
esac
done

if [ -z "$INPUT_PATH" ] 
then
    echo "Input path is required. Exiting..."
    exit 1
fi

if [ -z "$CERT_ID" ] 
then
    echo "Certificate ID is required. Exiting..."
    exit 1
fi

codesign --options "runtime" --timestamp --force --deep --sign "$CERT_ID" $INPUT_PATH

spctl -a -vvv $INPUT_PATH

exit 0