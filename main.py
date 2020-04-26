#-*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QLCDNumber, QVBoxLayout, QHBoxLayout, QApplication, QWidget, QLabel, QLineEdit, QPushButton, QDialog, QComboBox, QMessageBox)
from PyQt5.QtCore import QTimer, QTime, QSettings
from PyQt5.QtGui import QIcon

from AddTFSTaskWindow import *
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

        self.resize(400, 300)

        self.lcdNumber = QLCDNumber()
        self.lcdNumber.setNumDigits(8)

        self.btnStartPause = QPushButton('', self)
        self.btnStartPause.setIcon(QIcon('play_icon.png'))
        self.btnStartPause.clicked.connect(self.manageStartPauseClickedEvent)
        
        self.btnAddTfsTask = QPushButton('', self)
        self.btnAddTfsTask.setIcon(QIcon('plus_icon.png'))
        self.btnAddTfsTask.clicked.connect(self.manageAddTFSTaskEvent)

        self.dutyTimeCompLbl = QLabel()        

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

        mainLayout.addLayout(layoutTimer)
        mainLayout.addLayout(fieldsInputLayout)
        mainLayout.addWidget(self.btnStartPause)
        mainLayout.addLayout(layoutDutyStat)

        self.timer = QTimer(self)
        self.currTimeLCD = QTime(0,0,0)
        self.currTimeDuty = QTime(0,0,0)

        self.timer.timeout.connect(self.incrementTimer)

        self.updateTimeLCD()
        self.updateDutyTimeDisp()

        self.startTime = 0
        self.stopTime = 0
 
    def initTFSTaskCombobox(self):

        taskTFSGirolist = self.backlogMgr.getListTasksFromGUI()

        for taskDesc in taskTFSGirolist:
            self.taskTFSCb.addItem(taskDesc)

        firstText = self.taskTFSCb.currentText()
        self.backlogMgr.setCurrentTaskFromGUI(firstText)

        self.taskTFSCb.currentIndexChanged.connect(self.manageCbTFSIndexChange)

    def manageCbTFSIndexChange(self):

        currText = self.taskTFSCb.currentText()
        self.backlogMgr.setCurrentTaskFromGUI(currText)

        self.updateTimeLCD()

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

    def manageStartPauseClickedEvent(self):

        currText = self.taskTFSCb.currentText()
        self.backlogMgr.manageClickButtonFromGUI(currText)

        if self.timer.isActive():
            self.timer.stop()

            self.btnStartPause.setIcon(QIcon('play_icon.png'))

            self.taskTFSCb.setEnabled(True)

        else:
            self.timer.start(1000)

            self.btnStartPause.setIcon(QIcon('pause_icon.png'))

            self.taskTFSCb.setEnabled(False)

    def manageAddTFSTaskEvent(self):

        ex = AddTFSTaskWindow(self)
        ex.show()

    def closeEvent(self, event):

        event.accept()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
