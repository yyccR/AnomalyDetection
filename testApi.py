#! /usr/bin/python

import csv
import os
import requests
import json
from datetime import datetime
from output.streamPlot import streamDetectionPlot
from output.multiStreamPlot import multiStreamDetectionPlot


def getData():
    # get the data.
    filePath = os.path.join(os.getcwd(), "test/data/heartBeat.csv")
    file = open(filePath)
    allData = csv.reader(file)
    # skip the first three lines.
    allData.next()
    allData.next()
    allData.next()
    inputData = [x for x in allData]
    return inputData


def convertData(dataList):
    transformedData = []
    # convert the data into json type.
    for line in dataList:
        transformedData.append(
            json.dumps(
                {"timestamp": line[0], "actualValue": line[1]}
            )
        )
    return transformedData


def convertMultiData(dataList):
    transformedData = []
    # convert the data into json type.
    for line in dataList:
        transformedData.append(
            json.dumps(
                {
                    "A": {"timestamp": line[0], "actualValue": line[1]},
                    "B": {"timestamp": line[0], "actualValue": line[2]},
                    "C": {"timestamp": line[0], "actualValue": line[3]}
                }
            )
        )
    return transformedData


def requestsHTMApi(streamData):
    # requests HTM api.
    inputData = {"streamData": streamData}
    url = "http://127.0.0.1:5000/api/HTM/v1.0/anomalyDetection/1"
    r = requests.post(url, inputData)
    return r.json()


def requestMultiHTMApi(streamData):
    inputData = {"streamData": streamData}
    url = "http://127.0.0.1:5000/api/HTM/v1.0/multiAnomalyDetection/1"
    r = requests.post(url, inputData)
    return r.json()


def run():
    # read the data from /output/data/heartBeat.csv, convert it into json type,
    # and initial the graph.
    data = convertData(getData())
    graph = streamDetectionPlot()
    graph.initPlot()
    for line in data:
        # requests the one field api.
        requestsData = requestsHTMApi(line)
        print requestsData
        # plot the data
        graph.anomalyDetectionPlot(
            requestsData["timestamp"],
            requestsData["actualValue"],
            requestsData["predictValue"],
            requestsData["anomalyScore"]
        )
    graph.close()


def runMulti():
    # read the data from /output/data/heartBeat.csv, convert it into json type,
    # and initial the graph.
    data = convertMultiData(getData())
    graph2 = multiStreamDetectionPlot()
    graph2.initPlot()
    for line in data:
        # requests the one field api.
        requestsData = requestMultiHTMApi(line)
        # print requestsData
        # print requestsData["A"]["timestamp"]
        # plot the data
        graph2.anomalyDetectionPlot(requestsData)
    graph2.close()


if __name__ == "__main__":
    run()
