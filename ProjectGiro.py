
from TaskGiro import *

class ProjectGiro():

    def __init__(self, iCode = ""):

        self.code = iCode
        self.description = ""
        self.taskGiroList = list()

    def addTasks(self, listTasksGiro):
        
        self.taskGiroList += listTasksGiro

    def addTasksFromCodes(self, listTasksGiroCodes):

        for code in listTasksGiroCodes:
            self.taskGiroList.append(TaskGiro(code))