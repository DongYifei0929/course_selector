#data
import requests
import json
import copy

#test
test=False
# ori_default={'课程号':'','课程名称':'','开课单位':'','课程类型':'','班号':'','学分':'','起止周':'','上课时间':'','教师':'','备注':'','开课学期':''}
# test_classbag=[ori_test,[[1,2],[1,3]],[1,2,3,4,5],99]
# test_classbag2=[ori_test2,[[4,7],[4,8]],[10,20,30,40,50],-1]
# test_allclass={'所有课程':[test_classbag,test_classbag2],'专业必修':[test_classbag2],'专业任选':[test_classbag2],'思想政治':[test_classbag],'大学英语':[test_classbag],'全校公选课':[test_classbag],'通选课':[test_classbag],'体育':[test_classbag],'专业限选':[test_classbag2]}

"""structure"""
class Person:
    def __init__(self,name,password):
        self.major='通用人工智能'
        self.grade=2
        self.name=name
        self.password=password
user=Person('momo','6')
user_send={}

class Class:
    def __init__(self,classbag):
        self.classbag=classbag#深拷贝
        self.ori=classbag[0]
        #ori解包方便换行显示
        self.id=self.ori['课程号']
        self.name=self.ori['课程名称']
        self.department=self.ori['开课单位']
        self.type=self.ori['课程类型']
        self.classnum=self.ori['班号']
        self.credit=self.ori['学分']
        self.durationweek=self.ori['起止周']
        self.str_time=self.ori['上课时间']
        self.teacher=self.ori['教师']
        self.remark=self.ori['备注']
        self.term=self.ori['开课学期']

        #timelist
        self.timelist=classbag[1]

        #reviews解包方便显示
        self.reviews=classbag[2]
        self.score=self.reviews[0]
        self.workload=self.reviews[1]
        self.morning8=self.reviews[2]
        self.choose_difficulty=self.reviews[3]
        self.quality=self.reviews[4]

        #推荐投点点数
        self.bet=classbag[3]

        #限选人数与已选人数
        self.ratio=classbag[4]
        self.capacity=classbag[4][0]
        self.chosen=classbag[4][1]

        #推荐指数
        if len(classbag)<6:
            self.exp=-1
        else:
            self.exp=classbag[5]#指数的英文真的是exp吗

    def __deepcopy__(self, memo):
        new_obj = type(self)(copy.deepcopy(self.classbag, memo))
        return new_obj
    
    def __eq__(self, other):
        if isinstance(other, Class):
            return self.ori == other.ori
        return False
    def __ne__(self, other):
        return not self == other

"""本地数据"""
#最终选择课表（存到本地文件）（里面是Class类）
final_table=[]

def setbetpoint():
    #存储推荐投点
    if recommendbet:
        for i,Aclass in enumerate(betlist):
            Bclass=final_table[final_table.index(Aclass)]
            Bclass.bet=recommendbet[i]
