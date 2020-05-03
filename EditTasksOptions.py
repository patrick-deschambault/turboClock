
from PyQt5.QtWidgets import (QFormLayout, QApplication, QWidget, QLabel, QLineEdit, QDialogButtonBox, QDialog)


class EditTasksOptions(QDialog):

    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):

        self.setWindowTitle("Create new TFS task")

        self.codeInput = QLineEdit(self)
        self.descInput = QLineEdit(self)
        self.projectCodeInput = QLineEdit(self)
        self.taskCodeInput = QLineEdit(self)
        
        buttonBox = QDialogButtonBox(self)
        buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        layout = QFormLayout(self)
        layout.addRow("Code:", self.codeInput)
        layout.addRow("Description:", self.descInput)
        layout.addRow("Project code:", self.projectCodeInput)
        layout.addRow("Task code:", self.taskCodeInput)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        