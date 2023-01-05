#!/bin/sh -e
if [ -z "$1" ]; then
    echo "Must specify tls or no-tls" 1>&2
    exit 1
elif [ "$1" = "tls" ]; then
    PORT=3001
elif [ "$1" = "no-tls" ]; then
    PORT=3000
else
    echo "Argument must be either tls or no-tls" 1>&2
    exit 1
fi

docker run --name nginx-container --network=host nginx-http:latest