FROM rabbitmq:3.10-management
ARG CONF_FILE

# SSL key and cert setup
COPY ./certs /etc/rabbitmq/
RUN chown rabbitmq:rabbitmq /etc/rabbitmq/*.pem
RUN chown rabbitmq:rabbitmq /etc/rabbitmq/*.p12

# RabbitMQ config 
COPY ${CONF_FILE} /etc/rabbitmq/rabbitmq.conf

