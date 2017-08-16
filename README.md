一、项目简介

本项目为基于numenta开源的智能计算框架nupic所写的异常检测restful api, 运行环境为Linux.

---
(一)、库安装


```python
pip install matlibplot
pip install flask
pip install flask_restful
pip install jsonify
pip install nupic
```

最后一个HTM的框架nupic, 详细版本的安装可以参加另外的《HTM算法》文档, 这里pip install nupic就可以在python上运行.

---
(二)、结构说明


- package类型：

在HTM项目下，有algorithm, api, dao, output, test 共4个package, 主要是algorithm和api两个package, algorithm是HTM算法的文件, api则是该项目的api文件, output里是api调用时的可视化输出, test里面是测试例子(单维度和多维度，包含测试数据, 在test/data路径下), dao待补充，具体为将数据输出到postgresql/mysql.

algorithm/实现了单维度(streamAnomalyDetect)和多维度(multiStreamAnomalyDetect)数据输入两种类型. 
还有swarm, run两个文件, 其中swarm是训练得到模型参数，耗时比较长，run则是运行swarm得到的参数.
此外，swarm_parameters里的文件是swarm的输入参数，model_parameters里的文件是swarm的输出参数，作为run方法的输入.
algorithm里建议使用 streamAnomalyDetect/multiStreamAnomalyDetect 这两种调用方式, swarm/run这种不推荐, 因为 swarm/run 需要先定义swarm_parameters作为swarm的输入, 其输出的model_parameters是run的输入, run的输出即为我们想要的结果, swarm步耗时过长, 且调用复杂, 所以这一方法没有写成api.

 api/实现了单维度(postStreamData)和多维度(postMultiStreamData)两种方法的post,具体post数据格式见下面例子.

---
- clone及测试

```python
git clone https://github.com/yyccR/AnomalyDetection.git
```


```python
cd clone的文件目录
python main.py
python testApi.py
```

在clone的相应目录下, 执行main.py文件, 启动api服务, 另外开窗口在同样的目录下执行testApi.py文件, 可以看到从本地读取文件, 逐条post到服务端, 请求得到结果, 输出到当前的可视化界面, 更详细的调用见下面的api调用.


---
二、api调用

(一)、curl examples

one field:

```python
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/anomalyDetection/1 -d streamData='{"timestamp":"2016-12-1 0:00:10","actualValue":3855.0}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/anomalyDetection/1 -d streamData='{"timestamp":"2016-12-1 0:00:20","actualValue":3865.0}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/anomalyDetection/2 -d streamData='{"timestamp":"2016-12-1 0:00:30","actualValue":3875.0}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/anomalyDetection/2 -d streamData='{"timestamp":"2016-12-1 0:00:40","actualValue":3885.0}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/anomalyDetection/2 -d streamData='{"timestamp":"2016-12-1 0:00:40","actualValue":3895.0}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/anomalyDetection/2 -d streamData='{"timestamp":"2016-12-1 0:00:50","actualValue":3995.0}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/anomalyDetection/3 -d streamData='{"timestamp":"2016-12-1 0:01:10","actualValue":3205.0}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/anomalyDetection/4 -d streamData='{"timestamp":"2016-12-1 0:01:20","actualValue":3325.0}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/anomalyDetection/5 -d streamData='{"timestamp":"2016-12-1 0:01:30","actualValue":3425.0}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/anomalyDetection/6 -d streamData='{"timestamp":"2016-12-1 0:01:40","actualValue":3435.0}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/anomalyDetection/7 -d streamData='{"timestamp":"2016-12-1 0:02:50","actualValue":3425.0}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/anomalyDetection/7 -d streamData='{"timestamp":"2016-12-1 0:03:50","actualValue":3325.0}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/anomalyDetection/7 -d streamData='{"timestamp":"2016-12-1 0:04:50","actualValue":3535.0}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/anomalyDetection/7 -d streamData='{"timestamp":"2016-12-1 0:05:50","actualValue":3645.0}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/anomalyDetection/7 -d streamData='{"timestamp":"2016-12-1 0:06:50","actualValue":3755.0}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/anomalyDetection/7 -d streamData='{"timestamp":"2016-12-1 0:07:50","actualValue":3915.0}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/anomalyDetection/7 -d streamData='{"timestamp":"2016-12-1 0:08:50","actualValue":4565.0}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/anomalyDetection/7 -d streamData='{"timestamp":"2016-12-1 0:09:50","actualValue":43265.0}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/anomalyDetection/7 -d streamData='{"timestamp":"2016-12-1 0:10:50","actualValue":3565.0}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/anomalyDetection/8 -d streamData='{"timestamp":"2016-12-1 0:11:10","actualValue":35465.0}' -X POST
```
result:
```python
[root@nupic ~]# curl -i  http://127.0.0.1:5000/api/HTM/v1.0/anomalyDetection/1 -d streamData='{"timestamp":"2016-12-1 0:00:20","actualValue":3865.0}' -X POST
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 112
Server: Werkzeug/0.11.15 Python/2.7.5
Date: Tue, 21 Feb 2017 08:23:05 GMT

{
  "actualValue": 3865.0,
  "anomalyScore": 1.0,
  "predictValue": 3865.0,
  "timestamp": "2016-12-1 0:00:20"
}
```

