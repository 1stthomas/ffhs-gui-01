# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 18:16:45 2018

@author: ctsoft
"""

import ctsoft.gui.elements as ctsel
import ctsoft.gui.xml as ctsxml
import tkinter as tk
from tkinter.filedialog import askopenfilename
import xml.etree.ElementTree as xmlee


class Controller(object):
    """
    The GUI Controller with basic Functionality.
    It is the start point of the GUI.

    Methods
    -------
    addWidget :
        Adds a widget with the specified key to the collection.
    changeImage :
        Changes the displayed image of the specified widget.
    createGui :
        Creates the GUI by calling corresponding ctsoft.gui.xml.Parser methods.
    getWidget :
        Returns the widget with the specified identifier.
    getWidgets :
        Returns the widget collection.
    openFileDialog :
        Opens the file dialog.
    setIdentifier :
        Sets the identifier name.
    runGui :
        Runs the GUI by starting the mainloop thread.
    """

    def __init__(self):
        """ Instanciates a Controller. """

        """ string : The name of the XML element id attribute. """
        self.__identifier = "id"
        """ ctsoft.gui.xml.Parser : The XMl parser. """
        self.__parser = ctsxml.Parser(self, "settings.gui.xml")
        """ mixed : None or the root Tkinter element after GUI creation. """
        self.__top = None
        """ dict : A collection of GUI widgets with an id. """
        self.__widgets = {}

    def addWidget(self, key, value):
        """
        Adds the widget with its specific id to the dict.

        Parameters
        ----------
        key : string
            The id of the widget which will be the dict key.
        value : object
            The specific GUI widget.
        """
        self.__widgets[key] = value

    def changeImage(self, parent, path, attributes={}):
        """
        Changes the Image of the underlying Element.

        Parameters
        ----------
        parent : object
            The parent with the image to change.
        path : string
            The path to the image to set.
        attributes : dict
            recognized keys: height and width, default values: 360/576
        """
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
        """
        Creates the GUI.
        """
        self.__parser.setIdentifier(self.__identifier)
        self.__top = self.__parser.createElements()

    def getWidget(self, key):
        """
        Returns the Widget with the requested id.

        Parameters
        ----------
        key : string
            The identifier of the requested widget.

        Returns
        -------
        widget : A Tkinter widget with the submited id.
        """
        return self.__widgets[key]

    def getWidgets(self):
        """
        Returns the Widget Container.

        Returns
        -------
        dict : A dictonary with all widgets with an id attribute.
        """
        return self.__widgets

    def openFileDialog(self, obj):
        """
        Open the File Dialog and sets the Filepath to the submitted Object.

        Parameters
        ----------
        obj : Object
            An Application Object which implements setFileName(fname).
        """
        fname = askopenfilename(filetypes=(("CSV files", "*.csv"),
                                           ("All files", "*.*")))
        if fname:
            obj.setFileName(fname)

    def setIdentifier(self, identifier):
        """
        Sets the Identifier, which defines the Attribute which desides, if
        a Widget should be collected.
        """
        self.__identifier = identifier

    def runGui(self):
        """
        Makes the GUI visible by starting the Mainloop Thread.
        """
        self.__top.mainloop()
