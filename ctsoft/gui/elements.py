# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 18:03:52 2018

@author: ctsoft
"""

import tkinter as tk


class TkGuiExtender(object):
    def __init__(self, master, element):
        super(TkGuiExtender, self).__init__()
        self.numerics = ["bd", "height", "ipadx", "ipady", "width"]
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

    def setOptions(self, options):
        for key in options:
            if key in self.numerics:
                self[key] = int(options[key])
            else:
                self[key] = options[key]

    def setParent(self, parent):
        self.__parent = parent


class TkButton(tk.Button, TkGuiExtender):
    def __init__(self, master, *args, **kw):
        tk.Button.__init__(self, master)
        TkGuiExtender.__init__(self, master, *args, **kw)
#        super(TkButton, self).__init__(self, master, *args, **kw)


class TkEntry(tk.Entry, TkGuiExtender):
    def __init__(self, master, *args, **kw):
        tk.Entry.__init__(self, master)
        TkGuiExtender.__init__(self, master, *args, **kw)
#        super(TkEntry, self).__init__(self, master, *args, **kw)


class TkFrame(tk.Frame, TkGuiExtender):
    def __init__(self, master, *args, **kw):
        tk.Frame.__init__(self, master)
        TkGuiExtender.__init__(self, master, *args, **kw)
#        super(TkFrame, self).__init__(master, *args, **kw)


class TkLabel(tk.Label, TkGuiExtender):
    def __init__(self, master, *args, **kw):
        tk.Label.__init__(self, master)
        TkGuiExtender.__init__(self, master, *args, **kw)
#        super(TkLabel, self).__init__(master, *args, **kw)
