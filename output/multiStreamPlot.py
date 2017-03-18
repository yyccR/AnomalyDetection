#! /usr/bin/python

import os
import csv
import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateFormatter
import matplotlib.ticker as ticker


class multiStreamDetectionPlot(object):
    """
    Anomaly plot output.
    """

    # initial the figure parameters.
    def __init__(self):
        # Turn matplotlib interactive mode on.
        plt.ion()
        # initial the plot variable.
        self.timestamp = []
        self.actualValueA = []
        self.actualValueB = []
        self.actualValueC = []
        self.predictValueA = []
        self.predictValueB = []
        self.predictValueC = []
        self.anomalyScoreA = []
        self.anomalyScoreB = []
        self.anomalyScoreC = []
        # self.tableValue = [[0, 0, 0, 0]]
        self.highlightList = []
        self.highlightListTurnOn = True
        self.anomalyScoreRange = [0, 1]
        self.actualValueRange = [0, 1]
        self.predictValueRange = [0, 1]
        self.timestampRange = [0, 1]
        self.anomalyScatterX = []
        self.anomalyScatterY = []

        # initial the figure.
        global fig
        fig = plt.figure(figsize=(18, 8), facecolor="white")
        fig.subplots_adjust(left=0.06, right=0.95, bottom=0.06, top=0.95, hspace=0.3)
        self.actualPredictValueGraph = fig.add_subplot(2, 1, 1)
        self.anomalyScoreGraph = fig.add_subplot(2, 1, 2)
        # self.anomalyValueTable = fig.add_axes([0.8, 0.1, 0.2, 0.8], frameon=False)

    # define the initial plot method.
    def initPlot(self):
        # initial six lines of the actualPredcitValueGraph.
        self.actualLineA, = self.actualPredictValueGraph.plot_date(self.timestamp, self.actualValueA, fmt="--",
                                                                   color="red", label="actual value A")
        self.predictLineA, = self.actualPredictValueGraph.plot_date(self.timestamp, self.predictValueA, fmt="-",
                                                                    color="red", label="predict value A")
        self.actualLineB, = self.actualPredictValueGraph.plot_date(self.timestamp, self.actualValueB, fmt="--",
                                                                   color="blue", label="actual value B")
        self.predictLineB, = self.actualPredictValueGraph.plot_date(self.timestamp, self.predictValueB, fmt="-",
                                                                    color="blue", label="predict value B")
        self.actualLineC, = self.actualPredictValueGraph.plot_date(self.timestamp, self.actualValueC, fmt="--",
                                                                   color="green", label="actual value C")
        self.predictLineC, = self.actualPredictValueGraph.plot_date(self.timestamp, self.predictValueC, fmt="-",
                                                                    color="green", label="predict value C")
        self.actualPredictValueGraph.legend(loc="upper right", frameon=False)
        self.actualPredictValueGraph.grid(True)

        # initial two lines of the anomalyScoreGraph.
        self.anomalyScoreLineA, = self.anomalyScoreGraph.plot_date(self.timestamp, self.anomalyScoreA, fmt="-",
                                                                   color="red", label="anomaly score A")
        self.anomalyScoreLineB, = self.anomalyScoreGraph.plot_date(self.timestamp, self.anomalyScoreB, fmt="-",
                                                                   color="blue", label="anomaly score B")
        self.anomalyScoreLineC, = self.anomalyScoreGraph.plot_date(self.timestamp, self.anomalyScoreC, fmt="-",
                                                                   color="green", label="anomaly score C")
        self.anomalyScoreGraph.legend(loc="upper right", frameon=False)
        self.baseline = self.anomalyScoreGraph.axhline(0.8, color='black', lw=2)

        # set the x/y label of the first two graph.
        self.anomalyScoreGraph.set_xlabel("datetime")
        self.anomalyScoreGraph.set_ylabel("anomaly score")
        self.actualPredictValueGraph.set_ylabel("value")

        # configure the anomaly value table.
        # self.anomalyValueTableColumnsName = ["timestamp", "actual value", "expect value", "anomaly score"]
        # self.anomalyValueTable.text(0.05, 0.99, "Anomaly Value Table", size=12)
        # self.anomalyValueTable.set_xticks([])
        # self.anomalyValueTable.set_yticks([])

        # axis format.
        self.dateFormat = DateFormatter("%m/%d %H:%M")
        self.actualPredictValueGraph.xaxis.set_major_formatter(ticker.FuncFormatter(self.dateFormat))
        self.anomalyScoreGraph.xaxis.set_major_formatter(ticker.FuncFormatter(self.dateFormat))

    # define the output method. timestamp, actualValue, predictValue, anomalyScore
    def anomalyDetectionPlot(self, inputData):

        # update the plot value of the graph.
        self.timestamp.append(datetime.datetime.strptime(inputData["A"]["timestamp"], "%Y-%m-%d %H:%M:%S"))
        self.actualValueA.append(float(inputData["A"]["actualValue"]))
        self.predictValueA.append(float(inputData["A"]["predictValue"]))
        self.anomalyScoreA.append(float(inputData["A"]["anomalyScore"]))
        self.actualValueB.append(float(inputData["B"]["actualValue"]))
        self.predictValueB.append(float(inputData["B"]["predictValue"]))
        self.anomalyScoreB.append(float(inputData["B"]["anomalyScore"]))
        self.actualValueC.append(float(inputData["C"]["actualValue"]))
        self.predictValueC.append(float(inputData["C"]["predictValue"]))
        self.anomalyScoreC.append(float(inputData["C"]["anomalyScore"]))

        # update the x/y range.
        self.timestampRange = [min(self.timestamp), max(self.timestamp) + datetime.timedelta(minutes=10)]
        self.actualValueRange = [min(self.actualValueB), max(self.actualValueB) + 1]
        self.predictValueRange = [min(self.predictValueB), max(self.predictValueB) + 1]

        # update the x/y axis limits
        self.actualPredictValueGraph.set_ylim(
            min(self.actualValueRange[0], self.predictValueRange[0]),
            max(self.actualValueRange[1], self.predictValueRange[1])
        )
        self.actualPredictValueGraph.set_xlim(
            self.timestampRange[1] - datetime.timedelta(days=1),
            self.timestampRange[1]
        )
        self.anomalyScoreGraph.set_xlim(
            self.timestampRange[1] - datetime.timedelta(days=1),
            self.timestampRange[1]
        )
        self.anomalyScoreGraph.set_ylim(
            self.anomalyScoreRange[0],
            self.anomalyScoreRange[1]
        )

        # update the two lines of the actualPredictValueGraph.
        self.actualLineA.set_xdata(self.timestamp)
        self.actualLineA.set_ydata(self.actualValueA)
        self.predictLineA.set_xdata(self.timestamp)
        self.predictLineA.set_ydata(self.predictValueA)
        self.actualLineB.set_xdata(self.timestamp)
        self.actualLineB.set_ydata(self.actualValueB)
        self.predictLineB.set_xdata(self.timestamp)
        self.predictLineB.set_ydata(self.predictValueB)
        self.actualLineC.set_xdata(self.timestamp)
        self.actualLineC.set_ydata(self.actualValueC)
        self.predictLineC.set_xdata(self.timestamp)
        self.predictLineC.set_ydata(self.predictValueC)

        # update the line of the anomalyScoreGraph.
        self.anomalyScoreLineA.set_xdata(self.timestamp)
        self.anomalyScoreLineA.set_ydata(self.anomalyScoreA)
        self.anomalyScoreLineB.set_xdata(self.timestamp)
        self.anomalyScoreLineB.set_ydata(self.anomalyScoreB)
        self.anomalyScoreLineC.set_xdata(self.timestamp)
        self.anomalyScoreLineC.set_ydata(self.anomalyScoreC)

        # update the scatter.
        if float(inputData["A"]["anomalyScore"]) >= 0.8 and float(inputData["B"]["anomalyScore"]) >= 0.8 and float(
                inputData["C"]["anomalyScore"]) >= 0.8:
            self.anomalyScatterX.append(datetime.datetime.strptime(inputData["A"]["timestamp"], "%Y-%m-%d %H:%M:%S"))
            self.anomalyScatterY.append(float(inputData["A"]["actualValue"]))
            self.anomalyScatterX.append(datetime.datetime.strptime(inputData["B"]["timestamp"],"%Y-%m-%d %H:%M:%S"))
            self.anomalyScatterY.append(float(inputData["B"]["actualValue"]))
            self.anomalyScatterX.append(datetime.datetime.strptime(inputData["C"]["timestamp"],"%Y-%m-%d %H:%M:%S"))
            self.anomalyScatterY.append(float(inputData["C"]["actualValue"]))
            self.actualPredictValueGraph.scatter(
                self.anomalyScatterX,
                self.anomalyScatterY,
                s=50,
                color="black"
            )

        # update the highlight of the anomalyScoreGraph.
        if float(inputData["A"]["anomalyScore"]) >= 0.8 and float(inputData["B"]["anomalyScore"]) >= 0.8 and float(
                inputData["C"]["anomalyScore"]) >= 0.8:
            self.highlightList.append(datetime.datetime.strptime(inputData["A"]["timestamp"],"%Y-%m-%d %H:%M:%S"))
            self.highlightListTurnOn = True
        else:
            self.highlightListTurnOn = False
        if len(self.highlightList) != 0 and self.highlightListTurnOn is False:
            self.anomalyScoreGraph.axvspan(
                self.highlightList[0] - datetime.timedelta(minutes=10),
                self.highlightList[-1] + datetime.timedelta(minutes=10),
                color="r",
                edgecolor=None,
                alpha=0.2
            )
            self.highlightList = []
            self.highlightListTurnOn = True

        # # update the anomaly value table.
        # if anomalyScore >= 0.8:
        #     # remove the table and then replot it
        #     self.anomalyValueTable.remove()
        #     self.anomalyValueTable = fig.add_axes([0.8, 0.1, 0.2, 0.8], frameon=False)
        #     self.anomalyValueTableColumnsName = ["timestamp", "actual value", "expect value", "anomaly score"]
        #     self.anomalyValueTable.text(0.05, 0.99, "Anomaly Value Table", size=12)
        #     self.anomalyValueTable.set_xticks([])
        #     self.anomalyValueTable.set_yticks([])
        #     self.tableValue.append([
        #         timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        #         actualValue,
        #         predictValue,
        #         anomalyScore
        #     ])
        #     if len(self.tableValue) >= 40: self.tableValue.pop(0)
        #     self.anomalyValueTable.table(
        #         cellText=self.tableValue,
        #         colWidths=[0.35] * 4,
        #         colLabels=self.anomalyValueTableColumnsName,
        #         loc=1,
        #         cellLoc="center"
        #     )

        # plot pause 0.0001 second and then plot the next one.
        plt.pause(0.0001)
        plt.draw()

    def close(self):
        plt.ioff()
        plt.show()
