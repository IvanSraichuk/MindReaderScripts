#!/usr/bin/env python
# coding: utf-8

# In[1]:


import wfdb
from wfdb import processing
import numpy as np

record_number = '06995'
def process_row(record_number, filename):

    filepath = 'D:/phd/mit-bih-atrial-fibrillation-database-1.0.0/files/' + record_number
    record = wfdb.rdrecord(filepath) 
    annotation = wfdb.rdann(filepath,'atr', shift_samps=True)
    rightAnsw = np.zeros(len(record.p_signal))
    with open('hmm\\'+ filename) as f:
        lines = f.readlines()[1:]
        lines = [int(x.strip())-1 for x in lines]
    overlap = int(len(record.p_signal)/len(lines))
    rightAnswProcessed = np.zeros(int(len(rightAnsw)/overlap))

    for i in annotation.sample:
        rightAnsw[i] = 1
    for i in range(0, len(rightAnsw), overlap):
        endArray = min(i + 256, len(rightAnsw))
        rightAnswProcessed[int(i/overlap)] = max(rightAnsw[i:endArray])

    
    m = np.zeros((2,2), int)
    TP = 0
    TN = 0
    FN = 0
    FP = 0
    for i in range(len(lines)):
        if lines[i] > 0 and rightAnswProcessed[i] > 0:
            TP += 1
        elif lines[i] == 0 and rightAnswProcessed[i] == 0:
            TN += 1
        elif lines[i] > 0 and rightAnswProcessed[i] == 0:
            FN += 1
        else:
            FP += 1
    print(TP, FN)
    print(FP, TN)
    positive = 0 if TP == 0 else (TP/ (TP + FN))
    negative = 0 if TN == 0 else (TN/ (TN + FP))
    return positive, negative

# In[2]:
entries = os.listdir('C:\\Users\\houfo\\Documents\\MindReaderScripts\\hmm')
for entry in entries:
    if "traceback" in entry:
        print("====="+entry+"=====")
        print(process_row(entry[0:5], entry))
        print("==============")

# In[3]:
print(process_row('05091', '05091ECG.txtx2_traceback.csv'))