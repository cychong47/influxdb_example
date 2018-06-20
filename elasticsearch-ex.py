"""Tutorial on using the InfluxDB client."""

import argparse
import time
import random

from datetime import datetime
from elasticsearch import Elasticsearch

def setup_db(host, port):
    client = Elasticsearch([{'host':host, 'port':port}])

    return client

def add_data(client, dl_tp, ul_tp):
    json_body = {
            "host": "server01",
            "region": "us-west",
            "dl_tp" : 0,
            "ul_tp" : 0,
            }

    #json_body[0]['time'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    json_body['dl_tp'] = int(dl_tp)
    json_body['ul_tp'] = int(ul_tp)

    #print("Write points: {0}".format(json_body))

    res = client.index(index='example', doc_type='throughput', body=json_body)
    if res['result'] != 'created':
        print("Error to indexing a new data")

def main(host, port):
    """Instantiate a connection to the InfluxDB."""

    client = setup_db(host, port)

    while True:
        dl_tp = random.uniform(150*1000000,200*1000000)
        ul_tp = random.uniform(50*1000000,70*1000000)
        add_data(client, dl_tp, ul_tp)
        time.sleep(1)

def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=9200,
                        help='port of InfluxDB http API')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port)
