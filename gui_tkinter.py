# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 14:45:53 2018

@author: ctsoft
"""

import ctsoft.gui.xml as ctsxml


t1 = ctsxml.Interpreter("settings.gui.xml")
# t1 = ctsxml.Interpreter("settings.gui.minimal.xml")
top = t1.createElements()
top.mainloop()
