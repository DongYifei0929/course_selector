#main pages
#pages stack, including a main page and an edit page
from PySide6.QtWidgets import (QApplication, QMessageBox,QTableWidget,QTableWidgetItem, QSlider,QWidget,QVBoxLayout,QHBoxLayout,QTreeWidget,
                              QTreeWidgetItem,QMenu,QListWidgetItem,QSpacerItem,QLabel,QSizePolicy)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor,QFont
import random
import copy
from datetime import datetime
import re


from class_pages import Class_pages
from person_info import Person_page
from bet_window import Bet_page
import data as d
import api

test=d.test

class TimeContent:
    def __init__(self,timetable):
        self.timetable=timetable#引用
        self.pre=[('06','26','10'),('07','01','10')]
        self.fix=[(('09','02','10'),('09','09','10')),(('09','10','10'),('09','17','10')),(('09','18','10'),('09','25','10'))]
        now=str(datetime.now())
        self.now=re.split('-| |:',now)

        self.showTime()
    def switchStage(self):
        if self.now[1]==self.pre[1][0]:
            if self.now[2]==self.pre[1][1]:
                return self.now[3]>self.pre[1][2]
            return self.now[2]>self.pre[1][1]
        return self.now[1]>self.pre[1][0]
    def showTime(self):
        tt=self.timetable
        for idx in [0,1]:
            t=self.pre[idx]
            text=f"{t[0]}月{t[1]}日{t[2]}:00"
            content=QTableWidgetItem(text)
            tt.setItem(0,idx+1,content)
        for i in [0,1,2]:
            for idx in [0,1]:
                t=self.fix[i][idx]
                text=f"{t[0]}月{t[1]}日{t[2]}:00"
                content=QTableWidgetItem(text)
                tt.setItem(i+1,idx+1,content)

class tableMethods:
    def __init__(self,app):
        self.app=app
        self.running_pages=[]
    def listToTable(self,classList,classTable,creditTag):
        classTable.clearContents()
        self.deCombine(classTable)
        credit_sum=0
        for Aclass in classList:
            credit_sum+=int(Aclass.credit)
            timelist=Aclass.timelist
            text=str(Aclass.name+'\n'+Aclass.teacher)
            colornum=(random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
            while(abs(colornum[0]-colornum[1])+abs(colornum[1]-colornum[2])+abs(colornum[2]-colornum[0])<30):
                colornum=(random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))#防止颜色过灰
            color = QColor(colornum[0],colornum[1],colornum[2])#设置随机颜色
            font = QFont()
            font.setPointSize(10)  # 设置字体大小
            for time in timelist:
                col=time[0]-1
                row=time[1]-1
                content=QTableWidgetItem(text)
                content.setData(Qt.UserRole, copy.deepcopy(Aclass))
                content.setBackground(color)
                content.setFont(font)
                classTable.setItem(row, col, content)
        creditTag.setText('总学分：'+str(credit_sum))
        self.combineCells(classTable)
    def combineCells(self,table):
        for col in range(table.columnCount()):
            for row in range(table.rowCount()):
                current_item = table.item(row, col)
                if not current_item:
                    continue

                # 检查下方单元格是否相同，相同则合并并跳过
                for next in range(row + 1, table.rowCount()):
                    next_item = table.item(next, col)
                    if next_item and next_item.text() == current_item.text():
                        table.setSpan(row, col, next-row+1, 1)
                    else:
                        break
    def deCombine(self,table):
        for row in range(12):
            for col in range(7):
                table.setSpan(row, col, 1, 1)
    def goClassInformation(self,row,col,t):
        text = t.item(row, col).text() if t.item(row, col) else ""
        if not text.strip():
            return
        item=t.item(row, col).data(Qt.UserRole)
        classpages = Class_pages(self.app,item)
        classpages.ui.show()
        self.running_pages.append(classpages)
 
