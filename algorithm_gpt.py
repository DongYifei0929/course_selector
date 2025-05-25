# load the data
import requests
BASE_URL="http://10.7.21.186:8000"
API_PATH="/courses"
response=requests.get(f"{BASE_URL}{API_PATH}")
if response.status_code==200:
    data=response.json()

# set courses
import re
import random
class Course:
    def __init__(self,course_information):
        self.original=course_information #给原始字典留档
        self.id=course_information['课程号']
        self.name=course_information['课程名称']
        self.type=course_information['课程类型']
        self.credit=int(course_information['学分'])
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
        self.available=100
        self.chosen=random.randint(20,400)
        self.probability=min(1,self.available/self.chosen) #选课概率
        self.evaluated=[random.randint(60,100),random.randint(40,100)] #百分制
        # 分别是给分 任务量
        if [1,1] in self.time_list or [2,1] in self.time_list or [3,1] in self.time_list or [4,1] in self.time_list or [5,1] in self.time_list or [6,1] in self.time_list or [7,1] in self.time_list: 
            self.evaluated.append(-8)
        else: self.evaluated.append(0) #对早八的厌恶程度
        self.evaluated.append(1/self.probability) #选课难度

course_list={'所有课程':[],'专业必修':[],'专业任选':[],'思想政治':[],'大学英语':[],'全校公选课':[],'通选课':[],'体育':[],'专业限选':[]}

for i in range(len(data)):
    new_course=Course(data[i])
    if new_course.type in course_list.keys():
        course_list[new_course.type].append(new_course)
# transport the data to jyls

# load the comments --optional?
class Comment:
    def __init__(self,comment):
        self.general=comment['总体']
        self.score=comment['给分']
        self.workload=comment['任务量']
        self.quality=comment['内容质量']
# transport the data to jyls

from typing import List, Dict
class Preference:
    preferences: Dict[str,float] # 给分 任务量 时间段 选课难度 （通勤难度、上四休三）
    must_take: List[str]=[]
    must_not_take: List[str]=[]
    expected_credits: Dict[str,int]
    available_courses: List[Course] 
# get data from jyls *needs communicate*

# needs api
def filter_according_to_semester(grade):
    if grade==24: return '一下'
    elif grade==23: return '二下'
    elif grade==22: return '三下'
    else: return '四下'

# filter courses
def course_filter(prompts:Dict[str,str]): #课程号 课名 开课类型 开课单位 班号 老师 地点 etc.
    filtered_list=course_list['所有课程']
    for key in prompts.keys():
        if prompts[key]==None: continue
        values=[course.original[key] for course in filtered_list]
        if prompts[key] not in values: continue
        filtered_list=[course for course in filtered_list if course.original[key]==prompts[key]]
    return filtered_list
# transport the data to jyls

API_PATH1="/courses2"
response1=requests.get(f"{BASE_URL}{API_PATH1}") #导入培养方案课程
if response1.status_code==200:
    data1=response1.json()

available_courses=[]
def get_available_courses(grade): # get data from jyls
    semester=filter_according_to_semester(grade)
    for course in data1:
        if semester in course['选课学期']:
            target_list=[ele for ele in course_list['所有课程'] if ele.id==course['课程号']] #把专业必修和专业选修筛出来
    available_courses.extend(target_list)
    for key in course_list.keys():
        if key=='专业必修' or key=='专业任选': continue
        available_courses.extend(course_list[key])

# recommend courses
# with weights
def recommend_with_weights(preferences:Dict[str,float],must_take:List[str],must_not_take:List[str],available_courses:List[Course],expected_credits:List[Dict[str,int]]) -> List[Dict]:
    recommended=[]
    credits={'所有课程':0,'专业必修':0,'专业任选':0,'思想政治':0,'大学英语':0,'全校公选课':0,'通选课':0,'体育':0,'专业限选':0}
    occupied_times=[] # 简单起见，只要求其他课程不能与专业必修课时间冲突
    for type in course_list.keys():
        #一开始需要分一下课的种类
        if type=='所有课程': continue
        categorized_courses=[course for course in available_courses if course.type==type]
        # 给分 任务量 时间段
        weights=[10,10,5,3]
        cnt=[[0,i] for i in len(preferences)]
        for i,course in enumerate(categorized_courses):
            for j,value in enumerate(preferences.values()):
                score=course.evaluated[j]-value
                if j==2 and course.evaluated==0: score=0 
                #特判：如果维度是早八而这节课不是早八，score归零 
                cnt[i][0]+=weights[j]*score
            if course.name in must_take:
                cnt[i][0]+=1e9
            if course.name in must_not_take:
                cnt[i][0]-=1e9
        cnt.sort(key=lambda x: x[0],reverse=True)
        name_list=[] #已选课程名列表(不能重复)
        for i,ele in enumerate(cnt):
            course=categorized_courses[ele[1]]
            if course.name in name_list: #不重复选课
                continue
            if credits['所有课程']+course.credit>expected_credits['所有课程'] \
            or credits[course.type]+course.credit>expected_credits[course.type]: 
                continue
            for time in course.time_list:
                if time in occupied_times:
                    continue
            if course.type=='专业必修': # 专业必修课的时间不能有其他课
                occupied_times.extend(course.time_list)
            name_list.append(course.name)
            recommended.append(course)
            credits['所有课程']+=course.credit
            credits[course.type]+=course.credit
    return recommended
    #生成多套课表？

