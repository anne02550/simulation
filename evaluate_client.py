import argparse
import json

from evaluation_utils import run_glucose_monitor_simulation, run_heart_monitor_simulation


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Protocol timing script')
    parser.add_argument('--protocol', type=str, help='The protocol to use (options AMQP, COAP, HTTP, MQTT)')
    parser.add_argument('--tls', action='store_true')
    parser.add_argument('--no-tls', dest='tls', action='store_false')

    args = parser.parse_args()
    protocol = args.protocol
    tls = args.tls

    print(f"Running test with protocol: {protocol}, tls: {tls}")

    heart_data_publish_times = run_heart_monitor_simulation(protocol, tls)
    glucose_publish_times = run_glucose_monitor_simulation(protocol, tls)

    tls_str = 'tls' if tls else 'no-tls'
    with open(f"../results/timing/results-{protocol}-{tls_str}.json", "w") as f:
        json.dump({
            "heart_data_publish_times": heart_data_publish_times,
            "glucose_publish_times": glucose_publish_times
        }, f)
