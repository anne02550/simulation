#!/bin/sh -e
if [ -z "$1" ]; then
    echo "Must specify tls or no-tls" 1>&2
    exit 1
elif [ "$1" = "tls" ]; then
    TAG="californium-dtls"
elif [ "$1" = "no-tls" ]; then
    TAG="californium-basic"
else
    echo "Argument must be either tls or no-tls" 1>&2
    exit 1
fi

docker build --tag $TAG --file ./files/Dockerfile ./files