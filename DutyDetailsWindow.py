from PyQt5.QtWidgets import (QFormLayout, QApplication, QDateEdit, QWidget, QDialog, QTextEdit, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel)
from PyQt5.QtCore import (QDate)

from BacklogData import *
from Task import *

class DutyDetailsWindow(QDialog):

    def __init__(self, parent, iBacklogData):
        super().__init__(parent)

        self.backlogData = iBacklogData

        self.setWindowTitle("Duty details")
        self.setMinimumWidth(500)

        mainLayout = QVBoxLayout(self)

        self.currDutyDate = self.backlogData.currDuty.date
        currDutyDateLabel = QLabel("Workday date: ")
        self.currDutyDateEdit = QDateEdit(self)

        self.currDutyDateLayout = QHBoxLayout(self)
        self.currDutyDateLayout.addWidget(currDutyDateLabel)
        self.currDutyDateLayout.addWidget(self.currDutyDateEdit)

        self.initCurrDutyDateEdit()

        self.dutySummaryTableWidget = QTableWidget(self)

        summaryDailyTasksLabel = QLabel("Summary of daily tasks")
        self.initDutySummaryTableWidget()

        self.totalCompTime =  datetime.timedelta(seconds = self.backlogData.currDuty.totalTimeCompleted)
        self.totalCompTimeLabel = QLabel("Total completed time: " + str(self.totalCompTime))

        mainLayout.addLayout(self.currDutyDateLayout)
        mainLayout.addWidget(summaryDailyTasksLabel)
        mainLayout.addWidget(self.dutySummaryTableWidget)
        mainLayout.addWidget(self.totalCompTimeLabel)


    def initCurrDutyDateEdit(self):

        splitDate = self.currDutyDate.split('-')

        year = int(splitDate[0])
        month = int(splitDate[1])
        day = int(splitDate[2])

        self.currDutyDateEdit.setDate(QDate(year,month,day))
        self.currDutyDateEdit.setCalendarPopup(True)

    def initDutySummaryTableWidget(self):

        nbCol = 3
        nbRow = len(self.backlogData.currDuty.tasksRegistered)

        self.dutySummaryTableWidget.setColumnCount(nbCol)
        self.dutySummaryTableWidget.setRowCount(nbRow)

        listStr = list()
        listStr = ["Title", "Project code", "Daily completed time"]

        self.dutySummaryTableWidget.setHorizontalHeaderLabels(listStr)

        for i in range(0, nbRow):

            title = self.backlogData.currDuty.tasksRegistered[i].title
            prjCode = self.backlogData.currDuty.tasksRegistered[i].prjCode
            compTime = str(datetime.timedelta(seconds = self.backlogData.currDuty.tasksRegistered[i].completedTime))

            self.dutySummaryTableWidget.setItem(i,0, QTableWidgetItem(title))
            self.dutySummaryTableWidget.setItem(i,1, QTableWidgetItem(prjCode))
            self.dutySummaryTableWidget.setItem(i,2, QTableWidgetItem(compTime))

    def genTaskRegisteredString(self):

        s = 'Time to log for the ' + self.currDutyDate + ':\n'
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

        