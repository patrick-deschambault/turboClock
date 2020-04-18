
from datetime import timedelta
from Piece import *

class TaskGiro():

    def __init__(self, iCode = ""):

        self.code = iCode
        self.description = ""
        
        self.completedTime = 0.0
        self.estimatedTime = 0.0
    
    def addCompletedTime(self, iTimeInSeconds):

        self.completedTime += iTimeInSeconds



