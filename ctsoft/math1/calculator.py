# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 20:43:07 2018

@author: ctsoft
"""

import os
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