class treeMethods:
    def __init__(self):
        pass
    def loadClassList(self,tree):
        tree.clear()
        # 第一级分类
        compulsory = QTreeWidgetItem(["专业必修"])
        selective=QTreeWidgetItem(["专业任选"])
        politics = QTreeWidgetItem(["思政"])
        english=QTreeWidgetItem(["英语"])
        pe=QTreeWidgetItem(["体育"])
        general=QTreeWidgetItem(["通选"])
        public=QTreeWidgetItem(["学校公选"])
        limited=QTreeWidgetItem(["专业限选"])
        #第二级子节点
        for Aclass in d.politics:
            node=QTreeWidgetItem(politics,[Aclass.name+' '+Aclass.teacher+' '+Aclass.classnum+'班'])
            node.setData(0,Qt.UserRole, Aclass)
        for Aclass in d.compulsory:
            node=QTreeWidgetItem(compulsory,[Aclass.name+' '+Aclass.teacher+' '+Aclass.classnum+'班'])
            node.setData(0,Qt.UserRole,Aclass)
        for Aclass in d.selective:
            node=QTreeWidgetItem(selective,[Aclass.name+' '+Aclass.teacher+' '+Aclass.classnum+'班'])
            node.setData(0,Qt.UserRole,Aclass)
        for Aclass in d.english:
            node=QTreeWidgetItem(english,[Aclass.name+' '+Aclass.teacher+' '+Aclass.classnum+'班'])
            node.setData(0,Qt.UserRole,Aclass)
        for Aclass in d.pe:
            node=QTreeWidgetItem(pe,[Aclass.name+' '+Aclass.teacher+' '+Aclass.classnum+'班'])
            node.setData(0,Qt.UserRole,Aclass)
        for Aclass in d.general:
            node=QTreeWidgetItem(general,[Aclass.name+' '+Aclass.teacher+' '+Aclass.classnum+'班'])
            node.setData(0,Qt.UserRole,Aclass)
        for Aclass in d.public:
            node=QTreeWidgetItem(public,[Aclass.name+' '+Aclass.teacher+' '+Aclass.classnum+'班'])
            node.setData(0,Qt.UserRole,Aclass)
        for Aclass in d.limited:
            node=QTreeWidgetItem(limited,[Aclass.name+' '+Aclass.teacher+' '+Aclass.classnum+'班'])
            node.setData(0,Qt.UserRole,Aclass)

        tree.addTopLevelItem(compulsory)
        tree.addTopLevelItem(politics)
        tree.addTopLevelItem(english)
        tree.addTopLevelItem(pe)
        tree.addTopLevelItem(general)
        tree.addTopLevelItem(selective)
        tree.addTopLevelItem(public)
        tree.addTopLevelItem(limited)
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
trm=treeMethods()

