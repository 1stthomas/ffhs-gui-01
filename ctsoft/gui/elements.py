# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 18:03:52 2018

@author: ctsoft
"""

import tkinter as tk


class TkBase(object):
    def __init__(self):
        super(TkBase, self).__init__()
        self.__numerics = ["bd", "height", "ipadx", "ipady", "maxsize-x",
                           "maxsize-y", "minsize-x", "minsize-y", "padx",
                           "pady", "xscrollincrement", "yscrollincrement",
                           "width", "wraplength"]
        self.methodToOptions = {}

    def handle2ParamMethod(self, element, remove=True):
        for method in self.methodToOptions:
            if self.methodToOptions[method][0] in element.attrib and \
                    self.methodToOptions[method][1] in element.attrib:
                method_ = getattr(self, method)
                method_(element.attrib[self.methodToOptions[method][0]],
                        element.attrib[self.methodToOptions[method][1]])
                if remove:
                    del element.attrib[self.methodToOptions[method][0]]
                    del element.attrib[self.methodToOptions[method][1]]
            elif self.methodToOptions[method][0] in element.attrib:
                method_ = getattr(self, method)
                method_(element.attrib[self.methodToOptions[method][0]])
                if remove:
                    del element.attrib[self.methodToOptions[method][0]]
            elif self.methodToOptions[method][1] in element.attrib:
                method_ = getattr(self, method)
                method_(element.attrib[self.methodToOptions[method][1]])
                if remove:
                    del element.attrib[self.methodToOptions[method][1]]

    def setOptions(self, options):
        for key in options:
            if key == "id":
                continue
            elif key in self.__numerics:
                self[key] = int(options[key])
            else:
                self[key] = options[key]


class TkWidget(TkBase):
    def __init__(self, master, element):
        super(TkWidget, self).__init__()
        self.setParent(master)

    def doPack(self, element):
        pack = element.findall("pack")
        if pack is not None:
            self.pack(pack[0].attrib)
        else:
            self.pack()

    def getParent(self):
        return self.__parent

    def getSelf(self):
        return self

    def setParent(self, parent):
        self.__parent = parent


class TkWidgetSimple(TkWidget):
    def __init__(self, master, element):
        super(TkWidget, self).__init__()
        self.setOptions(element.attrib)
        self.doPack(element)
        


class TkButton(tk.Button, TkWidgetSimple):
    def __init__(self, master, *args, **kw):
        tk.Button.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)
#        super(TkButton, self).__init__(self, master, *args, **kw)


class TkCanvas(tk.Canvas, TkWidgetSimple):
    def __init__(self, master, *args, **kw):
        tk.Canvas.__init__(self, master)
        TkWidgetSimple.__init__(self, master, *args, **kw)


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
        self.methodToOptions = {"maxsize": ("maxsize-x", "maxsize-y"),
                                "minsize": ("minsize-x", "minsize-y"),
                                "resizeable": ("resizeable-x",
                                               "resizeable-y")}
        self.setOptions(element)

    def setOptions(self, element):
        self.handle2ParamMethod(element)

        if "title" in element.attrib:
            self.title(element.attrib["title"])
            del element.attrib["title"]

        TkBase.setOptions(self, element.attrib)
