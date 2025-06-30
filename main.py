#main
#controller
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader

from log_in_page import Log_in
from main_pages import Main_pages
from class_pages import Class_pages
import data as d
import api


app = QApplication([])

def loginRun(app):
    login = Log_in(app)
    login.ui.show()
    app.exec()
    return login.guard

def mainPagesRun(app):
    mainpages = Main_pages(app)
    mainpages.ui.show()
    app.exec()

if __name__=="__main__":
    api.get_database()
    guard=loginRun(app)
    if guard:
        mainPagesRun(app)