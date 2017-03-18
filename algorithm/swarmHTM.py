#! /usr/bin/python

import os
import pprint

from nupic.swarming import permutations_runner
from swarm_parameters.swarm_parameters_fieldX import fieldX


# write the swarm parameters into file.
def writeModelParams(modelParams, modelParamsName):
    outDir = os.path.join(os.getcwd(), "model_params")
    if not os.path.isdir(outDir):
        os.mkdir(outDir)
    outputName = "%s_model_params.py" % modelParamsName
    outPath = os.path.join(outDir, outputName)
    pp = pprint.PrettyPrinter(indent=2)
    with open(outPath, "wb") as outFile:
        modelParamsString = pp.pformat(modelParams)
        outFile.write("MODEL_PARAMS = \\\n%s" % modelParamsString)
    return outPath

# swarm training and get the parameters.
def swarm(inputFile):
    swarmWorkDir = os.path.abspath("swarmHTM")
    if not os.path.exists(swarmWorkDir):
        os.mkdir(swarmWorkDir),
    modelParams = permutations_runner.runWithConfig(
        fieldX,
        {"maxWorker": 4, "overwrite": True},
        outputLabel="output",
        outDir=swarmWorkDir,
        permWorkDir=swarmWorkDir
    )
    modelParamsName = os.path.splitext(inputFile)[0]
    writeModelParams(modelParams, modelParamsName)


if __name__ == "__main__":
    swarm("heartBeat.csv")
