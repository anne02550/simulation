#!/bin/sh -e
if [ -z "$1" ]; then
    echo "Must specify tls or no-tls" 1>&2
    exit 1
elif [ "$1" = "tls" ]; then
    TAG="rabbit-amqp-tls"
elif [ "$1" = "no-tls" ]; then
    TAG="rabbit-amqp-basic"
else
    echo "Argument must be either tls or no-tls" 1>&2
    exit 1
fi

docker run -d --name $TAG --network=host -p 15672:15672 $TAG:latest
docker logs $TAG --follow