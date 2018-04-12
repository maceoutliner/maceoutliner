#! /usr/bin/env bash

PRODUCTION_FILE='requirements.txt'
DEV_FILE='test_requirements.txt'
usage="$(basename "$0") [-h/--help] [-p FILENAME] [-d FILENAME] -- Program to sync pipenv lockfile to pip-compatible requirements.

where:
     -h/--help Show this help text
     -p FILENAME Specify what file should be used for production packages (default: requirements.txt)
     -d FILENAME Specify what file should be used for development packages (default: test_requirements.txt)
"
while [ ! $# -eq 0 ]
do
    case "$1" in
        --help | -h)
            echo "$usage"
            exit
            ;;
        -p )
            PRODUCTION_FILE="$2"
            ;;
        -d )
            DEV_FILE="$2"
            ;;
        * )
            echo "You have specified an invalid option."
            echo "$usage"
            exit 1
            ;;
    esac
    shift
    shift
done


echo "Starting sync of Pipenv to pip-compatible requirements..."
echo "-------------"
if [ "$PRODUCTION_FILE" != "requirements.txt" ]; then
    echo "Using production file of ${PRODUCTION_FILE}."
fi
echo "Syncing production requirement packages..."
pipenv lock --requirements | grep -v "#" | cut -d' ' -f1 > $PRODUCTION_FILE
echo "Syncing production VCS packages..."
pipenv lock --requirements | grep "#" | sed 's/# //' >> $PRODUCTION_FILE
echo "Finished production packages!"

echo "--------------"
if [ "$DEV_FILE" != "test_requirements.txt" ]; then
    echo "Using development file of ${DEV_FILE}."
fi
echo "Syncing dev requirement packages..."
pipenv lock --dev --requirements | grep -v "#" | cut -d' ' -f1 > $DEV_FILE
echo "Syncing dev VCS packages..."
pipenv lock --dev --requirements | grep "#" | sed 's/# //' >> $DEV_FILE
echo "Finished dev packages!"
echo "--------------"
echo "Done!"
