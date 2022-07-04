import os
import time
from datetime import datetime, timezone
from influxdb import InfluxDBClient
import sys
import serial
import re
import numpy as np
import pandas as pd

def ArduinoRead(c,ser):
    ser.write((c + "\n").encode('utf-8'))
    #time.sleep(1)
    time.sleep(0.2)
    data = ser.readline().decode().strip().split(',')
    data = [float(item) for item in data]
    return(data)

def main():
    host = 'localhost'
    port = 8086
    dbuser = 'user'
    dbuser_password = 'user'
    dbname = 'ThermalCycle'
    client = InfluxDBClient(host, port, dbuser, dbuser_password, dbname)

    '''シリアル通信の設定'''
    ser = serial.Serial('/dev/cu.usbmodem14401',9600,timeout=None)

    # bmp180

    while True:
        try:
            temp = ArduinoRead('t',ser)
            t0 = float(temp[0]) #温度
            t1 = float(temp[1]) 
            t2 = float(temp[2]) 
            t3 = float(temp[3]) 
            t4 = float(temp[4]) 
            t5 = float(temp[5]) 
            t6 = float(temp[6]) 
            t7 = float(temp[7])
            print(temp)

            pressure = ArduinoRead('p',ser)
            p0 = float(pressure[0]) #温度
            p1 = float(pressure[1]) 
            p2 = float(pressure[2]) 
            p3 = float(pressure[3]) 
            p4 = float(pressure[4]) 
            p5 = float(pressure[5]) 
            p6 = float(pressure[6]) 
            p7 = float(pressure[7])
            print(pressure)
            
            sdata = [
                    {
                        "measurement": "ThermalCycle",
                        "tags": {
                            "host": "host"},
                            "time": datetime.now(timezone.utc).isoformat(),
                            "fields": {
                                "temperature 0 [degree]": float(t0),
                                "temperature 1 [degree]": float(t1),
                                "temperature 2 [degree]": float(t2),
                                "temperature 3 [degree]": float(t3),
                                "temperature 4 [degree]": float(t4),
                                "temperature 5 [degree]": float(t5),
                                "temperature 6 [degree]": float(t6),
                                "temperature 7 [degree]": float(t7),
                                "pressure 0 [Pa]": float(p0),
                                "pressure 1 [Pa]": float(p1),
                                "pressure 2 [Pa]": float(p2),
                                "pressure 3 [Pa]": float(p3),
                                "pressure 4 [Pa]": float(p4),
                                "pressure 5 [Pa]": float(p5),
                                "pressure 6 [Pa]": float(p6),
                                "pressure 7 [Pa]": float(p7),
                            }
                    }
                    ]
            client.write_points(sdata)
            time.sleep(1)

        except KeyboardInterrupt:
            print("Ctrl+Cで停止しました")
            break

            

if __name__ == "__main__":
    main()
