import requests
import os

address = "ubuntu"
basic_port = 3000
secure_port = 3001


class HttpClient:

    def __init__(self):
        self.url = f"http://{address}:{basic_port}/some-resource/"

    def send(self, data):
        requests.post(self.url, json=data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class HttpClientSecure:

    def __init__(self):
        os.environ["REQUESTS_CA_BUNDLE"] = "./servers/http-nginx/files/certs/ca_certificate.pem"
        self.url = url = f"https://{address}:{secure_port}/some-resource/"

    def send(self, data):
        requests.post(self.url, json=data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class HttpClientWithSession:

    def __init__(self):
        self.url = f"http://{address}:{basic_port}/some-resource/"
        self.session = requests.Session()

    def send(self, data):
        self.session.post(self.url, json=data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class HttpClientSecureWithSession:

    def __init__(self):
        os.environ["REQUESTS_CA_BUNDLE"] = "./servers/http-nginx/files/certs/ca_certificate.pem"
        self.url = url = f"https://{address}:{secure_port}/some-resource/"
        self.session = requests.Session()

    def send(self, data):
        self.session.post(self.url, json=data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
