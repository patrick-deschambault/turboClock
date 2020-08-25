
import copy
import datetime

from Task import Task

class Duty():

    def __init__(self):

        self.date = datetime.datetime.now().strftime('%Y-%m-%d')

        self.mondayDateCurrWeek = self.getMondayDateOfCurrWeek(self.date)

        self.pieces = list()

        self.tasksRegistered = list()

        self.totalTimeCompleted = 0


    def addPiece(self, iPiece):
        
        self.pieces.append(iPiece)

        self.registerPieceForTaskStats(iPiece)

    def getMondayDateOfCurrWeek(self, iDate):

        format = '%Y-%m-%d'
        date = datetime.datetime.strptime(iDate, format)
        weekday = date.weekday()

        return (date - datetime.timedelta(days=weekday)).strftime(format)

    def registerPieceForTaskStats(self, iPiece):
    
        taskOfPce = copy.copy(iPiece.task)

        isTaskIDFoundInRegisteredTasks = False
        isTaskNoIDFoundInRegisteredTasks = False
        index = 0

        if len(self.tasksRegistered) > 0:

            for i, currTask in enumerate(self.tasksRegistered):

                if currTask.id != "":
                    if currTask.id == taskOfPce.id:
                        isTaskIDFoundInRegisteredTasks = True
                        index = i
                        break
                    else:
                        continue
                else:
                    if currTask.title != "":
                        if currTask.prjCode == taskOfPce.prjCode and currTask.title == taskOfPce.title:
                            
                            isTaskNoIDFoundInRegisteredTasks = True
                            index = i
                            break
                        else:
                            continue
                    else:
                        #Impossible to register a task with no description with time completed
                        continue

            if isTaskIDFoundInRegisteredTasks or isTaskNoIDFoundInRegisteredTasks:
                self.tasksRegistered[index].addCompletedTime(taskOfPce.completedTime)
                self.totalTimeCompleted += taskOfPce.completedTime
            else:
                self.tasksRegistered.append(taskOfPce)
                self.totalTimeCompleted += taskOfPce.completedTime
        else:
            self.tasksRegistered.append(taskOfPce)
            self.totalTimeCompleted += taskOfPce.completedTime





        

