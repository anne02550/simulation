import datetime
import json
import random
import time
from clients.amqp import AmqpClient, AmqpTlsClient
from clients.coap import CoapClient, CoapTlsClient
from clients.http import HttpClient, HttpClientSecure
from clients.mqtt import MqttClient, MqttTlsClient

# ---------------------------------------------------------------------------------------------------------------------
# Client utilities
# ---------------------------------------------------------------------------------------------------------------------


client_types = {
    ("AMQP", False): AmqpClient,
    ("AMQP", True): AmqpTlsClient,
    ("COAP", False): CoapClient,
    ("COAP", True): CoapTlsClient,
    ("HTTP", False): HttpClient,
    ("HTTP", True): HttpClientSecure,
    ("MQTT", False): MqttClient,
    ("MQTT", True): MqttTlsClient,
}


def get_client(protocol, tls):
    # fetches the messaging client for the given protocol and tls settings
    return client_types[(protocol, tls)]


# ---------------------------------------------------------------------------------------------------------------------
# HEART MONITOR SIMULATION
# ---------------------------------------------------------------------------------------------------------------------
n_heart_simulations = 1000
n_heart_messages_per_simulation = 10


def build_mock_heart_monitor_message():
    # Builds a simulated message from a pretend heart monitoring device.
    # Intended to be sampled at 1 kHz, to test small, frequent messages.
    # Returns: the message as a json string
    return json.dumps({
        "ECG": random.random(),
        "PCG": random.random(),
        "PPG": random.random(),
        "FSR": random.random()
    })


def get_mock_heart_monitor_messages(n_messages):
    return [build_mock_heart_monitor_message() for _ in range(n_messages)]


def run_heart_monitor_simulation(protocol, tls):
    client_type = get_client(protocol, tls)

    heart_data_publish_times = []
    with client_type() as client:

        for _ in range(n_heart_simulations):

            # build fake messages to send
            msgs = get_mock_heart_monitor_messages(n_heart_messages_per_simulation)

            # send messages and time how long it took
            start_time = time.time()
            for msg in msgs:
                client.send(msg)
            end_time = time.time()

            # add times to results
            heart_data_publish_times.append(end_time - start_time)

            print(end_time - start_time)
    return heart_data_publish_times


# ---------------------------------------------------------------------------------------------------------------------
# GLUCOSE MONITOR SIMULATION
# ---------------------------------------------------------------------------------------------------------------------


# Fake glucose messages are too big for COAP,
# So it has to break the data down into
# 4 messages with 2 hours of simulated data each,
# AMQP and MQTT work with one message for all the data
glucose_message_configs = {
    "AMQP": (8, 1),
    "COAP": (2, 4),
    "HTTP": (8, 1),
    "MQTT": (8, 1),
}
n_glucose_simulations = 100
sleep_time_between_glucose_simulations = 5  # number of seconds between glucose simulation runs


def build_mock_glucose_monitor_message(n_hours):
    # Builds a simulated message from a pretend glucose monitoring device.
    # Intended to be sampled at once every few hours, to test large, infrequent messages.
    # Returns: the message as a json string
    samples_per_hour = 4

    results = []

    id = 1
    time_now = datetime.datetime.utcnow().isoformat()  # e.g. "2020-07-10 15:00:00.000"
    glucose_reading = random.random() + 4  # e.g. 4.7323244958367479

    for _ in range(n_hours * samples_per_hour):
        results.append({
            "id": id,
            "time": time_now,
            "record_type": 1,
            "glucose": glucose_reading,
        })
        id += 1

    return json.dumps(results)


def get_glucose_monitor_messages(protocol):
    n_hours, n_messages = glucose_message_configs[protocol]
    return [build_mock_glucose_monitor_message(n_hours) for _ in range(n_messages)]


def run_glucose_monitor_simulation(protocol, tls):
    client_type = get_client(protocol, tls)

    glucose_publish_times = []
    with client_type() as client:

        for _ in range(n_glucose_simulations):

            # build fake messages to send
            messages = get_glucose_monitor_messages(protocol)

            # send messages and time how long it took
            start_time = time.time()
            for message in messages:
                client.send(message)
            end_time = time.time()

            # add times to results
            glucose_publish_times.append(end_time - start_time)
            print(end_time - start_time)

            time.sleep(sleep_time_between_glucose_simulations)

    return glucose_publish_times
