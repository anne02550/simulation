import argparse
import time
import json
import multiprocessing as mp
import psutil

from evaluation_utils import run_heart_monitor_simulation


# Starts a simulation in a new process, then records the processes cpu utilization 100 times a second
def monitor(target):
    worker_process = mp.Process(target=target)
    worker_process.start()
    p = psutil.Process(worker_process.pid)

    # log cpu usage of `worker_process` every 10 ms
    cpu_percents = []
    while worker_process.is_alive():
        cpu_percents.append(p.cpu_percent())
        time.sleep(0.01)

    worker_process.join()
    return cpu_percents


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Protocol timing script')
    parser.add_argument('--protocol', type=str, help='The protocol to use (options AMQP, COAP, HTTP, MQTT)')
    parser.add_argument('--tls', action='store_true')
    parser.add_argument('--no-tls', dest='tls', action='store_false')

    args = parser.parse_args()
    protocol = args.protocol
    tls = args.tls

    print(f"Running test with protocol: {protocol}, tls: {tls}")

    heart_data_cpu = monitor(lambda: run_heart_monitor_simulation(protocol, tls))

    tls_str = 'tls' if tls else 'no-tls'
    with open(f"../results/cpu/cpu-results-{protocol}-{tls_str}.json", "w") as f:
        json.dump({
            "heart_data_cpu": heart_data_cpu
        }, f)
