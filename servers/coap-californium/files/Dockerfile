FROM openjdk:11

RUN apt-get update
RUN apt-get install -y maven

COPY server-code/ .
RUN mvn package

CMD java -cp ./target/cf-server-app-1.0-SNAPSHOT.jar com.tam.app.App