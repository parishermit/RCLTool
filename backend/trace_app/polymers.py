import sys
import pickle
from config import *
sys.path.append("..")
from root_cause_analysis.tracerca.tracerca import tracerca

with open(os.path.join(out_path,"pred_abnormal_trace_ind.pkl"),'br') as f:
    pred_abnormal_trace_ind = pickle.load(f)
with open(os.path.join(out_path,"trace_list.pkl"),'br') as f:
    trace_list = pickle.load(f)

pred_abnormal_trace_list = []
for ind in pred_abnormal_trace_ind:
    pred_abnormal_trace_list.append(trace_list[ind])

print(len(pred_abnormal_trace_list))
start_time_list = [trace.root_span.start_time for trace in pred_abnormal_trace_list]
minutes_list = [dt.hour * 60 + dt.minute for dt in start_time_list]
# print(Counter(minutes_list))

time2traces = {}
for i in set(minutes_list):
    time2traces[i]=[]
for i in range(len(minutes_list)):
    time2traces[minutes_list[i]].append(pred_abnormal_trace_list[i])

test_fault_injection_list = list(time2traces.values())


res = tracerca(test_fault_injection_list)
with open(os.path.join(out_path,"label.txt"),'a') as fw:
    fw.write(f"\n{len(pred_abnormal_trace_list)}\nroot cause analysis: ")
    fw.write(res)

print(len(pred_abnormal_trace_list))
start_time_list = [trace.root_span.start_time for trace in pred_abnormal_trace_list]
minutes_list = [dt.hour * 60 + dt.minute for dt in start_time_list]
# print(Counter(minutes_list))

time2traces = {}
for i in set(minutes_list):
    time2traces[i]=[]
for i in range(len(minutes_list)):
    time2traces[minutes_list[i]].append(pred_abnormal_trace_list[i])