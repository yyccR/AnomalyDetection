#!/usr/bin/python

import json
from flask import Flask, jsonify
from flask_restful import Api, reqparse, Resource
from api.postStreamData import post_stream_data
from api.postMultiStreamData import post_multi_stream_data

app = Flask(__name__)
api = Api(app)

# api.add_resource(get_HTM_parameters, "/api/HTM/v1.0/HTMParametes")
# api.add_resource(post_stream_parameters, "/api/HTM/v1.0/streamParameters")
# api.add_resource(post_stream_data, "/api/HTM/v1.0/anomalyDetection")


# initial the object of "post stream data".
ResourceForPostStreamData = []
for i in xrange(2): ResourceForPostStreamData.append(post_stream_data())
# initial the object of "multiple post stream data".
ResourceForMultiPostStreamData = []
for i in xrange(2): ResourceForMultiPostStreamData.append(post_multi_stream_data())


# allocating the resource for "post stream data".
@app.route("/api/HTM/v1.0/anomalyDetection/<int:model_id>", methods=['POST'])
def post(model_id):
    targetModel = ResourceForPostStreamData[model_id]
    result = targetModel.post()
    return result


# allocating the resource for "multiple post stream data".
@app.route("/api/HTM/v1.0/multiAnomalyDetection/<int:model_id>", methods=['POST'])
def postMulti(model_id):
    targetModel = ResourceForMultiPostStreamData[model_id]
    result = targetModel.post()
    return result


if __name__ == '__main__':
    app.run(debug=True)
