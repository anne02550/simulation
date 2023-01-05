#!/bin/sh -e
if [ -z "$1" ]; then
    echo "Must specify tls or no-tls" 1>&2
    exit 1
elif [ "$1" = "tls" ]; then
    docker run -it \
    -e EMQX__LISTENERS__SSL__EXTERNAL=8883 \
    -e EMQX__LISTENERS__SSL__EXTERNAL__KEYFILE=/etc/certs/emqx.key \
    -e EMQX__LISTENERS__SSL__EXTERNAL__CERTFILE=/etc/certs/emqx.pem \
    -e EMQX__LISTENERS__SSL__EXTERNAL__CACERTFILE=/etc/certs/ca.pem \
    -e EMQX__LISTENERS__SSL__EXTERNAL__VERIFY=verify_none \
    -e EMQX__LISTENERS__SSL__EXTERNAL__FAIL_IF_NO_PEER_CERT=false \
    --name emqx -p 18083:18083 -p 8883:8883 emqx:4.4.4
elif [ "$1" = "no-tls" ]; then
    docker run -it -e EMQX__LISTENERS__TCP__DEFAULT__BIND=1883 \
    --name emqx -p 18083:18083 -p 1883:1883 emqx:4.4.4
else
    echo "Argument must be either tls or no-tls" 1>&2
    exit 1
fi
