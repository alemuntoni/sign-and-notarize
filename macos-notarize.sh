#!/bin/bash

INPUT_PATH=""
NOTAR_USER=""
NOTAR_PASSWORD=""
NOTAR_TEAM_ID=""

#checking for parameters
for i in "$@"
do
case $i in
    -i=*|--input_path=*)
        INPUT_PATH="${i#*=}"
        shift # past argument=value
        ;;
    -nu=*|--notarization_user=*)
        NOTAR_USER="${i#*=}"
        shift # past argument=value
        ;;
    -nt=*|--notarization_team=*)
        NOTAR_TEAM_ID="${i#*=}"
        shift # past argument=value
        ;;
    -np=*|--notarization_pssw=*)
        NOTAR_PASSWORD="${i#*=}"
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
else
    echo "Input path: $INPUT_PATH"
fi

xcrun notarytool store-credentials "notarytool-profile" --apple-id $NOTAR_USER --team-id $NOTAR_TEAM_ID --password $NOTAR_PASSWORD

ditto -c -k --keepParent "$INPUT_PATH" "notarization.zip"

xcrun notarytool submit "notarization.zip" --keychain-profile "notarytool-profile" --wait

xcrun stapler staple "$INPUT_PATH"

rm -rf notarization.zip

exit 0