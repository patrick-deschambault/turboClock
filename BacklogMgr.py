
from TaskGiro import *
from ProjectGiro import *
from TFSTask import *
import os

from BacklogData import *

class BacklogMgr():

    def __init__(self):

        self.backlogData = BacklogData()


    def loadGiroTaskProjectCodesData(self):

        with open('girotaskprojectcodes.dat', 'r') as file:
            for line in file:

                if(line != ""):
                    line_list = line.split(",")

                    projectGiroCode = line_list[0]

                    taskGiroCodelist = list()
                    taskGiroCodelist = line_list[1:]

                    self.addNewProject(projectGiroCode, taskGiroCodelist)

                else:
                    break
        file.close()
    
    def loadGiroTFSData(self):

        with open('giroTFS.dat', 'r') as file:
            for line in file:

                if(line != ""):
                    line_list = line.split(",")

                    tfsCode = line_list[0]
                    tfsDescription = line_list[1]
                    tfsProjectCode = line_list[2]
                    tfsTaskCode = line_list[3].split('\n')[0]

                    self.addNewTFSTask(tfsCode, tfsDescription, tfsProjectCode, tfsTaskCode)
        file.close()

    def loadDuty(self, iDate, iDuty):

        duty = Duty()
        folderNameDuty = duty.computeMondayDateWeek(iDate)

        path = folderNameDuty + '\\' + iDate.strftime("%Y-%m-%d") 

        with open(path,'r') as file:
            for line in file:

                lineSplit = line.split(',')

                prjCode = lineSplit[0]
                taskCode = lineSplit[1]
                tfsTaskCode = lineSplit[2]
                desc = lineSplit[3]
                date = lineSplit[4]
                startTime = lineSplit[5]
                endTime = lineSplit[6]
                dTime = lineSplit[7]

                

                newPiece = Piece()

                iDuty.addPiece(newPiece)

    
    def addNewProject(self, projectCodeGiro, taskGiroCodelist):

        self.backlogData.projectGirolist.append(ProjectGiro(projectCodeGiro))
        self.backlogData.projectGirolist[-1].addTasksFromCodes(taskGiroCodelist)
    
    def addNewTFSTask(self, tfsCode, tfsDescription, tfsProjectCode, tfsTaskCode):
        
        isProjFound, projIndex = self.isProjectExist(tfsProjectCode)

        if isProjFound:

            isTaskFound, indexTask = self.isTaskInProjectExist(tfsProjectCode, tfsTaskCode)

            if isTaskFound:

                projectToAdd = self.backlogData.projectGirolist[projIndex]
                taskToAdd =   projectToAdd.taskGiroList[indexTask]

                self.backlogData.taskTFSGirolist.append(TFSTask(tfsCode, \
                                                                tfsDescription, \
                                                                projectToAdd, \
                                                                taskToAdd))
    
    def createPiece(self, iTaskTFS, iStartDateTime, iEndDateTime):

        newPiece = Piece(iTaskTFS, iStartDateTime, iEndDateTime)

        iTaskTFS.addCompletedTime(newPiece.deltaTime)

        self.backlogData.currDuty.addPiece(newPiece)
        #self.backlogData.pieces.append(newPiece)

        self.savePieceToDutyFile(self.backlogData.currDuty, newPiece)


    def savePieceToDutyFile(self, duty, pce):

        weekDateString = duty.mondayDateCurrWeek.strftime("%Y-%m-%d") 

        if not os.path.exists('week_' + weekDateString):
            os.makedirs('week_' + weekDateString)

        s = ""

        s += str(pce.tfsTask.projectGiro.code)
        s += ","
        s += str(pce.tfsTask.taskGiro.code)
        s += ","
        s += str(pce.tfsTask.code)
        s += ","
        s += str(pce.tfsTask.description)
        s += ","
        s += str(pce.startDateTime.strftime("%Y-%m-%d"))
        s += ","
        s += str(pce.startDateTime.strftime("%H:%M:%S"))
        s += ","
        s += str(pce.endDateTime.strftime("%H:%M:%S"))
        s += ","
        s += str(pce.deltaTime)
        s += '\n'

        dutyDateStringFormat = duty.date.strftime("%Y-%m-%d") 

        with open('week_' + weekDateString + '\\duty_' + dutyDateStringFormat + '.dat', "a") as file:
            file.write(s)
            file.close()


    def isProjectExist(self, iProjectCode):

        isFound = False
        index = 0
        for index, project in enumerate(self.backlogData.projectGirolist):
            
            if project.code == iProjectCode:
                isFound = True
                break

        return isFound, index

    def isTaskInProjectExist(self, iProjectCode, iTaskCode):

        isFound = False
        isProjectFound, index = self.isProjectExist(iProjectCode)

        if isProjectFound and index >= 0:

            for index, task in enumerate(self.backlogData.projectGirolist[index].taskGiroList):
                if task.code == iTaskCode:
                    isFound = True
                    break
 
        return isFound, index
    
    def getTFSTasks(self):
        return self.backlogData.taskTFSGirolist

    def setCurrentTFSTask(self, iIndex):
        
        tfsTaskList = self.backlogData.taskTFSGirolist

        if iIndex >= 0 and iIndex < len(tfsTaskList):
            self.backlogData.currTFSTask = self.backlogData.taskTFSGirolist[iIndex]

            self.backlogData.currProjectCode = self.backlogData.currTFSTask.projectGiro.code
            self.backlogData.currTaskCode = self.backlogData.currTFSTask.taskGiro.code

    def getCurrentTaskCode(self):
        return self.backlogData.currTaskCode

    def getCurrentProjectCode(self):
        return self.backlogData.currProjectCode


    def createTimeSheet(self, weekDateString):

        folderPath = 'week_' + weekDateString
        files = []
        tasksToLog = []

        if os.path.exists(folderPath):
            
            for r,d,f in os.walk(folderPath):
                for file in f:
                    if '.dat' in file:
                        files.append(os.path.join(r,file))

        for dutyDateFilename in files:
            with open (dutyDateFilename, 'r') as file:
                for pieceData in file:

                    pieceDataSplit = pieceData.split(',')

                    currPrjCode = pieceDataSplit[0]
                    currTaskCode = pieceDataSplit[1]
                    currTaskTFSCode = pieceDataSplit[2]
                    currDescription = pieceDataSplit[3]
                    currTimeCompleted = pieceDataSplit[7]

            
            print(tasksToLog[0])



                    


                