class Main_pages:

    def __init__(self,app):
        self.app=app
        uiLoader = QUiLoader()       
        self.ui = uiLoader.load('ui/main_pages.ui')

        self.tm=tableMethods(app)
        tc=TimeContent(self.ui.timetable)
        self.BuTuiXuan=tc.switchStage()

        self.connections()
        self.switchPages()
        self.initpage()

        #存储临时窗口引用，防丢失
        self.running_pages = []

    def initpage(self):
        if self.BuTuiXuan:
            self.goTransition()
            return
        #加载主课表
        self.loadClassTable()
        #加载收藏列表
        self.loadlike()
        #加载自定义列表在goEdit里
        #加载用户名
        self.ui.greeting1.setText('你好,'+d.user.name+'!')
        #显示当前时间
        self.drawTimeTable()
        #默认显示页面
        self.ui.setCurrentIndex(0)
        #设置默认全屏（伪）
        self.ui.setGeometry(0,23,1440,840)
    def connections(self):
        #偏好
        #偏好编辑
        self.ui.morning8.valueChanged.connect(self.morning8Changed)
        self.ui.score.valueChanged.connect(self.scoreChanged)
        self.ui.workload.valueChanged.connect(self.workloadChanged)
        self.ui.bet.valueChanged.connect(self.betChanged)
        self.ui.quality.valueChanged.connect(self.qualityChanged)
        #根据偏好更新课表
        self.ui.get_recommend.clicked.connect(self.recommend)
        self.ui.applytable.clicked.connect(self.apply)
        #学分要求(无需槽函数)

        #自定义偏好
        #搜索特定课程
        self.ui.must_search.textChanged.connect(lambda text,tree=self.ui.must:trm.filterItems(text,tree))
        self.ui.no_search.textChanged.connect(lambda text,tree=self.ui.no:trm.filterItems(text,tree))
        #更新列表
        self.ui.must.itemDoubleClicked.connect(lambda item,column,must_no=d.must_take:self.preChoose(item,column,must_no))
        self.ui.no.itemDoubleClicked.connect(lambda item,column,must_no=d.wont_take:self.preChoose(item,column,must_no))
        #删除自定义偏好
        self.ui.mustlist.customContextMenuRequested.connect(lambda pos,must_no_list=d.must_take,must_no=self.ui.mustlist :self.listShowDelete(pos,must_no_list,must_no))
        self.ui.nolist.customContextMenuRequested.connect(lambda pos,must_no_list=d.wont_take,must_no=self.ui.nolist :self.listShowDelete(pos,must_no_list,must_no))
        #传prompt
        self.ui.prompt.clicked.connect(self.sendPrompt)

        #自定义
        #搜索框
        self.ui.search_bar.textChanged.connect(lambda text,tree=self.ui.search_tree:trm.filterItems(text,tree))
        # 双击选择
        self.ui.search_tree.itemDoubleClicked.connect(self.selectClass)
        #右键显示详情
        self.ui.search_tree.customContextMenuRequested.connect(lambda pos,tree=self.ui.search_tree: self.listShowMenu(pos,tree))
        #删除课程
        #已在createtable函数中连接
        #创建新课表
        self.ui.createtable.clicked.connect(self.createNewTable)
        #删除课表
        self.ui.deletetable.clicked.connect(self.deleteTable)

        #收藏课程
        #添加收藏课程在大课表，自定义栏，推荐列表栏中实现
        #查看收藏课程详情
        #删除收藏课程
        self.ui.likelist.customContextMenuRequested.connect(self.likeShowMenu)
        #选择收藏课程
        self.ui.likelist.itemDoubleClicked.connect(self.selectClass)

        #推荐列表（半自定义）
        self.ui.recommend_list.itemDoubleClicked.connect(self.selectClass)
        self.ui.recommend_list.customContextMenuRequested.connect(lambda pos,tree=self.ui.recommend_list: self.listShowMenu(pos,tree))

        #获取推荐投点
        self.ui.getbet.clicked.connect(self.getbet)

        #便捷转阶段
        self.ui.timetable.cellClicked.connect(self.goTransition)
    def switchPages(self):
        #页面转换
        self.ui.enter_person.clicked.connect(self.openPerson)
        self.ui.enter_edit.clicked.connect(self.goEdit)
        self.ui.enter_main.clicked.connect(self.backMain)
        self.ui.class_table.cellClicked.connect(lambda row, col, t=self.ui.class_table: self.tm.goClassInformation(row, col, t))
        self.ui.ttoedit.clicked.connect(self.goEdit)
        self.ui.hometo.clicked.connect(self.backMain)

    def drawTimeTable(self):
        for i in range(self.ui.timetable.rowCount()):
            for j in range(self.ui.timetable.columnCount()):
                item = self.ui.timetable.item(i, j)
                item.setBackground(QColor('white'))
        idx=0
        if self.BuTuiXuan:
            idx=1
        item = self.ui.timetable.item(idx, 0)
        item.setBackground(QColor(174,255,174))

    def loadClassTable(self):
        self.ui.class_table.clearContents()#清空已有内容
        d.loadFinalTable()
        self.tm.listToTable(d.final_table,self.ui.class_table,self.ui.credit_tag)
        self.loadBetList()
    def loadTransitionTable(self):
        self.ui.transition_table.clearContents()
        d.loadFinalTable()
        self.tm.listToTable(d.final_table,self.ui.transition_table,self.ui.credit_tag)

    def loadBetList(self):
        d.betlist.clear()
        self.ui.waittable.setRowCount(0)
        for Aclass in d.final_table:
            if Aclass.ori['课程类型']!='专业必修':
                Cclass=copy.deepcopy(Aclass)
                Cclass.bet=Aclass.bet
                d.betlist.append(Cclass)
        self.ui.waittable.setRowCount(len(d.betlist))
        for i,bet in enumerate(d.betlist):
            if bet.bet!=-1 and not self.BuTuiXuan:
                content=QTableWidgetItem(bet.name+'\n'+'推荐投点：'+str(bet.bet))
            else:
                content=QTableWidgetItem(bet.name)
            font = QFont()
            font.setPointSize(11)  # 设置字体大小
            content.setFont(font)
            self.ui.waittable.setItem(i, 0, content)
    def renewRecommendList(self):
        self.ui.recommend_list.clear()
        for Aclass in d.recommendlist:
            if int(Aclass.exp*100)/100!=-1:
                item = QListWidgetItem(Aclass.name+' '+Aclass.teacher+' '+Aclass.classnum+'班'+'\n'+'推荐指数：'+str(int(Aclass.exp*100)/100))
            else:
                item = QListWidgetItem(Aclass.name+' '+Aclass.teacher+' '+Aclass.classnum+'班')
            item.setData(Qt.UserRole, copy.deepcopy(Aclass))
            self.ui.recommend_list.addItem(item)
    def loadlike(self):
        d.loadlike()
        for Aclass in d.likelist:
            self.addLike(Aclass,True)

    def morning8Changed(self,value):
        self.ui.morning8_tag.setText("不想上早八  当前值："+str(value))
        d.prefscore[0]=value
    def scoreChanged(self,value):
        self.ui.score_tag.setText("希望给分好  当前值："+str(value))
        d.prefscore[1]=value
    def workloadChanged(self,value):
        self.ui.workload_tag.setText("不希望任务量大  当前值："+str(value))
        d.prefscore[2]=value
    def betChanged(self,value):
        self.ui.bet_tag.setText("不希望掉课  当前值："+str(value))
        d.prefscore[3]=value
    def qualityChanged(self,value):
        self.ui.quality_tag.setText("希望学到干货  当前值："+str(value))
        d.prefscore[4]=value

    def preChoose(self,item,column,must_no):
        Aclass = item.data(0, Qt.UserRole)
        if Aclass not in must_no:
            must_no.append(Aclass)
        self.refreshList()#定义就在下面，更新显示的列表
    def listShowMenu(self,pos,tree):
        item=tree.itemAt(pos)
        if tree is self.ui.search_tree:
            Aclass=item.data(0,Qt.UserRole)
        else:
            Aclass=item.data(Qt.UserRole)
        menu = QMenu(tree)
        info_action = menu.addAction("查看详情")
        def info_action_triggered():
            self.TgoClassInformation(Aclass)
        info_action.triggered.connect(info_action_triggered)
        like_action=menu.addAction("收藏")
        def like_action_triggered():
            self.addLike(Aclass)
        like_action.triggered.connect(like_action_triggered)
        menu.exec(tree.viewport().mapToGlobal(pos))
    def listShowDelete(self,pos,must_no_list,must_no):
        menu = QMenu(must_no)
        
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
        for Aclass in d.must_take:
            item = QListWidgetItem(Aclass.name+' '+Aclass.teacher+' '+Aclass.classnum+'班')
            item.setData(Qt.UserRole, copy.deepcopy(Aclass))  # 将自定义对象存储到 item 的数据中
            self.ui.mustlist.addItem(item)
        for Aclass in d.wont_take:
            item = QListWidgetItem(Aclass.name+' '+Aclass.teacher+' '+Aclass.classnum+'班')
            item.setData(Qt.UserRole, copy.deepcopy(Aclass))  # 将自定义对象存储到 item 的数据中
            self.ui.nolist.addItem(item)

    def createNewTable(self):
        #结合了更新edit列表和ui创建列表
        d.edit_tables.append([])
        self.createTable(len(d.edit_tables)-1)
        #来到新的页面
        self.ui.edit_classtables.setCurrentIndex(len(d.edit_tables)-1)
    def createTable(self,num):
        #首先创建一个新tag
            page = QWidget()
            layout = QVBoxLayout()
            #创建总学分tag
            small_layout=QHBoxLayout()
            spacer=QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
            tag=QLabel()
            tag.setStyleSheet("""
                font-size: 15px;
                color:rgb(70, 70, 70);
                              """)
            #修饰table
            table= QTableWidget(12, 7)
            table.setObjectName("table"+str(num))
            for i in range(12):
                table.setRowHeight(i,48)
            for i in range(7):
                table.setColumnWidth(i,125)
            table.setEditTriggers(QTableWidget.NoEditTriggers)
            table.setStyleSheet("""
            QTableWidget::item:selected {
                    background-color:rgb(240, 245, 255);
                    color: black;
            }
            QTableWidget::item {
                color: rgb(70,70,70);
            }
        """)
            #课程详情入口
            table.cellClicked.connect(lambda row, col, t=table: self.tm.goClassInformation(row, col, t))
            #连接删除信号和槽
            table.setContextMenuPolicy(Qt.CustomContextMenu)
            table.customContextMenuRequested.connect(self.showMenu)
            #组装学分tag
            small_layout.addSpacerItem(spacer)
            small_layout.addWidget(tag)
            #组装tab页
            layout.addWidget(table)
            layout.addLayout(small_layout)
            page.setLayout(layout)
            self.ui.edit_classtables.addTab(page, '课表'+str(num+1))
            #动态存储属性
            setattr(self.ui, "table"+str(num), table)
            setattr(self.ui,"tag"+str(num),tag)
            return table,tag
    def recommend(self):
        #将没有槽函数的spinboxes值存起来
        d.supcredit=self.ui.supcredit.value()
        d.classnum[0]=self.ui.selective.value()
        d.classnum[1]=self.ui.politics.value()
        d.classnum[2]=self.ui.english.value()
        d.classnum[3]=self.ui.publics.value()
        d.classnum[4]=self.ui.general.value()
        d.classnum[5]=self.ui.pe.value()
        d.classnum[6]=self.ui.limited.value()
        #根据data获得推荐课表与推荐列表
        api.get_recommend(test)

        num=len(d.edit_tables)-1
        classList=d.edit_tables[num]
        table,tag=self.createTable(num)
        self.tm.listToTable(classList,table,tag)
        #来到新的页面
        self.ui.edit_classtables.setCurrentIndex(num)
        #更新推荐tab
        self.renewRecommendList()
    def deleteTable(self):
        current_index=self.ui.edit_classtables.currentIndex()
        if current_index == -1:
            return
        reply = QMessageBox.question(
            self.ui,
            "确认操作",
            "确认删除当前编辑中课表",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.No:
            return
        self.ui.edit_classtables.removeTab(current_index)
        d.edit_tables[current_index]=None
        d.edit_tables = [obj for obj in d.edit_tables if obj is not None]

        #更新table们的名字
        for i in range(current_index,len(d.edit_tables)):
            tablename="table"+str(i+1)
            table = getattr(self.ui, tablename, None)
            setattr(self.ui, "table"+str(i), table)

    def apply(self):
        #最终选择一个课表，并回到首页
        num=self.ui.edit_classtables.currentIndex()
        if num==-1:
            QMessageBox.critical(
                self.ui,
                "提示", 
                "请先新建课表！", 
                QMessageBox.Ok 
            )
            return
        reply = QMessageBox.question(
            self.ui,
            "确认操作",
            "确认选择当前课表",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.No:
            return
        d.final_table=copy.deepcopy(d.edit_tables[num])
        d.saveFinalTable()
        self.loadClassTable()
        self.backMain()

    def showMenu(self, pos):
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
        like_action=menu.addAction('收藏')
        def on_action_triggered():
            self.addLike(item.data(Qt.UserRole))
        like_action.triggered.connect(on_action_triggered)
        
        menu.exec(table.viewport().mapToGlobal(pos))
    def delete(self):
        #找到当前课表
        table_num=self.ui.edit_classtables.currentIndex()
        tablename="table"+str(table_num)
        tagname="tag"+str(table_num)
        table = getattr(self.ui, tablename, None)
        tag=getattr(self.ui,tagname,None)

        row = table.currentRow()
        col = table.currentColumn()
        if row != -1 and col != -1:
            item = table.item(row, col)
            Aclass=item.data(Qt.UserRole)
            d.edit_tables[table_num] = [Bclass for Bclass in d.edit_tables[table_num] if Bclass != Aclass]
            self.tm.listToTable(d.edit_tables[table_num],table,tag)

    def selectClass(self,item,column=-1):
        Aclass=None
        if column==-1:#list对象触发
            Aclass=item.data(Qt.UserRole)
        else:
            Aclass = item.data(0, Qt.UserRole)
        table_num=self.ui.edit_classtables.currentIndex()
        if table_num==-1:#无课表
            QMessageBox.critical(
                self.ui,
                "提示", 
                "请先新建课表！", 
                QMessageBox.Ok 
            )
            return
        flag=True
        for Bclass in d.edit_tables[table_num]:
            if Aclass.name==Bclass.name:#重课
                flag=False
                QMessageBox.critical(
                self.ui,
                "提示", 
                "课程重复，选课失败！", 
                QMessageBox.Ok 
                )
                break
            for time in Aclass.timelist:
                for timeb in Bclass.timelist:
                    if time==timeb:#时间冲突
                        flag=False
                        QMessageBox.critical(
                        self.ui,
                        "提示", 
                        "时间冲突，选课失败！", 
                        QMessageBox.Ok 
                        )
                        break
                if not flag:
                    break
            if not flag:
                    break
        if flag:#无重复课程，且无时间冲突
            d.edit_tables[table_num].append(Aclass)
        tablename="table"+str(table_num)
        table = getattr(self.ui, tablename, None)
        tagname="tag"+str(table_num)
        tag=getattr(self.ui,tagname,None)
        self.tm.listToTable(d.edit_tables[table_num],table,tag)

    def addLike(self,Aclass,init=False):
        if not init:
            #非初始不执行后端数据变化操作
            for Bclass in d.likelist:
                if Bclass==Aclass:
                    QMessageBox.critical(
                    self.ui,
                    "提示", 
                    "已收藏该课程！", 
                    QMessageBox.Ok 
                    )
                    return
            d.likelist.append(Aclass)
        item = QListWidgetItem(Aclass.name+' '+Aclass.teacher+' '+Aclass.classnum+'班')
        item.setData(Qt.UserRole, copy.deepcopy(Aclass))
        self.ui.likelist.addItem(item)
        if not init:
            #非初始不执行后端数据变化操作
            QMessageBox.information(
                self.ui,  # 当前窗口实例
                "操作成功",  # 消息框标题
                "收藏课程成功！",  # 消息框内容
                QMessageBox.Ok  # 按钮选项
            )
            d.savelike()
    def likeShowMenu(self,pos):
        item=self.ui.likelist.itemAt(pos)
        Aclass=item.data(Qt.UserRole)
        menu = QMenu(self.ui.likelist)
        info_action = menu.addAction("查看详情")
        def info_action_triggered():
            self.TgoClassInformation(Aclass)
        info_action.triggered.connect(info_action_triggered)
        delete_action = menu.addAction("删除")
        delete_action.triggered.connect(self.likeDelete)
        menu.exec(self.ui.likelist.viewport().mapToGlobal(pos))
    def likeDelete(self):
        row = self.ui.likelist.currentRow()
        if row != -1:
            Aclass=self.ui.likelist.currentItem().data(Qt.UserRole)
            self.ui.likelist.takeItem(row)
            d.likelist = [Bclass for Bclass in d.likelist if Bclass != Aclass]
            d.savelike()

    def changeFinalTable(self):
        d.edit_tables.clear()#重要！
        self.ui.edit_classtables.clear()
        d.final_table.clear()
        selected_items = self.ui.transition_table.selectedItems()
        for item in selected_items:
            Aclass=item.data(Qt.UserRole)
            if Aclass not in d.final_table:
                d.final_table.append(Aclass)
        d.saveFinalTable()
        self.loadClassTable()
    def sendPrompt(self):
        prompt=self.ui.prompttext.toPlainText()
        ret=api.get_list(prompt)
        if isinstance(ret,str):
            QMessageBox.critical(
            self.ui,
            "提示", 
            "ai无法给您一个满意的推荐呢，可以尝试更改要求哦", 
            QMessageBox.Ok 
            )
        self.renewRecommendList()
        self.ui.tabWidget.setCurrentIndex(2)

    def getbet(self):
        #打开投点窗口
        if not self.BuTuiXuan:
            betpage=Bet_page(self.app,self)#把自己也传过去，便于更新列表
            betpage.ui.show()
            self.running_pages.append(betpage)
        else:
            QMessageBox.critical(
            self.ui,
            "提示", 
            "补退选阶段不能投点", 
            QMessageBox.Ok 
            )
    def openPerson(self):
        personpage = Person_page(self.app)
        personpage.ui.show()
        self.running_pages.append(personpage)
    def goEdit(self):
        self.ui.setGeometry(0,23,1440,840)
        self.ui.setCurrentIndex(1)
        #标签管理
        if self.BuTuiXuan:
            self.changeFinalTable()
            self.ui.tabWidget.setTabVisible(0, False)
            self.ui.tabWidget.setTabVisible(1, True)
            self.ui.tabWidget.setCurrentIndex(1)
        else:
            self.ui.tabWidget.setTabVisible(0, True)
            self.ui.tabWidget.setTabVisible(1, False)
            self.ui.tabWidget.setCurrentIndex(0)
        #加载课程列表
        trm.loadClassList(self.ui.search_tree)
        trm.loadClassList(self.ui.must)
        trm.loadClassList(self.ui.no)
        #加载当前课表
        if len(d.edit_tables)==0:
            d.edit_tables.append(copy.deepcopy(d.final_table))
            table,tag=self.createTable(0)
            self.tm.listToTable(d.final_table,table,tag)
    def goTransition(self,row=-1,column=-1):
        if self.BuTuiXuan:
            if row==0 and column==0:
                self.BuTuiXuan=False
                self.ui.setCurrentIndex(1)
            else:
                return
        if (row==1 and column==0) or (row==-1 and column==-1):
            self.BuTuiXuan=True
            self.ui.setGeometry(150,50,900,780)
            self.ui.setCurrentIndex(2)
            self.loadTransitionTable()
    def backMain(self):
        self.ui.setGeometry(0,23,1440,840)
        self.ui.setCurrentIndex(0)
        self.drawTimeTable()
    def TgoClassInformation(self,Aclass):
        classpages=Class_pages(self.app,Aclass)
        classpages.ui.show()
        self.running_pages.append(classpages)