from Task import *
from Duty import *

from datetime import *
import os
import copy

class Backlog():

    def __init__(self):

        self.tasks = list()

    def addTask(self, iTask):

        if not self.taskExist(iTask):
            self.tasks.append(iTask)

    def deleteTask(self, iTask):

        index = self.getIndexFromTask(iTask)

        if index != None:
            self.tasks.pop(index)

    def editTask(self, iTaskToEdit, iEditedTask):

        index = self.getIndexFromTask(iTaskToEdit)

        if index != None:
            self.tasks[index].title = iEditedTask.title
            self.tasks[index].prjCode = iEditedTask.prjCode
            self.tasks[index].completedTime = iEditedTask.completedTime
            self.tasks[index].estimatedTIme = iEditedTask.estimatedTime

    def getIndexFromTask(self, iTask):

        index = None

        for i, currTask in enumerate(self.tasks):
            if iTask.title == currTask.title and iTask.prjCode == currTask.prjCode:
                index = i
                break
            else: 
                continue

        return index

    def taskExist(self, iTask):

        if self.getIndexFromTask(iTask) != None:
            return True
        else:
            return False

    def validateTask(self, iTask):

        prjCode = iTask.prjCode
        title = iTask.title

        errors = list()

        if (prjCode == '' ):
            errors.append("*Project code required")

        if (title == ''):
            errors.append("*Title required")

        return errors

    def save(self, iFilename):

        if not os.path.exists(iFilename):
            os.makedirs(iFilename)

        s = ""

        for currTask in self.tasks:

            s += str(currTask.id)
            s += ';'
            s += str(currTask.prjCode)
            s += ';'
            s += str(currTask.title)
            s += ';'
            s += str(int(currTask.completedTime))
            s += ';'
            s += str(int(currTask.estimatedTime))
            s += '\n'

        with open(iFilename, "w") as file:
            file.write(s)
            file.close()

    def load(self, iFilename):

        fileExist = os.path.isfile(iFilename)

        if not fileExist:
            file = open(iFilename, 'w')
            file.close()
            return
        
        file = open(iFilename, 'r')

        for line in file:

            if (line != ""):

                line = line.split(";")

                currTask = Task()

                currTask.id = line[0]
                currTask.prjCode = line[1]
                currTask.title = line[2]
                currTask.completedTime = int(line[3])
                currTask.estimatedTime = int(line[4].rstrip('\n'))

                self.addTask(currTask)

            else:
                break

        file.close()

    def getIndexTaskFromInternalId(self, iInternalId):

        for i, currTask in enumerate(self.tasks):

            if currTask.internalId == iInternalId:
                return i
            
