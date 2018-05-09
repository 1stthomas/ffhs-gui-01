# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 14:46:05 2018

@author: ctsoft
"""

import xml.etree.ElementTree as xmlee
import ctsoft.gui.elements as ctsel
import ctsoft.gui.extensions as ctsex


class Parser(object):
    """
    Parses the XML of the GUI and calls the Builder to create the GUI.

    Methods
    -------
    addElementById :
        Adds an Tkinter widget to the controllers collection with its id
        as key.
    check4Id :
        Checks whetever the XML element contains an attribute which matches
        the defined identifier.
    createElements :
        Creates the GUI elements.
    getFileContent :
        Returns the content of an XML file as an xml.etree.ElementTree.
    parseXml :
        Parses the XML elements and calls the builder with the found elements.
    setIdentifier :
        Sets the identifier definition.
    """
    def __init__(self, controller, filename, encoding="UTF-8", method="xml"):
        """
        Instanciates a Parser by setting the instance variables and calling
        getFileContent().

        Parameters
        ----------
        controller : ctsoft.gui.Controller
            The GUI controller.
        filename : string
            The name of the file with the XML definitions.
        encoding : string
            The encoding of the submitted XML file. @Todo: what reason??
        method : string
            @Todo: what is the reason for this parameter??
        """
        self.__controller = controller
        self.__encoding = encoding
        self.__filename = filename
        self.__identifier = ""
        self.__method = method
        self.__builder = Builder()

        if filename is not "":
            self.__content = self.getFileContent(self.__filename)

    def addElementById(self, elementXml, elementTk):
        """
        Adds an Tkinter Widget to the defined Controller collection.

        Parameters
        ----------
        elementXml : xml.etree.ElementTree
            The XML element of the current Tkinter widget.
        elementTk : object
            The Tkinter widget to collect.
        """
        self.__controller.addWidget(elementXml.attrib["id"], elementTk)

    def check4Id(self, element):
        """
        Checks if the submitted XML element contains an attribute
        defined as the identifier.

        Parameters
        ----------
        element : xml.etree.ElementTree
            The Xml element to check.

        Returns
        -------
        boolean : True if the identifier could be found.
        """
        if self.__identifier in element.attrib:
            return True
        else:
            return False

    def createElements(self):
        """
        Starts the GUI creation.

        Returns
        -------
        tk.Tk : The Tkinter Root Window.
        """
        if self.__builder.checkRootTag(self.__content):
            elements = self.__content.findall("*")

            for el in elements:
                self.parseXml(el, {})

            return self.__builder.getRoot()
        else:
            print("The Element ", self.__content.tag, " is unkown.")
            return None

    def getFileContent(self, filename):
        """
        Returns the parsed XML content of the submitted Filename.

        Parameters
        ----------
        filename : string
            The file name of the XML definitions of the GUI.

        Returns
        -------
        xml.etree.ElementTree : The parsed XML document.
        """
        return xmlee.parse(filename).getroot()

    def parseXml(self, element, parent):
        """
        Parses the XML Element and creates the Tkinter widget according to
        the found widget definitions.
        This is a recursive method.

        Parameters
        ----------
        element : xml.etree.ElementTree
            The current XML element with its children.
        parent : mixed
            None if the element is the root window, or the parent widget of
            the current one.
        """
        doRec = self.__builder.create(element, parent)
        parent = self.__builder.getCurrent()
        if self.check4Id(element) is True:
            self.addElementById(element, parent)

        if doRec is False:
            # do not parse inner elements
            return parent

        if self.__builder.doChangeParent():
            # change the parent due to a tkinter extension which has another
            # parent to append the inner elements
            parent = self.__builder.getChangedParent()

        if self.__builder.doChangeXml():
            # change the xml due to a tkinter extension which has another
            # xml element with content
            element = self.__builder.getChangedXml()

        if element:
            elements = element.findall("*")

            for el in elements:
                # parse the inner elements
                self.parseXml(el, parent)

            # handle grid layout settings
            self.__builder.close(parent, element)

        return parent

    def setContent(self, content):
        self.__content = content

    def setController(self, controller):
        self.__controller = controller

    def setIdentifier(self, identifier):
        """
        Sets the identifier.

        Parameters
        ----------
        identifier : string
            The identifier.
        """
        self.__identifier = identifier


class Builder:
    """
    Creates the GUI Components by translating the XML into the Tkinter Widgets.

    Methods
    -------
    checkRootTag :
        Checks the XML tag name against the rootName variable value.
    close :
        Used by widgets controlled by the grid to set row definitions.
    create :
        Creates a widget as found in the XML definitions.
    getCurrent :
        Returns the current widget.
    getRoot :
        Returns the root widget of the GUI.
    getRootName :
        Returns the tag name of the root element of the XML document.
    getWidgetClassName :
        Returns the class name according to the submitted tag name.
    getWindowName :
        Returns the tag name of the root widget.
    setCurrent :
        Sets the current widget.
    """
    def __init__(self):
        self.__changedParent = None
        self.__changedXml = None
        self.__current = None
        self.__doChangeParent = False
        self.__doChangeXml = False
        self.__root = None
        self.__rootName = "gui"
        self.__skippedWidgets = ["column", "grid", "image", "pack", "row"]
        self.__widgets = ["button", "canvas", "checkbutton", "entry",
                          "frame", "label", "labelframe", "listbox",
                          "menu", "optionmenu", "radiobutton", "scale",
                          "scrollbar", "text", "toplevel"]
        self.__windowName = "window"

    def checkRootTag(self, element):
        """
        Checks whetever the XML tag name is equal to the rootName variable
        value.

        Parameters
        ----------
        element : xml.etree.ElementTree
            The XML element to check.

        Returns
        -------
        boolean : True if the XML tag name is equal to rootName.
        """
        if element.tag == self.__rootName:
            return True
        else:
            return False

    def close(self, current, xml):
        """
        Sets the Row Definitions of Elements, which are organized by the
        Grid Layout Manager.
        This Method is used by Parsers parseXml() at the end of the widget
        creation cycles.

        Parameters
        ----------
        current : object
            Extended Tkinter widgets like descendants of
            ctsoft.gui.elements.TkBase .
        xml : xml.etree.ElementTree
            The XML definitions of the current widget.
        """
        self.setCurrent(current)
        if current.getOrganizeTypeChildren() == "grid":
            rows = xml.findall("row")
            current.setRows(rows)

    def create(self, xml, parent):
        """
        Creates the widgets by calling their constructors. Defined tag names
        will be skipped.

        xml : xml.etree.ElementTree
            The XML element of the widget to be created.
        parent : xml.etree.ElementTree
            The parent widget of the new one.
        """
        self.__doChangeXml = False
        if xml.tag in self.__skippedWidgets:
            return False
        elif xml.tag in self.__widgets:
            widgetClassName = self.getWidgetClassName(xml.tag)
            class_ = getattr(ctsel, widgetClassName)
            self.__current = class_(parent, xml)
            images = xml.findall("image")
            if images:
                for image in images:
                    # only the last one will be displayed
                    self.__current.setImage(image)
        elif xml.tag == "radiobuttongroup":
            self.__current = ctsex.RadiobuttonGroup(parent, xml)
            return False
        elif xml.tag == "scrollable":
            self.__current = ctsex.ContainerScrollable(parent, xml)
            self.__doChangeParent = True
            self.__changedParent = self.__current.getChangedParent()
            self.__doChangeXml = True
            self.__changedXml = self.__current.getXmlContent()
        elif xml.tag == "tabs":
            self.__current = ctsex.ContainerTabs(parent, xml)
            self.__current.setParser(Parser(self, ""))
            self.__current.createWidgets()
            return False
        elif xml.tag == self.__windowName:
            self.__current = ctsel.TkWindow(xml)
            self.__root = self.__current
        else:
            print("=> tag ", xml.tag, " does not exist.")

    def doChangeParent(self):
        return self.__doChangeXml

    def doChangeXml(self):
        return self.__doChangeXml

    def getChangedParent(self):
        return self.__changedParent

    def getChangedXml(self):
        return self.__changedXml

    def getCurrent(self):
        """
        Returns the current widget.

        Returns
        -------
        object : The current widget of the builder instance.
        """
        return self.__current

    def getRoot(self):
        """
        Returns the Root Element, normally an instance of TkWindow.

        Returns
        -------
        ctsoft.gui.xml.TkWindow : The window widget.
        """
        return self.__root

    def getRootName(self):
        """
        Returns the Root Element Name.

        Returns
        -------
        string : The name of the root element of the XML document.
        """
        return self.__rootName

    def getWidgetClassName(self, tagName):
        """
        Returns the Class Name of the submitted XML Tag Name.

        Parameters
        ----------
        tagName : string
            The tag name to transfer.

        Returns
        -------
        string : The class names according to the submitted tag name.
        """
        if tagName == "labelframe":
            className = "TkLabelFrame"
        elif tagName == "optionmenu":
            className = "TkOptionMenu"
        elif tagName == "toplevel":
            className = "TkToplevel"
        else:
            className = "Tk" + tagName.capitalize()

        return className

    def getWindowName(self):
        """
        Returns the Tag Name of the Root Element.

        Returns
        -------
        string : The tag name of the root element.
        """
        return self.__windowName

    def setChangedParent(self, parent):
        self.__changedParent = parent

    def setChangedXml(self, xml):
        self.__changedXml = xml

    def setCurrent(self, current):
        """
        Sets the curren Widget.

        Parameters
        ----------
        current : object
            One of the Tkinter extensions in the ctsoft.gui.elements modul.
        """
        self.__current = current
