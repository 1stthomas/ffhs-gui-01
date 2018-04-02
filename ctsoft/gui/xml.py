# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 14:46:05 2018

@author: ctsoft
"""

import tkinter as tk
import xml.etree.ElementTree as xmlee
import ctsoft.gui.elements as ctsel


class Parser:
    def __init__(self, controller, filename, encoding="UTF-8", method="xml"):
        self.__controller = controller
        self.__encoding = encoding
        self.__filename = filename
        self.__identifier = ""
        self.__method = method
        self.__builder = Builder()

        self.__content = self.getFileContent(self.__filename)

    def check4Id(self, element):
        if self.__identifier in element.attrib:
            return True
        else:
            return False

    def createElements(self):

        if self.__builder.checkRootTag(self.__content):
            elements = self.__content.findall("*")

            for el in elements:
                self.parseXml(el, {})

            return self.__builder.getRoot()
        else:
            print("The Element ", self.__content.tag, " is unkown.")
            return None

    def getFileContent(self, filename):
        return xmlee.parse(self.__filename).getroot()

    def parseXml(self, element, parent):
        if self.__builder.create(element, parent) is False:
            return

        parent = self.__builder.getCurrent()

        if self.check4Id(element) is True:
            self.addElementById(element, parent)

        elements = element.findall("*")

        for el in elements:
            self.parseXml(el, parent)

        self.__builder.close(parent, element)

    def addElementById(self, elementXml, elementTk):
        self.__controller.addWidget(elementXml.attrib["id"], elementTk)

    def setIdentifier(self, identifier):
        self.__identifier = identifier


class Builder:
    def __init__(self):
        self.__current = None
        self.__root = None
        self.__rootName = "gui"
        self.__skippedWidgets = ["grid", "image", "pack", "row"]
        self.__widgets = ["button", "canvas", "checkbutton", "entry",
                          "frame", "label", "labelframe", "listbox",
                          "menu", "optionmenu", "radiobutton", "scale",
                          "text"]
        self.__windowName = "window"

    def checkRootTag(self, element):
        if element.tag == self.__rootName:
            return True
        else:
            return False

    def close(self, current, xml):
        self.setCurrent(current)
        if current.getOrganizeTypeChildren() == "grid":
            rows = xml.findall("row")
            current.setRows(rows)

    def create(self, element, parent):
        if element.tag in self.__skippedWidgets:
            return False
        elif element.tag in self.__widgets:
            widgetClassName = self.getWidgetClassName(element.tag)
            class_ = getattr(ctsel, widgetClassName)
            self.__current = class_(parent, element)
            images = element.findall("image")
            if images:
                for image in images:
                    # only the last one will be displayed
                    self.__current.setImage(image)
        elif element.tag == "radiobuttongroup":
            self.__current = ctsel.RadiobuttonGroup(parent, element)
            return False
        elif element.tag == "window":
            self.__current = ctsel.TkWindow(element)
            self.__root = self.__current
        else:
            print("=> tag ", element.tag, " does not exist.")

    def getCurrent(self):
        return self.__current

    def getRoot(self):
        return self.__root

    def getRootName(self):
        return self.__rootName

    def getWidgetClassName(self, tagName):
        if tagName == "labelframe":
            className = "TkLabelFrame"
        elif tagName == "optionmenu":
            className = "TkOptionMenu"
        else:
            className = "Tk" + tagName.capitalize()

        return className

    def getWindowName(self):
        return self.__windowName

    def setCurrent(self, current):
        self.__current = current
