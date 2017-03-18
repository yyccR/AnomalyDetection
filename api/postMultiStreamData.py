#! /usr/bin/python

import json
import numpy as np
from flask import jsonify
from flask.ext.restful import Resource, reqparse

from algorithm.multiStreamAnomalyDetect import multi_stream_anomaly_detect


class post_multi_stream_data(Resource):
    """
    post stream data for anomaly detection with multiple fields.
    """

    def __init__(self,
                 fields=["A", "B", "C"],
                 predictStep=2,
                 enablePredict=True,
                 maxValue=[25000, 33000, 33000],
                 minValue=[-16000, -33000, -33000],
                 minResolution=[0.5, 0.5, 0.5]):
        # initial the parametes and the target objects.
        self.timestamp = []
        self.actualValue = []
        self.anomalyScore = []
        self.predictValue = []
        self.output = []
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(name="streamData", type=str, required=False)
        self.detectObject = multi_stream_anomaly_detect(
            fields=fields,
            predictStep=predictStep,
            enablePredict=enablePredict,
            maxValue=maxValue,
            minValue=minValue,
            minResolution=minResolution
        )

    def post(self):
        # parse the stream data and convert it into proper type.
        args = self.parser.parse_args()["streamData"]
        inputData = json.loads(args)

        # compute the anomaly scores and predict values.
        self.output = self.detectObject.multiAnomalyDetect(inputData)

        return jsonify(self.output)
