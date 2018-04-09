# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 16:23:22 2018

@author: ctsoft
"""

import csv
import ctsoft.gui.controller as ctsguicnt
import ctsoft.gui.utils as ctsguiutil
import ctsoft.math1.calculator as ctscalc


class App(object):
    def __init__(self):
        self.__cntGui = ctsguicnt.Controller()
        self.__defaults = {"delimiter": ",", "filename": "No File Selected",
                           "input-value": "Not Implemented atm"}

    def displayPlot(self, path):
        container = self.getPlotContainer()
        self.__cntGui.changeImage(container, path)

    def displayMessage(self, msg):
        self.getMessageWidget()["text"] += msg + "\n"

    def getCanvasContainer(self):
        return self.__cntGui.getWidget("container-canvas")

    def getControllerGui(self):
        return self.__cntGui

    def getFileContent(self, path):
        data = []
        with open(path, newline="") as csvfile:
            reader = csv.reader(csvfile,
                                delimiter=self.__defaults["delimiter"])
            ind = 0
            for row in reader:
                val = row[0].split(";")
                index = 0
                for v in val:
                    if ind == 0:
                        data.append([])
                    data[index].append(float(v))
                    index += 1
                ind += 1
        return data

    def getFileNameButtonWidget(self):
        return self.__cntGui.getWidget("file-dialog")

    def getFileNameTextWidget(self):
        return self.__cntGui.getWidget("file-path")

    def getInput(self):
        data = []
        path = self.getFileNameTextWidget()["text"]
        if path == "" or path == self.__defaults["filename"]:
            path = ""

        if path is not "":
            data = self.getFileContent(path)

        plotType = self.getPlotType()
        print("data: ", data, " \n - value: ", plotType)
        inputObj = ctsguiutil.Input(plotType, data)

        return inputObj

    def getMessageWidget(self):
        return self.__cntGui.getWidget("gui-message")

    def getPlotContainer(self):
        return self.__cntGui.getWidget("container-plot")

    def getPlotType(self):
        return self.getPlotTypeWidget().getValue()

    def getPlotTypeWidget(self):
        return self.__cntGui.getWidget("chart-type")

    def getResetButtonWidget(self):
        return self.__cntGui.getWidget("button-reset")

    def getSubmitButtonWidget(self):
        return self.__cntGui.getWidget("button-submit")

    def handleOutput(self, outputObj):
        errors = outputObj.getErrors()
        if errors:
            for error in errors:
                self.displayMessage("Application Exception: " + error)
        else:
            msgs = outputObj.getMessages()
            if msgs:
                for msg in msgs:
                    self.displayMessage(msg)
            self.displayPlot(outputObj.getPath())

    def handleSubmit(self):
        inputObj = self.getInput()
        errors = self.validateInput(inputObj)
        if errors:
            for error in errors:
                self.displayMessage(error)
        else:
            calc = ctscalc.Calculator()
            outputObj = calc.createPlot(inputObj)
            self.handleOutput(outputObj)

    def resetGui(self):
        self.setFileName(self.__defaults["filename"])
        self.setInputValue(self.__defaults["input-value"])
        self.getPlotContainer().delete("all")

    def run(self):
        self.__cntGui.createGui()
        self.setupGui()
        self.__cntGui.runGui()

    def setFileName(self, fname):
        widget = self.__cntGui.getWidget("file-path")
        widget.configure(text=fname)

    def setInputValue(self, iValue):
        widget = self.__cntGui.getWidget("input-widget")
        widget.delete(0, len(widget.get()))
        widget.insert(0, iValue)

    def setupGui(self):
        fdButton = self.getFileNameButtonWidget()
        fdButton.configure(command=lambda arg=self:
                           self.__cntGui.openFileDialog(arg))
        fdText = self.getFileNameTextWidget()
        if fdText["text"] == "":
            fdText.configure(text=self.__defaults["filename"])
        formSubmit = self.getSubmitButtonWidget()
        formSubmit.configure(command=self.handleSubmit)
        resetSubmit = self.getResetButtonWidget()
        resetSubmit.configure(command=self.resetGui)

    def validateInput(self, inputObj):
        errors = []

        if bool(inputObj.getData()) is False:
            errors.append("No Data found.")
        if inputObj.getPlotType() == "":
            errors.append("Invalid plot type found.")

        return errors
