#!/bin/sh

START=`date +%s`

echo "[INFO] ========================================================================"
echo "[INFO]"
echo "[INFO] Artushima: Development Database Migration Script"
echo "[INFO]"
echo "[INFO] ========================================================================"
echo "[INFO]"

if [ ! -f "properties.txt" ]; then
	echo "[ERROR] File 'properties.txt' does not exist!"
	exit 1
fi

echo "[INFO] Reading the 'properties.txt' file..."

DB_ROOT_PASSWORD=$(grep "DB_ROOT_PASSWORD" properties.txt | sed "s/DB_ROOT_PASSWORD=//g")

if [ "$DB_ROOT_PASSWORD" == "" ];
then
    echo "[ERROR] Property DB_ROOT_PASSWORD not provided!"
    exit 1
fi

DB_CONTAINER_NAME=$(grep "DB_CONTAINER_NAME" properties.txt | sed "s/DB_CONTAINER_NAME=//g")

if [ "$DB_CONTAINER_NAME" == "" ];
then
    echo "[ERROR] Property DB_CONTAINER_NAME not provided!"
	exit 1
fi

echo "[INFO] ------------------------------------------------------------------------"
echo "[INFO] Executing migrations..."

cd ../../artushima-db/migration

for FILE in *.sql;
do
    echo "[INFO] Migrating: $FILE"
    MESSAGE=$`docker exec -i $DB_CONTAINER_NAME mysql --user=root --password=$DB_ROOT_PASSWORD artushimadb < $FILE 2>&1`

    if [ "$?" != "0" ];
    then
        echo "[ERROR] When migrating: $file_name"
        echo "[ERROR]"
        echo "$MESSAGE"
        exit 1
    fi
done

END=`date +%s`
DURATION=$((END-START))

echo "[INFO] All scripts migrated in $DURATION seconds."