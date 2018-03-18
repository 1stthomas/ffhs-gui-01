# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 18:03:52 2018

@author: ctsoft
"""

import tkinter as tk


class TkBase(object):
    def __init__(self):
        super(TkBase, self).__init__()
        self.numerics = ["bd", "height", "ipadx", "ipady", "maxsize-x",
                         "maxsize-y", "minsize-x", "minsize-y", "padx", "pady",
                         "xscrollincrement", "yscrollincrement", "width",
                         "wraplength"]

    def setOptions(self, options):
        for key in options:
            if key == "id":
                continue
            elif key in self.numerics:
                self[key] = int(options[key])
            else:
                self[key] = options[key]


class TkWidget(TkBase):
    def __init__(self, master, element):
        super(TkWidget, self).__init__()
        self.setParent(master)
        self.setOptions(element.attrib)
        self.doPack(element)

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


class TkButton(tk.Button, TkWidget):
    def __init__(self, master, *args, **kw):
        tk.Button.__init__(self, master)
        TkWidget.__init__(self, master, *args, **kw)
#        super(TkButton, self).__init__(self, master, *args, **kw)


class TkEntry(tk.Entry, TkWidget):
    def __init__(self, master, *args, **kw):
        tk.Entry.__init__(self, master)
        TkWidget.__init__(self, master, *args, **kw)
#        super(TkEntry, self).__init__(self, master, *args, **kw)


class TkFrame(tk.Frame, TkWidget):
    def __init__(self, master, *args, **kw):
        tk.Frame.__init__(self, master)
        TkWidget.__init__(self, master, *args, **kw)
#        super(TkFrame, self).__init__(master, *args, **kw)


class TkLabel(tk.Label, TkWidget):
    def __init__(self, master, *args, **kw):
        tk.Label.__init__(self, master)
        TkWidget.__init__(self, master, *args, **kw)
#        super(TkLabel, self).__init__(master, *args, **kw)


class TkWindow(tk.Tk, TkBase):
    def __init__(self, element, *args, **kw):
        tk.Tk.__init__(self)
        TkBase.__init__(self)
        self.setOptions(dict(element.attrib))

    def setOptions(self, attributes):
        if "maxsize-x" in attributes and "maxsize-y" in attributes:
            self.maxsize(attributes["maxsize-x"], attributes["maxsize-y"])
            del attributes["maxsize-x"]
            del attributes["maxsize-y"]
        elif "maxsize-x" in attributes:
            self.maxsize(attributes["maxsize-x"], None)
            del attributes["maxsize-x"]
        elif "maxsize-y" in attributes:
            self.maxsize(None, attributes["maxsize-y"])
            del attributes["maxsize-y"]

        if "minsize-x" in attributes and "minsize-y" in attributes:
            self.minsize(attributes["minsize-x"], attributes["minsize-y"])
            del attributes["minsize-x"]
            del attributes["minsize-y"]
        elif "minsize-x" in attributes:
            self.minsize(attributes["minsize-x"], None)
            del attributes["minsize-x"]
        elif "minsize-y" in attributes:
            self.minsize(None, attributes["minsize-y"])
            del attributes["minsize-y"]

        if "resizable-x" in attributes and "resizable-y" in attributes:
            self.resizable(attributes["resizable-x"], attributes["resizable-y"])
            del attributes["resizable-x"]
            del attributes["resizable-y"]
        elif "minsize-x" in attributes:
            self.resizable(attributes["resizable-x"], None)
            del attributes["resizable-x"]
        elif "minsize-y" in attributes:
            self.resizable(None, attributes["resizable-y"])
            del attributes["resizable-y"]

        if "title" in attributes:
            self.title(attributes["title"])
            del attributes["title"]

        TkBase.setOptions(self, attributes)
