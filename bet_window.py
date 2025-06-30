from PySide6.QtWidgets import QApplication, QMessageBox, QTextBrowser,QListWidgetItem,QTableWidgetItem,QSpinBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QColor,QFont,QDesktopServices
from PySide6.QtCore import QUrl
from PySide6.QtCore import Qt
import data as d
import api
import copy

class Bet_page:

    def __init__(self,app,mainpage):
        self.app=app
        self.mainpage=mainpage
        uiLoader = QUiLoader()
        self.ui = uiLoader.load('ui/betpage.ui')

        self.ui.bet.clicked.connect(self.getpoints)

        self.betlist=[]#存储spinbox对象的引用，内容为all,chosen元组

        self.loadinfo()

    def loadinfo(self):
        self.ui.bettable.setRowCount(0)
        self.ui.bettable.setColumnCount(3)
        self.ui.bettable.setColumnWidth(0, 200)  # 第一列宽度200px
        self.ui.bettable.setColumnWidth(1, 80) 
        self.ui.bettable.setColumnWidth(2, 80) 
        self.ui.bettable.setHorizontalHeaderLabels(["课程", "限选人数", "已选人数"])
        self.ui.bettable.setRowCount(len(d.betlist))
        for i,bet in enumerate(d.betlist):
            content=QTableWidgetItem(bet.name)
            font = QFont()
            font.setPointSize(11)  # 设置字体大小
            content.setFont(font)
            
            spinbox = QSpinBox()
            spinbox.setObjectName(f"all{i}")
            spinbox.setRange(0, 3000)  # 设置数值范围
            spinbox.setValue(0)      # 默认值

            spinbox2 = QSpinBox()
            spinbox2.setObjectName(f"chosen{i}")
            spinbox2.setRange(0, 3000)  # 设置数值范围
            spinbox2.setValue(0)      # 默认值
            
            # 将SpinBox放入单元格
            self.ui.bettable.setCellWidget(i,1,spinbox)
            self.ui.bettable.setCellWidget(i,2,spinbox2)
            self.ui.bettable.setItem(i, 0, content)
            #将spinbox存储引用
            self.betlist.append((spinbox,spinbox2))

    def getpoints(self):
        d.capacity.clear()
        for i,pair in enumerate(self.betlist):
            d.capacity.append((pair[0].value(),pair[1].value()))
        if d.capacity:
            api.get_bet()
            d.setbetpoint()
        QMessageBox.information(
                self.ui,  # 当前窗口实例
                "推荐投点",  # 消息框标题
                "已为您生成推荐投点方案！关闭窗口以查看推荐点数",  # 消息框内容
                QMessageBox.Ok  # 按钮选项
            )
        self.mainpage.loadBetList()
        d.saveFinalTable()