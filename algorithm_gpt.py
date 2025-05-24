# course_selector/main.py
from requests import *
from fastapi import FastAPI
from routes import course, preference, review, recommend

app = FastAPI(title="选课机系统")

app.include_router(course.router, prefix="/course")
app.include_router(preference.router, prefix="/preference")
app.include_router(review.router, prefix="/review")
app.include_router(recommend.router, prefix="/recommend")

# course_selector/routes/recommend.py
from fastapi import APIRouter
from models.recommender import recommend_courses
from pydantic import BaseModel
from typing import List, Dict

router = APIRouter()

class PreferenceInput(BaseModel):
    preferences: Dict[str, float]
    must_take: List[str] = []
    available_courses: List[Dict]  # Each course has 'name', 'teacher', 'time_slot', etc.

@router.post("/generate")
def generate_schedule(data: PreferenceInput):
    recommended = recommend_courses(data.preferences, data.must_take, data.available_courses)
    return {"recommended_courses": recommended}

# course_selector/models/recommender.py
import torch
import torch.nn as nn
import numpy as np

# 把每个课转化成一个vector
def encode_course(course: dict, preference_keys: List[str]) -> np.ndarray:
    # Simple encoder: numeric preference projection + keyword boost
    vec = np.array([course.get(k, 0.0) for k in preference_keys], dtype=np.float32)
    if course['name'] in course.get('tags', []):
        vec += 0.5  # boost known interest
    return vec

class NeuralNetwork(nn.Module):
    def __init__(self, input_dim,hidden_dim=64,output_dim=1):
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

input_dim,hidden_dim,output_dim=10,64,1
device=torch.device("cpu")
model=NeuralNetwork(input_dim,hidden_dim,output_dim).to(device)

Loss=nn.CrossEntropyLoss()
Optimizer=torch.optim.Adam(model.parameters(),lr=1e-3)

def train():
    max_epoch=5
    batch_size=64
    num_samples=1000
    input_size=10 ##
    X = torch.randn(num_samples, input_size).to(device)
    y = torch.randint(0, 1, (num_samples,)).to(device)
    dataset = torch.utils.data.TensorDataset(X, y)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
    for i in range(max_epoch):
        for input,label in dataloader:
            output=model(input)
            loss=Loss(output,label)

            Optimizer.zero_grad()
            loss.backward()
            Optimizer.step()

def recommend_courses_with_NN(preferences: Dict[str, float], must_take: List[str], courses: List[Dict]) -> List[Dict]:
    preference_keys = list(preferences.keys())
    net = NeuralNetwork(len(preferences))
    net.eval()

    results = []
    for course in courses:
        vec = torch.tensor(encode_course(course, preference_keys))
        with torch.no_grad():
            score = net(vec).item()
        results.append((score, course))

    results.sort(key=lambda x: -x[0])
    final = [r[1] for r in results if r[1]['name'] in must_take or r[0] > 0.5]
    return final[:10]  # return top 10 recommended

def recommend_course_with_weights(preferences: Dict[str, float], must_take: List[str], courses: List[Dict], credits: List[Dict[str,int]]) -> List[Dict]:
    #一开始需要分一下课的种类 type
    recommended=[]
    types=["专业必修","专业任选","思政","通识课","全校公选课","大学英语课"]
    for type in types:
        categorized_courses=[course for course in courses if course['type']==type]
        weights=[1 for _ in len(preferences)]
        cnt=[[0,i] for i in len(preferences)]
        for i,course in enumerate(categorized_courses):
            score=[1 for _ in range(len(weights))] #把course各个维度映射到
            for j in preferences.values():
                cnt[i][0]+=weights[j]*score[j]
            if course['name'] in must_take:
                cnt[i][0]+=1e9
        cnt.sort(key=lambda x: x[0],reverse=True)
        if type=="专业必修":
            recommended.append(categorized_courses[cnt[0][1]])
        else:
            sum=categorized_courses[cnt[0][1]]['credit']
            id=0
            while(sum<=credits[type]):
                recommended.append(categorized_courses[cnt[id][1]])
                id+=1
                sum+=categorized_courses[cnt[id][1]]['credit']
    return recommended