import requests
import json
import copy
import data as d

from phase1 import generate_schedule,get_available_courses,distribute_stake
from phase2 import get_course_recommendations,API_KEY

# 服务器URL
#server_url = "http://10.3.68.46:8000"
# server_url = "http://172.20.10.7:8000"
# server_url = "http://192.168.3.37:8000"
#server_url = "http://10.3.152.110:8000"

available_courses=[]
L1,D2,L3=0,[],[]
def get_database():
    global available_courses
    d.packuser()
    D1=d.user_send
    global L1
    available_courses,L1=get_available_courses(D1['年级'])
    d.loadData(L1)

def get_recommend(test=False):
    d.packinfo()
    L4=d.must_send
    L5=d.wont_send
    global D2
    D2=d.pref_send
    D3=d.num_send
    global L3
    L2,L3=generate_schedule(D2,L4,L5,D3,available_courses)
    d.get_recommend(L2,L3)
    return

def get_bet():
    L8=d.capacity
    L9=distribute_stake(L8)
    d.recommendbet=L9
    return

def get_list(prompt):
    L6=d.packfinal()
    S1=prompt
    available_courses_transport=get_available_courses(L1)[1]
    L7=get_course_recommendations(API_KEY,L3[10:40],available_courses_transport['专业必修'],L6,D2,S1)
    if isinstance(L7,str):
        return L7
    d.get_recommend([],L7)
    return