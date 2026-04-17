#!/bin/sh

IID=`docker ps -f name=calendaronline-1 |  awk 'NR > 1 {print $1}'`

echo "IMAGE ID --> $IID"
docker exec -it $IID /bin/sh
