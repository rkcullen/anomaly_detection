
from __future__ import print_function
from datetime import datetime
import logging
import sys

import os
import pandas as pd
import grpc
import csv
import json

import anomaly_detection_pb2
import anomaly_detection_pb2_grpc


def run():
    
    anomaly_detection_host = os.getenv("ANOMALY_DETECTION_HOST", "localhost")
    with grpc.insecure_channel(f"{anomaly_detection_host}:50051") as channel:
        stub = anomaly_detection_pb2_grpc.TwitterAnomalyDetectionStub(channel)
        with open('test_data_1.csv', "r") as f:
            data1 = f.read() + "\n"
            result = stub.DetectAnomalies(anomaly_detection_pb2.Request(raw_json=data1, only_last="day"))
        for key in sorted (result.pairs):
            root.info(key + ": " + str(result.pairs[key]))

if __name__ == '__main__':
    logging.basicConfig(filename='output.log', level=logging.INFO)
    root = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    root.addHandler(handler)
    run()
