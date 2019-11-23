#!/bin/sh

# Variables
SCRIPT_VERSION="1.0"
CONTAINER_NAME="artushima-db1"
IMAGE_NAME="artushima-db:1.0"
ROOT_PASSWD="dev"
ADMIN_PASSWD="dev"

START=`date +%s`

echo "[INFO] ========================================================================"
echo "[INFO]"
echo "[INFO] Artushima: Development Database Building Script"
echo "[INFO]"
echo "[INFO] Script version: $SCRIPT_VERSION"
echo "[INFO]"
echo "[INFO] ========================================================================"
echo "[INFO]"

echo "[INFO] Stopping and removing the container..."
STATUS=$(docker stop $CONTAINER_NAME 2>&1)
if echo "$STATUS" | grep "No such container" &> /dev/null; then
	echo "[INFO] Container does not already exist."
elif echo "$STATUS" | grep "^$CONTAINER_NAME$" &> /dev/null; then
	echo "[INFO] Container stopped."
	docker rm $CONTAINER_NAME &> /dev/null
	echo "[INFO] Container removed."
else
	echo "[ERROR] $STATUS"
	exit 1
fi

echo "[INFO] ------------------------------------------------------------------------"

echo "[INFO] Removing the image..."
STATUS=$(docker image rm $IMAGE_NAME 2>&1)
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
docker build --tag $IMAGE_NAME . &> /dev/null
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
	--name $CONTAINER_NAME \
	--env MYSQL_ROOT_PASSWORD=$ROOT_PASSWD \
	$IMAGE_NAME \
	&> /dev/null
if [ "$?" != "0" ]; then
	echo "[ERROR] Error while creating the container!"
	exit 1
fi
echo "[INFO] Container created and started."

echo "[INFO] ------------------------------------------------------------------------"

echo "[INFO] Waiting until the MySQL Server is up..."
docker ps | grep "Up.*(healthy).*$CONTAINER_NAME" &> /dev/null
STATUS=$?
while [ $STATUS != 0 ];
do
	sleep 1
	docker ps | grep "Up.*(healthy).*$CONTAINER_NAME" &> /dev/null
	STATUS=$?
done
echo "[INFO] MySQL Server is up and running."

echo "[INFO] ------------------------------------------------------------------------"

echo "[INFO] Creating users..."
docker exec $CONTAINER_NAME mysql \
	--user=root \
	--password=$ROOT_PASSWD \
	--execute "CREATE USER 'admin'@'%' IDENTIFIED BY '$ADMIN_PASSWD';" \
	&> /dev/null
if [ "$?" != "0" ]; then
	echo "[ERROR] Error while creating user admin!"
	exit 1
fi
echo "[INFO] User created: admin"

echo "[INFO] All users created."

echo "[INFO] ------------------------------------------------------------------------"

echo "[INFO] Granting privileges to users..."

docker exec $CONTAINER_NAME mysql \
	--user=root \
	--password=$ROOT_PASSWD \
	--execute "GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%';" \
	&> /dev/null
if [ "$?" != "0" ]; then
	echo "[ERROR] Error while granting privileges to user admin!"
	exit 1
fi
echo "[INFO] Privileges granted to user admin."

echo "[INFO] Privileges granted."

echo "[INFO] ------------------------------------------------------------------------"

END=`date +%s`
DURATION=$((END-START))

echo "[INFO] Dockerized database built in $DURATION seconds."