def saveFinalTable():
    data = []
    for Aclass in final_table:
        data.append([Aclass.ori,Aclass.timelist,Aclass.reviews,Aclass.bet,Aclass.ratio,Aclass.exp])
    with open('data/final_table.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4) 
def loadFinalTable():
    final_table.clear()
    with open('data/final_table.json', 'r', encoding='utf-8') as f:
        allclass = json.load(f) 
    for classbag in allclass:
        final_table.append(Class(classbag))

#收藏课程
likelist=[]
def savelike():
    like=[]
    for Aclass in likelist:
        like.append([Aclass.ori,Aclass.timelist,Aclass.reviews,Aclass.bet,Aclass.ratio,Aclass.exp])
    with open('data/likes.json', 'w', encoding='utf-8') as f:
        json.dump(like, f, ensure_ascii=False, indent=4)
def loadlike():
    likelist.clear()
    with open('data/likes.json', 'r', encoding='utf-8') as f:
        like = json.load(f) 
    for classbag in like:
        likelist.append(Class(classbag))

#缓存的编辑中课表
edit_tables=[]#(Class对象的list的list,main_pages调用)

"""数据库"""
majors=['计算机科学与技术','智能科学与技术','通用人工智能']

#Class对象的list
all=[]
compulsory=[]
selective=[]
politics=[]
english=[]
public=[]
general=[]
pe=[]
limited=[]

#数据库接口
def loadData(allclass={}):
    # if allclass=={}:
    #     with open('data/database.json', 'r', encoding='utf-8') as f:
    #         allclass = json.load(f) 

    global all,compulsory,selective,politics,english,public,general,pe,limited
    all.clear()
    if '所有课程' in allclass.keys():
        alltemp=allclass['所有课程']
        for classbag in alltemp:
            Aclass=Class(classbag)
            all.append(Aclass)
    compulsory.clear()
    if '专业必修' in allclass.keys():
        compulsorytemp=allclass['专业必修']
        for classbag in compulsorytemp:
            Aclass=Class(classbag)
            compulsory.append(Aclass)
    selective.clear()
    if '专业任选' in allclass.keys():
        selectivetemp=allclass['专业任选']
        for classbag in selectivetemp:
            Aclass=Class(classbag)
            selective.append(Aclass)
    politics.clear()
    if '思想政治' in allclass.keys():
        politicstemp=allclass['思想政治']
        for classbag in politicstemp:
            Aclass=Class(classbag)
            politics.append(Aclass)
    english.clear()
    if '大学英语' in allclass.keys():
        englishtemp=allclass['大学英语']
        for classbag in englishtemp:
            Aclass=Class(classbag)
            english.append(Aclass)
    public.clear()
    if '全校公选课' in allclass.keys():
        publictemp=allclass['全校公选课']
        for classbag in publictemp:
            Aclass=Class(classbag)
            public.append(Aclass)
    general.clear()
    if '通选课' in allclass.keys():
        generaltemp=allclass['通选课']
        for classbag in generaltemp:
            Aclass=Class(classbag)
            general.append(Aclass)
    pe.clear()
    if '体育' in allclass.keys():
        petemp=allclass['体育']
        for classbag in petemp:
            Aclass=Class(classbag)
            pe.append(Aclass)
    limited.clear()
    if '专业任选' in allclass.keys():
        limitedtemp=allclass['专业任选']
        for classbag in limitedtemp:
            Aclass=Class(classbag)
            limited.append(Aclass)


"""api收发：数据暂存和打包"""
#偏好
#偏好评分
prefscore=[0,0,0,0,0]
pref_send={}
#自定义偏好列表
must_take=[]#必选课
wont_take=[]#必不选课
must_send=[]
wont_send=[]
#门数
classnum=[0,0,0,0,0,0,0]
num_send={}
#学分上限
supcredit=25
#接收推荐课程的列表
recommendlist=[]

#投点
#最终选择课表中需要投点的课程
betlist=[]
#推荐投点界面输入的已选限选人数
capacity=[]
#接收到的推荐投点数
recommendbet=[]

#推荐课表接口
def packuser():
    #打包用户信息
    global user,user_send
    user_send['专业']=user.major
    user_send['年级']=user.grade
def packinfo():
    #打包发送数据
    #偏好评分
    global prefscore, pref_send
    strs=['给分','任务量','早八厌恶程度','选课难度','水分']
    for i in range(len(prefscore)):
        pref_send[strs[i]]=prefscore[i]
    #筛选列表
    global must_take,wont_take,must_send,wont_send
    for Aclass in must_take:
        must_send.append(Aclass.ori)
    for Aclass in wont_take:
        wont_send.append(Aclass.ori)
    #预期每个类别的选课数量
    global classnum,num_send,supcredit
    num_send['总学分']=supcredit
    strs=['专业任选','思想政治','大学英语','全校公选课','通选课','体育','专业限选']
    for i in range(len(strs)):
        num_send[strs[i]]=classnum[i]
def packfinal():
    #打包已选上课程数据，将class转化为classbag
    global final_table
    ret=[]
    for Aclass in final_table:
        ret.append([Aclass.ori,Aclass.timelist,Aclass.reviews,Aclass.ratio])
    return ret

#处理收到的classbag列表
def get_recommend(ori_recommendtable=[],ori_recommendlist=[]):
    global recommendlist

    #处理接收数据
    recommendlist.clear()
    table=[]
    for classdict in ori_recommendtable:
        Aclass=Class(classdict)
        table.append(Aclass)
    if table:
        edit_tables.append(table)
    #print(ori_recommendlist)
    if ori_recommendlist and len(ori_recommendlist[0])>=6:
        ori_recommendlist.sort(key=lambda classbag:-1*classbag[5])
    for classbag in ori_recommendlist:
        Aclass=Class(classbag)
        recommendlist.append(Aclass)
    #print(recommendlist)

#所有课程，专业必修，专业任选，思想政治，大学英语，全校公选课，通选课，体育，专业限选
#接收：
#       database(可选课程列表)  {分类:['list' ['bag' {ori},[timelist],[scores], bet_int=-1,[限选人数，已选人数] 'bagend'] 'listend']}
#       recommend table,  [ [{ori},[timelist],[scores],bet_int,[限选人数，已选人数],推荐指数_floatorint ] ]
#       recommend list, [ [{ori},[timelist],[scores],bet_int,[限选人数，已选人数],推荐指数_floatorint ] ]
#发送：
#       一个用户：dict,包括专业，年级 {'专业':'cs', '年级': 1}
#       偏好评分：dict，包含各个float型 {'给分' '任务量' '早八厌恶' '选课难度' '水分': 0}
#       筛选列表：must and wont, [{ori}]
#       每类课程门数：int  学分上限：int {'专业必选': 0,...,'学分上限':0}
#       review评分：更新课程数据（有时间实现）
#       投点数据：list，元素为tuple，(限选，已选)