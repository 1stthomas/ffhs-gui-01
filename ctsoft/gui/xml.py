# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 14:46:05 2018

@author: ctsoft
"""

import tkinter as tk
import xml.etree.ElementTree as xmlee
import ctsoft.gui.elements as ctsel


class Interpreter:
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
        self.__builder.create(element, parent)
        parent = self.__builder.getCurrent()

        if self.check4Id(element) is True:
            self.setElementById(element, parent)

        elements = element.findall("*")

        for el in elements:
            self.parseXml(el, parent)

    def setElementById(self, elementXml, elementTk):
        self.__controller.addWidget(elementXml.attrib["id"], elementTk)

    def setIdentifier(self, identifier):
        self.__identifier = identifier


class Builder:
    def __init__(self):
        self.__current = {}
        self.__root = {}
        self.__rootName = "gui"
        self.__windowName = "window"

    def checkRootTag(self, element):
        if element.tag == self.__rootName:
            return True
        else:
            return False

    def create(self, element, parent):
        if element.tag == "pack":
            return
        elif element.tag == "button":
            self.__current = ctsel.TkButton(parent, element)
        elif element.tag == "entry":
            self.__current = ctsel.TkEntry(parent, element)
        elif element.tag == "frame":
            self.__current = ctsel.TkFrame(parent, element)
        elif element.tag == "label":
            self.__current = ctsel.TkLabel(parent, element)
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

    def getWindowName(self):
        return self.__windowName
