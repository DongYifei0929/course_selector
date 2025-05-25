#main pages
#pages stack, including a main page and an edit page
from PySide6.QtWidgets import (QApplication, QMessageBox,QTableWidget,QTableWidgetItem, QSlider,QWidget,QVBoxLayout,QTreeWidget, 
                              QTreeWidgetItem,QMenu,QListWidgetItem)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt
from class_pages import Class_pages
from person_info import Person_page

import data as d

class Main_pages:

    def __init__(self,app):
        self.app=app
        uiLoader = QUiLoader()       
        self.ui = uiLoader.load('ui/main_pages.ui')

        #加载主课表
        self.loadClassTable()
        #加载课程列表
        self.loadClassList(self.ui.search_tree)
        self.loadClassList(self.ui.must)
        self.loadClassList(self.ui.no)
        #默认显示一个空课表
        self.createTable(0)

        #偏好
        #偏好编辑
        self.ui.morning8.valueChanged.connect(self.morning8Changed)
        self.ui.score.valueChanged.connect(self.scoreChanged)
        self.ui.workload.valueChanged.connect(self.workloadChanged)
        #根据偏好更新课表
        self.ui.get_recommend.clicked.connect(self.recommend)
        self.ui.applytable.clicked.connect(self.apply)
        #自定义偏好
        #搜索特定课程
        self.ui.must_search.textChanged.connect(lambda text,tree=self.ui.must:self.filterItems(text,tree))
        self.ui.no_search.textChanged.connect(lambda text,tree=self.ui.no:self.filterItems(text,tree))
        #更新列表
        self.ui.must.itemDoubleClicked.connect(lambda item,column,must_no=d.mustlist:self.preChoose(item,column,must_no))
        self.ui.no.itemDoubleClicked.connect(lambda item,column,must_no=d.nolist:self.preChoose(item,column,must_no))
        #删除自定义偏好
        self.ui.mustlist.customContextMenuRequested.connect(lambda pos,must_no_list=d.mustlist,must_no=self.ui.mustlist :self.listShowDelete(pos,must_no_list,must_no))
        self.ui.nolist.customContextMenuRequested.connect(lambda pos,must_no_list=d.nolist,must_no=self.ui.nolist :self.listShowDelete(pos,must_no_list,must_no))


        #自定义
        #搜索框
        self.ui.search_bar.textChanged.connect(lambda text,tree=self.ui.search_tree:self.filterItems(text,tree))
        # 双击选择
        self.ui.search_tree.itemDoubleClicked.connect(self.selectClass)
        #删除课程
        #已在createtable函数中连接

        #页面转换
        self.ui.enter_person.clicked.connect(self.openPerson)
        self.ui.enter_edit.clicked.connect(self.goEdit)
        self.ui.enter_main.clicked.connect(self.backMain)
        self.ui.class_table.cellClicked.connect(self.MgoClassInformation)

        #默认显示页面
        self.ui.setCurrentIndex(0)
        #设置默认全屏（伪）
        screen = QApplication.primaryScreen().geometry()
        self.ui.setGeometry(screen)
        #存储临时窗口引用，防丢失
        self.running_pages = []

    def listToTable(self,classList,classTable):
        if not classList:
            print("Empty class table, go and edit?")
            return
        for Aclass in classList:
            col=Aclass.day
            rows=Aclass.time
            text=str(Aclass.name+'\n'+Aclass.teacher)
            content=QTableWidgetItem(text)
            content.setData(Qt.UserRole, Aclass)
            for row in rows:
                classTable.setItem(row, col, content)

    def loadClassTable(self):#TODO test
        self.ui.class_table.clearContents()#清空已有内容

        classTable=d.classtabletest#TODO: test内容
        self.listToTable(classTable,self.ui.class_table)
    def loadClassList(self,tree):
        # 第一级分类
        major = QTreeWidgetItem(["培养方案"])
        politic = QTreeWidgetItem(["思政"])
        english=QTreeWidgetItem(["英语"])
        pe=QTreeWidgetItem(["体育"])
        general=QTreeWidgetItem(["通识"])
        cross=QTreeWidgetItem(["跨院系"])
        others=QTreeWidgetItem(["其他"])
        #第二级分类（培养方案）
        compulsory=QTreeWidgetItem(major,["必修"])
        selective=QTreeWidgetItem(major,["选修"])
        #第二级分类（跨院系）(暂)
        #第二级子节点
        for Aclass in d.politic_classes:
            node=QTreeWidgetItem(politic,[Aclass.name])
            node.setData(0,Qt.UserRole, Aclass)
        #第三级子节点
        for Aclass in d.compulsory_classes:
            node=QTreeWidgetItem(compulsory,[Aclass.name])
            node.setData(0,Qt.UserRole,Aclass)

        tree.addTopLevelItem(major)
        tree.addTopLevelItem(politic)
        tree.addTopLevelItem(english)
        tree.addTopLevelItem(pe)
        tree.addTopLevelItem(general)
        tree.addTopLevelItem(cross)
        tree.addTopLevelItem(others)

    def morning8Changed(self,value):
        self.ui.morning8_tag.setText("早八接受度  当前值："+str(value))
        d.testscores[0]=value
    def scoreChanged(self,value):
        self.ui.score_tag.setText("给分不好接受度  当前值："+str(value))
        d.testscores[1]=value
    def workloadChanged(self,value):
        self.ui.workload_tag.setText("任务量大接受度  当前值："+str(value))
        d.testscores[2]=value
    def preChoose(self,item,column,must_no):
        Aclass = item.data(0, Qt.UserRole)
        if Aclass not in must_no:
            must_no.append(Aclass)
        self.refreshList()#定义就在下面，更新显示的列表
    def listShowDelete(self,pos,must_no_list,must_no):
        menu = QMenu(self.ui.edit_classtables)
        
        delete_action = menu.addAction("删除")
        delete_action.triggered.connect(lambda tri,must_no_list=must_no_list,must_no=must_no:self.listDelete(tri,must_no_list,must_no))
        
        menu.exec(must_no.viewport().mapToGlobal(pos))
    def listDelete(self,tri,must_no_list,must_no):
        row = must_no.currentRow()
        if row != -1:
            item=must_no.item(row)
            Aclass=item.data(Qt.UserRole)
            must_no_list.remove(Aclass)
            self.refreshList()
    def refreshList(self):
        self.ui.mustlist.clear()
        self.ui.nolist.clear()
        for Aclass in d.mustlist:
            item = QListWidgetItem(Aclass.name)
            item.setData(Qt.UserRole, Aclass)  # 将自定义对象存储到 item 的数据中
            self.ui.mustlist.addItem(item)
        for Aclass in d.nolist:
            item = QListWidgetItem(Aclass.name)
            item.setData(Qt.UserRole, Aclass)  # 将自定义对象存储到 item 的数据中
            self.ui.nolist.addItem(item)

    def createTable(self,num):
        #首先创建一个新tag
            page = QWidget()
            layout = QVBoxLayout()
            #修饰table
            table= QTableWidget(12, 7)
            table.setObjectName("table"+str(num))
            for i in range(12):
                table.setRowHeight(i,55)
            for i in range(7):
                table.setColumnWidth(i,135)
            table.setEditTriggers(QTableWidget.NoEditTriggers)
            #课程详情入口
            table.cellClicked.connect(lambda row, col, t=table: self.EgoClassInformation(row, col, t))
            #连接删除信号和槽
            table.setContextMenuPolicy(Qt.CustomContextMenu)
            table.customContextMenuRequested.connect(self.showDelete)
            #组装
            layout.addWidget(table)
            page.setLayout(layout)
            self.ui.edit_classtables.addTab(page, str(num))
            setattr(self.ui, "table"+str(num), table)#动态设置属性，方便改动
            return table
    def recommend(self):
        #根据data获得推荐课表
        d.get_recommend()
        #清空当前tags
        while self.ui.edit_classtables.count() > 0:
            widget = self.ui.edit_classtables.widget(self.ui.edit_classtables.count() - 1)
            self.ui.edit_classtables.removeTab(self.ui.edit_classtables.count() - 1)
            widget.deleteLater()
        for num in range(3):
            classList=d.recommendTables[num]
            table=self.createTable(num)
            self.listToTable(classList,table)
    def apply(self):
        #最终选择一个课表，并回到首页
        num=self.ui.edit_classtables.currentIndex()
        d.classtabletest=d.recommendTables[num]
        self.loadClassTable()
        self.backMain()

    def showDelete(self, pos):
        #找到当前课表
        table_num=self.ui.edit_classtables.currentIndex()
        tablename="table"+str(table_num)
        table = getattr(self.ui, tablename, None)
        #找到当前单元格，检测是否为空
        item = table.itemAt(pos)
        text = item.text() if item else ""
        if not text.strip():
            return

        menu = QMenu(self.ui.edit_classtables)
        
        delete_action = menu.addAction("删除")
        delete_action.triggered.connect(self.delete)
        
        menu.exec(table.viewport().mapToGlobal(pos))
    def delete(self):
        #找到当前课表
        table_num=self.ui.edit_classtables.currentIndex()
        tablename="table"+str(table_num)
        table = getattr(self.ui, tablename, None)

        row = table.currentRow()
        col = table.currentColumn()
        if row != -1 and col != -1:
            item = table.item(row, col)
            Aclass=item.data(Qt.UserRole)
            d.recommendTables[table_num].remove(Aclass)
            table.setItem(row, col, QTableWidgetItem(""))

    def filterItems(self, text,tree):
        text = text.lower()#大小写不敏感
        root = tree.invisibleRootItem()
        self.filterTreeItem(root, text)
    def filterTreeItem(self, item, text):
        child_count = item.childCount()
        match_found = False

        # 检查当前节点是否匹配（非叶子节点只检查自身文本）
        if text == "" or text in item.text(0).lower():
            match_found = True
        else:
            # 如果是叶子节点，检查是否匹配
            if child_count == 0:
                item.setHidden(True)
                return False

        # 递归检查子节点
        for i in range(child_count):
            child = item.child(i)
            if self.filterTreeItem(child, text):
                match_found = True

        # 设置当前节点显隐
        item.setHidden(not match_found)
        if match_found and item.parent():  # 确保匹配项的父节点可见
            item.parent().setHidden(False)
        return match_found
    def selectClass(self,item,column):
        Aclass = item.data(0, Qt.UserRole)
        table_num=self.ui.edit_classtables.currentIndex()
        if Aclass not in d.recommendTables[table_num]:
            d.recommendTables[table_num].append(Aclass)
        tablename="table"+str(table_num)
        table = getattr(self.ui, tablename, None)
        self.listToTable(d.recommendTables[table_num],table)

    def openPerson(self):
        personpage = Person_page(self.app)
        personpage.ui.show()
        self.running_pages.append(personpage)
    def goEdit(self):
        self.ui.setCurrentIndex(1)
    def backMain(self):
        self.ui.setCurrentIndex(0)
    def MgoClassInformation(self,row,col):
        text = self.ui.class_table.item(row, col).text() if self.ui.class_table.item(row, col) else ""
        if not text.strip():
            return
        item=self.ui.class_table.item(row, col).data(Qt.UserRole)
        classpages = Class_pages(self.app,item)
        classpages.ui.show()
        self.running_pages.append(classpages)
    def EgoClassInformation(self,row,col,t):
        text = t.item(row, col).text() if t.item(row, col) else ""
        if not text.strip():
            return
        item=t.item(row, col).data(Qt.UserRole)
        classpages = Class_pages(self.app,item)
        classpages.ui.show()
        self.running_pages.append(classpages)