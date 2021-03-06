from app.connections import _dynamodb_connect
from app.elasticache import _elasticache_flush
from app.functions import _percentage_change
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime
from flask import Response, request

import json
import os
import pprint
import sys


def _ddb_query():
    ddb, dax = _dynamodb_connect()
    content  = request.json
    SLT      = os.environ['SENSORLOCATION_TABLE']
    SDT      = os.environ['SENSORDATA_TABLE']

    if content['Query'] == 'locations':
        ddb_loc_table = ddb.Table(SLT)
        dax_loc_table = dax.Table(SLT)

        # Run DynamoDB table scan
        ddb_start = datetime.now()
        ddb_locations = ddb_loc_table.scan()

        for ddbl in ddb_locations['Items']:
            next
        ddb_stop = datetime.now()
        ddb_diff = (ddb_stop-ddb_start).total_seconds()

        # Run DAX table scan
        dax_start = datetime.now()
        dax_locations = dax_loc_table.scan()
        for daxl in dax_locations:
            next
        dax_stop = datetime.now()
        dax_diff = (dax_stop-dax_start).total_seconds()

        diff = _percentage_change(ddb_diff,dax_diff)
        payload = json.dumps({"DAX Time": str(dax_diff),
                              "DynamoDB Time": str(ddb_diff),
                              "Measurement": "Seconds",
                              "Percentage Change": diff},
                              indent=1)

        return payload

    elif content['Query'].startswith('sensor'):
        ddb_data_table = ddb.Table(SDT)
        dax_data_table = dax.Table(SDT)

        # Run DynamoDB query
        ddb_start = datetime.now()
        ddb_data = ddb_data_table.query(
            KeyConditionExpression=Key('sensorName').eq(content['Query']),
            ScanIndexForward=True
        )
        ddbcount=0
        for ddbd in ddb_data['Items']:
            ddbcount+=1
        ddb_stop = datetime.now()
        ddb_diff = (ddb_stop-ddb_start).total_seconds()

        # Run DAX query
        dax_start = datetime.now()
        dax_data = dax_data_table.query(
            KeyConditionExpression=Key('sensorName').eq(content['Query']),
            ScanIndexForward=True
        )
        daxcount=0
        for dax in dax_data['Items']:
            daxcount+=1
        dax_stop = datetime.now()
        dax_diff = (dax_stop-dax_start).total_seconds()

        diff = _percentage_change(ddb_diff,dax_diff)
        payload = json.dumps({"DynamoDB Time": str(ddb_diff),
                              "DynamoDB Items" : str(ddbcount),
                              "DAX Time": str(dax_diff),
                              "DAX Items" : str(daxcount),
                              "Measurement": "Seconds",
                              "Percentage Increase": diff},
                              indent=1)

        return payload