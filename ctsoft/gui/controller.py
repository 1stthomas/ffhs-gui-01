# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 18:16:45 2018

@author: zoom4u
"""

import ctsoft.gui.xml as ctsxml


class Controller(object):
    def __init__(self):
        self.__identifier = "id"
        self.__parser = ctsxml.Parser(self, "settings.gui.xml")
        self.__top = {}
        self.__widgets = {}

    def addWidget(self, key, value):
        self.__widgets[key] = value

    def createGui(self):
        self.__parser.setIdentifier(self.__identifier)
        self.__top = self.__parser.createElements()

    def getWidget(self, key):
        return self.__widgets[key]

    def getWidgets(self):
        return self.__widgets

    def setIdentifier(self, identifier):
        self.__identifier = identifier

    def runGui(self):
        self.__top.mainloop()
