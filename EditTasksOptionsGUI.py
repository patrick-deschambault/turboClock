
from PyQt5.QtWidgets import (QFormLayout, QApplication, QWidget, QLabel, QLineEdit, QDialogButtonBox, QDialog, QHBoxLayout, QVBoxLayout, QListWidget, QPushButton)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QModelIndex

import datetime

from Task import *

class EditTasksOptionsGUI(QDialog):

    def __init__(self, parent, iBacklogMgr):
        super().__init__(parent)

        self.backlogMgr = iBacklogMgr

        self.currTaskSelected = ""

        self.newItemEnum = 0

        self.initUI()

    def initUI(self):

        self.setWindowTitle("Edit tasks")
        self.resize(1000, 400)

        mainLayout =  QVBoxLayout(self)
        listViewTaskViewLayout = QHBoxLayout()
        self.listViewLayout = QVBoxLayout()

        self.listTasksView = QListWidget(self)

        self.loadTasksOptions()
        
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

    def manageCurrItemChangeTaskList(self):

        currItemIndex = self.listTasksView.currentRow()
        self.updateCurrTaskLineEdits(currItemIndex)

    def updateCurrTaskLineEdits(self, iCurrentTaskRow):

        self.currTaskSelected = self.backlogMgr.backlogData.tasks[iCurrentTaskRow]

        self.idInput.setText(self.currTaskSelected.id)
        self.titleInput.setText(self.currTaskSelected.title)
        self.prjCodeInput.setText(self.currTaskSelected.prjCode)

        compTime = str(datetime.timedelta(seconds = self.currTaskSelected.completedTime))
        self.completedTime.setText(compTime)

        estimatedTime = str(datetime.timedelta(seconds = self.currTaskSelected.estimatedTime))
        self.estimatedTime.setText(estimatedTime)

        self.percAccomplished = str(self.currTaskSelected.completionRatio)

    def loadTasksOptions(self):

        self.currTaskOptions = self.backlogMgr.backlogData.tasks
        self.initListViewOfTasks()

    def initListViewOfTasks(self):

        for currTask in self.currTaskOptions:
            
            currId = currTask.id
            currTitle = currTask.title
            textItem = currId + ' - ' + currTitle

            self.listTasksView.addItem(textItem)

        self.listTasksView.currentItemChanged.connect(self.manageCurrItemChangeTaskList)

    def manageAddTaskClickedButton(self):

        self.newItemEnum += 1

        newTask = Task()
        #self.backlogMgr.manageAddTaskBacklogDataFromGUI()
        
        self.listTasksView.addItem('New Item {}'.format(str(self.newItemEnum)))

        self.currTaskSelected = self.currTaskOptions[-1]

        lastRowListView = self.listTasksView.count() - 1
        self.listTasksView.setCurrentRow(lastRowListView)

    def manageDeleteTaskClickedButton(self):

        selectedItem = self.listTasksView.selectedItems()

        identifier = self.currTaskSelected.id
        prjCode = self.currTaskSelected.prjCode
        title = self.currTaskSelected.title

        if not selectedItem:
            return
        else:
            for item in selectedItem:
                elemIndex = QModelIndex(self.listTasksView.indexFromItem(item)).row()
                self.listTasksView.takeItem(self.listTasksView.row(item))

                self.backlogMgr.deleteTaskBacklogData(identifier, prjCode, title)

