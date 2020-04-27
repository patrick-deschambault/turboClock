from PyQt5.QtWidgets import (QFormLayout, QApplication, QWidget, QDialog, QTextEdit, QVBoxLayout)

from BacklogData import *
from Task import *

class TasksDetailsWindow(QDialog):

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

        taskSummaryText = self.genTasksString()
        self.textEdit.setText(taskSummaryText)

    def genTasksString(self):

        s = 'Tasks summary:\n'
        s += '\n'

        for currTask in self.backlogData.tasks:

            s += currTask.id
            s += ' - '
            s += currTask.prjCode
            s += ' - '
            s += currTask.title
            s += '\n'
            s += 'Time logged: ' + str(datetime.timedelta(seconds = currTask.completedTime)) + '\n'
            s += 'Estimated Time: ' + str(datetime.timedelta(seconds = currTask.estimatedTime)) + '\n'
            s += 'Completion ratio: ' + str(currTask.completionRatio) + '%\n'
            s += '\n'

        return s

        


        


        