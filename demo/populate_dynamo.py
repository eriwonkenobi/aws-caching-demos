#!/usr/bin/env python

from amazondax import AmazonDaxClient
from decimal import *

import boto3
import datetime
import json
import os
import random
import string
import time

NORTHERNMOST = 49.
SOUTHERNMOST = 25.
EASTERNMOST  = -66.
WESTERNMOST  = -124.
SENSORS      = 500
RECORDS      = 10000
T            = SENSORS*RECORDS
                    
store = boto3.resource('dynamodb', endpoint_url=os.environ['DYNAMODB_ENDPOINT'])
sensorLocation = store.Table(os.environ['SENSORLOCATION_TABLE'])
sensorData = store.Table(os.environ['SENSORDATA_TABLE'])

item = sensorLocation.get_item(
  Key={
    'sensorName': 'sensor' + str(SENSORS-1)
  }
)

def _gen_lat_lng():
    lat = round(random.uniform(SOUTHERNMOST, NORTHERNMOST), 6)
    lng = round(random.uniform(EASTERNMOST, WESTERNMOST), 6)
    return(lat,lng)


print('Checking DynamoDB')
if 'Item' not in item:
    print('Populating DynamoDB Table with ' + str(T), ' records, this could take a while')

    dt = datetime.datetime(2016, 2, 25, 23, 23)
    startTime=(round(time.mktime(dt.timetuple())))
    
    for i in range(1, SENSORS):
        sensor = 'sensor' + str(i)
        print(sensor)
        lat,lon = _gen_lat_lng()
        sensorLocation.put_item(
            Item={
                'sensorName': sensor,
                'lat': str(lat),
                'long': str(lon)
            }
        )
        with sensorData.batch_writer() as batchData:
            for p in range(0, RECORDS):
                T-=1
                if 'DYNAMODB_ENDPOINT' in os.environ:
                    print(T)
                startTime += 10
                item = {'sensorName': sensor, 'timestamp': startTime, 'datapoint': random.randint(20,90)}
                batchData.put_item(Item=item)
else:
    print("DynamoDB Table Already Populated with test data")
