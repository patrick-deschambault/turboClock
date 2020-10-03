
import copy
import datetime
import os

from Task import Task
from Piece import Piece

class Duty():

    def __init__(self):

        self.date = ""

        self.pieces = list()

        self.tasksRegistered = list()

        self.totalTimeCompleted = 0

    def addPiece(self, iPiece):
        
        self.pieces.append(iPiece)

        self.registerTask(iPiece.task)

    def registerTask(self, iTask):
    
        task = copy.copy(iTask)

        taskRegistered = False
        index = 0

        if len(self.tasksRegistered) > 0:

            for i, currTask in enumerate(self.tasksRegistered):

                if currTask.title != "":
                    if currTask.prjCode == task.prjCode and currTask.title == task.title:
                            
                        taskRegistered = True
                        index = i
                        break
                    else:
                        continue
                else:
                    continue

            if taskRegistered:
                self.tasksRegistered[index].addCompletedTime(task.completedTime)
                self.totalTimeCompleted += task.completedTime
            else:
                self.tasksRegistered.append(task)
                self.totalTimeCompleted += task.completedTime
        else:
            self.tasksRegistered.append(task)
            self.totalTimeCompleted += task.completedTime

    def load(self, iFileName):

        dutyDataExist = os.path.isfile(iFileName)
        
        if not dutyDataExist:
            file = open(iFileName, 'w+')
            file.close()
            return

        file = open(iFileName,'r')

        for line in file:
            if line != '\n':
                lineSplit = line.split(';')

                taskId = lineSplit[0]
                taskPrjCode = lineSplit[1]
                title = lineSplit[2]

                currDtyDate = datetime.datetime.now()
                formatDateTime = '%Y-%m-%d %H:%M:%S'

                startTime = datetime.datetime.strptime(currDtyDate + ' ' + lineSplit[3],  formatDateTime)
                endTime =   datetime.datetime.strptime(currDtyDate + ' ' + lineSplit[4].rstrip('\n'),  formatDateTime)

                newTask = Task(taskPrjCode, title, taskId)
                newPiece = Piece(newTask, startTime, endTime)

                self.addPiece(newPiece)

        file.close()

    def save(self, iFilename):

        if not os.path.exists(iFilename):
            os.makedirs(iFilename)

        s = ""

        for currPiece in self.pieces:

            s += str(currPiece.task.id)
            s += ";"
            s += str(currPiece.task.prjCode)
            s += ";"
            s += str(currPiece.task.title)
            s += ";"
            s += str(currPiece.startDateTime.strftime("%H:%M:%S"))
            s += ";"
            s += str(currPiece.endDateTime.strftime("%H:%M:%S"))
            s += '\n'

        with open(iFilename, "a") as file:
            file.write(s)
            file.close()

