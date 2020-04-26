from Task import *
from Duty import *

from datetime import *
import os

from BacklogData import *

class BacklogMgr():

    def __init__(self):

        self.backlogData = BacklogData()

        self.initCurrDate()

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
        
        file = open(self.backlogData.pathTasksData, 'r')
        for line in file:

            if(line != ""):
                line = line.split(";")

                taskId = line[0]
                taskProjectCode = line[1]
                taskTitle = line[2]
                completedTime = int(line[3].rstrip('\n'))

                self.addNewTask(taskId, taskProjectCode, taskTitle, completedTime)

            else:
                break
        file.close()

    def loadDutyData(self, iDate, iDuty):

        dutyDataExist = os.path.isfile(self.backlogData.pathTasksData)
        if not dutyDataExist:
            file = open(self.backlogData.pathTasksData, 'w+')
            file.close()

        file = open(self.backlogData.filenameDutyData,'r')
        for line in file:
            if line != '\n':
                lineSplit = line.split(';')

                taskId = lineSplit[0]
                taskPrjCode = lineSplit[1]
                title = lineSplit[2]

                currDtyDate = self.backlogData.currDuty.date
                formatDateTime = '%Y-%m-%d %H:%M:%S'

                startTime = datetime.datetime.strptime(currDtyDate + ' ' + lineSplit[4],  formatDateTime)
                endTime =   datetime.datetime.strptime(currDtyDate + ' ' + lineSplit[5].rstrip('\n'),  formatDateTime)

                newTask = Task(taskPrjCode, title, taskId)
                newPiece = Piece(newTask, startTime, endTime)

                iDuty.addPiece(newPiece)

        file.close()

    def initCurrDuty(self):

        currDate = self.backlogData.currDate
        self.loadDutyData(currDate, self.backlogData.currDuty)
    
    def addNewTask(self, iId, iPrjCode, iTitle, iCompletedTime = 0):
        
        newTask = Task(iPrjCode, iTitle, iId)
        newTask.addCompletedTime(iCompletedTime)

        if not self.isTaskAlreadyExist(newTask):
            self.backlogData.tasks.append(newTask)

    def addPieceToCurrDuty(self, iPiece):

        self.backlogData.currDuty.addPiece(iPiece)

        taskBacklog = self.isTaskAlreadyExist(iPiece.task)
        taskBacklog.completedTime += iPiece.task.completedTime

    def isTaskAlreadyExist(self, iTask):

        alreadyExist = False

        for currTask in self.backlogData.tasks:
            if iTask.id == currTask.id:
                return currTask
            else:
                if iTask.id == "":
                    if iTask.title == currTask.title and \
                        iTask.prjCode == currTask.prjCode:
                        return currTask
                    else: 
                        continue
                else:
                    continue

        return alreadyExist

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
        s += str(iPiece.task.completedTime)
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

    def setCurrentTaskFromGUI(self, iComboboxText):
        
        split_cbboxText = iComboboxText.split(';')

        currTaskId = split_cbboxText[0]

        self.backlogData.currTask = self.getTaskFromId(currTaskId)
 

    def getListTasksFromGUI(self):

        cbboxElmDesclist = list()

        for task in self.backlogData.tasks:
            cbboxElmDesc = ''

            if task.id:
                cbboxElmDesc = task.id + ';' + \
                               task.title        
            else:
                cbboxElmDesc = task.prjCode + ';' + \
                               task.title
                               
            cbboxElmDesclist.append(cbboxElmDesc)
            
        return cbboxElmDesclist

    def getCurrDutyTimeCompletedFromGUI(self):

        secCompleted = self.backlogData.currDuty.totalTimeCompleted
        return str(datetime.timedelta(seconds = secCompleted))

    def getCompletedTimeCurrTaskFromGUI(self):

        secCompleted = self.backlogData.currTask.completedTime
        return str(datetime.timedelta(seconds = secCompleted))

    def manageClickButtonFromGUI(self, iCbboxText):

        currTaskId = iCbboxText.split(';')[0]
        self.backlogData.currTask = self.getTaskFromId(currTaskId)

        if self.backlogData.currTask.id != '':
            if not self.backlogData.isTimerRunning:
                self.startPiece()
            else:
                self.endPiece()
            return True
        else:
            return False

    def getTaskFromId(self, iId):

        for currTask in self.backlogData.tasks:
            if currTask.id == iId:
                return copy.copy(currTask)
            else:
                continue

        emptyTask = Task()  
        return emptyTask

'''
    def manageOpenEventFromGUI(self):
        self.initCurrDuty()
        

    def manageCloseEventFromGUI(self):
        print("end")


    def getCurrPrjCodeGUI(self):
        split_res = self.backlogData.currTask.prjCode.split('-')[0]
        return split_res

    def getCurrTaskFromGUI(self):
        split_res = self.backlogData.currTask.prjCode.split('-')[1:]
        return split_res



'''                  
