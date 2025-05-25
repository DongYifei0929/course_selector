#data

#structure
class Person:
    def __init__(self):
        self.major="cs"
        self.grade="5"
        self.double_major="no"

class Class:
    #成员未对齐
    def __init__(self,testnum):
        self.number=0

        self.name="Advanced mathmatic"+str(testnum)
        self.teacher="Gao Tie"
        self.day=testnum+2
        self.time=[testnum,testnum+1]
        
        self.general=84
        self.quality=66
        self.workload=100
        self.score=59

class Preference:#没必要，权当顺序标识
    #成员未对齐
    def __init__(self,scores):
        self.morning8=scores[0]
        self.score=scores[1]
        self.workload=scores[2]

#functions
#推荐课表接口
def get_recommend():
    recommendTables.clear()
    recommendTables.append([classtest3,classtest4])
    recommendTables.append([classtest1,classtest2])
    recommendTables.append([classtest1,classtest3])

#数据库接口（打开本地文件）
def loadData():
    pass

#test
user=Person()
classtest1=Class(1)
classtest2=Class(2)
classtest3=Class(3)
classtest4=Class(4)
classtabletest=[classtest1,classtest2]

#数据库
majors=['cs','ai']

politic_classes=[classtest1]
compulsory_classes=[classtest2]

#偏好数据
#偏好评分
testscores=[0,0,0]
#自定义偏好列表
mustlist=[]#必选课
nolist=[]#必不选课

#推荐课表返回值
recommendTables=[[]]