"""Tutorial on using the InfluxDB client."""

import argparse
import time
import random

from datetime import datetime
from influxdb import InfluxDBClient

def setup_db(host, port):
    user = 'root'
    password = 'root'
    dbname = 'example'
    dbuser = 'smly'
    dbuser_password = 'my_secret_password'

    client = InfluxDBClient(host, port, user, password, dbname)

    print("Create database: " + dbname)
    client.create_database(dbname)

    print("Create a retention policy")
    client.create_retention_policy('awesome_policy', '3d', 3, default=True)

    print("Switch user: " + dbuser)
    client.switch_user(dbuser, dbuser_password)

    return client

def add_data(client, dl_tp, ul_tp):
    json_body = [
        {
            "measurement": "throughput",
            "tags": {
                "host": "server01",
                "region": "us-west"
            },
            "time": "2009-11-10T23:00:00Z",
            "fields": {
                "dl_tp" : 0,
                "ul_tp" : 0,
            }
        }
    ]

    json_body[0]['time'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    json_body[0]['fields']['dl_tp'] = int(dl_tp)
    json_body[0]['fields']['ul_tp'] = int(ul_tp)

    #print("Write points: {0}".format(json_body))

    client.write_points(json_body)

def main(host='localhost', port=8086):
    """Instantiate a connection to the InfluxDB."""

    client = setup_db(host, port)

    while True:
        dl_tp = random.uniform(150*1000000,200*1000000)
        ul_tp = random.uniform(50*1000000,70*1000000)
        add_data(client, dl_tp, ul_tp)
        time.sleep(1)


    query = 'select value from cpu_load_short;'
    print("Querying data: " + query)
    result = client.query(query)

    print("Result: {0}".format(result))

#    print("Switch user: " + user)
#    client.switch_user(user, password)
#
#    print("Drop database: " + dbname)
#    client.drop_database(dbname)


def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port)
