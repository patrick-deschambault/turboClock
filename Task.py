import copy

from datetime import timedelta
from datetime import datetime
import time
import datetime

class Task():

    def __init__(self, iPrjCode = "", iTitle = "", iID = ""):

        self.internalId = 0
        self.id = iID
        self.prjCode = iPrjCode
        self.title = iTitle
        
        self.completedTime = 0.0
        self.estimatedTime = 0.0

        self.completionRatio = 0

    def __copy__(self):
        
         taskToReturn = Task(self.prjCode, self.title, self.id)
         taskToReturn.completedTime = self.completedTime
         taskToReturn.estimatedTime = self.estimatedTime
         taskToReturn.completionRatio = self.completionRatio

         return taskToReturn

    def addCompletedTime(self, iTimeInSeconds):

        self.completedTime += iTimeInSeconds

        self.compCompletionRatio()

    def substractCompletedTime(self, iTimeInSeconds):

        self.completedTime -= iTimeInSeconds
        self.compCompletionRatio()

    def setCompletedTime(self, iCompletedTimeStr):

        x = time.strptime(iCompletedTimeStr, '%H:%M:%S')
        self.completedTime = datetime.timedelta(hours = x.tm_hour, minutes = x.tm_min, seconds=x.tm_sec).total_seconds()

    def completedTimeStr(self):

        timeStr = datetime.timedelta(seconds = self.completedTime)
        return timeStr

    def setEstimatedTime(self, iEstimatedTimeStr):

        x = time.strptime(iEstimatedTimeStr, '%H:%M:%S')
        self.estimatedTime = datetime.timedelta(hours = x.tm_hour, minutes = x.tm_min, seconds=x.tm_sec).total_seconds()

        self.compCompletionRatio()

    def compCompletionRatio(self):
        
        if(self.estimatedTime > 0):
            
            self.completionRatio = int(self.completedTime / self.estimatedTime)

        else:
            self.completionRatio = 0

        
