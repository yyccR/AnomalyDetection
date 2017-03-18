#! /usr/bin/python

import csv
import os
import datetime

from nupic.frameworks.opf.modelfactory import ModelFactory
from model_params import heartBeat_model_params

# date time type.
# 2016-12-1 0:00:00
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def createModel():
    # create the model with the parameters that from the swarm training.
    model = ModelFactory.create(heartBeat_model_params.MODEL_PARAMS)
    model.enableInference({
        "predictedField": "a"
    })
    return model


def runModel(model):
    # input file:
    inputFilePath = os.path.join(os.getcwd(), "../test/data/heartBeat.csv")
    inputFile = open(inputFilePath, "r")
    csvReader = csv.reader(inputFile)
    csvReader.next()
    csvReader.next()
    csvReader.next()

    # output file:
    outputPath = os.path.join(os.getcwd(), "../test/data/heartBeatAnomalyDetect_output.csv")
    outputFile = open(outputPath, "w+")
    writeFile = csv.writer(outputFile)
    # columns name.
    columnsName = ["timestamp", "a", "prediction","anomalyScore"]
    writeFile.writerow(columnsName)

    count = 0
    for row in csvReader:
        count += 1
        if count % 100 == 0:
            print "Read %i lines..." % count
        # format the timestamp.
        timestamp = datetime.datetime.strptime(row[0], DATE_FORMAT)
        # get the target value: a.
        actualValue = float(row[1])
        # put the timestamp and the target value into the model.
        result = model.run({
            "timestamp": timestamp,
            "a": actualValue
        })
        prediction = result.inferences["multiStepBestPredictions"][1]
        anomalyScore = result.inferences["anomalyScore"]
        writeFile.writerow([timestamp, actualValue, prediction,anomalyScore])
        print "a value = %s prediction = %s anomalyScore = %s" % (str(actualValue), str(prediction),str(anomalyScore))
    inputFile.close()
    outputFile.close()


def runTest():
    model = createModel()
    runModel(model)


if __name__ == "__main__":
    runTest()
