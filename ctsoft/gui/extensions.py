# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 21:41:25 2018

@author: ctsoft
"""

import tkinter as tk
import tkinter.ttk as ttk
import ctsoft.gui.elements as ctsel
import ctsoft.gui.elementsttk as ctselttk


class ContainerScrollable(object):
    """
    Container with x- and y-Scrollbars.
    This extension is built on a canvas tkinter widget, which holds a frame
    with the defined scrollbars and the scrollable content.

    Methods
    -------
    addScrollbar :
        Adds a scrollbar for the specified orientation.
    createCanvas :
        Creates the underlying container as canvas.
    createCanvasFrame :
        Creates the container, which contains the content.
    createScrollbarWidget :
        Populates the canvas with the scrollbar widgets.
    createWidgets :
        Starting method to create the scrollbar extension.
    defineCanvasFrameDimension :
        Sets the canvas expand parameters.
    getCanvas :
        Returns the canvas widget.
    getCanvasFrame :
        Returns the child of the canvas widget.
    getChangedParent :
        Returns the changed parent.
    getParent :
        Returns the parent of the scrollbar widget.
    getScrollbar :
        Returns the scrollbar sepcified by the orientation.
    getScrollbars :
        Returns the defined scrollbars.
    getXmlContent :
        Returns the xml elements of the scrollbar widget.
    handleContent :
        Creates the content and appends to the scrollbar container.
    setCanvas :
        Sets the canvas widget.
    setCanvasFrame :
        Sets the first frame widget of the canvas.
    setChangedParent :
        Sets the changed parent.
    setFrameDimensions :
        Sets the event listener to update the scollbars.
    setXmlContent :
        Sets the xml content of the scrollbar widget.
    populate :
        Sets default content for testing the scrollbar widget.
    _bindMousewheel :
        Event listener for the mouse wheel event.
    _onCanvasFrameDimension :
        Eventlistener for the resize event.
    _onFrameConfigure :
        Event configuration for the scrollbars.
    _onMousewheel :
        Event handler for the mouse wheel event.
    _unbindMousewheel :
        Removes the event listener for the mouse wheel event.
    """
    def __init__(self, parent, xml, *args, **kw):
        """
        Instanciates a Scrollbar Container.

        Parameters
        ----------
        parent : object
            One of the Tkinter widget extensions in this module as parent
            of the new Scrollbar Container.
        xml : xml.etree.ElementTree
            The element definitions of the new RadiobuttonGroup.
        """

        """ ctsoft.gui.elements.TkCanvas : The canvas widget """
        self.__canvas = None
        self.__canvasFrameDimension = None
        self.__changedParent = None
        self.__frame = None
        self.__parent = parent
        self.__scrollbars = {}
        self.__xmlContent = None

        self.createWidgets(xml)
        self.handleContent(xml)

    def addScrollbar(self, orient, scrollbar):
        """
        Adds a Scrollbar Widget to the Collection.

        Parameters
        ----------
        orient : string
            The scrollbar orientation.
        scrollbar : ctsoft.gui.elements.TkScrollbar
            The scrollbar widget to add to the collection.
        """
        self.__scrollbars[orient] = scrollbar

    def createCanvas(self, parent, xmlCanvas):
        """
        Creates the Canvas widget which contains the Scrollbars and the
        Base Frame Widget.

        Parameters
        ----------
        parent : object
            The parent widget of the scrollbar extension.
        xmlCanvas : xml.etree.ElementTree
            The xml definitions of the scrollbar extension.

        Returns
        -------
        ctsoft.gui.elements.TkCanvas : The created canvas widget.
        """
        canvas = ctsel.TkCanvas(parent, xmlCanvas)
        canvas.grid(column=0, row=0, sticky="nwse")
        self.setCanvas(canvas)

        return canvas

    def createCanvasFrame(self, parent, xml):
        """
        Creates the Frame Widget which contains the Content.

        Parameters
        ----------
        parent : object
            Normally the canvas widget.
        xml : xml.etree.ElementTree
            The xml definitions of the frame to be created.

        Returns
        -------
        ctsoft.gui.elements.TkFrame : The created frame widget.
        """
        frame = ctsel.TkFrame(parent, xml)
        self.setCanvasFrame(frame)

        return frame

    def createScrollbarWidget(self, parent, xml):
        """
        Creates the Scrollbar Widget with the XML Definitions.

        Parameters
        ----------
        parent : object
            Normally the canvas widget.
        xml : xml.etree.ElementTree
            The xml definitions of the scrollbar to be created.

        Returns
        -------
        ctsoft.gui.elements.TkScrollbar : The created scrollbar widget.
        """
        sb = ctsel.TkScrollbar(parent, xml)

        if xml.attrib.get("orient", "vertical") == "vertical":
            # Set the default value for the case it is not set already.
            xml.attrib["orient"] = "vertical"
            # Compose the Canvas scrollcommand for y with the scrollbar.
            self.__canvas.configure(yscrollcommand=sb.set)
            # Compose the scrollbar action with the canvas viewport.
            sb.configure(command=self.__canvas.yview)
            # configure the layout manager of the scrollbar
            sb.grid(column=1, row=0, sticky="nes")
        else:
            # The vertical orientation is default.
            sb.configure(orient="horizontal")
            self.__canvas.configure(xscrollcommand=sb.set)
            sb.configure(command=self.__canvas.xview)
            sb.grid(column=0, row=1, sticky="esw")

        self.addScrollbar(xml.attrib["orient"], sb)

        return sb

    def createWidgets(self, xml):
        """
        Starting Point of the Scrollbar Extension. All required Methods will be
        executed to meet the XML definitions.

        Parameters
        ----------
        xml : xml.etree.ElementTree
            The xml definitions of the scrollbar extension.
        """
        parent = self.getParent()
        xmlSetup = xml.find("setup")

        xmlCanvas = xmlSetup.find("canvas")
        canvas = self.createCanvas(parent, xmlCanvas)

        xmlFrame = xmlCanvas.find("frame")
        frame = self.createCanvasFrame(canvas, xmlFrame)

        xmlScrollbars = xmlSetup.findall("scrollbar")
        for xmlScrollbar in xmlScrollbars:
            self.createScrollbarWidget(parent, xmlScrollbar)

        # Define the row and column behavior of the grid manager.
        parent.rowconfigure(0, weight=1)
        parent.rowconfigure(1, weight=0)
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=0)

        self.canvasWindow = canvas.create_window((0, 0), window=frame,
                                                 anchor="nw",
                                                 tags="self.__frame")

        # Bind the event handler to the desired events.
        frame.bind("<Configure>", self._onFrameConfigure)
        frame.bind('<Enter>', self._bindMousewheel)
        frame.bind('<Leave>', self._unbindMousewheel)

        # make sure the inner frame size is filled and updated if defined.
        self.defineCanvasFrameDimension(xmlFrame)
        self.setFrameDimensions()

#        self.populate(frame)

    def defineCanvasFrameDimension(self, xml):
        """
        Sets the Parameters to define the required Scrollbars.

        Parameters
        ----------
        xml : xml.etree.ElementTree
            The xml definitions of the frame which is the content container.
        """
        xmlDimension = xml.find("dimension")

        if "fill" in xmlDimension.attrib:
            if xmlDimension.attrib["fill"] == "both":
                self.__canvasFrameDimension = "both"
            elif xmlDimension.attrib["fill"] == "x":
                self.__canvasFrameDimension = "x"
            elif xmlDimension.attrib["fill"] == "y":
                self.__canvasFrameDimension = "y"

    def getCanvas(self):
        """
        Returns the Canvas Widget of the Scrollbar Extension.

        Returns
        -------
        ctsoft.gui.elements.TkCanvas : The canvas widget of the scrollbar
            extension.
        """
        return self.__canvas

    def getCanvasFrame(self):
        """
        Returns the Frame under the Canvas widget.

        Returns
        -------
        ctsoft.gui.elements.TkFrame : The frame widget which contains the
            scrollable content.
        """
        return self.__frame

    def getChangedParent(self):
        """
        Returns the changed Parent of the Scrollbar Extension which is the
        Frame which collects the scrollable Content.

        Returns
        -------
        object : A tkinter widget.
        """
        return self.__changedParent

    def getParent(self):
        """
        Returns the Parent of the Scrollbar Extension.

        Returns
        -------
        object : A tkinter widget.
        """
        return self.__parent

    def getScrollbar(self, orient):
        """
        Returns the Scrollbar with the requested Orientation.

        Returns
        -------
        ctsoft.gui.elements.TkScrollbar : The scrollbar widget or None if no
            one could be found.
        """
        return self.__scrollbars.get(orient, None)

    def getScrollbars(self):
        """
        Returns alll defined Scrollbar Widgets.

        Returns
        -------
        dictionary : All defined scrollbar widgets with their orientation
            as key.
        """
        return self.__scrollbars

    def getXmlContent(self):
        """
        Returns the XMl Defintions of the scrollable Content.

        Returns
        -------
        xml.etree.ElementTree : The XML defintions of the scrollable content.
        """
        return self.__xmlContent

    def handleContent(self, xml):
        """
        Searches the defined XML Content and sets it to the related Property.

        Parameters
        ----------
        xml : xml.etree.ElementTree
            The xml definitions of the scrollbar extension with the scrollable
            content.
        """
        self.setXmlContent(xml.find("content"))
        self.setChangedParent(self.getCanvasFrame())

    def setCanvas(self, canvas):
        """
        Sets the Canvas Widget of the Scrollbar Extension.

        Parameters
        ----------
        canvas : ctsoft.gui.elements.TkCanvas
            The canvas widget to set.
        """
        self.__canvas = canvas

    def setCanvasFrame(self, frame):
        """
        Sets the Canvas Frame Widget of the Scrollbar Extension which is the
        one with the Scrollbars and the scrollable Content.

        Parameters
        ----------
        frame : ctsoft.gui.elements.TkFrame
            The frame widget to set.
        """
        self.__frame = frame

    def setChangedParent(self, parent):
        """
        Sets the changed Parent.

        Parameters
        ----------
        parent : object
            The changed parent widget to set.
        """
        self.__changedParent = parent

    def setFrameDimensions(self):
        """
        Sets the Event Listener to update the Scrollbars if the Definitions are
        met.
        """
        if self.__canvasFrameDimension is not None:
            self.getCanvas().bind('<Configure>', self._onCanvasFrameDimension)

    def setXmlContent(self, xmlContent):
        """
        Sets the XML Definitions of the Scrollable Content.

        Parameters
        ----------
        xmlContent : xml.etree.ElementTree
            The XML defintions of the scrollable content.
        """
        self.__xmlContent = xmlContent

    def populate(self, parent):  # just for testing..
        """
        Populates the Parent Widget with test Content.
        This method is just for testing and should not be used for the
        application.

        Parameters
        ----------
        parent : object
            The parent widget which needs to be populated with test content.
        """
        for row in range(100):
            tk.Label(parent, text="%s" % row, width=3, borderwidth="1",
                     relief="solid").grid(row=row, column=0)
            t = "this is the second column for row %s" % row
            tk.Label(parent, text=t).grid(row=row, column=1)

    def _bindMousewheel(self, event):
        """
        Binds a Mousewheel Event Listener to the Canvas of the Scrollable
        Extension.

        Parameters
        ----------
        event : object
            The enter event of the canvas.
        """
        canvas = self.getCanvas()
        canvas.bind_all("<MouseWheel>", self._onMousewheel)

    def _onCanvasFrameDimension(self, event):
        """
        Event Handler of the Canvas resize.

        Parameters
        ----------
        event : object
            The resize event of the canvas.
        """
        canvas = self.getCanvas()
        frame = self.getCanvasFrame()

        canvasHeight = event.height
        canvasWidth = event.width

        # Get the new canvas dimensions
        if canvasWidth <= frame.winfo_reqwidth():
            canvasWidth = frame.winfo_reqwidth()
        if canvasHeight <= frame.winfo_reqheight():
            canvasHeight = frame.winfo_reqheight()

        if self.__canvasFrameDimension == "both":
            canvas.itemconfig(self.canvasWindow, height=canvasHeight,
                              width=canvasWidth)
        elif self.__canvasFrameDimension == "x":
            canvas.itemconfig(self.canvasWindow, width=canvasWidth)
        elif self.__canvasFrameDimension == "y":
            canvas.itemconfig(self.canvasWindow, height=canvasHeight)

    def _onFrameConfigure(self, event):
        """
        Event Configuration for the Scrollbars.

        Parameters
        ----------
        event : object
            The configure event of the canvas.
        """
        canvas = self.getCanvas()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def _onMousewheel(self, event):
        """
        Event Handler of the Mouse Wheel Event over the Canvas Widget.

        Parameters
        ----------
        event : object
            The mouse wheel event over the canvas widget.
        """
        canvas = self.getCanvas()
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _unbindMousewheel(self, event):
        """
        Removes the Event Handler of the Mouse Wheel Event over the Canvas
        Widget.

        Parameters
        ----------
        event : object
            The mouse wheel event over the canvas widget.
        """
        canvas = self.getCanvas()
        canvas.unbind_all("<MouseWheel>")


class ContainerTabs(object):
    """
    Extension to show Tabs.
    This Extension uses the ttk.Notebook Widget.

    Methods
    -------
    addTab :
        Adds a Tab to the notebook.
    createWidgets :
        Starting to build the notebook with tabs
    getBase :
        Returns the notebook widget.
    getParent :
        Returns the parent of the notebook widget.
    getParser :
        Returns the parser object.
    getXml :
        Returns the XML definitions of this notebook.
    manageLayout :
        Sets the defined layout manager, or an empty pack as default.
    setParent :
        Sets the parent of the notebook widget.
    setParser :
        Sets the parser.
    setXml :
        Sets the XML with the element definitions of the notebook.
    """
    def __init__(self, master, xml, *args, **kw):
        """
        Instanciates a ContainerTab.

        Parameters
        ----------
        master : object
            One of the Tkinter widget elements in this module as parent
            of the new notebook widget.
        element : xml.etree.ElementTree
            The element definitions of the new notebook.
        """
        print(*args)
        print(**kw)
        self.__base = None
        self.__parent = None
        self.__parser = None
        self.__tabs = {}
        self.__xml = None

        self.setParent(master)
        self.setXml(xml)

    def addTab(self, parent, xml):
        """
        Creates a Tab as defined and adds it to the Notebook Widget.

        Parameters
        ----------
        parent : ctsoft.gui.elements.TtkNotebook
            The notebook widget.
        """
        parser = self.getParser()
        xmlInner = xml.find("*")
        tab = parser.parseXml(xmlInner, parent)
        tabText = xml.attrib.get("text", "")
        parent.add(tab, text=tabText)

    def createWidgets(self):
        """ Creates the Notebook Widget with its Content. """
        xml = self.getXml()
        if str(xml.tag) != "tabs":
            # This error should not be raised if the process is comming from
            # the ctsoft.gui.xml.builder
            raise ValueError("The needed XML element is \"tabs\", ",
                             "found %s" % xml.tag)

        # Grab the parent of the notebook widget.
        parent = self.getParent()

        # create the notebook widget.
        self.__base = ctselttk.TtkNotebook(parent, xml)
        # layout manager
        self.manageLayout(self.__base, xml)

        xmlTabs = xml.findall("tab")

        if not xmlTabs:
            # if no tabs for the notebook were defined.
            # Therefor an empty notebook widget is not allowed.
            raise ValueError("No tabs found under the tabs element")

        for xmlTab in xmlTabs:
            # Create the tabs.
            self.addTab(self.__base, xmlTab)

    def getBase(self):
        """
        Returns the Notebook widget if it is already created.

        Returns
        -------
        ctsoft.gui.elements.TtkNotebook : The the notebook widget.
        """
        return self.__base

    def getParent(self):
        """
        Returns the Parent widget of the Notebook widget.

        Returns
        -------
        object : The parent widget of the notebook.
        """
        return self.__parent

    def getParser(self):
        """
        Returns the current XML Parser.

        Returns
        -------
        ctsoft.gui.xml.Parser : The XML Parser.
        """
        return self.__parser

    def getXml(self):
        """
        Returns the XML Definitions of the Notebook widget.

        Returns
        -------
        xml.etree.ElementTree : The parent widget of the notebook.
        """
        return self.__xml

    def manageLayout(self, widget, xml):
        """
        Sets the Layout Manager if defined. Default Manager is pack.

        Parameters
        ----------
        widget : object
            An extended tkinter widget which will be layout managed.
        xml : xml.etree.ElementTree
            The XML element of the current widget.
        """
        xmlGrid = xml.find("grid")

        if xmlGrid:
            # row- and column-configure is not implemented atm.
            widget.grid(xmlGrid.attrib)
        else:
            xmlPack = xml.find("pack")

            if xmlPack:
                # use the founded pack definitions
                widget.pack(xmlPack.attrib)
            else:
                # sue the pack manager as the default.
                widget.pack()

    def setParent(self, parent):
        """
        Sets the Parent widget of the Notebook widget.

        Parameters
        ----------
        parent : object
            The parent widget of the notebook.
        """
        self.__parent = parent

    def setParser(self, parser):
        """
        Sets the XML Parser.

        Parameters
        ----------
        xml : ctsoft.gui.xml.Parser
            The XML Parser.
        """
        self.__parser = parser

    def setXml(self, xml):
        """
        Sets the XML Definitions of the Notebook with its Content.

        Parameters
        ----------
        xml : xml.etree.ElementTree
            The XML definitions of the notebook and its content.
        """
        self.__xml = xml


class RadiobuttonGroup(object):
    """
    Handles a bundle of Radiobuttons.

    Methods
    -------
    createRadiobuttons :
        Creates the radiobutton group.
    createRadiobutton :
        Creates a single radiobutton.
    doNothing :
        This is a dummy method to make the radiobutton group working.
    getValue :
        Returns the selected value.
    """
    def __init__(self, master, element, *args, **kw):
        """
        Instanciates a RadiobuttonGroup.

        Parameters
        ----------
        master : object
            One of the Tkinter widget elements in this module as parent
            of the new RadiobuttonGroup.
        element : xml.etree.ElementTree
            The element definitions of the new RadiobuttonGroup.
        """

        """ list : Collection of tk.Radiobutton widgets. """
        self.__radios = []
        """ mixed : The value container as tk.IntVar() or tk.StringVar. """
        self.__variable = None

        self.createRadiobuttons(master, element)

    def createRadiobuttons(self, master, xml):
        """
        Creates a Radiobutton Group.
        All radiobutton elements beneath the group xml element will be created.

        Parameters
        ----------
        master : object
            The parent widget of the TkRadiobuttons.
        element : xml.etree.ElementTree
            Definitions of the Ra TkRadiobutton widget.
        """
        radios = xml.findall("radiobutton")
        if "variable-type" in xml.attrib and \
                xml.attrib["variable-type"] == "string":
            self.__variable = tk.StringVar()
        else:
            self.__variable = tk.IntVar()

        if "default-value" in xml.attrib:
            self.__variable.set(xml.attrib["default-value"])

        layoutType = "default"
        if "layout-type" in xml.attrib:
            layoutType = xml.attrib["layout-type"]

        for radio in radios:
            self.createRadiobutton(master, radio, layoutType)

    def createRadiobutton(self, master, xml, layoutType):
        """
        Creates a Single Radiobutton Widget and apends it to the radio
        collection.

        Parameters
        ----------
        master : object
            Parent Tkinter widget of this one.
        xml : xml.etree.ElementTree
            Definitions of the current TkRadiobutton widget.
        layoutType : string
            For "frame" the TkRadiobutton will have a surrounding tk.Frame.
        """
        if layoutType == "frame":
            # frameOptions = {"bg": "#FFFFFF", "padx": "5"}
            frame = tk.Frame(master)
            # frame = tk.Frame(master, frameOptions)
            framePack = {"expand": "True", "fill": "x", "side": "top"}
            frame.pack(framePack)

            radio = ctsel.TkRadiobutton(frame, xml)
        else:
            radio = ctsel.TkRadiobutton(master, xml)

        radio.configure(command=self.doNothing,
                        variable=self.__variable)
        packOptions = {}
        pack = xml.findall("pack")
        if pack:
            for option in pack[0].attrib:
                packOptions[option] = pack[0].attrib[option]
        else:
            packOptions = {"expand": "True", "fill": "x", "side": "left"}
        radio.pack(packOptions)
        self.__radios.append(radio)

    def doNothing(self):
        """
        This is a dummy.
        Without setting a command for the radio, the radios behave crazy.
        """
        pass

    def getValue(self):
        """
        Returns the Value of the selected Radiobutton.

        Returns
        -------
        mixed : The value of the selected Radiobutton widget as tk.IntVar.get()
            or tk.StringVar.get().
        """
        return self.__variable.get()
