#detailed class page
#include class information and class reviews page
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader

class Class_pages:

    def __init__(self,app,Aclass):
        self.app=app
        uiLoader = QUiLoader()       
        self.ui = uiLoader.load('ui/class_information.ui')

        self.Aclass=Aclass

        self.ui.class_name.setText(Aclass.name)
        self.ui.general.setValue(Aclass.general)
        self.ui.quality.setValue(Aclass.quality)
        self.ui.workload.setValue(Aclass.workload)
        self.ui.score.setValue(Aclass.score)

        self.ui.enter_reviews.clicked.connect(self.goReviews)
        self.ui.enter_information.clicked.connect(self.backInformation)

    def goReviews(self):
        self.ui.setCurrentIndex(1)
    
    def backInformation(self):
        self.ui.setCurrentIndex(0)