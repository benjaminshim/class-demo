# !/bin/sh
# Some common shell stuff

echo "Importing from common.sh"

DB=databasesplusoneDB
USER=cm5685
CONNECT_STR="mongodb+srv://databasesplusone.zrimlpx.mongodb.net/"
if [ -z $DATA_DIR ]
then
    DATA_DIR=/Users/carolinamartin/desktop/soft_eng/project/databases_plus_one/data
fi
BKUP_DIR=$DATA_DIR/bkup
EXP=/usr/local/bin/mongoexport
IMP=/usr/local/bin/mongoimport

if [ -z $MONGO_PASSWD ]
then
    echo "You must set MONGO_PASSWD in your env before running this script."
    exit 1
fi

declare -a UsersCollections=("restaurants" "users")
