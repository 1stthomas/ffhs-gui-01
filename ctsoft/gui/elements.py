# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 18:03:52 2018

@author: ctsoft
"""

import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter.font import Font as tkFont


class TkBase(object):
    """
    The Base Object of the Tkinter Extensions.
    Provides methods to set properties, handles methods comming as Options,
    create photo images.

    Methods
    -------
    createPhotoImage :
        Creates a PIL PhotoImage and sets it on itself.
    getFont :
        Returns the font of the current widget.
    getOrganizeType :
        Returns the organize type of the current widget.
    getOrganizeTypeChildren :
        Returns the organize type of the children.
    getPhotoImage :
        Returns the PIL PhotoImage or None.
    handle1ParamMethods :
        Handles the defined 1 parameter method settings.
    handle2ParamMethods :
        Handles the defined 2 parameter method settings.
    setFont :
        Sets the font of the current widget.
    setOptions :
        Sets the options defined on the XML element.
    setOrganizeType :
        Sets the organize type of the current widget.
    setOrganizeTypeChildren :
        Sets the organize type of the children.
    setPhotoImage :
        Sets the PIL PhotoImage.
    setRows :
        Configures the rows by the grid manager.

    Attributes
    ----------
    methodTo1Option : dict
        Definitions, which attributes of the xml element will be called as
        a 1 parameter method.
    methodTo2Options : dict
        Definitions, which attributes of the xml element will be called as
        a 2 parameter method.
    """

    def __init__(self):
        """
        Instanciates a TkBase.

        Parameters
        ----------
        master : xml.etree.ElementTree
            The element definitions of the new TkBase.
        element : xml.etree.ElementTree
            The element definitions of the new TkBase.
        """
        super(TkBase, self).__init__()

        """ string : The font of the current instance. """
        self.__font = False
        """ string : The id of the current instance. """
        self.__id = ""
        """ list : Properties which will be prototyped to int. """
        self.__numerics = ["bd", "height", "ipadx", "ipady", "maxsize-x",
                           "maxsize-y", "minsize-x", "minsize-y", "padx",
                           "pady", "xscrollincrement", "yscrollincrement",
                           "width", "wraplength"]
        """ mixed : A PIL ImageTk.PhotoImage or None. """
        self.__photoImage = None
        self.methodTo1Option = {}
        self.methodTo2Options = {}

        self.setOrganizeType("pack")
        self.setOrganizeTypeChildren("pack")

    def createPhotoImage(self, path, dimension={}):
        """
        Creates a PIL PhotoImage which can be accessed by calling
        getPhotoImage() of the Instance with the requested Image.

        Parameters
        ----------
        path : string
            The path to the image file.
        dimension : dict
            the width and height of the PhotoImage.
        """
        pathSanitized = path
        if path[0] == "/":
            # it is a relative path
            pathSanitized = os.getcwd() + path
        img = Image.open(pathSanitized)
        width = int(dimension.get("width", 0))
        height = int(dimension.get("height", 0))

        if width > 0 or height > 0:
            # image resizing needed
            if width > 0 and height > 0:
                img = img.resize((width, height), Image.ANTIALIAS)
            elif width > 0:
                height = int(round(img.height * width / img.width))
                img = img.resize((width, height), Image.ANTIALIAS)
            elif height > 0:
                width = int(round(img.width * height / img.height))
                img = img.resize((width, height), Image.ANTIALIAS)
        photoImage = ImageTk.PhotoImage(img)
        self.setPhotoImage(photoImage)

    def getFont(self):
        """
        Returns the Font of the current Instance.

        Returns
        -------
        string : The font of the current instance.
        """
        return self.__font

    def getOrganizeType(self):
        """
        Returns the Organize Type of the current Instance.

        Returns
        -------
        string : The organize type of the current instance.
        """
        return self.__organizeType

    def getOrganizeTypeChildren(self):
        """
        Returns the Organize Type of the Children of the current Instance.

        Returns
        -------
        string : The organize type of the Children of the current instance.
        """
        return self.__organizeTypeChildren

    def getPhotoImage(self):
        """
        Returns the PhotoImage.

        Returns
        -------
        object : A PIL PhotoImage or None.
        """
        return self.__photoImage

    def handle1ParamMethods(self, xml, remove=True):
        """
        Tries to call all defined 1 Parameter Methods.

        Parameters
        ----------
        xml : xml.etree.ElementTree
            The XML definition of the current GUI element.
        remove : boolean
            If True, the attribtes which define a 1 parameter method will
                be removed from the xml element.
        """
        for method in self.methodTo1Option:
            method_ = getattr(self, method)
            method_(xml.attrib[method])
            if remove:
                del xml.attrib[method]

    def handle2ParamMethods(self, xml, remove=True):
        """
        Tries to call all defined 2 PArameter Methods.

        Parameters
        ----------
        xml : xml.etree.ElementTree
            The XML definition of the current GUI element.
        remove : boolean
            If True, the attribtes which define a 1 parameter method will
                be removed from the xml element.
        """
        for method in self.methodTo2Options:
            if self.methodTo2Options[method][0] in xml.attrib and \
                    self.methodTo2Options[method][1] in xml.attrib:
                method_ = getattr(self, method)
                method_(xml.attrib[self.methodTo2Options[method][0]],
                        xml.attrib[self.methodTo2Options[method][1]])
                if remove:
                    del xml.attrib[self.methodTo2Options[method][0]]
                    del xml.attrib[self.methodTo2Options[method][1]]
            elif self.methodTo2Options[method][0] in xml.attrib:
                method_ = getattr(self, method)
                method_(xml.attrib[self.methodTo2Options[method][0]])
                if remove:
                    del xml.attrib[self.methodTo2Options[method][0]]
            elif self.methodTo2Options[method][1] in xml.attrib:
                method_ = getattr(self, method)
                method_(xml.attrib[self.methodTo2Options[method][1]])
                if remove:
                    del xml.attrib[self.methodTo2Options[method][1]]

    def setFont(self, font):
        """
        Sets the font of the current Tkinter widget.

        Parameters
        ----------
        font : string
            The font definition.
        """
        self.__font = font

    def setOptions(self, options):
        """
        Sets the submitted Options to the current Tkinter Widget.

        Parameters
        ----------
        options : dict
            A dictonary with the key as the property name and the value as
            the property value.
        """
        for key in options:
            if key == "id":
                self.__id = options[key]
            elif key == "font":
                opts = options[key].replace("'", "").split(", ")
                d = {}
                for opt in opts:
                    arr = opt.split(": ")
                    d[arr[0]] = arr[1]
                self.__font = tkFont(**d)
                self.configure(font=self.__font)
            elif key == "textvariable":
                self[key] = tk.StringVar(value=options[key])
            elif key in self.__numerics:
                self[key] = int(options[key])
            else:
                self[key] = options[key]

    def setOrganizeType(self, organizeType):
        """
        Sets the Organize Type of the current Tkinter Widget.

        Parameters
        ----------
        organizeType : string
            A shot form of the layout manager of the current Tkinter widget.
            Accepted values: "", "pack", "grid".
        """
        self.__organizeType = organizeType

    def setOrganizeTypeChildren(self, organizeTypeChildren):
        """
        Sets the Organize Type of the Children of the current Tkinter Widget.

        Parameters
        ----------
        organizeTypeChildren : string
            A shot form of the layout manager of the children of the
            current Tkinter widget. Accepted values: "", "pack", "grid".
        """
        self.__organizeTypeChildren = organizeTypeChildren

    def setPhotoImage(self, photoImage):
        """
        Sets the PhotoImage of the current Tkinter Widget.

        Parameters
        ----------
        photoImage : object
            a PIL photoImage instance.
        """
        self.__photoImage = photoImage

    def setRows(self, rows):
        """
        Configures the Row definition of a grid managed Tkinter Widget by
        calling the rowconfigure() Method.

        Parameters
        ----------
        rows : xml.etree.ElementTree
            A row element with the attributes to match the rowconfigure().
        """
        for row in rows:
            num = row.attrib["num"]
            del row.attrib["num"]
            self.rowconfigure(num, row.attrib)


class TkWidget(TkBase):
    """
    Extends TkBase.
    Implements a method to store the parent widget which is called on
    initialization.

    Methods
    -------
    createImage :
        Creates a PIL PhotoImage with predefined attributes.
    getParent :
        Returns the parent of the current widget.
    getSelf :
        Returns itself.
    organize :
        Calls the layout manager on the current widget.
    setImage :
        Sets a PIL PhotoImage.
    setParent :
        Sets the parent of the current widget.
    """

    def __init__(self, master, element):
        """
        Instanciates a TkWidget.

        Parameters
        ----------
        master : xml.etree.ElementTree
            The element definitions of the new TkWidget.
        element : xml.etree.ElementTree
            The element definitions of the new TkWidget.
        """
        super(TkWidget, self).__init__()

        """ object : The parent element of the current widget. """
        self.__parent = None
        self.setParent(master)

    def createImage(self, xml):
        """
        Creates a PIL PhotoImage from an XML Object with the definied
        dimensions.

        Parameters
        ----------
        xml : xml.etree.ElementTree
            An image xml element with a path attribute and
            optional dimension attributes.
        """
        dimension = {}
        if "height" in xml:
            dimension["height"] = xml["height"]
        if "width" in xml:
            dimension["width"] = xml["width"]

        self.createPhotoImage(xml["path"], dimension)

    def getParent(self):
        """
        Returns the Parent Tkinter Widget of the current Widget.

        Returns
        -------
        __parent : object
            The parent Tkinter widget of the current one.
        """
        return self.__parent

    def getSelf(self):
        """
        Returns the current Tkinter Widget.

        Returns
        -------
        self : object
            The current Tkinter widget.
        """
        return self

    def organize(self, xml):
        """
        Configures the Layout Manager of the current Tkinter widget.
        This is done by calling pack() for the pack layout manager, or
        columnconfigure() and setting the organize type of the current and
        its children for the grid layout manager.

        Parameters
        ----------
        xml : xml.etree.ElementTree
            The XML element of the layout manager. Supported layout managers:
                - pack
                - grid
        """
        pack = xml.findall("pack")
        grid = xml.findall("grid")
        if pack:
            self.pack(pack[0].attrib)
        elif grid:
            self.grid(grid[0].attrib)
            parent = self.getParent()
            parentAttr = grid[0].findall("column")[0]
            num = parentAttr.attrib["num"]
            del parentAttr.attrib["num"]
            parent.columnconfigure(num, parentAttr.attrib)
            self.setOrganizeType("grid")
            parent.setOrganizeTypeChildren("grid")

    def setImage(self, xml):
        """
        Creates a PIL PhotoImage and sets it to the current Tkinter Widget.

        Parameters
        ----------
        xml : xml.etree.ElementTree
            A XML element with the image definitions.
        """
        self.createImage(xml.attrib)
        self.image = self.getPhotoImage()

    def setParent(self, parent):
        """
        Sets the Parent of the current Tkinter Widget.

        Parameters
        ----------
        parent : object
            The parent widget of the current Tkinter widget.
        """
        self.__parent = parent


class TkWidgetSimple(TkWidget):
    """
    Extends TkWidget.
    If the submitted element is not an empty dict the following methods are
    executed:
        - setOptions(xml.attrib)
        - organize(xml)
    """

    def __init__(self, master, element):
        """
        Instanciates a TkWidgetSimple.

        Parameters
        ----------
        master : xml.etree.ElementTree
            The element definitions of the new TkWidgetSimple.
        element : xml.etree.ElementTree
            The element definitions of the new TkWidgetSimple.
        """
        super(TkWidgetSimple, self).__init__(master, element)

        if element:
            self.setOptions(element.attrib)
            self.organize(element)


class TkButton(tk.Button, TkWidgetSimple):
    """
    Extends tk.Button and TkWidgetSimple.
    This Object is an Extension of the Tkinter Button Widget which is needed
    to make it possible to build a GUI with XML Definitions.
    """

    def __init__(self, master, *args, **kw):
        """
        Instanciates a TkButton.

        Parameters
        ----------
        master : xml.etree.ElementTree
            The element definitions of the new TkButton.
        """
        tk.Button.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)
#        super(TkButton, self).__init__(self, master, *args, **kw)


class TkCanvas(tk.Canvas, TkWidgetSimple):
    """
    Extends tk.Button and TkWidgetSimple.
    This Object is an Extension of the Tkinter Button Widget which is needed
    to make it possible to build a GUI with XML Definitions.
    This extension implements a method to add an image.

    Methods
    -------
    setImage :
        Sets an PIL PhotoImage and displays it.
    """

    def __init__(self, master, *args, **kw):
        """
        Instanciates a TkCanvas.

        Parameters
        ----------
        master : xml.etree.ElementTree
            The element definitions of the new TkCanvas.
        """
        tk.Canvas.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)

    def setImage(self, xml):
        """
        Adds an Image to the Canvas Widget.

        Parameters
        ----------
        xml : xml.etree.ElementTree
            An image XML element with following optional attributes:
                - x : The margin to the left border of the image.
                - y : The margin to the top border of the image.
                - anchor : The horizontal and vertical alignment of the image.
        """
        self.createImage(xml.attrib)

        img = self.getPhotoImage()
        xVal = int(xml.attrib.get("x", "0"))
        yVal = int(xml.attrib.get("y", "0"))
        anchor = xml.attrib.get("anchor", "nw")
        self.create_image(xVal, yVal, image=img, anchor=anchor)


class TkCheckbutton(tk.Checkbutton, TkWidgetSimple):
    """
    Extends tk.Checkbutton and TkWidgetSimple.
    This Object is an Extension of the Tkinter Checkbutton Widget which is
    needed to make it possible to build a GUI with XML Definitions.
    """

    def __init__(self, master, *args, **kw):
        """
        Instanciates a TkCheckbutton.

        Parameters
        ----------
        master : xml.etree.ElementTree
            The element definitions of the new TkCheckbutton.
        """
        tk.Checkbutton.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)


class TkEntry(tk.Entry, TkWidgetSimple):
    """
    Extends tk.Entry and TkWidgetSimple.
    This Object is an Extension of the Tkinter Entry Widget which is
    needed to make it possible to build a GUI with XML Definitions.
    """

    def __init__(self, master, *args, **kw):
        """
        Instanciates a TkEntry.

        Parameters
        ----------
        master : xml.etree.ElementTree
            The element definitions of the new TkEntry.
        """
        tk.Entry.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)


class TkFrame(tk.Frame, TkWidgetSimple):
    """
    Extends tk.Frame and TkWidgetSimple.
    This Object is an Extension of the Tkinter Frame Widget which is
    needed to make it possible to build a GUI with XML Definitions.
    """

    def __init__(self, master, *args, **kw):
        """
        Instanciates a TkFrame.

        Parameters
        ----------
        master : xml.etree.ElementTree
            The element definitions of the new TkFrame.
        """
        tk.Frame.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)


class TkLabel(tk.Label, TkWidgetSimple):
    """
    Extends tk.Label and TkWidgetSimple.
    This Object is an Extension of the Tkinter Label Widget which is
    needed to make it possible to build a GUI with XML Definitions.
    """

    def __init__(self, master, *args, **kw):
        """
        Instanciates a TkLabel.

        Parameters
        ----------
        master : xml.etree.ElementTree
            The element definitions of the new TkLabel.
        """
        tk.Label.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)


class TkLabelFrame(tk.LabelFrame, TkWidgetSimple):
    """
    Extends tk.LabelFrame and TkWidgetSimple.
    This Object is an Extension of the Tkinter LabelFrame Widget which is
    needed to make it possible to build a GUI with XML Definitions.
    """

    def __init__(self, master, *args, **kw):
        """
        Instanciates a TkLabelFrame.

        Parameters
        ----------
        master : xml.etree.ElementTree
            The element definitions of the new TkLabelFrame.
        """
        tk.LabelFrame.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)


class TkListbox(tk.Listbox, TkWidgetSimple):
    """
    Extends tk.Listbox and TkWidgetSimple.
    This Object is an Extension of the Tkinter Listbox Widget which is
    needed to make it possible to build a GUI with XML Definitions.
    """

    def __init__(self, master, *args, **kw):
        """
        Instanciates a TkListbox.

        Parameters
        ----------
        master : xml.etree.ElementTree
            The element definitions of the new TkListbox.
        """
        tk.Listbox.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)


class TkMenu(tk.Menu, TkWidgetSimple):
    """
    Extends tk.Menu and TkWidgetSimple.
    This Object is an Extension of the Tkinter Menu Widget which is
    needed to make it possible to build a GUI with XML Definitions.
    """

    def __init__(self, master, *args, **kw):
        """
        Instanciates a TkMenu.

        Parameters
        ----------
        master : xml.etree.ElementTree
            The element definitions of the new TkMenu.
        """
        tk.Menu.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)


class TkOptionMenu(tk.OptionMenu, TkWidgetSimple):
    """
    Extends tk.OptionMenu and TkWidgetSimple.
    This Object is an Extension of the Tkinter OptionMenu Widget which is
    needed to make it possible to build a GUI with XML Definitions.
    """

    def __init__(self, master, *args, **kw):
        """
        Instanciates a TkOptionMenu.

        Parameters
        ----------
        master : xml.etree.ElementTree
            The element definitions of the new TkOptionMenu.
        """
        tk.OptionMenu.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)


class TkRadiobutton(tk.Radiobutton, TkWidgetSimple):
    """
    Extends tk.Radiobutton and TkWidgetSimple.
    This Object is an Extension of the Tkinter Radiobutton Widget which is
    needed to make it possible to build a GUI with XML Definitions.
    """

    def __init__(self, master, *args, **kw):
        """
        Instanciates a TkRadiobutton.

        Parameters
        ----------
        master : xml.etree.ElementTree
            The element definitions of the new TkRadiobutton.
        """
        tk.Radiobutton.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)


class TkScale(tk.Scale, TkWidgetSimple):
    """
    Extends tk.Scale and TkWidgetSimple.
    This Object is an Extension of the Tkinter Scale Widget which is
    needed to make it possible to build a GUI with XML Definitions.
    """

    def __init__(self, master, *args, **kw):
        """
        Instanciates a TkScale.

        Parameters
        ----------
        master : xml.etree.ElementTree
            The element definitions of the new TkScale.
        """
        tk.Scale.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)


class TkScrollbar(tk.Scrollbar, TkWidgetSimple):
    """
    Extends tk.Scrollbar and TkWidgetSimple.
    This Object is an Extension of the Tkinter Scrollbar Widget which is
    needed to make it possible to build a GUI with XML Definitions.
    """

    def __init__(self, master, *args, **kw):
        """
        Instanciates a TkScrollbar.

        Parameters
        ----------
        master : xml.etree.ElementTree
            The element definitions of the new TkScrollbar.
        """
        tk.Scrollbar.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)


class TkText(tk.Text, TkWidgetSimple):
    """
    Extends tk.Text and TkWidgetSimple.
    This Object is an Extension of the Tkinter Text Widget which is
    needed to make it possible to build a GUI with XML Definitions.
    """

    def __init__(self, master, *args, **kw):
        """
        Instanciates a TkText.

        Parameters
        ----------
        master : xml.etree.ElementTree
            The element definitions of the new TkText.
        """
        tk.Text.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)


class TkWindow(tk.Tk, TkBase):
    """
    Extends tk.Tk and TkBase.
    This Object is an Extension of the Tkinter Root window which is
    needed to make it possible to build a GUI with XML Definitions.
    The setOptions method of the TkBase class is overriden by also handling
    the method parameters.

    Methods
    -------
    setOptions :
        Sets the defined options and respects defined method options.
    """

    def __init__(self, element, *args, **kw):
        """
        Instanciates a TkWindow.

        Parameters
        ----------
        element : xml.etree.ElementTree
            The element definitions of the new TkWindow.
        """
        tk.Tk.__init__(self)
        TkBase.__init__(self)
        self.methodTo1Option = {"title": "title"}
        self.methodTo2Options = {"maxsize": ("maxsize-x", "maxsize-y"),
                                 "minsize": ("minsize-x", "minsize-y"),
                                 "resizeable": ("resizeable-x",
                                                "resizeable-y")}
        self.setOptions(element)

    def setOptions(self, xml):
        """
        Overrides TkBase.setOptions() by calling following method sequence:
            handle1ParamMethods
            handle2ParamMethods
            TkBase.setOptions

        @Todo: Should be the TkBase.setOptions()!!
        """
        self.handle1ParamMethods(xml)
        self.handle2ParamMethods(xml)

        TkBase.setOptions(self, xml.attrib)


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

            radio = TkRadiobutton(frame, xml)
        else:
            radio = TkRadiobutton(master, xml)

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
        self.__content = None
        self.__parent = parent

        self.createWidgets(xml)

    def createScrollbarWidget(self, parent, canvas, xml):
        sb = TkScrollbar(parent, xml)
        orientation = getattr(self.canvas, "orient", "vertical")
        if orientation == "vertical":
            xml.attrib["orient"] = "vertical"
            self.canvas.configure(yscrollcommand=sb.set)
            sb.configure(command=self.canvas.yview)
        else:
            self.canvas.configure(xscrollcommand=sb.set)
            sb.configure(command=self.canvas.xview)
        return sb

    def createWidgets(self, xml):
        parent = self.getParent()
        xmlSetup = xml.find("setup")
        xmlCanvas = xmlSetup.find("canvas")
        self.canvas = TkCanvas(parent, xmlCanvas)
        self.canvas.pack(self.getPackOptions(xmlCanvas))
        xmlFrame = xmlCanvas.find("frame")
        frame = TkFrame(self.canvas, xmlFrame)

        xmlScrollbars = xmlSetup.findall("scrollbar")
        for xmlScrollbar in xmlScrollbars:
            sb = self.createScrollbarWidget(parent, self.canvas, xmlScrollbar)
            sb.pack(self.getPackOptions(xmlScrollbar))

        self.canvas.create_window((0,0), window=frame,
                                  anchor="nw", tags="frame")
        frame.bind("<Configure>", self.onFrameConfigure)

        self.populate(frame)
        self.setContent({})

    def getPackOptions(self, xmlWidget):
        packOptions = xmlWidget.find("pack")
        if packOptions:
            return packOptions
        else:
            packOptions = {}

        if xmlWidget.tag == "canvas":
            packOptions["expand"] = "True"
            packOptions["fill"] = "both"
            packOptions["side"] = "left"
        elif xmlWidget.tag == "frame":
            packOptions["expand"] = "True"
            packOptions["fill"] = "both"
            packOptions["side"] = "top"
        elif xmlWidget.tag == "scrollbar":
            if xmlWidget.attrib["orient"] == "vertical":
#            if getattr(xmlWidget.attrib, "orient") == "vertical":
                packOptions["fill"] = "y"
                packOptions["side"] = "right"
            else:
                packOptions["fill"] = "x"
                packOptions["side"] = "left"

        return packOptions

    def getContent(self):
        return self.__content

    def getParent(self):
        return self.__parent

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def setContent(self, xml):
        self.__content = xml

    def populate(self, frame):  # just for testing..
        for row in range(100):
            tk.Label(frame, text="%s" % row, width=3, borderwidth="1",
                     relief="solid").grid(row=row, column=0)
            t = "this is the second column for row %s" %row
            tk.Label(frame, text=t).grid(row=row, column=1)
