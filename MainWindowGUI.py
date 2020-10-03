#-*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QLCDNumber, QVBoxLayout, QHBoxLayout, QApplication, QWidget, QLabel, QLineEdit, QPushButton, QDialog, QComboBox, QMessageBox, QProgressBar, QSystemTrayIcon)
from PyQt5.QtCore import QTimer, QTime, QSettings
from PyQt5.QtGui import QIcon, QPalette, QColor

from EditBacklogGUI import *
from EditDutyGUI import *

from datetime import timedelta

from Backlog import *
from Piece import *

import sys

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.backlog = Backlog()

        self.backlog.load("C:\\Users\\Patrick\\Documents\\Python\\Giro\\turboClock\\Data\\tasksData.dat")

        self.currTask = Task()

        self.currPiece = Piece()

        self.currDuty = Duty()

        self.currTaskItemRow = 0

        self.isTimerRunning = False

        self.editTasksGUI = EditBacklogGUI(self, self.backlog)

        self.initUI()

    def initUI(self):

        self.setWindowTitle("TurboClock")

        self.resize(400, 300)
        self.setWindowIcon(QIcon('Images//clock.png'))

        self.icon = QSystemTrayIcon(self)
        self.icon.setIcon(QIcon('Images//clock.png'))
        self.icon.setVisible(True)
        
        self.lcdNumber = QLCDNumber()
        self.lcdNumber.setNumDigits(8)

        self.btnStartPause = QPushButton('', self)
        self.btnStartPause.setIcon(QIcon('Images//play_icon.png'))
        self.btnStartPause.clicked.connect(self.manageStartPauseClickButton)

        self.btnDutyDetails = QPushButton('Duty details...')
        self.btnDutyDetails.clicked.connect(self.manageDutyDetailsClickedEvent)

        self.btnAddTfsTask = QPushButton('', self)
        self.btnAddTfsTask.setIcon(QIcon('Images//plus_icon.png'))
        self.btnAddTfsTask.clicked.connect(self.manageEditTasksOptions)

        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)

        self.dutyTimeCompLbl = QLabel()        

        self.taskCb = QComboBox(self)
        self.initTaskCombobox()

        mainLayout = QVBoxLayout(self)

        layoutTimer = QVBoxLayout()
        layoutTimer.addWidget(self.lcdNumber)

        fieldsInputLayout = QHBoxLayout()

        layoutInputCodes = QVBoxLayout()
        layoutInputCodes.addWidget(self.taskCb)

        layoutAddBtn = QVBoxLayout()
        layoutAddBtn.addWidget(self.btnAddTfsTask)

        fieldsInputLayout.addLayout(layoutInputCodes)
        fieldsInputLayout.addLayout(layoutAddBtn)

        layoutDutyStat = QHBoxLayout()
        layoutDutyStat.addWidget(self.dutyTimeCompLbl)

        layoutProgressBar = QHBoxLayout()
        layoutProgressBar.addWidget(self.progressBar)

        mainLayout.addLayout(layoutTimer)
        mainLayout.addLayout(fieldsInputLayout)
        mainLayout.addWidget(self.btnStartPause)
        mainLayout.addWidget(self.btnDutyDetails)
        mainLayout.addWidget(self.progressBar)
        mainLayout.addLayout(layoutDutyStat)

        self.timer = QTimer(self)
        self.deltaTimer = 0
        self.currTimeLCD = QTime(0,0,0)
        self.currTimeDuty = QTime(0,0,0)

        self.timer.timeout.connect(self.incrementTimer)

        self.updateTimeLCD()
        self.updateDutyTimeDisp()
        self.updateProgressBarDisplay()

    def initTaskCombobox(self):

        self.updateTaskCombobox()

        self.taskCb.currentIndexChanged.connect(self.manageCbIndexChange)

    def updateProgressBarDisplay(self):

        estimatedTime = self.currTask.estimatedTime

        if estimatedTime == 0:
            return

        ratioFromTimer = (self.deltaTimer / estimatedTime)

        totalCompletionPerc = int((self.currTask.completionRatio + ratioFromTimer) * 100)

        if totalCompletionPerc <= 100:
            self.progressBar.setValue(totalCompletionPerc)
        else:
            self.progressBar.setValue(100)
    
    def updateTaskCombobox(self):

        currTaskIndex = 0

        self.taskCb.clear()

        tasks = self.backlog.tasks

        for currTask in tasks:

            taskDesc = currTask.title + ' - ' + currTask.prjCode
            self.taskCb.addItem(taskDesc)

        self.taskCb.setCurrentIndex(currTaskIndex)

        self.manageSelectedTaskChange(self.taskCb.currentText())

    def manageCbIndexChange(self):

        self.currTaskItemRow = self.taskCb.currentIndex()

        if self.currTaskItemRow >= 0 and self.currTaskItemRow <= self.taskCb.count():

            currTextCb = self.taskCb.currentText()
            self.manageSelectedTaskChange(currTextCb)

        self.updateTimeLCD()

        self.deltaTimer = 0
        self.updateProgressBarDisplay()

    def updateTimeLCD(self):

        currTaskTimeStr = str(datetime.timedelta(seconds = self.currTask.completedTime))
        currTaskTime_split = str(currTaskTimeStr).split(':')

        h = int(currTaskTime_split[0])
        m = int(currTaskTime_split[1])
        s = int(currTaskTime_split[2])

        self.currTimeLCD = QTime(h,m,s)
        self.lcdNumber.display(self.currTimeLCD.toString('hh:mm:ss'))

    def updateDutyTimeDisp(self):

        currDutyTimeStr = str(datetime.timedelta(seconds = self.currDuty.totalTimeCompleted))
        currDutyTime_split = currDutyTimeStr.split(':')

        h = int(currDutyTime_split[0])
        m = int(currDutyTime_split[1])
        s = int(currDutyTime_split[2])

        self.currTimeDuty = QTime(h,m,s)
        self.dutyTimeCompLbl.setText('Daily time completed: ' + self.currTimeDuty.toString('hh:mm:ss'))

    def incrementTimer(self):

        self.currTimeLCD = self.currTimeLCD.addSecs(1)
        self.lcdNumber.display(self.currTimeLCD.toString('hh:mm:ss'))

        self.currTimeDuty = self.currTimeDuty.addSecs(1)
        self.dutyTimeCompLbl.setText('Daily time completed: ' + self.currTimeDuty.toString('hh:mm:ss'))

        self.deltaTimer += 1

        self.updateProgressBarDisplay()

    def manageSelectedTaskChange(self, iCbbText):

        splitCurrTextCb = iCbbText.split(' - ')

        title = splitCurrTextCb[0]
        prjCode = splitCurrTextCb[1]

        indexBacklogCurrTask = self.backlog.getIndexFromTask(Task(prjCode, title))  

        if indexBacklogCurrTask != None:

            if self.isTimerRunning:

                self.endPiece()
                self.startPiece()

            self.currTask = self.backlog.tasks[indexBacklogCurrTask]

        else:
            return

    def startPiece(self):
        
        self.currPiece = Piece(self.currTask, datetime.datetime.now())        
        self.isTimerRunning = True

    def endPiece(self):

        self.currPiece.setEndDateTime(datetime.datetime.now())

        self.currDuty.addPiece(self.currPiece)

        self.currTask.addCompletedTime(self.currPiece.task.completedTime)

        self.isTimerRunning = False

    def manageStartPauseClickButton(self):

        if self.currTask:

            self.deltaTimer = 0

            if self.isTimerRunning:
                self.timer.stop()
                self.endPiece()
                self.btnStartPause.setIcon(QIcon('Images//play_icon.png'))
            else:
                self.timer.start(1000)
                self.startPiece()
                self.btnStartPause.setIcon(QIcon('Images//pause_icon.png'))

    def manageDutyDetailsClickedEvent(self):
        pass

    def manageEditTasksOptions(self):

        self.editTasksGUI.exec_()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
