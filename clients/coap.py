from coapthon.client.helperclient import HelperClient
import socket
from dtls.wrapper import wrap_client


class CoapClient:

    def __init__(self, use_timeout_fix=False):
        self.client = HelperClient(server=('127.0.0.1', 5683))
        self.use_timeout_fix = use_timeout_fix

    def send(self, data):
        if self.use_timeout_fix:
            response = self.client.post('some-resource/', data, timeout=0.2)
        else:
            response = self.client.post('some-resource/', data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.stop()


class CoapTlsClient:

    def __init__(self, use_timeout_fix=False):

        secure_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        secure_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        secure_socket = wrap_client(
                secure_socket,
                keyfile="./servers/coap-californium/files/server-code/certs/root.pem",
                certfile="./servers/coap-californium/files/server-code/certs/root.pem",
                do_handshake_on_connect=True)

        self.client = HelperClient(server=('127.0.0.1', 5684), sock=secure_socket)
        self.use_timeout_fix = use_timeout_fix

    def send(self, data):
        if self.use_timeout_fix:
            response = self.client.post('some-resource/', data, timeout=0.2)
        else:
            response = self.client.post('some-resource/', data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.stop()