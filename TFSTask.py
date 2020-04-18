
from ProjectGiro import *
from TaskGiro import *

from PyQt5.QtCore import QTime

class TFSTask():

    def __init__(self, iCode, iDescription, iProjectGiro, iTaskGiro):

        self.code = iCode
        self.description = iDescription

        self.projectGiro = iProjectGiro
        self.taskGiro= iTaskGiro

        self.completedTime = 0
        self.estimatedTime = 0

    def addCompletedTime(self, iTimeInSeconds):

        self.completedTime += iTimeInSeconds
        self.taskGiro.completedTime += iTimeInSeconds
        


