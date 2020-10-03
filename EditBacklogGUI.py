
from PyQt5.QtWidgets import (QFormLayout, QApplication, QWidget, QLabel, QLineEdit, QDialogButtonBox, QDialog, QHBoxLayout, QVBoxLayout, QListWidget, QPushButton, QMessageBox)
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import Qt, QModelIndex

from datetime import datetime, timedelta
import enum

from Task import *
from Backlog import *

class State(enum.Enum):

    ADDING_TASK = 0
    DELETE_TASK = 1
    SELECT_TASK = 2

class EditBacklogGUI(QDialog):

    def __init__(self, parent, iBacklog):
        super().__init__(parent)

        self.backlog = iBacklog 

        self.tempoBacklog = copy.deepcopy(self.backlog)

        self.currTask = Task()

        self.tempoTask = Task()

        self.currRowSelected = 0

        self.newItemEnum = 0

        self.listState = State.SELECT_TASK

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

        self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)

        self.listViewLayout.addWidget(self.listTasksView)
        self.listViewLayout.addWidget(self.addTaskButton)
        self.listViewLayout.addWidget(self.deleteTaskButton)

        listViewTaskViewLayout.addLayout(self.listViewLayout)
        listViewTaskViewLayout.addLayout(self.layoutCurrTask)

        mainLayout.addLayout(listViewTaskViewLayout)
        mainLayout.addWidget(self.buttonbox)

        self.invalidTaskErrMsg = QMessageBox()
        self.invalidTaskErrMsg.setText("The current task is invalid.")
        self.invalidTaskErrMsg.setIcon(QMessageBox.Critical)

        self.initListViewOfTasks()

        self.updateCurrTaskSelected()

    def exec_(self):

        self.tempoBacklog = copy.deepcopy(self.backlog)

        self.initListViewOfTasks()

        self.updateCurrTaskSelected()

        self.titleInputErr.setVisible(False)
        self.prjCodeInputErr.setVisible(False)
        
        self.exec()

    def initCurrTaskLineEdits(self):

        self.titleInputErr = QLabel(self)

        self.titleInput = QLineEdit(self)
        self.titleInput.editingFinished.connect(self.manageTitleEntered)

        self.prjCodeInputErr = QLabel(self)
        self.prjCodeInput = QLineEdit(self)
        self.completedTime = QLineEdit(self)
        self.estimatedTime = QLineEdit(self)
        self.percAccomplished = QLineEdit(self)
        self.percAccomplished.setEnabled(False)

        self.redPalette = QPalette()
        redColor = QColor(255, 0, 0)
        self.redPalette.setColor(QPalette.WindowText, redColor)

        self.titleInputErr.setText("* A title is required.")
        self.layoutCurrTask.addWidget(self.titleInputErr)
        self.titleInputErr.setVisible(False)
        self.titleInputErr.setPalette(self.redPalette)

        self.layoutCurrTask.addRow("Title:", self.titleInput)
        
        self.prjCodeInputErr.setText("* A project code is required.")
        self.layoutCurrTask.addWidget(self.prjCodeInputErr)
        self.prjCodeInputErr.setVisible(False)
        self.prjCodeInputErr.setPalette(self.redPalette)

        self.layoutCurrTask.addRow("Project code:", self.prjCodeInput)
        self.layoutCurrTask.addRow("Completed time:", self.completedTime)
        self.layoutCurrTask.addRow("Estimated time:", self.estimatedTime)
        self.layoutCurrTask.addRow("Percentage accomplished:", self.percAccomplished)

    def manageTitleEntered(self):

        self.updateTextRowListView(self.currRowSelected, self.titleInput.text())
    
    def manageCurrRowChangeList(self):

        prevRowSelected = self.currRowSelected
        self.currRowSelected = self.listTasksView.currentRow()

        if self.listState == State.ADDING_TASK:
            pass
        elif self.listState == State.DELETE_TASK:
            pass
        else:

            self.updateTaskFromLineEdits(self.tempoTask)

            isTaskNotValid = self.tempoBacklog.validateTask(self.tempoTask)

            if len(isTaskNotValid):
                self.titleInputErr.setVisible(True)
                self.prjCodeInputErr.setVisible(True)
                self.currRowSelected = prevRowSelected
                self.listTasksView.setCurrentRow(self.currRowSelected)

            else:
                self.titleInputErr.setVisible(False)
                self.prjCodeInputErr.setVisible(False)

                self.updateTaskFromLineEdits(self.currTask)

                self.updateTextRowListView(prevRowSelected, self.currTask.title)

                self.updateCurrTaskSelected()

    def updateCurrTaskSelected(self):

        tasks = self.tempoBacklog.tasks

        if self.currRowSelected >= 0 and self.currRowSelected < len(tasks):
            self.currTask = tasks[self.currRowSelected]
        else:
            self.currTask = Task()

        self.updateCurrTaskLineEdits()

    def updateCurrTaskLineEdits(self):

        self.titleInput.setText(self.currTask.title)
        self.prjCodeInput.setText(self.currTask.prjCode)

        compTime = str(timedelta(seconds = self.currTask.completedTime))
        self.completedTime.setText(compTime)

        estimatedTime = str(timedelta(seconds = self.currTask.estimatedTime))
        self.estimatedTime.setText(estimatedTime)

        self.percAccomplished = str(self.currTask.completionRatio)

    def initListViewOfTasks(self):

        self.listTasksView.clear()

        for currTask in self.tempoBacklog.tasks:
            
            self.listTasksView.addItem(currTask.title)

        self.currRowSelected = 0
        self.listTasksView.setCurrentRow(self.currRowSelected)

        self.listTasksView.itemSelectionChanged.connect(self.manageCurrRowChangeList)
        
    def manageAddTaskClickedButton(self):

        self.listState = State.ADDING_TASK

        self.newItemEnum += 1
        
        self.listTasksView.addItem('New Item {}'.format(str(self.newItemEnum)))

        lastRowListView = self.listTasksView.count() - 1
        self.listTasksView.setCurrentRow(lastRowListView)

        self.tempoBacklog.addTask(Task())

        self.updateCurrTaskSelected()

        self.listState = State.SELECT_TASK

    def manageDeleteTaskClickedButton(self):

        self.newItemEnum -= 1

        self.listState = State.DELETE_TASK

        self.listTasksView.takeItem(self.currRowSelected)
        
        self.currRowSelected = self.listTasksView.currentRow()

        countListItems = self.listTasksView.count()

        if countListItems >= 0:

            self.tempoBacklog.deleteTask(self.currTask)

            self.updateCurrTaskSelected()

        self.listState = State.SELECT_TASK

    def updateTaskFromLineEdits(self, iTask):
                
        iTask.title = self.titleInput.text()
        iTask.prjCode = self.prjCodeInput.text()

        iTask.setCompletedTime(self.completedTime.text())
        iTask.setEstimatedTime(self.estimatedTime.text())

    def closeEvent(self, event):

        self.reject()

    def accept(self):

        self.updateTaskFromLineEdits(self.tempoTask)

        isTaskNotValid = self.backlog.validateTask(self.tempoTask)

        if len(isTaskNotValid):

            self.invalidTaskErrMsg.exec()
            self.titleInputErr.setVisible(True)
            self.prjCodeInputErr.setVisible(True)
            return
            
        else:
            self.updateTaskFromLineEdits(self.currTask)

        self.close()

    def updateTextRowListView(self, iRow, iTaskTitle):

        item = self.listTasksView.item(iRow)
        item.setText(iTaskTitle)

