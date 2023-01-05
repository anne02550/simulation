import ssl
import pika

address = "ubuntu"
basic_port = 5672
secure_port = 5671

class AmqpClient:

    def __init__(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(address, port=basic_port))
        self.channel = connection.channel()
        self.channel.queue_declare(queue='some-resource')

    def send(self, data):
        self.channel.basic_publish(exchange='', routing_key='some-resource', body=data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class AmqpTlsClient:

    def __init__(self):
        cert_path = "./servers/amqp-rabbitmq/files/certs"

        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(f"{cert_path}/ca_certificate.pem")
        context.load_cert_chain(f"{cert_path}/client_ubuntu_certificate.pem", f"{cert_path}/client_ubuntu_key.pem", password="bunnies")
        ssl_options = pika.SSLOptions(context)

        conn_params = pika.ConnectionParameters(address, port=secure_port, ssl_options=ssl_options)

        connection = pika.BlockingConnection(conn_params)
        self.channel = connection.channel()
        self.channel.queue_declare(queue='some-resource')

    def send(self, data):
        self.channel.basic_publish(exchange='', routing_key='some-resource', body=data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
