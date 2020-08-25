from Task import *
from Duty import *

from datetime import *
import os

from BacklogData import *

import copy

class BacklogMgr():

    def __init__(self):

        self.backlogData = BacklogData()

        dataPath = os.getcwd() + '\\Data'

        if not os.path.exists(dataPath):
            os.mkdir(dataPath)

        self.initPathData(dataPath)

        if not os.path.isfile(self.backlogData.filenameDutyData):
            file = open(self.backlogData.filenameDutyData, 'w')
            file.close()

        self.loadTasksData()
        self.initCurrDuty()

    def initPathData(self, iPathData):

        self.backlogData.pathData = iPathData

        self.initCurrDate()
        self.initPathCurrWeekData()
        self.initFilenameCurrDutyData()
        self.initTasksPathData()
        
    def initCurrDate(self):

        now = datetime.datetime.now()
        self.backlogData.currDate = now.strftime("%Y-%m-%d")

    def initPathCurrWeekData(self):

        now = datetime.datetime.now().strftime("%Y-%m-%d")
        mondayDateOfWeek = self.backlogData.currDuty.getMondayDateOfCurrWeek(now) 
        self.backlogData.pathWeekData = self.backlogData.pathData + '\\' + mondayDateOfWeek

        if not os.path.exists(self.backlogData.pathWeekData):
            os.mkdir(self.backlogData.pathWeekData)

    def initFilenameCurrDutyData(self):
        
        today = self.backlogData.currDate
        self.backlogData.filenameDutyData = self.backlogData.pathWeekData + '\\' + \
                                            today + '.dat'

    def initTasksPathData(self):

        self.backlogData.pathTasksData = self.backlogData.pathData + '\\' + \
                                         'tasksData.dat'

    def loadTasksData(self):

        dutyDataExist = os.path.isfile(self.backlogData.pathTasksData)
        if not dutyDataExist:
            file = open(self.backlogData.pathTasksData, 'w')
            file.close()
            return
        
        file = open(self.backlogData.pathTasksData, 'r')

        for line in file:

            if (line != ""):
                line = line.split(";")

                taskId = line[0]
                taskProjectCode = line[1]
                taskTitle = line[2]
                completedTime = int(line[3])
                estimatedTime = str(line[4].rstrip('\n'))

                self.addNewTask(taskId, taskProjectCode, taskTitle, completedTime, estimatedTime)

            else:
                break
        file.close()

    def loadDutyData(self, iDate, iDuty):

        dutyDataExist = os.path.isfile(self.backlogData.pathTasksData)
        
        if not dutyDataExist:
            file = open(self.backlogData.pathTasksData, 'w+')
            file.close()
            return

        file = open(self.backlogData.filenameDutyData,'r')

        for line in file:
            if line != '\n':
                lineSplit = line.split(';')

                taskId = lineSplit[0]
                taskPrjCode = lineSplit[1]
                title = lineSplit[2]

                currDtyDate = self.backlogData.currDuty.date
                formatDateTime = '%Y-%m-%d %H:%M:%S'

                startTime = datetime.datetime.strptime(currDtyDate + ' ' + lineSplit[3],  formatDateTime)
                endTime =   datetime.datetime.strptime(currDtyDate + ' ' + lineSplit[4].rstrip('\n'),  formatDateTime)

                newTask = Task(taskPrjCode, title, taskId)
                newPiece = Piece(newTask, startTime, endTime)

                iDuty.addPiece(newPiece)

        file.close()

    def initCurrDuty(self):

        currDate = self.backlogData.currDate
        self.loadDutyData(currDate, self.backlogData.currDuty)

    def addNewTask(self, iId, iPrjCode, iTitle, iCompletedTime = 0, iEstimatedTime = ""):
        
        newTask = Task(iPrjCode, iTitle, iId)
        newTask.addCompletedTime(iCompletedTime)
        newTask.setEstimatedTime(iEstimatedTime)

        if not self.getIndexTaskBacklogData(newTask):
            self.backlogData.tasks.append(newTask)

    def addPieceToCurrDuty(self, iPiece):

        self.backlogData.currDuty.addPiece(iPiece)

        index = self.getIndexTaskBacklogData(iPiece.task)

        if index >= 0:
            taskBacklog = self.backlogData.tasks[index]
            taskBacklog.completedTime += iPiece.task.completedTime

    def getIndexTaskBacklogData(self, iTask):

        index = None

        for i, currTask in enumerate(self.backlogData.tasks):
            if iTask.title == currTask.title and \
                iTask.prjCode == currTask.prjCode:
                index = i
                break
            else: 
                continue

        return index

    def editTaskFromGUI(self, iIndex, iTaskFromGUI):
        
        errors = self.validateTask(iTaskFromGUI)

        if not errors:

            if (iIndex >= 0 and iIndex < len(self.backlogData.tasks)):
                self.backlogData.tasks[iIndex] = iTaskFromGUI
            else:
                # Need some refactoring here. We should 
                # call addNewTask(iTaskFromGUI) but it does not exist.
                if(not self.getIndexTaskBacklogData(iTaskFromGUI)):
                    self.backlogData.tasks.append(iTaskFromGUI)
                else:
                    errors.append("*Task already exist")
        
        return errors

    def validateTask(self, iTask):

        prjCode = iTask.prjCode
        title = iTask.title

        errors = list()

        if (prjCode == '' ):
            errors.append("*Project code required")

        if (title == ''):
            errors.append("*Title required")

        return errors

    def writePieceToDutyData(self, iPiece):
        
        dty = Duty()

        pceDate = iPiece.startDateTime.strftime("%Y-%m-%d")
        pceDateMondayWeek = dty.getMondayDateOfCurrWeek(iPiece.startDateTime.strftime("%Y-%m-%d"))

        filePath = self.backlogData.pathData + '\\' + \
                   pceDateMondayWeek + '\\' + \
                   pceDate + '.dat'

        if not os.path.exists(filePath):
            os.makedirs(filePath)

        s = ""

        s += str(iPiece.task.id)
        s += ";"
        s += str(iPiece.task.prjCode)
        s += ";"
        s += str(iPiece.task.title)
        s += ";"
        s += str(iPiece.startDateTime.strftime("%H:%M:%S"))
        s += ";"
        s += str(iPiece.endDateTime.strftime("%H:%M:%S"))
        s += '\n'

        with open(filePath, "a") as file:
            file.write(s)
            file.close()

    def writeTasksData(self):

        filePath = self.backlogData.pathData + '\\' + 'tasksData.dat'

        if not os.path.exists(filePath):
            os.makedirs(filePath)

        s = ""

        for currTask in self.backlogData.tasks:

            s += str(currTask.id)
            s += ';'
            s += str(currTask.prjCode)
            s += ';'
            s += str(currTask.title)
            s += ';'
            s += str(int(currTask.completedTime))
            s += ';'
            s += str(datetime.timedelta(seconds = currTask.estimatedTime))
            s += '\n'

        with open(filePath, "w") as file:
            file.write(s)
            file.close()
    
    def initCurrTask(self):
        self.backlogData.currtask = Task()

    def startPiece(self):
        
        now = datetime.datetime.now()
        
        self.backlogData.currPiece = Piece(self.backlogData.currTask, now)        

        self.backlogData.isTimerRunning = True

    def endPiece(self):

        now = datetime.datetime.now()

        self.backlogData.currPiece.setEndDateTime(now)
        self.addPieceToCurrDuty(self.backlogData.currPiece)

        self.writePieceToDutyData(self.backlogData.currPiece)
        self.writeTasksData()

        self.backlogData.isTimerRunning = False

    def setCurrentTaskFromGUI(self, iIndexCbb):

        try:
            self.backlogData.currTask = self.backlogData.tasks[iIndexCbb]
            self.backlogData.currTaskIndex = iIndexCbb
        except:
            print("Error: index must be a strictly positive integer")

    def getTasksFromGUI(self):

        return copy.deepcopy(self.backlogData.tasks)

    def getCurrDutyTimeCompletedFromGUI(self):

        secCompleted = self.backlogData.currDuty.totalTimeCompleted
        return str(datetime.timedelta(seconds = secCompleted))

    def getCompletedTimeCurrTaskFromGUI(self):

        secCompleted = self.backlogData.currTask.completedTime
        return str(datetime.timedelta(seconds = secCompleted))

    def manageClickButtonFromGUI(self):

        if self.backlogData.currTask:
            if not self.backlogData.isTimerRunning:
                self.startPiece()
            else:
                self.endPiece()

    def manageTaskChangeFromGUI(self, iCbbIndex):

        if self.backlogData.isTimerRunning:
            self.endPiece()
            self.setCurrentTaskFromGUI(iCbbIndex)
            self.startPiece()
        else:
            self.setCurrentTaskFromGUI(iCbbIndex)
       
    def manageAddTaskBacklogDataFromGUI(self, iId, iPrjCode, iTitle, iCompletedTime, iEstimatedTime):
        
        self.addNewTask(iId, iPrjCode, iTitle, iCompletedTime, iEstimatedTime)

    def manageDeleteTaskBacklogDataFromGUI(self, iId, iPrjCode, iTitle):
        
        self.deleteTaskBacklogData(iId, iPrjCode,iTitle)

    def deleteTaskBacklogData(self, iId, iPrjCode, iTitle):

        taskToDelete = Task(iPrjCode, iTitle, iId)

        index = self.getIndexTaskBacklogData(taskToDelete)

        if index:
            self.backlogData.tasks.pop(index)

    def replaceTasksBacklogData(self, iTasksList):

        if len(iTasksList) > 0:

            self.backlogData.tasks.clear()
            self.backlogData.tasks = copy.copy(iTasksList)

            self.writeTasksData()

    def getCompletionRatio(self, iTaskRow):

        if iTaskRow >= 0 and iTaskRow < len(self.backlogData.tasks):
            
            timeCompleted = self.backlogData.tasks[iTaskRow].completedTime
            estimatedTime = self.backlogData.tasks[iTaskRow].estimatedTime

            if estimatedTime != 0:
                ratio = int((timeCompleted / estimatedTime) * 100)
            else:
                ratio = 0

        return ratio
            
