import copy
from datetime import timedelta

class Task():

    def __init__(self, iCode = "", iTitle = "", iID = ""):

        self.id = iID
        self.prjCode = iCode
        self.title = iTitle
        
        self.completedTime = 0.0
        self.estimatedTime = 0.0

    def __copy__(self):
        
         taskToReturn = Task(self.prjCode, self.title, self.id)
         taskToReturn.completedTime = self.completedTime
         taskToReturn.estimatedTime = self.estimatedTime

         return taskToReturn
    
    def addCompletedTime(self, iTimeInSeconds):

        self.completedTime += iTimeInSeconds

    def substractCompletedTime(self, iTimeInSeconds):

        self.completedTime -= iTimeInSeconds
