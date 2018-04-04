# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 18:03:52 2018

@author: ctsoft
"""

import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter.font import Font as tkFont
#from tkinter.filedialog import askopenfilename


class TkBase(object):
    def __init__(self):
        super(TkBase, self).__init__()
        self.__numerics = ["bd", "height", "ipadx", "ipady", "maxsize-x",
                           "maxsize-y", "minsize-x", "minsize-y", "padx",
                           "pady", "xscrollincrement", "yscrollincrement",
                           "width", "wraplength"]
        self.methodTo2Options = {}
        self.methodTo1Option = {}
        self.__id = ""
        self.__font = False
        self.__photoImage = {}
        self.setOrganizeType("pack")
        self.setOrganizeTypeChildren("pack")

    def createPhotoImage(self, path, dimension={}):
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
        return self.__font

    def getOrganizeType(self):
        return self.__organizeType

    def getOrganizeTypeChildren(self):
        return self.__organizeTypeChildren

    def getPhotoImage(self):
        return self.__photoImage

    def handle1ParamMethods(self, element, remove=True):
        for method in self.methodTo1Option:
            method_ = getattr(self, method)
            method_(element.attrib[method])
            if remove:
                del element.attrib[method]

    def handle2ParamMethods(self, element, remove=True):
        for method in self.methodTo2Options:
            if self.methodTo2Options[method][0] in element.attrib and \
                    self.methodTo2Options[method][1] in element.attrib:
                method_ = getattr(self, method)
                method_(element.attrib[self.methodTo2Options[method][0]],
                        element.attrib[self.methodTo2Options[method][1]])
                if remove:
                    del element.attrib[self.methodTo2Options[method][0]]
                    del element.attrib[self.methodTo2Options[method][1]]
            elif self.methodTo2Options[method][0] in element.attrib:
                method_ = getattr(self, method)
                method_(element.attrib[self.methodTo2Options[method][0]])
                if remove:
                    del element.attrib[self.methodTo2Options[method][0]]
            elif self.methodTo2Options[method][1] in element.attrib:
                method_ = getattr(self, method)
                method_(element.attrib[self.methodTo2Options[method][1]])
                if remove:
                    del element.attrib[self.methodTo2Options[method][1]]

    def setFont(self, font):
        self.__font = font

    def setOptions(self, options):
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
        self.__organizeType = organizeType

    def setOrganizeTypeChildren(self, organizeTypeChildren):
        self.__organizeTypeChildren = organizeTypeChildren

    def setPhotoImage(self, photoImage):
        self.__photoImage = photoImage

    def setRows(self, rows):
        for row in rows:
            num = row.attrib["num"]
            del row.attrib["num"]
            self.rowconfigure(num, row.attrib)


class TkWidget(TkBase):
    def __init__(self, master, element):
        super(TkWidget, self).__init__()
        self.__parent = None
        self.setParent(master)

    def createImage(self, xml):
        dimension = {}
        if "height" in xml:
            dimension["height"] = xml["height"]
        if "width" in xml:
            dimension["width"] = xml["width"]

        self.createPhotoImage(xml["path"], dimension)

    def getParent(self):
        return self.__parent

    def getSelf(self):
        return self

    def organize(self, element):
        pack = element.findall("pack")
        grid = element.findall("grid")
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
        self.createImage(xml.attrib)
        self.image = self.getPhotoImage()

    def setParent(self, parent):
        self.__parent = parent


class TkWidgetSimple(TkWidget):
    def __init__(self, master, element):
        super(TkWidgetSimple, self).__init__(master, element)
        if element:
            self.setOptions(element.attrib)
            self.organize(element)


class TkButton(tk.Button, TkWidgetSimple):
    def __init__(self, master, *args, **kw):
        tk.Button.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)
#        super(TkButton, self).__init__(self, master, *args, **kw)


class TkCanvas(tk.Canvas, TkWidgetSimple):
    def __init__(self, master, *args, **kw):
        tk.Canvas.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)

    def setImage(self, xml):
        self.createImage(xml.attrib)
        img = self.getPhotoImage()
        xVal = int(xml.attrib.get("x", "0"))
        yVal = int(xml.attrib.get("y", "0"))
        anchor = xml.attrib.get("anchor", "nw")
        self.create_image(xVal, yVal, image=img, anchor=anchor)


class TkCheckbutton(tk.Checkbutton, TkWidgetSimple):
    def __init__(self, master, *args, **kw):
        tk.Checkbutton.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)


class TkEntry(tk.Entry, TkWidgetSimple):
    def __init__(self, master, *args, **kw):
        tk.Entry.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)


class TkFrame(tk.Frame, TkWidgetSimple):
    def __init__(self, master, *args, **kw):
        tk.Frame.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)


class TkLabel(tk.Label, TkWidgetSimple):
    def __init__(self, master, *args, **kw):
        tk.Label.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)


class TkLabelFrame(tk.LabelFrame, TkWidgetSimple):
    def __init__(self, master, *args, **kw):
        tk.LabelFrame.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)


class TkListbox(tk.Listbox, TkWidgetSimple):
    def __init__(self, master, *args, **kw):
        tk.Listbox.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)


class TkMenu(tk.Menu, TkWidgetSimple):
    def __init__(self, master, *args, **kw):
        tk.Menu.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)


class TkOptionMenu(tk.OptionMenu, TkWidgetSimple):
    def __init__(self, master, *args, **kw):
        tk.OptionMenu.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)


class TkRadiobutton(tk.Radiobutton, TkWidgetSimple):
    def __init__(self, master, *args, **kw):
        tk.Radiobutton.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)


class TkScale(tk.Scale, TkWidgetSimple):
    def __init__(self, master, *args, **kw):
        tk.Scale.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)


class TkText(tk.Text, TkWidgetSimple):
    def __init__(self, master, *args, **kw):
        tk.Text.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)


class TkWindow(tk.Tk, TkBase):
    def __init__(self, element, *args, **kw):
        tk.Tk.__init__(self)
        TkBase.__init__(self)
        self.methodTo1Option = {"title": "title"}
        self.methodTo2Options = {"maxsize": ("maxsize-x", "maxsize-y"),
                                 "minsize": ("minsize-x", "minsize-y"),
                                 "resizeable": ("resizeable-x",
                                                "resizeable-y")}
        self.setOptions(element)

    def setOptions(self, element):
        self.handle1ParamMethods(element)
        self.handle2ParamMethods(element)

        TkBase.setOptions(self, element.attrib)


class RadiobuttonGroup(object):
    def __init__(self, master, element, *args, **kw):
        self.__radios = []
        self.__variable = None
        self.createRadiobuttons(master, element)

    def createRadiobuttons(self, master, element):
        radios = element.findall("radiobutton")
        if "variable-type" in element.attrib and \
                element.attrib["variable-type"] == "string":
            self.__variable = tk.StringVar()
        else:
            self.__variable = tk.IntVar()

        if "default-value" in element.attrib:
            self.__variable.set(element.attrib["default-value"])

        layoutType = "default"
        if "layout-type" in element.attrib:
            layoutType = element.attrib["layout-type"]

        for radio in radios:
            self.createRadiobutton(master, radio, layoutType)

    def createRadiobutton(self, master, element, layoutType):
        if layoutType == "frame":
#            frameOptions = {"bg": "#FFFFFF", "padx": "5"}
            frame = tk.Frame(master)
#            frame = tk.Frame(master, frameOptions)
            framePack = {"expand": "True", "fill": "x", "side": "top"}
            frame.pack(framePack)

            radio = TkRadiobutton(frame, element)
        else:
            radio = TkRadiobutton(master, element)
        radio.configure(command=self.doNothing,
                        variable=self.__variable)
        packOptions = {}
        pack = element.findall("pack")
        if pack:
            for option in pack[0].attrib:
                packOptions[option] = pack[0].attrib[option]
        else:
            packOptions = {"expand": "True", "fill": "x", "side": "left"}
        radio.pack(packOptions)
        self.__radios.append(radio)

    def doNothing(self):
        # Without setting a command for the radio, the radios behave crazy
        pass

    def getValue(self):
        return self.__variable.get()
