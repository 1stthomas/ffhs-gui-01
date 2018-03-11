# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 14:46:05 2018

@author: ctsoft
"""

import tkinter as tk
import xml.etree.ElementTree as xmlee
import ctsoft.gui.elements as ctsel


class Interpreter:
    def __init__(self, filename, encoding="UTF-8", method="xml"):
        self.__filename = filename
        self.__encoding = encoding
        self.__method = method

        self.__content = self.getFileContent(self.__filename)

    def createElements(self):
        builder = Builder()

        if builder.checkRootTag(self.__content):
            elements = self.__content.findall("*")

            for el in elements:
                parser = Parser(builder)
                parser.parseXml(el, {})

            return builder.getRoot()
        else:
            print("The Element ", self.__content.tag, " is unkown.")
            return None

    def getFileContent(self, filename):
        return xmlee.parse(self.__filename).getroot()


class Parser:
    def __init__(self, builder):
        self.__builder = builder

    def parseXml(self, element, parent):
        self.__builder.create(element, parent)
        parent = self.__builder.getCurrent()

        elements = element.findall("*")

        for el in elements:
            self.parseXml(el, parent)


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
            self.__current = ctsel.TkButton(parent, element.attrib, element)
        elif element.tag == "entry":
            self.__current = ctsel.TkEntry(parent, element.attrib, element)
        elif element.tag == "frame":
            self.__current = ctsel.TkFrame(parent, element.attrib, element)
        elif element.tag == "label":
            self.__current = ctsel.TkLabel(parent, element.attrib, element)
        elif element.tag == "window":
            self.__root = tk.Tk()
            self.__root.title("Thomastest")
            self.__current = self.__root
        else:
            print("=> tag ", element.tag, " does not exist.")

    def createRoot(self, element):
        if element.tag == self.__windowName:
            self.__root = tk.Tk()
            self.__root.title("Thomastest")
            self.__current = self.__root
        else:
            self.__root -1

    def getCurrent(self):
        return self.__current

    def getRoot(self):
        return self.__root

    def getRootName(self):
        return self.__rootName

    def getWindowName(self):
        return self.__windowName
