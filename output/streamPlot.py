#! /usr/bin/python

import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.ticker as ticker


class streamDetectionPlot(object):
    """
    Anomaly detection mapping for one field.
    """

    # initial the figure parameters.
    def __init__(self):
        # Turn matplotlib interactive mode on.
        plt.ion()
        # initial the plot variable.
        self.timestamp = []
        self.actualValue = []
        self.predictValue = []
        self.anomalyScore = []
        self.tableValue = [[0, 0, 0, 0]]
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
        fig.subplots_adjust(left=0.06, right=0.70)
        self.actualPredictValueGraph = fig.add_subplot(2, 1, 1)
        self.anomalyScoreGraph = fig.add_subplot(2, 1, 2)
        self.anomalyValueTable = fig.add_axes([0.8, 0.1, 0.2, 0.8], frameon=False)

    # define the initial plot method.
    def initPlot(self):
        # initial two lines of the actualPredcitValueGraph.
        self.actualLine, = self.actualPredictValueGraph.plot_date(self.timestamp, self.actualValue, fmt="-",
                                                                  color="red", label="actual value")
        self.predictLine, = self.actualPredictValueGraph.plot_date(self.timestamp, self.predictValue, fmt="-",
                                                                   color="blue", label="predict value")
        self.actualPredictValueGraph.legend(loc="upper right", frameon=False)
        self.actualPredictValueGraph.grid(True)

        # initial two lines of the anomalyScoreGraph.
        self.anomalyScoreLine, = self.anomalyScoreGraph.plot_date(self.timestamp, self.anomalyScore, fmt="-",
                                                                  color="red", label="anomaly score")
        self.anomalyScoreGraph.legend(loc="upper right", frameon=False)
        self.baseline = self.anomalyScoreGraph.axhline(0.8, color='black', lw=2)

        # set the x/y label of the first two graph.
        self.anomalyScoreGraph.set_xlabel("datetime")
        self.anomalyScoreGraph.set_ylabel("anomaly score")
        self.actualPredictValueGraph.set_ylabel("value")

        # configure the anomaly value table.
        self.anomalyValueTableColumnsName = ["timestamp", "actual value", "expect value", "anomaly score"]
        self.anomalyValueTable.text(0.05, 0.99, "Anomaly Value Table", size=12)
        self.anomalyValueTable.set_xticks([])
        self.anomalyValueTable.set_yticks([])

        # axis format.
        self.dateFormat = DateFormatter("%m/%d %H:%M")
        self.actualPredictValueGraph.xaxis.set_major_formatter(ticker.FuncFormatter(self.dateFormat))
        self.anomalyScoreGraph.xaxis.set_major_formatter(ticker.FuncFormatter(self.dateFormat))

    # define the output method.
    def anomalyDetectionPlot(self, timestamp, actualValue, predictValue, anomalyScore):

        # update the plot value of the graph.
        self.timestamp.append(datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"))
        self.actualValue.append(float(actualValue))
        self.predictValue.append(float(predictValue))
        self.anomalyScore.append(float(anomalyScore))

        # update the x/y range.
        self.timestampRange = [min(self.timestamp), max(self.timestamp) + datetime.timedelta(minutes=10)]
        self.actualValueRange = [min(self.actualValue), max(self.actualValue) + 1]
        self.predictValueRange = [min(self.predictValue), max(self.predictValue) + 1]

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
        self.actualLine.set_xdata(self.timestamp)
        self.actualLine.set_ydata(self.actualValue)
        self.predictLine.set_xdata(self.timestamp)
        self.predictLine.set_ydata(self.predictValue)

        # update the line of the anomalyScoreGraph.
        self.anomalyScoreLine.set_xdata(self.timestamp)
        self.anomalyScoreLine.set_ydata(self.anomalyScore)

        # update the scatter.
        if anomalyScore >= 0.8:
            self.anomalyScatterX.append(datetime.datetime.strptime(timestamp,"%Y-%m-%d %H:%M:%S"))
            self.anomalyScatterY.append(float(actualValue))
            self.actualPredictValueGraph.scatter(
                self.anomalyScatterX,
                self.anomalyScatterY,
                s=50,
                color="black"
            )

        # update the highlight of the anomalyScoreGraph.
        if float(anomalyScore) >= 0.8:
            self.highlightList.append(datetime.datetime.strptime(timestamp,"%Y-%m-%d %H:%M:%S"))
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

        # update the anomaly value table.
        if float(anomalyScore) >= 0.8:
            # remove the table and then replot it
            self.anomalyValueTable.remove()
            self.anomalyValueTable = fig.add_axes([0.8, 0.1, 0.2, 0.8], frameon=False)
            self.anomalyValueTableColumnsName = ["timestamp", "actual value", "expect value", "anomaly score"]
            self.anomalyValueTable.text(0.05, 0.99, "Anomaly Value Table", size=12)
            self.anomalyValueTable.set_xticks([])
            self.anomalyValueTable.set_yticks([])
            self.tableValue.append([
                timestamp,
                actualValue,
                predictValue,
                anomalyScore
            ])
            if len(self.tableValue) >= 40: self.tableValue.pop(0)
            self.anomalyValueTable.table(
                cellText=self.tableValue,
                colWidths=[0.35] * 4,
                colLabels=self.anomalyValueTableColumnsName,
                loc=1,
                cellLoc="center"
            )

        # plot pause 0.0001 second and then plot the next one.
        plt.pause(0.0001)
        plt.draw()

    def close(self):
        plt.ioff()
        plt.show()
