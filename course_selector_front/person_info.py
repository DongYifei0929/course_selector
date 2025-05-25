#personal information page
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader
import data as d

class Person_page:

    def __init__(self,app):
        self.app=app
        uiLoader = QUiLoader()       
        self.ui = uiLoader.load('ui/person_information.ui')

        for major in d.majors:
            self.ui.major.addItem(major)

        self.ui.major.currentIndexChanged.connect(self.majorChange)

    def majorChange(self):
        major = self.ui.major.currentText()
        d.user.major=major