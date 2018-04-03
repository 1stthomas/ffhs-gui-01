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

    def createCanvasWithImage(self, parent, path):
        canXml = xmlee.Element('canvas')
        imgXml = xmlee.Element('image')
        imgXml.attrib["height"] = 200
        imgXml.attrib["width"] = 385
        canvas = ctsel.TkCanvas(parent, canXml)
        canvas["bg"] = "red"
        canvas.pack(expand=True, fill="x")
        print("-- breite: ", parent.winfo_width())
        print("-- hoehe: ", parent.winfo_height())
        print("breite: ", canvas.winfo_width())
        print("hoehe: ", canvas.winfo_height())
        print("imgxml: ", imgXml.attrib)

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
