# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 20:43:07 2018

@author: ctsoft
"""

import os
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import ctsoft.math1.plots as plots
import ctsoft.gui.utils as utils


class Calculator(object):
    def __init__(self):
        self.__plotter = plots.Plotter()

    def createPlot(self, obj):
        outputObj = utils.Output()
        pt = obj.getPlotType()
        if pt == "function-single":
            fName = self.__plotter.createFunctionSingle(obj.getData())
        elif pt == "function-multiple":
            fName = self.__plotter.createFunctionMultiple(obj.getData())
        elif pt == "bar-chart":
            fName = self.__plotter.createBarChart(obj.getData())
        elif pt == "pie-chart":
            fName = self.__plotter.createPieChart(obj.getData())
        elif pt == "histogram":
            fName = self.__plotter.createHistogram(obj.getData())

        path = os.getcwd() + "/" + fName
        outputObj.setPath(path)
        return outputObj

    def createChartFunction(self, values, options):
        fName = "function_plot.jpg"
        cols = []
        for col in values:
            cols.append(col.getValues("float"))

        chartTitle = options["chart-title"]
        abscissaTitle = options["abscissa-title"]
        ordinateTitle = options["ordinate-title"]
        splinesCheck = options["splines-check"]
        newLen = options["splines-new-len"]

        fig = plt.figure()

        index = 1
        colNum = len(cols) - 1
        legend = []

        if splinesCheck == 1:
            newX = np.linspace(min(cols[0]), max(cols[0]), newLen)

            while index <= colNum:
                f1 = interp1d(cols[0], cols[index])
                f2 = interp1d(cols[0], cols[index], kind="cubic")
                plt.plot(cols[0], cols[index], 'o', newX, f1(newX), '-',
                         newX, f2(newX), '--')
                index += 1
                legend += ["data " + str(index - 1),
                           "linear " + str(index - 1),
                           "cubic " + str(index - 1)]

            plt.legend(legend, loc='best')
        else:
            while index <= colNum:
                plt.plot(cols[0], cols[index], 'o')
                legend += ["data " + str(index)]
                index += 1

            plt.legend(legend, loc="best")

        if chartTitle is not "":
            fig.suptitle(chartTitle)

        if abscissaTitle is not "":
            plt.xlabel(abscissaTitle)

        if ordinateTitle is not "":
            plt.ylabel(ordinateTitle)

#        plt.show()
        fig.savefig(fName)
        return fName
