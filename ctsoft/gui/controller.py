# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 18:16:45 2018

@author: zoom4u
"""

import ctsoft.gui.xml as ctsxml


class Controller(object):
    def __init__(self):
        self.__widgets = {}
        self.__interpreter = ctsxml.Interpreter("settings.gui.xml")
        self.__top = {}

    def addWidget(self, key, value):
        self.__widgets[key] = value

    def createGui(self):
        self.__top = self.__interpreter.createElements()

    def getWidget(self, key):
        return self.__widgets[key]

    def getWidgets(self):
        return self.__widgets

    def runGui(self):
        self.__top.mainloop()
