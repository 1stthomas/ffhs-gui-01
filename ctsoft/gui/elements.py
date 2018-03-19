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
        self.methodTo2Options = {}
        self.methodTo1Option = {}
        self.setOrganizeType("pack")
        self.setOrganizeTypeChildren("pack")

    def getOrganizeType(self):
        return self.__organizeType

    def getOrganizeTypeChildren(self):
        return self.__organizeTypeChildren

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

    def setRows(self, rows):
        for row in rows:
            num = row.attrib["num"]
            del row.attrib["num"]
            self.grid_rowconfigure(num, row)

    def setOptions(self, options):
        for key in options:
            if key == "id":
                continue
            elif key in self.__numerics:
                self[key] = int(options[key])
            else:
                self[key] = options[key]

    def setOrganizeType(self, organizeType):
        self.__organizeType = organizeType

    def setOrganizeTypeChildren(self, organizeTypeChildren):
        self.__organizeTypeChildren = organizeTypeChildren


class TkWidget(TkBase):
    def __init__(self, master, element):
        super(TkWidget, self).__init__()
        self.__parent = None
        self.setParent(master)

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
            parent.grid_columnconfigure(num, parentAttr.attrib)
            self.setOrganizeType("grid")
            parent.setOrganizeTypeChildren("grid")

    def setParent(self, parent):
        self.__parent = parent


class TkWidgetSimple(TkWidget):
    def __init__(self, master, element):
        super(TkWidgetSimple, self).__init__(master, element)
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
