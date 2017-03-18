#! /usr/bin/python

import json
import datetime
import numpy as np

from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.frameworks.opf.common_models.cluster_params import getScalarMetricWithTimeOfDayAnomalyParams


class multi_stream_anomaly_detect():
    """
    stream data anomaly detect for multiple fields.
    """

    def __init__(self, fields, predictStep, enablePredict, maxValue, minValue, minResolution):
        # # initial the parameters and data variables.
        self.fields = fields
        self.predictStep = predictStep
        self.enablePredict = enablePredict
        # metirc data for HTM parameters.
        self.metricData = {}
        for i in range(len(self.fields)):
            self.metricData[self.fields[i]] = xrange(
                int(minValue[i]), int(maxValue[i]), int((maxValue[i] - minValue[i]) / minResolution[i])
            )
        self.maxValue = maxValue
        self.minValue = minValue
        self.minResolution = minResolution
        self.timestamp = None
        self.actualValue = None
        self.predictValue = None
        self.anomalyScore = None
        self.parameters = None
        self.model = None
        self.models = {}
        self.modelResult = None
        self.output = {}

        # one HTM model for one field.
        for i in range(len(self.fields)):
            # get the model parameters.
            self.parameters = getScalarMetricWithTimeOfDayAnomalyParams(
                self.metricData[self.fields[i]],
                self.minValue[i],
                self.maxValue[i],
                self.minResolution[i]
            )
            # make sure the result contains the predictions.
            self.parameters["modelConfig"]["modelParams"]["clEnable"] = self.enablePredict
            # so we can modify the predict step by do that:
            self.parameters["modelConfig"]["modelParams"]["clParams"]["steps"] = self.predictStep
            # create the model
            self.model = ModelFactory.create(self.parameters["modelConfig"])
            self.model.enableInference(self.parameters["inferenceArgs"])
            self.models[self.fields[i]] = self.model

    def multiAnomalyDetect(self, inputData):
        # compute every field.
        for k in inputData.keys():
            # get the variables.
            self.timestamp = inputData[k]["timestamp"]
            self.actualValue = inputData[k]["actualValue"]

            # convert the timestamp/actualValue into proper type.
            # the string of input timestamp should be like this: 2017-2-18 0:00:00
            self.timestamp = datetime.datetime.strptime(self.timestamp, "%Y-%m-%d %H:%M:%S")
            self.actualValue = float(self.actualValue)
            # run the target model.
            self.modelResult = self.models[k].run({
                "c0": self.timestamp,
                "c1": self.actualValue
            })
            # get the target value.
            self.predictValue = self.modelResult.inferences["multiStepBestPredictions"][2]
            self.anomalyScore = float(self.modelResult.inferences["anomalyScore"])
            # output is a dict.
            self.output[k] = {
                "timestamp": datetime.datetime.strftime(self.timestamp, "%Y-%m-%d %H:%M:%S"),
                "actualValue": self.actualValue,
                "predictValue": self.predictValue,
                "anomalyScore": self.anomalyScore
            }

        return self.output
