# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 16:23:22 2018

@author: zoom4u
"""

import ctsoft.gui.controller as ctsguicnt


class App(object):
    def __init__(self):
        self.__cntGui = ctsguicnt.Controller()

    def run(self):
        self.__cntGui.createGui()
        self.__cntGui.runGui()

    def getControllerGui(self):
        return self.__cntGui
