import paho.mqtt.client as mqtt
import ssl

address = "localhost"
basic_port = 1883
secure_port = 8883


class MqttClient:

    def __init__(self):
        self.client = mqtt.Client()
        self.client.connect(address, port=basic_port, keepalive=60, bind_address="")

    def send(self, data):
        self.client.publish('/some-resource', data).wait_for_publish()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class MqttTlsClient:

    def __init__(self):
        cert_path = "./servers/mqtt-emqx/files/certs"

        self.client = mqtt.Client()
        self.client.tls_set(
            ca_certs=f"{cert_path}/ca.pem",
            certfile=f"{cert_path}/emqx.pem",
            keyfile=f"{cert_path}/emqx.key",
            cert_reqs=ssl.CERT_NONE,
            tls_version=ssl.PROTOCOL_TLSv1_2,
        )
        self.client.tls_insecure_set(True)
        self.client.connect(address, port=secure_port, keepalive=60, bind_address="")

    def send(self, data):
        self.client.publish('/some-resource', data).wait_for_publish()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
