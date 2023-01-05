#!/bin/sh -e
if [ -z "$1" ]; then
    echo "Must specify tls or no-tls" 1>&2
    exit 1
elif [ "$1" = "tls" ]; then
    CONF_FILE="rabbitmq-tls.conf"
    TAG="rabbit-amqp-tls"
elif [ "$1" = "no-tls" ]; then
    CONF_FILE="rabbitmq.conf"
    TAG="rabbit-amqp-basic"
else
    echo "Argument must be either tls or no-tls" 1>&2
    exit 1
fi

docker build --tag $TAG --build-arg CONF_FILE=$CONF_FILE --file ./files/Dockerfile ./files