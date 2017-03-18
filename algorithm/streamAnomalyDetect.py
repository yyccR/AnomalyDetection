#! /usr/bin/python

import json
import datetime
import numpy as np

from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.frameworks.opf.common_models.cluster_params import getScalarMetricWithTimeOfDayAnomalyParams


class stream_anomaly_detect():
    """
    stream data anomaly detect for one field.
    """

    def __init__(self, predictStep, enablePredict, maxValue, minValue, minResolution):
        # initial the parameters and data variables.
        self.predictStep = predictStep
        self.enablePredict = enablePredict
        self.metricData = xrange(int(minValue), int(maxValue), int((maxValue - minValue) / minResolution))
        self.maxValue = maxValue
        self.minValue = minValue
        self.minResolution = minResolution
        self.timestamp = None
        self.actualValue = None
        self.predictValue = None
        self.anomalyScore = None
        self.modelResult = None
        self.output = None

        # get the model parameters.
        self.parameters = getScalarMetricWithTimeOfDayAnomalyParams(
            self.metricData,
            self.minValue,
            self.maxValue,
            self.minResolution
        )
        # make sure the result contains the predictions.
        self.parameters["modelConfig"]["modelParams"]["clEnable"] = self.enablePredict
        # so we can modify the predict step by do that:
        self.parameters["modelConfig"]["modelParams"]["clParams"]["steps"] = self.predictStep
        # create the model
        self.model = ModelFactory.create(self.parameters["modelConfig"])
        self.model.enableInference(self.parameters["inferenceArgs"])

    def anomalyDetect(self, timestamp, actualValue):
        # anomaly detect method for one field.
        self.timestamp = timestamp
        self.actualValue = actualValue

        # convert the timestamp/actualValue into proper type.
        # the string of input timestamp should be like this: 2017-2-18 0:00:00
        self.timestamp = datetime.datetime.strptime(self.timestamp, "%Y-%m-%d %H:%M:%S")
        self.actualValue = float(self.actualValue)
        self.modelResult = self.model.run({
            "c0": self.timestamp,
            "c1": self.actualValue
        })
        self.predictValue = self.modelResult.inferences["multiStepBestPredictions"][2]
        self.anomalyScore = float(self.modelResult.inferences["anomalyScore"])
        self.output = {
            "timestamp": self.timestamp,
            "actualValue": self.actualValue,
            "predictValue": self.predictValue,
            "anomalyScore": self.anomalyScore
        }

        return self.output
