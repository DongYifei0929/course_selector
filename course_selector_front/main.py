#main
#controller
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader

from log_in_page import Log_in
from main_pages import Main_pages
from class_pages import Class_pages


app = QApplication([])

def loginRun(app):
    login = Log_in(app)
    login.ui.show()
    app.exec()

def mainPagesRun(app):
    mainpages = Main_pages(app)
    mainpages.ui.show()
    app.exec()

if __name__=="__main__":
    loginRun(app)
    print("exchange pages")
    mainPagesRun(app)
   

#TODO: 生成的动态窗口删除后没有从列表中消失，导致列表很长吃内存