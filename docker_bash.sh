#!/bin/sh

IID=$(docker ps -f name=calendaronline-1 | awk 'NR > 1 {print $1}')

if [ -z "$IID" ]; then
  echo "No running container found matching name=calendaronline-1" >&2
  exit 1
fi

echo "IMAGE ID --> $IID"
docker exec -it "$IID" /bin/sh
