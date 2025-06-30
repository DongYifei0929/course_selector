#personal information page
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader
import data as d
import api

class Person_page:

    def __init__(self,app):
        self.app=app
        uiLoader = QUiLoader()       
        self.ui = uiLoader.load('ui/person_information.ui')

        self.ui.set_pinfo.clicked.connect(self.infoChange)

        for major in d.majors:
            self.ui.major.addItem(major)
        for grade in range(1,6):
            self.ui.grade.addItem(str(grade))

        self.loadinfo()

    def loadinfo(self):
        self.ui.major_tag.setText(d.user.major)
        self.ui.grade_tag.setText(str(d.user.grade))

    def infoChange(self):
        reply = QMessageBox.question(
            self.ui,
            "确认操作",
            "确认更改个人信息（这将改变你的可选课表）",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.No:
            return
        major = self.ui.major.currentText()
        d.user.major=major
        grade=self.ui.grade.currentText()
        d.user.grade=int(grade)

        api.get_database()

        self.loadinfo()