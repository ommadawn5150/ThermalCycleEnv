import os
from random import random
import time
from datetime import datetime, timezone
from influxdb import InfluxDBClient
import sys
import serial
import re
import numpy as np
import pandas as pd
import random

from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
def main():
    '''
    # influxdb
    host = os.environ.get('INFLUXDB_HOST', 'localhost')
    port = os.environ.get('INFLUXDB_PORT', 8086)
    dbuser = os.environ.get('INFLUXDB_DBUSER', 'user')
    dbuser_password = os.environ.get('INFLUXDB_DBUSER_PASS', 'user')
    dbname = os.environ.get('INFLUXDB_DBNAME', 'Test')
    client = InfluxDBClient(host, port, dbuser, dbuser_password, dbname)
    '''
    '''シリアル通信の設定'''
    #ser = serial.Serial('/dev/cu.usbserial-1440',9600,timeout=None)


    # You can generate an API token from the "API Tokens Tab" in the UI
    token = "8_iiU2FAiPfzq5JQfQfFHO1eW0YqMJKC06ZCr-i86jmh6Ohgd6lGiS8ixWsW-rT8VhmWP_YZTcYMaNeFO4I71A=="
    org = "jlab"
    bucket = "test"

    with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:

        write_api = client.write_api(write_options=SYNCHRONOUS)

        data = "mem,host=host1 used_percent=23.43234543"
        write_api.write(bucket, org, data)


    # bmp180

    while True:
	# データ収集

        try:
	# データ
            data = [
                {
                    "measurement": "Test",
                    "tags": {
                        "host": "host"
                        },
                        "time": datetime.now(timezone.utc).isoformat(),
                        "fields": {
                            "random1": int(random.random()*100),
                            "random2": int(random.random()*100),
                        }
                }
            ]
            print(data)
            time.sleep(3)
	    # 書き込み
            client.write_points(data)
        
        except KeyboardInterrupt:   # exceptに例外処理を書く
            print('stop!')
             
if __name__ == "__main__":
    main()
