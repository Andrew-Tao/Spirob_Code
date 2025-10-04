import numpy as np 
import json
import matplotlib.pyplot as plt
import os
from pathlib import Path
from scipy.stats import norm

path0 = Path ("/home/spirob/Documents/Experiments/path_record_noise.txt")
with open(path0,"r") as f:
	path_record = json.load(f)

load_path = Path("/home/spirob/Documents/Experiments/Hysteresis_Experiment_test2025-09-19 00:39:44.445903/Load")
with open(load_path,"r") as f:
	sampling_load = json.load(f)
print(sampling_load)
sampling_load  = np.array(sampling_load)
sampling_load= sampling_load[sampling_load < -3e6]
def get_bell(lower,upper,data):
	
	segment = data[lower:upper]
	mean =  np.mean(segment)
	std_dev = np.std(data)
	return mean, std_dev
	
	
mean1, std_dev1 = get_bell(0,int(len(sampling_load)/8),sampling_load) #10s
mean2, std_dev2 = get_bell(0,int(len(sampling_load)/4),sampling_load) # 20s
mean3, std_dev3 = get_bell(0,int(len(sampling_load)/2),sampling_load) # 40s
mean4, std_dev4 = get_bell(0,int(len(sampling_load)/1),sampling_load) # 80s

x = np.linspace(mean4-4*std_dev4,mean4 + 4*std_dev4,1000)



y1 = norm.pdf(x,mean1,std_dev1)
y2 = norm.pdf(x,mean2,std_dev2)
y3 = norm.pdf(x,mean3,std_dev3)
y4 = norm.pdf(x,mean4,std_dev4)

plt.figure(1)
plt.hist(sampling_load,bins = 25, density = True, alpha = 0.6, color = 'skyblue', edgecolor = 'black')
plt.plot(x,y1,'r-',linewidth = 2,color = 'green',label = '10s')
plt.plot(x,y2,'r-',linewidth = 2,color = 'yellow',label='20s')
plt.plot(x,y3,'r-',linewidth = 2,color = 'orange',label='40s')
plt.plot(x,y4,'r-',linewidth = 2,color = 'red',label = '40s')
plt.legend()

plt.xlabel("stress(Pa)")
plt.ylabel("frequncy")
plt.title("Noise_Characterisation")
plt.grid(True)

plt.figure(2)
x_time = np.array([])
for i in range(len(sampling_load)):
	x_time = np.append(x_time,i)

plt.plot(x_time/100,sampling_load)

plt.xlabel("Time(s)")
plt.ylabel("Stress(Pa)")
plt.title("Noise_Characterisation")
plt.grid(True)

plt.show()
