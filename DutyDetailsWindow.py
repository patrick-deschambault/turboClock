from PyQt5.QtWidgets import (QFormLayout, QApplication, QWidget, QDialog, QTextEdit, QVBoxLayout)

from BacklogData import *
from Task import *

class DutyDetailsWindow(QDialog):

    def __init__(self, parent, iBacklogData):
        super().__init__(parent)

        self.backlogData = iBacklogData

        mainLayout = QVBoxLayout(self)

        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)
        self.doInit()

        self.textEdit.autoFormatting()

        mainLayout.addWidget(self.textEdit)

    def doInit(self):        
        
        taskRegInDutyText = self.genTaskRegisteredString()
        self.textEdit.setText(taskRegInDutyText)

    def genTaskRegisteredString(self):
        
        currDate = self.backlogData.currDuty.date

        s = 'Time to log for the ' + currDate + ':\n'
        s += '\n'

        for currTask in self.backlogData.currDuty.tasksRegistered:

            s += currTask.prjCode
            s += ' - '
            s += currTask.title
            s += ': '
            s += str(datetime.timedelta(seconds = currTask.completedTime))
            s += '\n'

        s += '\n'
        s += 'Total time completed: '
        s += str(datetime.timedelta(seconds = self.backlogData.currDuty.totalTimeCompleted))

        return s

        


        


        