#! /usr/bin/python
import os

# the path is the input file path.
path = os.path.join("file://../test/data/heartBeat.csv")

fieldX = {
    "includedFields": [
        {
            "fieldName": "timestamp",
            "fieldType": "datetime"
        },
        {
            "fieldName": "a",
            "fieldType": "float",
            "maxValue": 25000,
            "minValue": -16000
        }
    ],
    "streamDef": {
        "info": "heartBeat",
        "version": 1,
        "streams": [
            {
                "info": "heartBeat",
                "source": path,       # file path.
                "columns": [
                    "*"
                ]
            }
        ]
    },

    "inferenceType": "TemporalAnomaly",   # if "TemporalMultiStep": get the predict value without anomaly score.
    "inferenceArgs": {
        "predictionSteps": [
            1              # 1 predict step means the current predict value was adjusted by previous 1 value.
        ],
        "predictedField": "a"
    },
    "iterationCount": -1,  # if -1 then will compute all the columns.
    "swarmSize": "small"   # can be "small", "medium" and "big".
}
