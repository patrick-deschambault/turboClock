
from PyQt5.QtWidgets import (QFormLayout, QApplication, QWidget, QLabel, QLineEdit, QDialogButtonBox, QDialog, QHBoxLayout, QVBoxLayout, QListWidget)

class EditTasksOptions(QDialog):

    def __init__(self, parent, iBacklogMgr):
        super().__init__(parent)

        self.backlogMgr = iBacklogMgr

        self.data = iBacklogMgr.backlogData

        self.currTaskListView = ''

        self.initUI()

    def initUI(self):

        self.setWindowTitle("Edit tasks")

        mainLayout =  QVBoxLayout(self)
        listViewTaskViewLayout = QHBoxLayout()

        self.listTasksView = QListWidget(self)

        for currTask in self.data.tasks:
            
            currId = currTask.id
            currTitle = currTask.title

            textItem = currId + ' - ' + currTitle

            self.listTasksView.addItem(textItem)

        self.listTasksView.currentItemChanged.connect(self.manageCurrItemChangeTaskList)
        
        self.idInput = QLineEdit(self)
        self.titleInput = QLineEdit(self)
        self.prjCodeInput = QLineEdit(self)
        self.completedTime = QLineEdit(self)

        layoutCurrTask = QFormLayout()
        layoutCurrTask.addRow("Id:", self.idInput)
        layoutCurrTask.addRow("Title:", self.titleInput)
        layoutCurrTask.addRow("Project code:", self.prjCodeInput)
        layoutCurrTask.addRow("Completed time:", self.completedTime)

        listViewTaskViewLayout.addWidget(self.listTasksView)
        listViewTaskViewLayout.addLayout(layoutCurrTask)

        mainLayout.addLayout(listViewTaskViewLayout)
 

    def manageCurrItemChangeTaskList(self):

        currItemIndex = self.listTasksView.currentRow()

        self.currTaskListView = self.data.tasks[currItemIndex]

        self.idInput.setText(self.currTaskListView.id)
        self.titleInput.setText(self.currTaskListView.title)
        self.prjCodeInput.setText(self.currTaskListView.prjCode)
        self.completedTime.setText(str(self.currTaskListView.completedTime))

