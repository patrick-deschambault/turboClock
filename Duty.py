

import datetime
from TFSTask import *
from ProjectGiro import *
from TaskGiro import *

class Duty():

    def __init__(self):


        self.date = datetime.datetime.now()

        self.mondayDateCurrWeek = self.computeMondayDateWeek(self.date)

        self.pieces = list()

        self.TFSTaskUsed = list()


    def addPiece(self, iPiece):
        
        self.pieces.append(iPiece)

    def computeMondayDateWeek(self, iDate):

        weekday = iDate.weekday()

        return self.date - datetime.timedelta(days=weekday)

    def registerTasksTFSOfPieceToDuty(self, iPiece):
        

        # [x for x in myList if x.n == 30]  # list of all elements with .n==30

        iTaskTFS = iPiece.tfsTask

        if self.TFSTaskUsed != []:

            isTFSTaskFound = False

            for i, taskTFS in enumerate(self.TFSTaskUsed):

                if taskTFS.code == iTaskTFS.code:
                    isTFSTaskFound == True
                    TFSTaskFoundIndex = i
                    break
                else:
                    continue

            if not isTFSTaskFound:
                newProj = ProjectGiro(iTaskTFS.projectGiro.code)
                newTask = TaskGiro(iTaskTFS.taskGiro.code)

                self.TFSTaskUsed.append(TFSTask(iTaskTFS.code, iTaskTFS.description, newProj, newTask))
            else:
                self.TFSTaskUsed[TFSTaskFoundIndex].completedTime += iPiece.completedTime
        else:
            newProj = ProjectGiro(iTaskTFS.projectGiro.code)
            newTask = TaskGiro(iTaskTFS.taskGiro.code)

            self.TFSTaskUsed.append(TFSTask(iTaskTFS.code, iTaskTFS.description, newProj, newTask))
