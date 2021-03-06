# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 19:24:49 2018

@author: ctsoft
"""

import tkinter as tk


class Options(object):
    def __init__(self, dt, root, settings, xml=None):
        self.__dt = None
        self.__root = None
        self.__settings = None
        self.__widgets = {}
        self.__window = None
        self.__xml = None

        self.setController(dt)
        self.setRoot(root)
        self.setSettings(settings)
        self.setXml(xml)

    def addWidget(self, key, widget):
        self.__widgets[key] = widget

    def createWindow(self, xml=None):
        if xml:
            self.setXml(xml)

        xml = self.getXml()
        settings = self.getSettings()

        if xml and settings:
            parent = settings.getParent()
            root = self.getRoot()
            parser = settings.getParser()
            parser.setController(self)

            if parent:
                top = parser.parseXml(xml, parent)
            else:
                top = parser.parseXml(xml, root)

            self.setWindow(top)
            top.state(newstate="withdrawn")

            self.setupButtons()

    def destroy(self):
        top = self.getWindow()
        top.destroy()

    def display(self):
        top = self.getWindow()
        top.focus_force()
#        top.grab_set()
        top.state(newstate="normal")

    def getController(self):
        return self.__dt

    def getRoot(self):
        return self.__root

    def getSettings(self):
        return self.__settings

    def getWidget(self, key):
        return self.__widgets[key]

    def getWidgets(self):
        return self.__widgets

    def getWindow(self):
        return self.__window

    def getXml(self):
        return self.__xml

    def setController(self, cnt):
        self.__dt = cnt

    def setRoot(self, root):
        self.__root = root

    def setSettings(self, settings):
        self.__settings = settings

    def setupButtons(self):
        top = self.getWindow()
        cnt = self.getController()

        btnAbort = self.getWidget("options-button-abort")
        btnAbort.configure(command=cnt.abortOptions)

        top.protocol("WM_DELETE_WINDOW", cnt.abortOptions)

    def setWindow(self, window):
        self.__window = window

    def setXml(self, xml):
        self.__xml = xml


class ChartFunction(Options):
    def __init__(self, dt, root, settings, xml=None):
        super().__init__(dt, root, settings, xml)

    def create(self):
        dt = self.getController()

        chartTitleWidget = self.getWidget("options-chart-title-chart")
        chartTitle = chartTitleWidget.get()

        abscissaWidget = self.getWidget("options-chart-title-abscissa")
        abscissa = abscissaWidget.get()

        ordinateWidget = self.getWidget("options-chart-title-ordinate")
        ordinate = ordinateWidget.get()

        legendWidget = self.getWidget("options-chart-legend")
        legend = legendWidget.getValue()

        splinesCheckWidget = self.getWidget("options-chart-splines")
        splinesCheck = splinesCheckWidget.getValue()

        splinesLenWidget = self.getWidget("options-chart-splines-new-length")
        splinesNewLen = splinesLenWidget.get()

        d = {"chart-title": chartTitle, "abscissa-title": abscissa,
             "legend": legend, "ordinate-title": ordinate,
             "splines-check": splinesCheck, "splines-new-len": splinesNewLen}

        dt.createChartFunction(d)
        dt.closeOptions()

    def setupButtons(self):
        Options.setupButtons(self)

        btnCreate = self.getWidget("options-button-chart-function")
        btnCreate.configure(command=self.create)


class NewTable(Options):
    def __init__(self, dt, root, settings, xml=None):
        super().__init__(dt, root, settings, xml)

    def create(self):
        dt = self.getController()

        colsWidget = self.getWidget("options-new-table-cols")
        cols = colsWidget.get()

        rowsWidget = self.getWidget("options-new-table-rows")
        rows = rowsWidget.get()

        dt.addDataFieldByNewTable(cols, rows)
        dt.closeOptions()

    def setupButtons(self):
        Options.setupButtons(self)

        btnCreate = self.getWidget("options-button-new-table")
        btnCreate.configure(command=self.create)


class Splines(Options):
    def __init__(self, dt, root, settings, xml=None):
        super().__init__(dt, root, settings, xml)

    def create(self):
        pass

    def setupButtons(self):
        Options.setupButtons(self)

        btnCreate = self.getWidget("options-button-splines")
        btnCreate.configure(command=self.create)