multiple fields:

```python
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/multiAnomalyDetection/1 -d streamData='{"A":{"timestamp":"2016-12-1 0:00:10","actualValue":3855.0},"B":{"timestamp":"2016-12-1 0:00:10","actualValue":3855.0},"C":{"timestamp":"2016-12-1 0:00:10","actualValue":3855.0}}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/multiAnomalyDetection/1 -d streamData='{"A":{"timestamp":"2016-12-1 0:00:20","actualValue":3821.0},"B":{"timestamp":"2016-12-1 0:00:20","actualValue":3855.0},"C":{"timestamp":"2016-12-1 0:00:20","actualValue":3325.0}}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/multiAnomalyDetection/1 -d streamData='{"A":{"timestamp":"2016-12-1 0:00:30","actualValue":3425.0},"B":{"timestamp":"2016-12-1 0:00:30","actualValue":3855.0},"C":{"timestamp":"2016-12-1 0:00:30","actualValue":3425.0}}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/multiAnomalyDetection/1 -d streamData='{"A":{"timestamp":"2016-12-1 0:00:40","actualValue":3525.0},"B":{"timestamp":"2016-12-1 0:00:40","actualValue":3855.0},"C":{"timestamp":"2016-12-1 0:00:40","actualValue":3455.0}}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/multiAnomalyDetection/1 -d streamData='{"A":{"timestamp":"2016-12-1 0:00:50","actualValue":3635.0},"B":{"timestamp":"2016-12-1 0:00:50","actualValue":3855.0},"C":{"timestamp":"2016-12-1 0:00:50","actualValue":3435.0}}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/multiAnomalyDetection/1 -d streamData='{"A":{"timestamp":"2016-12-1 0:01:10","actualValue":4265.0},"B":{"timestamp":"2016-12-1 0:01:10","actualValue":3855.0},"C":{"timestamp":"2016-12-1 0:01:10","actualValue":3545.0}}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/multiAnomalyDetection/1 -d streamData='{"A":{"timestamp":"2016-12-1 0:01:20","actualValue":6375.0},"B":{"timestamp":"2016-12-1 0:01:20","actualValue":3855.0},"C":{"timestamp":"2016-12-1 0:01:20","actualValue":3655.0}}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/multiAnomalyDetection/1 -d streamData='{"A":{"timestamp":"2016-12-1 0:01:30","actualValue":6355.0},"B":{"timestamp":"2016-12-1 0:01:30","actualValue":3855.0},"C":{"timestamp":"2016-12-1 0:01:30","actualValue":7665.0}}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/multiAnomalyDetection/1 -d streamData='{"A":{"timestamp":"2016-12-1 0:01:40","actualValue":7575.0},"B":{"timestamp":"2016-12-1 0:01:40","actualValue":3855.0},"C":{"timestamp":"2016-12-1 0:01:40","actualValue":5255.0}}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/multiAnomalyDetection/1 -d streamData='{"A":{"timestamp":"2016-12-1 0:01:50","actualValue":7375.0},"B":{"timestamp":"2016-12-1 0:01:50","actualValue":3855.0},"C":{"timestamp":"2016-12-1 0:01:50","actualValue":6365.0}}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/multiAnomalyDetection/1 -d streamData='{"A":{"timestamp":"2016-12-1 0:02:10","actualValue":8585.0},"B":{"timestamp":"2016-12-1 0:02:10","actualValue":3855.0},"C":{"timestamp":"2016-12-1 0:02:10","actualValue":6475.0}}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/multiAnomalyDetection/1 -d streamData='{"A":{"timestamp":"2016-12-1 0:02:20","actualValue":8595.0},"B":{"timestamp":"2016-12-1 0:02:20","actualValue":3855.0},"C":{"timestamp":"2016-12-1 0:02:20","actualValue":7485.0}}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/multiAnomalyDetection/1 -d streamData='{"A":{"timestamp":"2016-12-1 0:02:30","actualValue":3855.0},"B":{"timestamp":"2016-12-1 0:02:30","actualValue":3855.0},"C":{"timestamp":"2016-12-1 0:02:30","actualValue":5245.0}}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/multiAnomalyDetection/1 -d streamData='{"A":{"timestamp":"2016-12-1 0:02:40","actualValue":3965.0},"B":{"timestamp":"2016-12-1 0:02:40","actualValue":3855.0},"C":{"timestamp":"2016-12-1 0:02:40","actualValue":7475.0}}' -X POST
curl -i  http://127.0.0.1:5000/api/HTM/v1.0/multiAnomalyDetection/1 -d streamData='{"A":{"timestamp":"2016-12-1 0:02:50","actualValue":9795.0},"B":{"timestamp":"2016-12-1 0:02:50","actualValue":3855.0},"C":{"timestamp":"2016-12-1 0:02:50","actualValue":8855.0}}' -X POST

```
result:
```python
[root@nupic ~]# curl -i  http://127.0.0.1:5000/api/HTM/v1.0/multiAnomalyDetection/1 -d streamData='{"A":{"timestamp":"2016-12-1 0:02:50","actualValue":9795.0}"B":{"timestamp":"2016-12-1 0:02:50","actualValue":3855.0},"C":{"timestamp":"2016-12-1 0:02:50","actualValue":8855.0}}' -X POST
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 435
Server: Werkzeug/0.11.15 Python/2.7.5
Date: Fri, 24 Feb 2017 05:39:33 GMT

{
  "A": {
    "actualValue": 9795.0,
    "anomalyScore": 0.44999998807907104,
    "predictValue": 3883.002,
    "timestamp": "2016-12-01 00:02:50"
  },
  "B": {
    "actualValue": 3855.0,
    "anomalyScore": 0.0,
    "predictValue": 3855.0,
    "timestamp": "2016-12-01 00:02:50"
  },
  "C": {
    "actualValue": 8855.0,
    "anomalyScore": 0.32499998807907104,
    "predictValue": 7482.0,
    "timestamp": "2016-12-01 00:02:50"
  }
}
```

