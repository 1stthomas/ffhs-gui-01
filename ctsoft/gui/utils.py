# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 18:07:09 2018

@author: ctsoft
"""


class Input(object):
    def __init__(self, plotType, data):
        self.__data = []
        self.__plotType = ""
        self.__plotTypes = {"bar", "func", "func_multi", "histo", "pie"}
        self.setPlotType(plotType)

    def getData(self):
        return self.__data

    def getPlotType(self):
        return self.__plotType

    def setData(self, data):
        self.__data = data

    def setPlotType(self, plotType):
        if plotType in self.__plotTypes:
            self.__plotType = plotType
            return True
        else:
            return False


class Output(object):
    def __init__(self, path, message):
        self.__message = message
        self.__path = path

    def getMessage(self):
        return self.__message

    def getPath(self):
        return self.__path

    def setMessage(self, message):
        self.__message = message

    def setPath(self, path):
        self.__path = path
