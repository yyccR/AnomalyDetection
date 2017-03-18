#! /usr/bin/python

import json
import numpy as np
from flask import jsonify
from flask.ext.restful import Resource, reqparse
from algorithm.streamAnomalyDetect import stream_anomaly_detect


class post_stream_data(Resource):
    """
    post stream data for anomaly detection with one field.
    """

    def __init__(self,
                 predictStep=2,
                 enablePredict=True,
                 maxValue=4200.0,
                 minValue=-4200.0,
                 minResolution=0.1
                 ):
        # initial the parameters and the target object.
        self.dataName = None
        self.timestamp = None
        self.actualValue = None
        self.predictValue = None
        self.anomalyScore = None
        self.output = []
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("streamData", type=str)
        self.detectObject = stream_anomaly_detect(
            predictStep=predictStep,
            enablePredict=enablePredict,
            maxValue=maxValue,
            minValue=minValue,
            minResolution=minResolution
        )

    def post(self):
        # parser the input data.
        args = self.parser.parse_args()["streamData"]
        # convert the json into proper type.
        inputData = json.loads(args)
        # get the target data.
        self.timestamp = inputData["timestamp"]
        self.actualValue = inputData["actualValue"]
        # compute the anomaly score and predict value.
        self.output = self.detectObject.anomalyDetect(self.timestamp, self.actualValue)
        self.predictValue = self.output["predictValue"]
        self.anomalyScore = self.output["anomalyScore"]

        return jsonify(
            timestamp=self.timestamp,
            actualValue=self.actualValue,
            predictValue=self.predictValue,
            anomalyScore=self.anomalyScore
        )
