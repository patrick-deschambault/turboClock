import datetime
from datetime import timedelta
from Task import Task
import copy

class Piece():

    def __init__(self, iTask = "", iStartDateTime = "", iEndDateTime = ""):

        self.datetimeFormat = '%Y-%m-%d %H:%M:%S'
        self.startDateTime = iStartDateTime
        self.endDateTime = iEndDateTime

        self.task = copy.copy(iTask)
        self.computeDeltaTime()

    def setStartDateTime(self, iStartDateTime):

        self.startDateTime = iStartDateTime

        if self.endDateTime:
            self.computeDeltaTime()

    def setEndDateTime(self, iEndDateTime):

        self.endDateTime = iEndDateTime

        if self.startDateTime:
            self.computeDeltaTime()

    def computeDeltaTime(self):

        if self.endDateTime != '' and self.startDateTime != '':

            startDT = str(self.startDateTime.strftime("%Y-%m-%d %H:%M:%S") )
            endDT = str(self.endDateTime.strftime("%Y-%m-%d %H:%M:%S"))

            dt = (datetime.datetime.strptime(endDT, self.datetimeFormat) \
                                     - datetime.datetime.strptime(startDT, self.datetimeFormat)).total_seconds()
                                     
            self.task.completedTime = dt


