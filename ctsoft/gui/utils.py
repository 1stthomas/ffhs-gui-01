# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 18:07:09 2018

@author: ctsoft
"""


class Input(object):
    def __init__(self, plotType="", data=[]):
        self.__data = []
        self.__plotType = ""
        self.__plotTypes = {"bar-chart", "function-single",
                            "function-multiple", "histogram", "pie-chart"}
        self.setData(data)
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
    def __init__(self, path="", messages=[], errors=[]):
        self.__errors = []
        self.__messages = []
        self.__path = path
        self.setMessages(messages)
        self.setErrors(errors)

    def addError(self, error):
        self.__errors.append(error)

    def addMessage(self, message):
        self.__messages.append(message)

    def getErrors(self):
        return self.__errors

    def getMessages(self):
        return self.__messages

    def getPath(self):
        return self.__path

    def setErrors(self, errors):
        self.__errors = errors

    def setMessages(self, messages):
        self.__messages = messages

    def setPath(self, path):
        self.__path = path
