
from PyQt5.QtWidgets import (QFormLayout, QApplication, QWidget, QLabel, QLineEdit, QDialogButtonBox, QDialog, QHBoxLayout, QVBoxLayout, QListWidget, QPushButton)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QModelIndex

import datetime
import enum

from Task import *

class State(enum.Enum):

    ADDING_TASK = 0
    DELETE_TASK = 1
    SELECT_TASK = 2

class EditTasksOptionsGUI(QDialog):

    def __init__(self, parent, iBacklogMgr):
        super().__init__(parent)

        self.backlogMgr = iBacklogMgr

        self.currTaskSelected = Task()

        self.currRowSelected = 0

        self.newItemEnum = 0

        self.isTakeItemFromList = False

        self.listState = State.SELECT_TASK

        self.tasksList = self.backlogMgr.getTasksFromGUI()

        self.currTaskErrors = list()

        self.initUI()

    def initUI(self):

        self.setWindowTitle("Edit tasks")
        self.resize(1000, 400)

        mainLayout =  QVBoxLayout(self)
        listViewTaskViewLayout = QHBoxLayout()
        self.listViewLayout = QVBoxLayout()

        self.listTasksView = QListWidget(self)
        
        self.layoutCurrTask = QFormLayout()

        self.initCurrTaskLineEdits()

        self.addTaskButton = QPushButton(self)
        self.addTaskButton.setIcon(QIcon("Images//plus_icon.png"))
        self.addTaskButton.clicked.connect(self.manageAddTaskClickedButton)

        self.deleteTaskButton = QPushButton(self)
        self.deleteTaskButton.setIcon(QIcon("Images//minus_icon.png"))
        self.deleteTaskButton.clicked.connect(self.manageDeleteTaskClickedButton)

        self.listViewLayout.addWidget(self.listTasksView)
        self.listViewLayout.addWidget(self.addTaskButton)
        self.listViewLayout.addWidget(self.deleteTaskButton)

        listViewTaskViewLayout.addLayout(self.listViewLayout)
        listViewTaskViewLayout.addLayout(self.layoutCurrTask)

        mainLayout.addLayout(listViewTaskViewLayout)

        self.loadTasksOptions()

        self.updateCurrTaskSelected()

    def initCurrTaskLineEdits(self):

        self.idInput = QLineEdit(self)
        self.titleInput = QLineEdit(self)
        self.prjCodeInput = QLineEdit(self)
        self.completedTime = QLineEdit(self)
        self.estimatedTime = QLineEdit(self)
        self.percAccomplished = QLineEdit(self)
        self.percAccomplished.setEnabled(False)

        self.layoutCurrTask.addRow("Id:", self.idInput)
        self.layoutCurrTask.addRow("Title:", self.titleInput)
        self.layoutCurrTask.addRow("Project code:", self.prjCodeInput)
        self.layoutCurrTask.addRow("Completed time:", self.completedTime)
        self.layoutCurrTask.addRow("Estimated time:", self.estimatedTime)
        self.layoutCurrTask.addRow("Percentage accomplished:", self.percAccomplished)

    def manageCurrRowChangeList(self):

        prevRowSelected = self.currRowSelected
        self.currRowSelected = self.listTasksView.currentRow()

        if self.listState == State.ADDING_TASK:
            
            self.tasksList.append(Task())

        elif self.listState == State.DELETE_TASK:
            
            countListItems = self.listTasksView.count()

            if countListItems > 0  and prevRowSelected >= 0:
                self.tasksList.pop(prevRowSelected)

                if self.currRowSelected > prevRowSelected:
                    self.currRowSelected = prevRowSelected
            else:
                pass
        else:
            pass

        self.updateCurrTaskSelected()

        self.setCurrTaskFromLineEdits()

    def updateCurrTaskSelected(self):

        if self.currRowSelected >= 0 and \
           self.currRowSelected < len(self.tasksList):

            self.currTaskSelected = self.tasksList[self.currRowSelected]
        else:
            self.currTaskSelected = Task()

        self.updateCurrTaskLineEdits()

    def updateCurrTaskLineEdits(self):

        self.idInput.setText(self.currTaskSelected.id)
        self.titleInput.setText(self.currTaskSelected.title)
        self.prjCodeInput.setText(self.currTaskSelected.prjCode)

        compTime = str(datetime.timedelta(seconds = self.currTaskSelected.completedTime))
        self.completedTime.setText(compTime)

        estimatedTime = str(datetime.timedelta(seconds = self.currTaskSelected.estimatedTime))
        self.estimatedTime.setText(estimatedTime)

        self.percAccomplished = str(self.currTaskSelected.completionRatio)

    def loadTasksOptions(self):

        self.initListViewOfTasks()

    def initListViewOfTasks(self):

        for currTask in self.tasksList:
            
            currId = currTask.id
            currTitle = currTask.title
            textItem = currId + ' - ' + currTitle

            self.listTasksView.addItem(textItem)

        self.currRowSelected = 0
        self.listTasksView.setCurrentRow(self.currRowSelected)

        self.listTasksView.itemSelectionChanged.connect(self.manageCurrRowChangeList)
        
    def manageAddTaskClickedButton(self):

        self.listState = State.ADDING_TASK

        self.newItemEnum += 1
        
        self.listTasksView.addItem('New Item {}'.format(str(self.newItemEnum)))

        lastRowListView = self.listTasksView.count() - 1
        self.listTasksView.setCurrentRow(lastRowListView)

        self.listState = State.SELECT_TASK


    def manageDeleteTaskClickedButton(self):

        self.listState = State.DELETE_TASK

        self.listTasksView.takeItem(self.currRowSelected)

        self.listState = State.SELECT_TASK

    def setCurrTaskFromLineEdits(self):
        
        self.currTaskSelected.id = self.idInput.text()
        self.currTaskSelected.title = self.titleInput.text()
        self.currTaskSelected.prjCode = self.prjCodeInput.text()

        self.currTaskSelected.setCompletedTime(self.completedTime.text())
        self.currTaskSelected.setEstimatedTime(self.estimatedTime.text())
