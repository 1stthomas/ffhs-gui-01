# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 21:41:25 2018

@author: zoom4u
"""

import tkinter as tk
import ctsoft.gui.elements as ctsel


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

    Properties
    ----------
    __radios : list
        Collection of tk.Radiobutton widgets.
    __variable : mixed
        The value container as tk.IntVar() or tk.StringVar.
    """
    def __init__(self, master, element, *args, **kw):
        """
        Instanciates a RadiobuttonGroup.

        Parameters
        ----------
        master : object
            One of the Tkinter widget extensions in this module as parent
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


class ContainerScrollable(object):
    def __init__(self, parent, xml, *args, **kw):
        self.__canvas = None
        self.__canvasFrameDimension = None
        self.__content = None
        self.__frame = None
        self.__parent = parent
        self.__scrollbars = {}

        self.createWidgets(xml)

    def addScrollbar(self, orient, scrollbar):
        self.__scrollbars[orient] = scrollbar

    def createCanvas(self, parent, xmlCanvas):
        canvas = ctsel.TkCanvas(parent, xmlCanvas)
        canvas.grid(column=0, row=0, sticky="nwse")
        self.setCanvas(canvas)

        return canvas

    def createCanvasFrame(self, parent, xml):
        frame = ctsel.TkFrame(parent, xml)
        self.setCanvasFrame(frame)

        return frame

    def createScrollbarWidget(self, parent, xml):
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
        parent = self.getParent()
        xmlSetup = xml.find("setup")

        xmlCanvas = xmlSetup.find("canvas")
        canvas = self.createCanvas(parent, xmlCanvas)

        xmlFrame = xmlCanvas.find("frame")
        frame = self.createCanvasFrame(canvas, xmlFrame)

        xmlScrollbars = xmlSetup.findall("scrollbar")
        for xmlScrollbar in xmlScrollbars:
            self.createScrollbarWidget(parent, xmlScrollbar)

        # Define the row and column behavior on resizing.
        parent.rowconfigure(0, weight=1)
        parent.rowconfigure(1, weight=0)
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=0)

        self.canvasWindow = canvas.create_window((0, 0), window=frame,
                                                 anchor="nw",
                                                 tags="self.__frame")

        frame.bind("<Configure>", self.onFrameConfigure)
        frame.bind('<Enter>', self._bindMousewheel)
        frame.bind('<Leave>', self._unbindMousewheel)

        # make sure the inner frames size is filled and updated if defined.
        self.defineCanvasFrameDimension(xmlFrame)
        self.setFrameDimensions(frame, xmlFrame)

        self.populate(frame)
        self.setContent({})

    def defineCanvasFrameDimension(self, xml):
        xmlDimension = xml.find("dimension")

        if "fill" in xmlDimension.attrib:
            if xmlDimension.attrib["fill"] == "both":
                self.__canvasFrameDimension = "both"
            elif xmlDimension.attrib["fill"] == "x":
                self.__canvasFrameDimension = "x"
            elif xmlDimension.attrib["fill"] == "y":
                self.__canvasFrameDimension = "y"

    def getCanvas(self):
        return self.__canvas

    def getCanvasFrame(self):
        return self.__frame

    def getContent(self):
        return self.__content

    def getParent(self):
        return self.__parent

    def getScrollbar(self, orient):
        return self.__scrollbars.get(orient, None)

    def getScrollbars(self):
        return self.__scrollbars

    def onCanvasFrameDimension(self, event):
        canvas = self.getCanvas()
        frame = self.getCanvasFrame()

        canvasHeight = event.height
        canvasWidth = event.width

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

    def onFrameConfigure(self, event):
        self.getCanvas().configure(scrollregion=self.__canvas.bbox("all"))

    def setCanvas(self, canvas):
        self.__canvas = canvas

    def setCanvasFrame(self, frame):
        self.__frame = frame

    def setContent(self, xml):
        self.__content = xml

    def setFrameDimensions(self, frame, xml):
        if self.__canvasFrameDimension is not None:
            self.getCanvas().bind('<Configure>', self.onCanvasFrameDimension)

    def populate(self, parent):  # just for testing..
        for row in range(100):
            tk.Label(parent, text="%s" % row, width=3, borderwidth="1",
                     relief="solid").grid(row=row, column=0)
            t = "this is the second column for row %s" % row
            tk.Label(parent, text=t).grid(row=row, column=1)

    def _bindMousewheel(self, event):
        canvas = self.getCanvas()
        canvas.bind_all("<MouseWheel>", self._onMousewheel)

    def _onMousewheel(self, event):
        canvas = self.getCanvas()
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _unbindMousewheel(self, event):
        canvas = self.getCanvas()
        canvas.unbind_all("<MouseWheel>")
