from concurrent import futures
import logging

import tad
import grpc

import json
import pandas as pd
from io import StringIO

import anomaly_detection_pb2
import anomaly_detection_pb2_grpc

class TwitterAnomalyDetection(anomaly_detection_pb2_grpc.TwitterAnomalyDetectionServicer):

    def dparserfunc(self, date):
        return pd.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    def DetectAnomalies(self, request, context):
        raw_csv = StringIO(request.raw_json) 
        data1 = pd.read_csv(raw_csv, index_col='timestamp', parse_dates=True, squeeze=True, date_parser=self.dparserfunc) 
        result = tad.anomaly_detect_ts(data1, alpha=0.05, direction="both", plot=False, longterm=True)
        print(result["anoms"].to_list())
        return anomaly_detection_pb2.Response(entries=result["anoms"].to_list())

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    anomaly_detection_pb2_grpc.add_TwitterAnomalyDetectionServicer_to_server(TwitterAnomalyDetection(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
