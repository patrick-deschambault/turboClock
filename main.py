#-*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QLCDNumber, QVBoxLayout, QHBoxLayout, QApplication, QWidget, QLabel, QLineEdit, QPushButton, QDialog,QComboBox)
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

        #Backlog Data Object

        #Backlog data init
        self.backlogMgr = BacklogMgr()
        self.backlogMgr.loadGiroTaskProjectCodesData()
        self.backlogMgr.loadGiroTFSData()

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

        self.btnAddProject = QPushButton('', self)
        self.btnAddProject.setIcon(QIcon('plus_icon.png'))

        self.btnAddTask = QPushButton('', self)
        self.btnAddTask.setIcon(QIcon('plus_icon.png'))

        self.taskTFSLabel = QLabel('Task Code TFS:')
        self.projectCodeLabel = QLabel('Project Code:')
        self.taskCodeLabel = QLabel('Task Code:')

        self.projectCodeInput = QLineEdit('')
        self.taskCodeInput = QLineEdit('')

        self.taskTFSCb = QComboBox(self)
        self.initTFSTaskCombobox()

        mainLayout = QVBoxLayout(self)

        layoutTimer = QVBoxLayout()
        layoutTimer.addWidget(self.lcdNumber)

        fieldsInputLayout = QHBoxLayout()

        layoutLabelsCodes = QVBoxLayout()
        layoutLabelsCodes.addWidget(self.taskTFSLabel)
        layoutLabelsCodes.addWidget(self.projectCodeLabel)
        layoutLabelsCodes.addWidget(self.taskCodeLabel)

        layoutInputCodes = QVBoxLayout()
        layoutInputCodes.addWidget(self.taskTFSCb)
        layoutInputCodes.addWidget(self.projectCodeInput)
        layoutInputCodes.addWidget(self.taskCodeInput)

        layoutAddBtn = QVBoxLayout()
        layoutAddBtn.addWidget(self.btnAddTfsTask)
        layoutAddBtn.addWidget(self.btnAddProject)
        layoutAddBtn.addWidget(self.btnAddTask)

        fieldsInputLayout.addLayout(layoutLabelsCodes)
        fieldsInputLayout.addLayout(layoutInputCodes)
        fieldsInputLayout.addLayout(layoutAddBtn)

        mainLayout.addLayout(layoutTimer)
        mainLayout.addLayout(fieldsInputLayout)
        mainLayout.addWidget(self.btnStartPause)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateLcdNumberContent)
        self.timer.start(1000)
        self.timer.stop()
        
        self.currentTime = QTime(0,0,0)
        self.lcdNumber.display(self.currentTime.toString('hh:mm:ss'))

        self.startTime = 0
        self.stopTime = 0
        
    def initTFSTaskCombobox(self):

        taskTFSGirolist = self.backlogMgr.getTFSTasks()

        for taskTFS in taskTFSGirolist:
            self.taskTFSCb.addItem(taskTFS.code + " - " + taskTFS.description)
        
        self.manageCbTFSIndexChange()

        self.taskTFSCb.currentIndexChanged.connect(self.manageCbTFSIndexChange)

    def manageCbTFSIndexChange(self):

        index = self.taskTFSCb.currentIndex()

        self.backlogMgr.setCurrentTFSTask(index)

        self.projectCodeInput.setText(self.backlogMgr.getCurrentProjectCode())
        self.taskCodeInput.setText(self.backlogMgr.getCurrentTaskCode())

    def updateLcdNumberContent(self):

        self.currentTime = self.currentTime.addSecs(1)
        self.lcdNumber.display(self.currentTime.toString('hh:mm:ss'))

    def manageStartPauseClickedEvent(self):

        if self.timer.isActive():
            self.timer.stop()
            #self.stopTime = self.currentTime.toString('hh:mm:ss')
            self.btnStartPause.setIcon(QIcon('play_icon.png'))

            self.stopTime = datetime.datetime.now()

            self.backlogMgr.createPiece(self.backlogMgr.backlogData.currTFSTask, \
                                        self.startTime, \
                                        self.stopTime)

            self.taskTFSCb.setEnabled(True)
            self.projectCodeInput.setEnabled(True)
            self.taskCodeInput.setEnabled(True)
            #self.printStatus()

        else:
            self.timer.start()
            self.startTime = datetime.datetime.now()

            self.btnStartPause.setIcon(QIcon('pause_icon.png'))

            self.backlogMgr.createTimeSheet('2020-04-13')
 
            self.taskTFSCb.setEnabled(False)
            self.projectCodeInput.setEnabled(False)
            self.taskCodeInput.setEnabled(False)
        
    def manageAddTFSTaskEvent(self):

        ex = AddTFSTaskWindow(self)
        ex.show()

    def closeEvent(self, event):

        event.accept()

    def printStatus(self):
        
        print("Current task TFS time completed:")
        print(self.backlogMgr.backlogData.currTFSTask.completedTime)

        print("\n")
        print("All pieces completed time:")
        for i,pce in enumerate(self.backlogMgr.backlogData.pieces):
            print(pce.deltaTime)

        print("\n")

        print("All tasks TFS in backlog time completed:")
        for i,task in enumerate(self.backlogMgr.backlogData.taskTFSGirolist):
            print(task.completedTime)

        print("\n")

        print("All backlog Information time completed:")
        for i,prj in enumerate(self.backlogMgr.backlogData.projectGirolist):

            print(str(prj.code) + ":")

            for j,task in enumerate(self.backlogMgr.backlogData.projectGirolist[i].taskGiroList):
                print(str(task.completedTime) + " ")

            print("\n")


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())