(二)、request examples

one field:

```python
streamData = json.dumps({"timestamp": "2017-2-18 0:00:00", "actualValue": 1000.0})
inputData = {"streamData": streamData}
url = "http://127.0.0.1:5000/api/HTM/v1.0/anomalyDetection/1"
r = requests.post(url, inputData)
```
result:
```python
>>> import csv
>>> import os
>>> import requests
>>> import json
>>> streamData = json.dumps({"timestamp": "2017-2-18 0:00:00", "actualValue": 1000.0})
>>> inputData = {"streamData": streamData} 
>>> url = "http://127.0.0.1:5000/api/HTM/v1.0/anomalyDetection/1"
>>> r = requests.post(url, inputData)
>>> json.loads(r.text)
{u'timestamp': u'2017-2-18 0:00:00', u'predictValue': 1000.0, u'actualValue': 1000.0, u'anomalyScore': 1.0}
```

multiple fields:
```python
streamData = json.dumps(
                {
                    "A": {"timestamp": "2017-2-18 0:00:00", "actualValue": 1000.0},
                    "B": {"timestamp": "2017-2-18 0:00:00", "actualValue": 2000.0},
                    "C": {"timestamp": "2017-2-18 0:00:00", "actualValue": 3000.0}
                }
            )
inputData = {"streamData": streamData}
url = "http://127.0.0.1:5000/api/HTM/v1.0/multiAnomalyDetection/1"
r = requests.post(url, inputData)
```
result:
```python
>>> import csv
>>> import os
>>> import requests
>>> import json
>>> streamData = json.dumps(
...                 {
...                     "A": {"timestamp": "2017-2-18 0:00:00", "actualValue": 1000.0},
...                     "B": {"timestamp": "2017-2-18 0:00:00", "actualValue": 2000.0},
...                     "C": {"timestamp": "2017-2-18 0:00:00", "actualValue": 3000.0}
...                 }
...             )
>>> inputData = {"streamData": streamData}
>>> url = "http://127.0.0.1:5000/api/HTM/v1.0/multiAnomalyDetection/1"
>>> r = requests.post(url, inputData)
>>> json.loads(r.text)
{
u'A': {u'timestamp': u'2017-02-18 00:00:00', u'predictValue': 1000.0, u'actualValue': 1000.0, u'anomalyScore': 1.0}, 
u'C': {u'timestamp': u'2017-02-18 00:00:00', u'predictValue': 3000.0, u'actualValue': 3000.0, u'anomalyScore': 1.0}, 
u'B': {u'timestamp': u'2017-02-18 00:00:00', u'predictValue': 2000.0, u'actualValue': 2000.0, u'anomalyScore': 1.0}
}

```

