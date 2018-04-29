# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 07:16:54 2018

@author: ctsoft
"""

import collections
import copy
import csv
import tkinter as tk
from tkinter.filedialog import askopenfilename
import xml.etree.ElementTree as xmlee
import ctsoft.gui.elements as ctsel
import ctsoft.gui.options as ctsop
import ctsoft.gui.xml as ctsxml


class DataCell(object):
    def __init__(self, settings, value=""):
        self.__value = tk.StringVar(value="")
        self.__widget = None

        self.setSettings(settings)
        self.setValue(value)

    def display(self):
        # get the required variables
        settings = self.getSettings()
        indexCol = settings.getIndex("col")
        indexRow = settings.getIndex("row")
        parser = settings.getParser()
        parent = settings.getParent()
        xml = settings.getXml()

        # adjust the grid parameters
        grid = xml.find("grid")
        grid.attrib["column"] = indexCol
        grid.attrib["row"] = indexRow

        # adjust the identifier
        identifier = "datatable-content-" + str(indexRow) \
                                          + "-" + str(indexCol)
        xml.attrib["id"] = identifier

        # create the widget
        widget = parser.parseXml(xml, parent)
        widget.configure(textvariable=self.__value)
        self.setWidget(widget)

    def getSettings(self):
        return self.__settings

    def getValue(self):
        return self.__value.get()

    def getWidget(self):
        return self.__widget

    def setSettings(self, settings):
        self.__settings = settings

    def setValue(self, value):
        self.__value.set(value)

    def setWidget(self, widget):
        self.__widget = widget


class DataColumn(object):
    def __init__(self, values, settings):
        self.__cells = []

        self.setSettings(settings)

        self.createColumn(values)

    def addCell(self, cell):
        self.__cells.append(cell)

    def createColumn(self, values, doDisplay=True):
        # get the required variables
        settings = self.getSettings()
        # init the row index
        index = 1
        # loop through the column values and create the cells
        for value in values:
            settings.setIndex("row", index)
            cell = DataCell(settings, value)
            if doDisplay:
                cell.display()
            self.addCell(cell)
            index += 1

    def display(self):
        cells = self.getCells()
        for cell in cells:
            cell.display()

    def getCell(self, index):
        cells = self.getCells()
        return cells[index]

    def getCells(self):
        return self.__cells

    def getSettings(self):
        return self.__settings

    def getValues(self):
        cells = self.getCells()
        values = []
        for cell in cells:
            values.append(cell.getValue())
        return values

    def setSettings(self, settings):
        self.__settings = settings


class DataField(object):
    def __init__(self, settings, indexField, fName="", data=[]):
        self.__countCols = 0
        self.__countRows = 0
        self.__data = []
        self.__defaults = {"delimiter": ","}
        self.__error = []
        self.__indexField = indexField  # not in use atm
        self.__widgets = {}

        self.setSettings(settings)

        if fName is not "":
            self.setFileName(fName)
            self.loadData()
        else:
            cols = len(data)
            rows = len(data[0])
            self.setCount("cols", cols)
            self.setCount("rows", rows)
            self.setData(data)

    def addColumn(self, column):
        self.__data.append(column)

    def addError(self, error):
        self.__error.append(error)

    def addWidget(self, key, widget):
        self.__widgets[key] = widget

    def checkData(self, data):
        hasError = False
        if isinstance(data, collections.Sequence) and \
                not isinstance(data, str):
            for row in data:
                if self.checkColumn(row) is False:
                    hasError = True
            return not hasError
        else:
            return False

    def checkColumn(self, row):
        for cell in row:
            if not isinstance(cell, (str, int, float)):
                error = "A datatype of the submitted data is invalid."
                error += " Please use one of the following types:"
                error += " str, int, float"
                self.addError(error)
                return False
        return True

    def destroy(self):
        settings = self.getSettings()
        parent = settings.getParent()
        widgets = parent.winfo_children()

        for widget in widgets:
            widget.destroy()

    def displayHeaders(self):
        indexCols = self.getCount("col")
        indexRows = self.getCount("row")
        settings = self.getSettings()
        parent = settings.getParent()
        parser = settings.getParser()
        parser.setController(self)

        topLeft = settings.getXml("topLeft")
        left = settings.getXml("left")
        top = settings.getXml("top")

        for row in range(0, indexRows+1):
            if row == 0:
                cell00 = copy.deepcopy(topLeft)
                parser.parseXml(cell00, parent)

                for col in range(1, indexCols+1):
                    cellTop = copy.deepcopy(top)
                    cellTop.attrib["text"] = self.getColHeaderNumber(col)
                    cellTop.find("grid").attrib["column"] = col
                    parser.parseXml(cellTop, parent)
            else:
                cellLeft = copy.deepcopy(left)
                cellLeft.attrib["text"] = row
                cellLeft.find("grid").attrib["row"] = row
                parser.parseXml(cellLeft, parent)

    def getColHeaderNumber(self, index):
        num = ""
        if index / 26 > 1:
            num += self.getColHeaderNumber(round(index / 26))
        cur = index % 26
        if cur == 0:
            cur = 26
        return str(num + chr(cur + 96)).upper()

    def getColumn(self, index):
        return self.getColumns()[index]

    def getColumns(self):
        return self.__data

    def getCount(self, cType):
        if cType is "col" or cType is "cols" or cType is "columns":
            return self.__countCols
        elif cType is "row" or cType is "rows":
            return self.__countRows

    def getErrors(self):
        return self.__error

    def getFileContent(self):
        fName = self.getFileName()
        data = []
        with open(fName, newline="") as csvfile:
            reader = csv.reader(csvfile,
                                delimiter=self.__defaults["delimiter"])
            ind = 0
            colMax = 0
            for row in reader:
                val = row[0].split(";")
                index = 0
                for v in val:
                    if ind == 0:
                        data.append([])
                    data[index].append(float(v))
                    index += 1
                if colMax < index:
                    colMax = index
                ind += 1

        self.setCount("row", ind)
        self.setCount("col", colMax)

        return data

    def getFileName(self):
        return self.__fName

    def getSettings(self):
        return self.__settings

    def getWidget(self, key):
        return self.__widgets[key]

    def getWidgets(self):
        return self.__widgets

    def loadData(self):
        data = self.getFileContent()
        print("df.loadData() >>> ", data)
        self.setData(data)

    def raiseError(self):
        errors = self.getErrors()
        if errors is []:
            errors.append("The data for the data table is mal formed.")
        raise ValueError(errors[0])

    def resetWidgets(self):
        self.__widgets = {}

    def setCount(self, cType, count):
        if cType is "col" or cType is "cols" or cType is "columns":
            self.__countCols = count
        elif cType is "row" or cType is "rows":
            self.__countRows = count

    def setData(self, data):
        self.resetWidgets()

        settings = self.getSettings()
        parser = settings.getParser()
        parser.setController(self)

        if data:
            self.displayHeaders()

            index = 1
            for col in data:
                settings.setIndex("col", index)
                column = DataColumn(col, settings)
                self.addColumn(column)
                index += 1

    def setError(self, error):
        self.__error = error

    def setFileName(self, fName):
        error = ""
        if fName is not "":
            if isinstance(fName, str):
                self.__fName = fName
            else:
                error = "The datatype of the file name has to be string."

        if error is not "":
            raise ValueError(error)

    def setSettings(self, settings):
        self.__settings = settings

    def updateDataByFile(self, fName):
        if fName is "":
            fName = self.getFileName()


class Dt(object):
    """
    The Controller of the Datatable.
    """
    def __init__(self, data=[]):
        self.__cOption = None
        self.__data = []
        self.__defaults = {"delimiter": ","}
        self.__root = None
        self.__settings = None
        self.__view = None
        self.__xml = None
        self.__widgets = {}

        self.setXmlFromFile("settings.gui.datatable.view.xml")
        self.createView()
        self.iniSettings()
        root = self.getRoot()

        if root is not None:
            root.mainloop()

    def abortOptions(self):
        cOption = self.getCurrentOptionWindow()
        cOption.destroy()
        cOption = None

    def addDataFieldByFileName(self, fName):
        settings = self.getSettings()

        self.destroyDataTableContent(0)

        df = DataField(settings, 1, fName)
        self.__data.append(df)

        print(self.__widgets)

    def addDataFieldByNewTable(self, cols, rows):
        settings = self.getSettings()
        parent = self.getView().getDatatableContent()
        settings.setParent(parent)
        print("parent: ", parent)

        self.destroyDataTableContent(0)

        data = []
        cells = []

        for row in range(0, int(rows)):
            cells.append("")

        for col in range(0, int(cols)):
            data.append(cells)

        df = DataField(settings, 1, "", data)
        self.__data.append(df)

        print(self.__widgets)

    def addWidget(self, key, widget):
        self.__widgets[key] = widget

    def closeOptions(self):
        cOption = self.getCurrentOptionWindow()
        cOption.destroy()
        cOption = None

    def createView(self):
        xml = self.getXml()
        view = View(self, None, xml)
        self.__view = view
        self.__root = view.create()

        print(view.getWidgets())

    def destroyDataTableContent(self, index):
        df = self.getDataByIndex(index)
        if df:
            df.destroy()

    def getCurrentOptionWindow(self):
        return self.__cOption

    def getData(self):
        return self.__data

    def getDataByIndex(self, index):
        if len(self.__data) > index:
            return self.__data[index]
        else:
            return None

    def getRoot(self):
        return self.__root

    def getSettings(self):
        return self.__settings

    def getView(self):
        return self.__view

    def getXml(self):
        return self.__xml

    def iniSettings(self):
        view = self.getView()
        parent = view.getDatatableContent()
        parser = ctsxml.Parser(self, "")
        parser.setIdentifier("id")

        xmlInput = self.getXml().find(".//*[@id='datatable-content-1-1']")
        xmlInput.attrib["id"] = ""
        xmlTopLeft = self.getXml().find(".//*[@id='datatable-content-0-0']")
        xmlTop = self.getXml().find(".//*[@id='datatable-content-0-1']")
        xmlLeft = self.getXml().find(".//*[@id='datatable-content-1-0']")
        xml = {}
        xml["input"] = xmlInput
        xml["topLeft"] = xmlTopLeft
        xml["top"] = xmlTop
        xml["left"] = xmlLeft

        self.__settings = SettingsDataCell(parent, parser, xml)

    def openFileDialog(self, this):
        """
        Open the File Dialog and sets the Filepath to the submitted Object.

        Parameters
        ----------
        obj : Object
            An Application Object which implements setFileName(fName).
        """
        fName = askopenfilename(filetypes=(("CSV files", "*.csv"),
                                           ("All files", "*.*")))
        if fName:
            this.addDataFieldByFileName(fName)

    def setCurrentOptionWindow(self, cOption):
        self.__cOption = cOption

    def setXmlFromFile(self, fName):
        self.__xml = xmlee.parse(fName).getroot()

    def showDataTable(self, index=1):
        view = self.getView()

        if view is None:
            view = View(self, None, self.getXml())

    def showNewTableSettings(self):
        root = self.getRoot()
        settings = self.getSettings()
        settings.setParent(None)
        parser = settings.getParser()

        xml = parser.getFileContent("settings.gui.new-table.xml")
        xmlToplevel = xml.find("*")

        options = ctsop.NewTable(self, root, settings, xmlToplevel)
        options.createWindow()
        options.display()
        self.setCurrentOptionWindow(options)
        options.display()


class Toolbar(object):
    def __init__(self, dt, parent, xml):
        self.__dt = None
        self.__parent = None

    def getDt(self):
        return self.__dt

    def getParent(self):
        return self.__parent

    def setDt(self, dt):
        self.__dt = dt

    def setParent(self, parent):
        self.__parent = parent


class View(object):
    """
    The View of the Datatable.
    """
    def __init__(self, dt, parent, xml):
        self.__dt = dt
        self.__parent = parent
        self.__parser = ctsxml.Parser(self, "")
        self.__parser.setIdentifier("id")
        self.__root = None
        self.__widgets = {}
        self.__xml = xml

    def addWidget(self, key, widget):
        self.__widgets[key] = widget

    def create(self):
        xmlOrg = self.getXml()
        xml = copy.deepcopy(xmlOrg)
        content = xml.find(".//*[@id='datatable-content']")
        for child in list(content):
            if str(child.tag) != "pack" and str(child.tag) != "grid":
                content.remove(child)

        self.__parser.setContent(xml)
        root = None

        parent = self.getParent()
        if parent is not None:
            self.__parser.parseXml(xml, parent)
        else:
            root = self.__parser.createElements()
            self.setRoot(root)

        self.setupToolbar()

        return root

    def getDt(self):
        return self.__dt

    def getDatatableContent(self):
        return self.__widgets["datatable-content"]

    def getDatatableContentWrapper(self):
        return self.__widgets["datatable-content-wrapper"]

    def getNewFileButton(self):
        return self.__widgets["toolbar-button-nfi"]

    def getOpenFileButton(self):
        return self.__widgets["toolbar-button-ofi"]

    def getSaveFileButton(self):
        return self.__widgets["toolbar-button-sfi"]

    def getParent(self):
        return self.__parent

    def getRoot(self):
        return self.__root

    def getTableTemplate(self):
        xml = self.getXml()
        tableTemplate = xml.find(".//*[@id='datatable-wrapper-content']")
        return tableTemplate

    def getWidgets(self):
        return self.__widgets

    def getXml(self):
        return self.__xml

    def setParent(self, parent):
        self.__parent = parent

    def setParser(self, parser):
        self.__parser = parser

    def setRoot(self, root):
        self.__root = root

    def setupToolbar(self):
        dt = self.getDt()

        ofiButton = self.getOpenFileButton()
        ofiButton.configure(command=lambda arg=dt: dt.openFileDialog(arg))

        dtwc = self.getDatatableContentWrapper()
        nfiButton = self.getNewFileButton()
        nfiButton.configure(command=lambda arg=dtwc: dt.showNewTableSettings())


class Settings(object):
    def __init__(self, parent, parser):
        self.__parent = None
        self.__parser = None

        self.setParent(parent)
        self.setParser(parser)

    def getParent(self):
        return self.__parent

    def getParser(self):
        return self.__parser

    def setParent(self, parent):
        self.__parent = parent

    def setParser(self, parser):
        self.__parser = parser


class SettingsXml(object):
    def __init__(self, parent, parser, xml=None):
        Settings.__init__(self, parent, parser)
        self.__xml = None

        if xml:
            self.setXml(xml)

    def getXml(self):
        return self.__xml

    def setXml(self, xml):
        self.__xml = xml


class SettingsToolbar(SettingsXml):
    def __init__(self, parent, parser, xml):
        Settings.__init__(self, parent, parser)
        self.__xml = None
        self.__xmlRootIdentifier = ""

        if xml:
            self.setXml(xml)

    def setXml(self, xml):
        parser = self.getParser()
        identifier = parser.getIdentifier()
        if identifier in xml.attrib and \
                xml.attrib[identifier] == "toolbar-wrapper":
            self.__xml = xml
        else:
            root = xml.find(".//*[@id='toolbar-wrapper']")
            if root:
                self.__xml = root


class SettingsDataCell(Settings):
    def __init__(self, parent, parser, xml):
        Settings.__init__(self, parent, parser)
        self.__xml = xml

    def getIndex(self, iType):
        if iType is "col" or iType is "column":
            return self.__indexColumn
        elif iType is "row":
            return self.__indexRow

    def getXml(self, key="input"):
        if key is "input" or key is "topLeft" or key is "top" or key is "left":
            return self.__xml[key]

    def raiseIndexError(self, iType):
        error = "The parameter has to be \"col\" or \"row\", found "
        error += "\"" + str(iType) + "\""
        raise ValueError(error)

    def setIndex(self, iType, value):
        if iType is "col" or iType is "column":
            self.__indexColumn = value
        elif iType is "row":
            self.__indexRow = value
        else:
            self.raiseIndexError(iType)
