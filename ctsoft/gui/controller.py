# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 18:16:45 2018

@author: zoom4u
"""

import ctsoft.gui.elements as ctsel
import ctsoft.gui.xml as ctsxml
import tkinter as tk
from tkinter.filedialog import askopenfilename
import xml.etree.ElementTree as xmlee


class Controller(object):
    def __init__(self):
        self.__identifier = "id"
        self.__parser = ctsxml.Parser(self, "settings.gui.xml")
        self.__top = {}
        self.__widgets = {}

    def addWidget(self, key, value):
        self.__widgets[key] = value

    def changeImage(self, parent, path, attributes={}):
        imgXml = xmlee.Element('image')
        imgXml.attrib["path"] = path
        if "height" in attributes:
            imgXml.attrib["height"] = attributes["height"]
        else:
            imgXml.attrib["height"] = "360"
        if "width" in attributes:
            imgXml.attrib["width"] = attributes["width"]
        else:
            imgXml.attrib["width"] = "576"
        parent.setImage(imgXml)

    def createGui(self):
        self.__parser.setIdentifier(self.__identifier)
        self.__top = self.__parser.createElements()

    def getWidget(self, key):
        return self.__widgets[key]

    def getWidgets(self):
        return self.__widgets

    def openFileDialog(self, obj):
        fname = askopenfilename(filetypes=(("CSV files", "*.csv"),
                                           ("All files", "*.*")))
        if fname:
            obj.setFileName(fname)

    def setIdentifier(self, identifier):
        self.__identifier = identifier

    def runGui(self):
        self.__top.mainloop()
