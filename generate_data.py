import numpy as np

np.random.seed(42)
original_data1=np.random.uniform(20,100,size=(2000,5))
original_data2=np.random.uniform(20,100,size=(2000,5))
DATA=np.concatenate((original_data1,original_data2),axis=0)

weights1=np.array([10,5,4,3,4]).T
weights2=np.array([7.5,7.5,5,3,3]).T
medium1=original_data1@weights1
medium2=original_data2@weights2

result1=np.random.normal(loc=medium1,scale=1.0)
result2=np.random.normal(loc=medium2,scale=1.0)
RESULTS=np.concatenate((result1,result2),axis=0)
RESULTS=RESULTS.reshape((4000,1))

'''
print('data is:')
print(DATA)
print('shape of data is:')
print(DATA.shape)
print('results is:')
print(RESULTS)
print('shape of results is:')
print(RESULTS.shape) # (4000,)
'''