# with neural network
import torch
import torch.nn as nn
import numpy as np

# 把对每个课的喜爱程度转化成一个vector
def encode_course(course:Course,preferences: Dict[str,float]) -> np.ndarray:
    vec=np.array([course.evaluated[i]-value for i,value in enumerate(preferences.values())], dtype=np.float32)
    return vec

class NeuralNetwork(nn.Module):
    def __init__(self,input_dim=4,hidden_dim=64,output_dim=1):
        # output is a comprehensive assessment to a course
        super().__init__()
        self.flatten=nn.Flatten()
        self.Net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim),
            nn.Sigmoid()
        )
    def forward(self, x):
        return self.Net(x)

input_dim,hidden_dim,output_dim=4,64,1
device=torch.device("cpu")
model=NeuralNetwork(input_dim,hidden_dim,output_dim).to(device)
Loss=nn.CrossEntropyLoss()
Optimizer=torch.optim.Adam(model.parameters(),lr=1e-3)

def train():
    max_epoch=5
    batch_size=64
    num_samples=1000
    input_size=4 ##
    X = torch.randn(num_samples, input_size).to(device)
    y = torch.randint(0, 1, (num_samples,)).to(device)
    dataset = torch.utils.data.TensorDataset(X, y)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
    for i in range(max_epoch):
        for input,label in dataloader:
            #forward
            output=model(input)
            loss=Loss(output,label)
            #backward
            Optimizer.zero_grad()
            loss.backward()
            Optimizer.step()

# must take & must not take from jyls
def calculate_with_NN(preferences:Dict[str,float],must_take:List[str],must_not_take:List[str],available_courses:List[Course]) -> List[Dict]:
    net=NeuralNetwork()
    train()
    result=[]
    for course in available_courses:
        vec=torch.tensor(encode_course(course,preferences))
        with torch.no_grad():
            score=net(vec).item()
        if course.name in must_take: score+=1e9
        if course.name in must_not_take: score+=-1e9
        result.append((score,course))
    result.sort(key=lambda x:x[0],reverse=True)
    return result

def recommend_with_NN(preferences:Dict[str,float],must_take:List[str],must_not_take:List[str],available_courses:List[Course],expected_credits=Dict[str,int]) -> List[Dict]:
    priority_list=calculate_with_NN(preferences,must_take,must_not_take,available_courses)
    recommended=[]
    credits={'所有课程':0,'专业必修':0,'专业任选':0,'思想政治':0,'大学英语':0,'全校公选课':0,'通选课':0,'体育':0,'专业限选':0}
    name_list=[]
    occupied_times=[] # 简单起见，只要求其他课程不能与专业必修课时间冲突 
    for score,course in priority_list:
        if course.name in name_list: continue
        if credits[course.type]+course.credit>expected_credits[course.type] \
        or credits['所有课程']+course.credit>expected_credits['所有课程']:
            continue
        for time in course.time_list:
            if time in occupied_times:
                continue
        if course.type=='专业必修':
            occupied_times.extend(course.time_list)
        name_list.append(course.name)
        recommended.append(course)
        credits['所有课程']+=course.credit
        credits[course.type]+=course.credit
    return recommended

def generate_schedule(data:Preference):
    recommended=recommend_with_weights(data.preferences,data.must_take,data.must_not_take,data.available_courses)
#    recommended=recommend_with_NN(data.preferences,data.must_take,data.must_not_take,data.available_courses)
    return {"recommended_courses": recommended}

# need to create data
