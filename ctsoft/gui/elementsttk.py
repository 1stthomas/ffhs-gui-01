# -*- coding: utf-8 -*-
"""
Created on Fri May 11 09:35:00 2018

@author: ctsoft
"""

import tkinter as tk
import tkinter.ttk as ttk
import ctsoft.gui.elements as ctsel


class TtkNotebook(ttk.Notebook, ctsel.TkWidget):
    def __init__(self, master, xml, *args, **kw):
        ttk.Notebook.__init__(self, master)
        ctsel.TkWidget.__init__(self, master, xml, *args, **kw)
