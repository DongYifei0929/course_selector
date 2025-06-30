# set courses
from utils import Course,course_list,data1
from Neural_Network import *

from typing import List, Dict

def filter_according_to_semester(grade):
    if grade==1: return '一下'
    elif grade==2: return '二下'
    elif grade==3: return '三下'
    else: return '四下'
# get data from jyls

# filter courses
def course_filter(prompts:Dict[str,str]): #课程号 课名 开课类型 开课单位 班号 老师 地点 etc.
    filtered_list=course_list['所有课程']
    for key in prompts.keys():
        if prompts[key]==None: continue
        values=[course.original[key] for course in filtered_list]
        if prompts[key] not in values: continue
        filtered_list=[course for course in filtered_list if course.original[key]==prompts[key]]
    return filtered_list

# use the curriculum to filter available courses
def get_available_courses(grade):
    available_courses=[]
    semester=filter_according_to_semester(grade)
    for course in data1:
        if semester in course['选课学期'] or course['选课学期']=='':
            target_list=[ele for ele in course_list['所有课程'] if ele.name==course['课程名称'] and ele.semester=='spring'] #把专业必修和专业选修筛出来
            available_courses.extend(target_list)
    for key in course_list.keys():
        if key=='所有课程' or key=='专业必修' or key=='专业任选' or key=='专业限选': 
            continue
        available_courses.extend(course_list[key])
    available_courses_transport={key:[[course.original,course.time_list,course.evaluated,-1,[course.available,course.chosen],-1] for course in course_list[key] if course in available_courses] for key in course_list}
    return available_courses,available_courses_transport

def recommend_with_NN(preferences:Dict[str,float],must_take:List[Dict],must_not_take:List[Dict],available_courses:List[Course],expected_num:Dict[str,int]):
    priority_list=calculate_with_NN(preferences,must_take,must_not_take,available_courses) 
    recommended=[]
    nums={'总学分':0,'专业任选':0,'思想政治':0,'大学英语':0,'全校公选课':0,'通选课':0,'体育':0,'专业限选':0}
    name_list=[]
    occupied_times=[] # 简单起见，只要求其他课程不能与专业必修课时间冲突
    for score,course in priority_list: #专业必修课
        if course.name in name_list: continue
        if course.type!='专业必修':
            continue
        if course.original in must_not_take:
            continue
        if nums['总学分']+course.credit>expected_num['总学分']:
            continue
        for time in course.time_list:
            if time in occupied_times:
                continue
        occupied_times.extend(course.time_list)
        name_list.append(course.name)
        recommended.append((score,course))
        nums['总学分']+=course.credit
    for score,course in priority_list: #其它课程
        if course.name in name_list: continue
        if course.credit==0: continue
        if course.type not in nums.keys():
            continue
        if nums[course.type]>=expected_num[course.type] or nums['总学分']+course.credit>expected_num['总学分']:
            continue
        for time in course.time_list:
            if time in occupied_times:
                continue
        name_list.append(course.name)
        recommended.append((score,course))
        nums['总学分']+=course.credit
        nums[course.type]+=1
    return recommended,priority_list

def distribute_stake(courses):
    bets=[97,61,31,2,0]
    tot=99
    ret=[]
    for available,chosen in courses:
        chosen+=0.001
        if tot<=5:
            ret.append(tot)
            tot=0
            continue
        probability=min(1,available/chosen)
        if probability<0.1 or probability>=0.95: 
            ret.append(0)
        elif 0.1<=probability<0.4: 
            for i in range(5):
                if tot>=bets[i]:
                    ret.append(bets[i])
                    tot-=bets[i]
                    break
        elif 0.4<=probability<0.7:
            for i in range(1,5):
                if tot>=bets[i]:
                    ret.append(bets[i])
                    tot-=bets[i]
                    break
        elif 0.7<=probability<0.95:
            for i in range(2,5):
                if tot>=bets[i]:
                    ret.append(bets[i])
                    tot-=bets[i]
                    break
    return ret

def generate_schedule(preferences,must_take,must_not_take,expected_num,available_courses):
    recommended,recommended_list=recommend_with_NN(preferences,must_take,must_not_take,available_courses,expected_num)
    recommended_table=[[course.original,course.time_list,course.evaluated,-1,[course.available,course.chosen],score] for score,course in recommended]
    recommended_list=[[course.original,course.time_list,course.evaluated,-1,[course.available,course.chosen],score] for score,course in recommended_list]
    return recommended_table,recommended_list