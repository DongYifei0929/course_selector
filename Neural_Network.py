import torch
import torch.nn as nn
import numpy as np
from typing import Dict,List
from utils import Course
from generate_data import DATA,RESULTS

# 把对每个课的喜爱程度转化成一个vector
def encode_course(course:Course,preferences: Dict[str,float]) -> np.ndarray:
    vec=np.array([course.evaluated[i]-value for i,value in enumerate(preferences.values())], dtype=np.float32)
    return vec

class NeuralNetwork(nn.Module):
    def __init__(self,input_dim=5,hidden_dim=64,output_dim=1):
        # output is a comprehensive assessment to a course
        super().__init__()
        self.flatten=nn.Flatten()
        self.Net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim),
        #    nn.Sigmoid()
        )
    def forward(self, x):
        return self.Net(x)

input_dim,hidden_dim,output_dim=5,64,1
device=torch.device("cpu")
model=NeuralNetwork(input_dim,hidden_dim,output_dim).to(device,dtype=torch.float32)
Loss=nn.MSELoss()
Optimizer=torch.optim.Adam(model.parameters(),lr=1e-3)

def train():
    max_epoch=5
    batch_size=64
    X = torch.from_numpy(DATA).to(device,dtype=torch.float32)
    y = torch.from_numpy(RESULTS).to(device,dtype=torch.float32)
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
def calculate_with_NN(preferences:Dict[str,float],must_take:List[Dict],must_not_take:List[Dict],available_courses:List[Course]):
    net=NeuralNetwork()
    train()
    result=[]
    for course in available_courses:
        vec=torch.tensor(encode_course(course,preferences))
        with torch.no_grad():
            score=net(vec).item()
        if course.original in must_take: score+=1e9
        if course.original in must_not_take: score+=-1e9
        result.append((score,course))
    result.sort(key=lambda x:x[0],reverse=True)
    return result