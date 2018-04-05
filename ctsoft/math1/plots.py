# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 19:46:00 2018

@author: zoom4u
"""

import matplotlib.pyplot as plt
from IPython.core.pylabtools import figsize


class Plotter(object):
    def __init__(self):
        self.__fName = "function_plot.png"
        figsize(8, 5)

    def createFunctionSingle(self, data):
        plt.plot(data[0], data[1])
        axis = [min(data[0]), max(data[0]), min(data[1]), max(data[1])]
        plt.axis(axis)
        plt.grid(True)
        plt.savefig(self.__fName)
        plt.show()
        return self.__fName

    def createFunctionMultiple(self, data):
        first = []
        index = 0
        for col in data:
            if index == 0:
                first = col
                index = 1
            else:
                plt.plot(first, col)
        plt.grid(True)
        plt.savefig(self.__fName)
        plt.show()
        return self.__fName

    def createBarChart(self, data):
        plt.bar(data[0], data[1])
        plt.savefig(self.__fName)
        plt.show()
        return self.__fName

    def createPieChart(self, data):
        plt.pie(data[0], shadow=True)
        plt.savefig(self.__fName)
        plt.show()
        return self.__fName

    def createHistogram(self, data):
        num_bins = 5
        n, bins, patches = plt.hist(data, num_bins)
#        n, bins, patches = plt.hist(data, num_bins, facecolor="blue")
        plt.savefig(self.__fName)
        plt.show()
        return self.__fName
