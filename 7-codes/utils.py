'''
# load the data
import requests
BASE_URL="http://10.7.21.186:8000"
API_PATH="/courses"
response=requests.get(f"{BASE_URL}{API_PATH}")
if response.status_code==200:
    data=response.json()

# load the curriculum, and add extra information to the existing courses
API_PATH1="/courses2"
response1=requests.get(f"{BASE_URL}{API_PATH1}") #导入培养方案课程
if response1.status_code==200:
    data1=response1.json()
'''
import ast
with open('data/所有课程.txt','r',encoding='utf-8') as f:
    content=f.read()
data=eval(content)
# data = ast.literal_eval(content)
with open('data/培养方案.txt','r',encoding='utf-8') as f:
    content=f.read()
data1=eval(content)

import re
import random

class Course:
    def __init__(self,course_information):
        self.original=course_information #给原始字典留档

        self.id=course_information['课程号']
        self.name=course_information['课程名称']
        self.type=course_information['课程类型']
        self.credit=float(course_information['学分'])
        
        self.time_list=[]
        self.time_str=course_information['上课时间'] #further process
        cleaned_str=re.sub(r'\([单双]\)','',self.time_str)
        pattern=r'([一二三四五六日])\(第(\d+)节-第(\d+)节\)'
        weekdays={'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'日':7}
        matches=re.findall(pattern,cleaned_str)
        for match in matches:
            weekday,start,end=match
            start,end=int(start),int(end)
            for time in range(start,end+1):
                self.time_list.append([weekdays[weekday],time])
        #time_list 形如: [[weekday=1~7,time=1~12],...]

        self.remark=course_information['备注'] #further process
        ind=self.remark.rfind('，') #注意是中文的逗号！
        self.location=self.remark[ind+1:]
        self.semester=course_information['开课学期']

        self.available=100
        self.chosen=random.randint(20,400)
        self.probability=min(1,self.available/self.chosen) #选课概率
        self.evaluated=[random.randint(60,100),random.randint(40,100)] #百分制
        # 分别是给分 任务量 早八厌恶 选课难度 水分
        if [1,1] in self.time_list or [2,1] in self.time_list or [3,1] in self.time_list or [4,1] in self.time_list or [5,1] in self.time_list or [6,1] in self.time_list or [7,1] in self.time_list: 
            self.evaluated.append(-8)
        else: self.evaluated.append(0) #对早八的厌恶程度
        self.evaluated.append(1/self.probability) #选课难度
        self.evaluated.append(random.randint(40,100)) #水分

        self.bet=-1

course_list={'所有课程':[],'专业必修':[],'专业任选':[],'思想政治':[],'大学英语':[],'全校公选课':[],'通选课':[],'体育':[],'专业限选':[]}
course_list_transport={'所有课程':[],'专业必修':[],'专业任选':[],'思想政治':[],'大学英语':[],'全校公选课':[],'通选课':[],'体育':[],'专业限选':[]}
# transport to jyls

for i in range(len(data)):
    new_course=Course(data[i])
    course_list['所有课程'].append(new_course)
    if new_course.type in course_list.keys():
        course_list[new_course.type].append(new_course)   

# {'category': [ [{original information},time_list,evaluated[0~4] ] , ...] }