#!/bin/sh -e
if [ -z "$1" ]; then
    echo "Must specify tls or no-tls" 1>&2
    exit 1
elif [ "$1" = "tls" ]; then
    TAG="californium-dtls"
    docker run -it --name $TAG --network=host $TAG:latest java -cp ./target/cf-server-app-1.0-SNAPSHOT.jar com.tam.app.AppSecure
elif [ "$1" = "no-tls" ]; then
    TAG="californium-basic"
    docker run -it --name $TAG --network=host $TAG:latest java -cp ./target/cf-server-app-1.0-SNAPSHOT.jar com.tam.app.App
else
    echo "Argument must be either tls or no-tls" 1>&2
    exit 1
fi
