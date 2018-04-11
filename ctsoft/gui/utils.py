# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 18:07:09 2018

@author: ctsoft
"""


class Input(object):
    """
    Data Transfer Object with GUI Information to the Business Logic.

    Methods
    -------
    getData :
        Returns the data to display.
    getPlotType :
        Returns the plot type.
    setData :
        Sets the data.
    setPlotType :
        Sets the plot type.
    """
    def __init__(self, plotType="", data=[]):
        """
        Instanciates an Input.
        Calls setData() and setPlotType().

        Parameters
        ----------
        plotType : string
            The plot type to display. Supported types are:
                bar-chart
                function-multiple
                function-single
                histogram
                pie-chart
        data : list
            The data to display as a list of x/y list items.
        """
        self.__data = []
        self.__plotType = ""
        self.__plotTypes = {"bar-chart", "function-single",
                            "function-multiple", "histogram", "pie-chart"}
        self.setData(data)
        self.setPlotType(plotType)

    def getData(self):
        """
        Returns the Data to display.

        Returns
        -------
        list : The data to display.
        """
        return self.__data

    def getPlotType(self):
        """
        Returns the Plot Type.

        Returns
        -------
        string : The plot type to display.
        """
        return self.__plotType

    def setData(self, data):
        """
        Sets the Data.

        Parameters
        ----------
        data : list
            A list of x/y list items.
        """
        self.__data = data

    def setPlotType(self, plotType):
        """
        Sets the Plot Type to display.

        Parameters
        ----------
        plotType : string
            The plot type to display. Use one of the following types:
                bar-chart
                function-multiple
                function-single
                histogram
                pie-chart

        Returns
        -------
        boolean : True if the plot type could be set.
        """
        if plotType in self.__plotTypes:
            self.__plotType = plotType
            return True
        else:
            return False


class Output(object):
    """
    Data Transfer Object with Buisiness Information to the GUI.

    Methods
    -------
    addError :
        Adds an error to the error list.
    addMessage :
        Adds a message to the message list.
    getErrors :
        Returns the error collection.
    getMessages :
        Returns the message collection.
    getPath :
        Returns the path to the generated plot.
    setErrors :
        Sets the error collection.
    setMessages :
        Sets the message collection.
    setPath :
        Sets the path to the generated plot.
    """
    def __init__(self, path="", messages=[], errors=[]):
        """
        Instanciates an Output.
        Calls setMessages() and setErrors().

        Parameters
        ----------
        path : string
            The path to the generated plot file.
        messages : list
            Messages to display.
        errors : list
            Errors occured on the plot creation.
        """
        self.__errors = []
        self.__messages = []
        self.__path = path
        self.setMessages(messages)
        self.setErrors(errors)

    def addError(self, error):
        """
        Adds an Error to the Error Collection.

        Parameters
        ----------
        error : string
            An error to add to the collection.
        """
        self.__errors.append(error)

    def addMessage(self, message):
        """
        Adds an Message to the Message Collection.

        Parameters
        ----------
        message : string
            An message to add to the collection.
        """
        self.__messages.append(message)

    def getErrors(self):
        """
        Returns the Error Collection.

        Returns
        -------
        list : A list of error strings.
        """
        return self.__errors

    def getMessages(self):
        """
        Returns the Message Collection.

        Returns
        -------
        list : A list of message strings.
        """
        return self.__messages

    def getPath(self):
        """
        Returns the Path to the generated Plot File.

        Returns
        -------
        string : The path to the generated plot file.
        """
        return self.__path

    def setErrors(self, errors):
        """
        Resets the Error Collection with the submitted list.

        Parameters
        ----------
        errors : list
            A list with error strings.
        """
        self.__errors = errors

    def setMessages(self, messages):
        """
        Resets the Message Collection with the submitted list.

        Parameters
        ----------
        messages : list
            A list with message strings.
        """
        self.__messages = messages

    def setPath(self, path):
        """
        Sets the Path to the generated Plot File.

        Parameters
        ----------
        path : string
            The path to the generated plot file.
        """
        self.__path = path
