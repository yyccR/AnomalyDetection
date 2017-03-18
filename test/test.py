#!flask/bin/python



































# # ! /usr/bin/python
#
# import json
# import datetime
# import numpy as np
# from flask import jsonify
#
# from nupic.frameworks.opf.modelfactory import ModelFactory
# from nupic.frameworks.opf.common_models.cluster_params import getScalarMetricWithTimeOfDayAnomalyParams
#
#
# class stream_anomaly_detect():
#     """
#     stream data anomaly detect for one field.
#     """
#
#     def __init__(self, predictStep=2, enablePredict=True, maxValue=100.0, minValue=-100.0, minResolution=0.1):
#         # initial the parameters and data variables.
#         self.predictStep = predictStep
#         self.enablePredict = enablePredict
#         self.metricData = np.arange(-1000, 1000, 0.001)
#         self.maxValue = maxValue
#         self.minValue = minValue
#         self.minResolution = minResolution
#         self.timestamp = None
#         self.actualValue = None
#         self.predictValue = None
#         self.anomalyScore = None
#         self.modelResult = None
#         self.output = None
#
#         # get the model parameters.
#         self.parameters = getScalarMetricWithTimeOfDayAnomalyParams(self.metricData)
#         # make sure the result contains the predictions.
#         self.parameters["modelConfig"]["modelParams"]["clEnable"] = self.enablePredict
#         # so we can modify the predict step by do that:
#         self.parameters["modelConfig"]["modelParams"]["clParams"]["steps"] = self.predictStep
#         # create the model
#         self.model = ModelFactory.create(self.parameters["modelConfig"])
#         self.model.enableInference(self.parameters["inferenceArgs"])
#
#     def anomalyDetect(self, timestamp, actualValue):
#         # anomaly detect method for one field.
#         self.timestamp = timestamp
#         self.actualValue = actualValue
#
#         # convert the timestamp/actualValue into proper type.
#         # the string of input timestamp should be like this: 2017-2-18 0:00:00
#         self.timestamp = datetime.datetime.strptime(self.timestamp, "%Y-%m-%d %H:%M:%S")
#         self.actualValue = float(self.actualValue)
#         self.modelResult = self.model.run({
#             "c0": self.timestamp,
#             "c1": self.actualValue
#         })
#         self.predictValue = self.modelResult.inferences["multiStepBestPredictions"][2]
#         self.anomalyScore = self.modelResult.inferences["anomalyScore"]
#         self.output = {"timestamp": self.timestamp,
#                        "actualValue": self.actualValue,
#                        "predictValue": self.predictValue,
#                        "anomalyScore": self.anomalyScore}
#
#         return self.output
#
#
# a = stream_anomaly_detect()
# result = a.anomalyDetect("2016-12-1 0:00:00", 3845)
# p = result["predictValue"]
# s = result["anomalyScore"]
#
# print p,type(p), s, type(s)
# # print jsonify({"p":p,"s":s})



















# from flask import Flask, jsonify
# from flask.ext.restful import Api, Resource, reqparse, request
# import json
#
# app = Flask(__name__)
# api = Api(app)
#
#
# class get_parameters(Resource):
#     def __init__(self):
#         self.a = "test 200"
#
#     def get(self):
#         return jsonify({"m": self.a})
#
#
# class post_stream_data(Resource):
#     def __init__(self):
#         self.timestamp = []
#         self.actualValue = []
#         self.predictValue = []
#         self.anomalyScore = []
#         self.parser = reqparse.RequestParser()
#         self.parser.add_argument("streamData", type=str)
#
#     def post(self):
#         args = self.parser.parse_args()["streamData"]
#         inputData = json.loads(args)
#         self.timestamp = inputData["timestamp"]
#         self.actualValue = inputData["actualValue"]
#         self.predictValue = inputData["predictValue"]
#         self.anomalyScore = inputData["anomalyScore"]
#         return jsonify({"timestamp": self.timestamp,
#                         "actualValue": self.actualValue,
#                         "predictValue": self.predictValue,
#                         "anomalyScore": self.anomalyScore
#                         })
#
#
# api.add_resource(get_parameters, "/")
# api.add_resource(post_stream_data, "/stream")
#
# if __name__ == "__main__":
#     app.run(debug=True)






# app = Flask(__name__)
#
# tasks = [
#     {
#         'id': 1,
#         'title': u'Buy groceries',
#         'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
#         'done': False
#     },
#     {
#         'id': 2,
#         'title': u'Learn Python',
#         'description': u'Need to find a good Python tutorial on the web',
#         'done': False
#     }
# ]
#
#
# auth = HTTPBasicAuth()
#
# @auth.get_password
# def get_password(username):
#     if username == 'miguel':
#         return 'python'
#     return None
#
# @auth.error_handler
# def unauthorized():
#     return make_response(jsonify({'error': 'Unauthorized access'}), 401)
#
#
# def make_public_task(task):
#     new_task = {}
#     for field in task:
#         if field == 'id':
#             new_task['uri'] = url_for('get_tasks', task_id=task['id'], _external=True)
#         else:
#             new_task[field] = task[field]
#     return new_task
#
#
# @app.route('/todo/api/v1.0/tasks', methods=['GET'])
# @auth.login_required
# def get_tasks():
#     # task = filter(lambda t: t["id"] == tasks_id, tasks)
#     # if len(task) == 0:
#     #     abort(404)
#     return jsonify({'tasks': map(make_public_task, tasks)})
#
#
# @app.route('/todo/api/v1.0/tasks', methods=['POST'])
# def create_task():
#     if not request.json or not 'title' in request.json:
#         abort(400)
#     task = {
#         'id': tasks[-1]['id'] + 1,
#         'title': request.json['title'],
#         'description': request.json.get('description', ""),
#         'done': False
#     }
#     tasks.append(task)
#     return jsonify({'task': task}), 201
#
#
# @app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
# def update_task(task_id):
#     task = filter(lambda t: t['id'] == task_id, tasks)
#     if len(task) == 0:
#         abort(404)
#     if not request.json:
#         abort(400)
#     if 'title' in request.json and type(request.json['title']) != unicode:
#         abort(400)
#     if 'description' in request.json and type(request.json['description']) is not unicode:
#         abort(400)
#     if 'done' in request.json and type(request.json['done']) is not bool:
#         abort(400)
#     task[0]['title'] = request.json.get('title', task[0]['title'])
#     task[0]['description'] = request.json.get('description', task[0]['description'])
#     task[0]['done'] = request.json.get('done', task[0]['done'])
#     return jsonify({'task': task[0]})
#
#
# @app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
# def delete_task(task_id):
#     task = filter(lambda t: t['id'] == task_id, tasks)
#     if len(task) == 0:
#         abort(404)
#     tasks.remove(task[0])
#     return jsonify({'result': True})
#
#
# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
