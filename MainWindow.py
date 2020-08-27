#-*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QLCDNumber, QVBoxLayout, QHBoxLayout, QApplication, QWidget, QLabel, QLineEdit, QPushButton, QDialog, QComboBox, QMessageBox, QProgressBar, QSystemTrayIcon)
from PyQt5.QtCore import QTimer, QTime, QSettings
from PyQt5.QtGui import QIcon, QPalette, QColor

from EditTasksOptionsGUI import *
from DutyDetailsWindow import *

import datetime

from BacklogMgr import *
from Piece import *

import sys

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        
        self.backlogMgr = BacklogMgr()

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
        self.btnStartPause.clicked.connect(self.manageStartPauseClickedEvent)

        self.btnDutyDetails = QPushButton('Duty details...')
        self.btnDutyDetails.clicked.connect(self.manageDutyDetailsClickedEvent)

        self.btnAddTfsTask = QPushButton('', self)
        self.btnAddTfsTask.setIcon(QIcon('Images//plus_icon.png'))
        self.btnAddTfsTask.clicked.connect(self.manageEditTasksOptions)

        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)

        self.dutyTimeCompLbl = QLabel()        

        self.currTaskItemRow = 0
        self.taskTFSCb = QComboBox(self)
        self.initTFSTaskCombobox()

        mainLayout = QVBoxLayout(self)

        layoutTimer = QVBoxLayout()
        layoutTimer.addWidget(self.lcdNumber)

        fieldsInputLayout = QHBoxLayout()

        layoutInputCodes = QVBoxLayout()
        layoutInputCodes.addWidget(self.taskTFSCb)

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

        self.startTime = 0
        self.stopTime = 0

        self.editTasksGUI = EditTasksOptionsGUI(self, self.backlogMgr)

    def initTFSTaskCombobox(self):

        self.updateTaskCombobox()

        self.taskTFSCb.currentIndexChanged.connect(self.manageCbTFSIndexChange)

    def updateProgressBarDisplay(self):

        estimatedTime = self.backlogMgr.backlogData.currTask.estimatedTime

        if estimatedTime == 0:
            return

        ratioFromTimer = (self.deltaTimer / estimatedTime) * 100

        totalCompletionRatio = self.backlogMgr.getCompletionRatio(self.backlogMgr.backlogData.currTaskIndex) + ratioFromTimer

        if totalCompletionRatio <= 100:
            self.progressBar.setValue(totalCompletionRatio)
        else:
            self.progressBar.setValue(100)
    
    def updateTaskCombobox(self):

        currTaskIndex = self.currTaskItemRow

        self.taskTFSCb.clear()

        taskList = self.backlogMgr.getTasksFromGUI()

        for currTask in taskList:

            taskDesc = currTask.title + ' (' + currTask.prjCode + ')'

            self.taskTFSCb.addItem(taskDesc)

        self.taskTFSCb.setCurrentIndex(currTaskIndex)

        self.backlogMgr.setCurrentTaskFromGUI(currTaskIndex)

    def manageCbTFSIndexChange(self):

        self.currTaskItemRow = self.taskTFSCb.currentIndex()

        if self.currTaskItemRow >= 0:
            self.backlogMgr.manageTaskChangeFromGUI(self.currTaskItemRow)

        self.updateTimeLCD()

        self.deltaTimer = 0
        self.updateProgressBarDisplay()

    def updateTimeLCD(self):

        currTaskTime_split = self.backlogMgr.getCompletedTimeCurrTaskFromGUI().split(':')

        h = int(currTaskTime_split[0])
        m = int(currTaskTime_split[1])
        s = int(currTaskTime_split[2])

        self.currTimeLCD = QTime(h,m,s)
        self.lcdNumber.display(self.currTimeLCD.toString('hh:mm:ss'))

    def updateDutyTimeDisp(self):

        currTaskTime_split = self.backlogMgr.getCurrDutyTimeCompletedFromGUI().split(':')

        h = int(currTaskTime_split[0])
        m = int(currTaskTime_split[1])
        s = int(currTaskTime_split[2])

        self.currTimeDuty = QTime(h,m,s)
        self.dutyTimeCompLbl.setText('Daily time completed: ' + self.currTimeDuty.toString('hh:mm:ss'))

    def incrementTimer(self):

        self.currTimeLCD = self.currTimeLCD.addSecs(1)
        self.lcdNumber.display(self.currTimeLCD.toString('hh:mm:ss'))

        self.currTimeDuty = self.currTimeDuty.addSecs(1)
        self.dutyTimeCompLbl.setText('Daily time completed: ' + self.currTimeDuty.toString('hh:mm:ss'))

        self.deltaTimer += 1

        self.updateProgressBarDisplay()

    def manageStartPauseClickedEvent(self):

        self.backlogMgr.manageClickButtonFromGUI()
        self.deltaTimer = 0

        if self.timer.isActive():
            self.timer.stop()
            self.btnStartPause.setIcon(QIcon('Images//play_icon.png'))
        else:
            self.timer.start(1000)
            self.btnStartPause.setIcon(QIcon('Images//pause_icon.png'))

    def manageDutyDetailsClickedEvent(self):

        ex = DutyDetailsWindow(self, self.backlogMgr.backlogData)
        ex.show()

    def manageEditTasksOptions(self):

        self.editTasksGUI.exec_()

        self.updateTaskCombobox()

    def closeEvent(self, event):

        event.accept()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
