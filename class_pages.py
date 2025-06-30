#detailed class page
#include class information and class reviews page
from PySide6.QtWidgets import QApplication, QMessageBox, QTextBrowser
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QColor,QFont,QDesktopServices
from PySide6.QtCore import QUrl
import data as d

class Class_pages:

    def __init__(self,app,Aclass):
        self.app=app
        uiLoader = QUiLoader()       
        self.ui = uiLoader.load('ui/class_information.ui')

        self.Aclass=Aclass
        self.reviews=[]

        #课程info
        self.ui.class_name.setText(Aclass.name)
        self.ui.quality.setValue(Aclass.quality)
        self.ui.workload.setValue(Aclass.workload)
        self.ui.score.setValue(Aclass.score)
        avr=(Aclass.quality+Aclass.workload+Aclass.score)/3
        self.ui.general.setValue(avr)

        self.ui.enter_reviews.clicked.connect(self.open_link)#打开链接

        self.loadinfo()

    def loadinfo(self):
        Aclass=self.Aclass
        text='课程号：'+Aclass.id+'\n'
        text+=('开课单位：'+Aclass.department+'\n')
        text+=('课程类型：'+Aclass.type+'\n')
        text+=('班号：'+Aclass.classnum+'\n')
        text+=('学分：'+Aclass.credit+'\n')
        text+=('起止周：'+Aclass.durationweek+'\n')
        text+=('上课时间：'+Aclass.str_time+'\n')
        text+=('教师：'+Aclass.teacher+'\n')
        text+=('备注：'+Aclass.remark+'\n')
        text+=('开课学期：'+Aclass.term+'\n'+'\n')
        self.ui.info.append(text)
        font = QFont()
        font.setPointSize(13)  # 设置字体大小为14pt
        self.ui.info.setFont(font)

    def open_link(self):
        url = QUrl("https://courses.pinzhixiaoyuan.com/") 
        QDesktopServices.openUrl(url)