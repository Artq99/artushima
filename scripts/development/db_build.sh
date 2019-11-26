#!/bin/sh

START=`date +%s`

echo "[INFO] ========================================================================"
echo "[INFO]"
echo "[INFO] Artushima: Development Database Building Script"
echo "[INFO]"
echo "[INFO] ========================================================================"
echo "[INFO]"

if [ ! -f "properties.txt" ];
then
	echo "[ERROR] File 'properties.txt' does not exist!"
	exit 1
fi

echo "[INFO] Reading the 'properties.txt' file..."

DB_IMAGE_NAME=$(grep "DB_IMAGE_NAME" properties.txt | sed "s/DB_IMAGE_NAME=//g")

if [ "$DB_IMAGE_NAME" == "" ];
then
    echo "[ERROR] Property DB_IMAGE_NAME not provided!"
	exit 1
fi

DB_CONTAINER_NAME=$(grep "DB_CONTAINER_NAME" properties.txt | sed "s/DB_CONTAINER_NAME=//g")

if [ "$DB_CONTAINER_NAME" == "" ];
then
    echo "[ERROR] Property DB_CONTAINER_NAME not provided!"
	exit 1
fi

DB_ROOT_PASSWORD=$(grep "DB_ROOT_PASSWORD" properties.txt | sed "s/DB_ROOT_PASSWORD=//g")

if [ "$DB_ROOT_PASSWORD" == "" ];
then
	echo "[ERROR] Property DB_ROOT_PASSWORD not provided!"
	exit 1
fi

DB_ADMIN_PASSWORD=$(grep "DB_ADMIN_PASSWORD" properties.txt | sed "s/DB_ADMIN_PASSWORD=//g")

if [ "$DB_ADMIN_PASSWORD" == "" ];
then
    echo "[ERROR] Property DB_ADMIN_PASSWORD not provided!"
    exit 1
fi

DB_APP_PASSWORD=$(grep "DB_APP_PASSWORD" properties.txt | sed "s/DB_APP_PASSWORD=//g")

if [ "$DB_APP_PASSWORD" == "" ];
then
	echo "[ERROR] Property DB_APP_PASSWORD not provided!"
	exit 1
fi

echo "[INFO] ------------------------------------------------------------------------"
echo "[INFO] Stopping and removing the container..."

STATUS=$(docker stop $DB_CONTAINER_NAME 2>&1)
if echo "$STATUS" | grep "No such container" &> /dev/null; then
	echo "[INFO] Container does not already exist."
elif echo "$STATUS" | grep "^$DB_CONTAINER_NAME$" &> /dev/null; then
	echo "[INFO] Container stopped."
	docker rm $DB_CONTAINER_NAME &> /dev/null
	echo "[INFO] Container removed."
else
	echo "[ERROR] $STATUS"
	exit 1
fi

echo "[INFO] ------------------------------------------------------------------------"
echo "[INFO] Removing the image..."

STATUS=$(docker image rm $DB_IMAGE_NAME 2>&1)
if echo "$STATUS" | grep "No such image" &> /dev/null; then
	echo "[INFO] Image does not already exist."
elif echo "$STATUS" | grep "Untagged" &> /dev/null; then
	echo "[INFO] Image removed."
else
	echo "[ERROR] $STATUS"
	exit 1
fi

echo "[INFO] ------------------------------------------------------------------------"
echo "[INFO] Creating the image..."

cd ../../artushima-db/development
docker build --tag $DB_IMAGE_NAME . &> /dev/null
if [ "$?" != "0" ]; then
	echo "[ERROR] Error while creating the image!"
	exit 1
fi
echo "[INFO] Image created."

echo "[INFO] ------------------------------------------------------------------------"
echo "[INFO] Creating and starting the container..."

docker run \
	--detach \
	--publish 3306:3306 \
	--name $DB_CONTAINER_NAME \
	--env MYSQL_ROOT_PASSWORD=$DB_ROOT_PASSWORD \
	$DB_IMAGE_NAME \
	&> /dev/null

if [ "$?" != "0" ]; then
	echo "[ERROR] Error while creating the container!"
	exit 1
fi
echo "[INFO] Container created and started."

echo "[INFO] ------------------------------------------------------------------------"
echo "[INFO] Waiting until the MySQL Server is up..."

docker ps | grep "Up.*(healthy).*$DB_CONTAINER_NAME" &> /dev/null
STATUS=$?
while [ $STATUS != 0 ];
do
	sleep 1
	docker ps | grep "Up.*(healthy).*$DB_CONTAINER_NAME" &> /dev/null
	STATUS=$?
done
echo "[INFO] MySQL Server is up and running."

echo "[INFO] ------------------------------------------------------------------------"
echo "[INFO] Creating users..."

docker exec $DB_CONTAINER_NAME mysql \
	--user=root \
	--password=$DB_ROOT_PASSWORD \
	--execute "CREATE USER 'admin'@'%' IDENTIFIED BY '$DB_ADMIN_PASSWORD';" \
	&> /dev/null

if [ "$?" != "0" ];
then
	echo "[ERROR] Error while creating user admin!"
	exit 1
fi
echo "[INFO] User created: admin"

docker exec $DB_CONTAINER_NAME mysql \
	--user=root \
	--password=$DB_ROOT_PASSWORD \
	--execute "CREATE USER 'app'@'%' IDENTIFIED BY '$DB_APP_PASSWORD';" \
	&> /dev/null

if [ "$?" != "0" ];
then
	echo "[ERROR] Error while creating user app!"
	exit 1
fi
echo "[INFO] User created: app"

echo "[INFO] All users created."

echo "[INFO] ------------------------------------------------------------------------"
echo "[INFO] Granting privileges to users..."

docker exec $DB_CONTAINER_NAME mysql \
	--user=root \
	--password=$DB_ROOT_PASSWORD \
	--execute "GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%';" \
	&> /dev/null

if [ "$?" != "0" ];
then
	echo "[ERROR] Error while granting privileges to user admin!"
	exit 1
fi
echo "[INFO] Privileges granted to user admin."

docker exec $DB_CONTAINER_NAME mysql \
	--user=root \
	--password=$DB_ROOT_PASSWORD \
	--execute "GRANT ALL PRIVILEGES ON *.* TO 'app'@'%';" \
	&> /dev/null

if [ "$?" != "0" ];
then
	echo "[ERROR] Error while granting privileges to user app!"
	exit 1
fi
echo "[INFO] Privileges granted to user app."

echo "[INFO] Privileges granted."

echo "[INFO] ------------------------------------------------------------------------"

END=`date +%s`
DURATION=$((END-START))

echo "[INFO] Dockerized database built in $DURATION seconds."