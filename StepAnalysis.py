from math import *
import numpy as np
import seaborn as sns
import random
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D

line_data = []
phononids = []
setids = []
data = []
phononid = 0
phononData = {}

#this requires that the step data is organized like this: id, .., .., \n
print("Collecting data . . . ")
directory = "Data/"
path = directory + "StepData.txt"
f = open(path, "r")
lines = f.readlines()
f.close()

print("Reading Data . . . ")
for i in range(0, len(lines) - 1):
    line = lines[i]
    if(line == "New Event\n"):
        break
    line_data = line[:-1].split(",")
    phononid = int(line_data[0])
    phononids.append(phononid)
    data.append(line_data)

setids = list(set(phononids))
setids.sort()

for i in range(len(setids)):
    phononData[setids[i]] = []

for i in range(len(phononids)):
    phononData[phononids[i]].append(data[i])

num = 0
pid = 0
for ID in phononData:
    pdata = phononData[ID]
    lenp = len(pdata)
    pid = int(pdata[0][6])
    if(pid < 1):
        continue
    parent = phononData[pid]
    vol = parent[0][5]
    v = vol[0]
    if(lenp <= 2):
        # num += 1
        # print(vol)
        # print(ID)
        if(v == "k" or v == "f"):
            num += 1
            print(vol)
            print(ID)
    # if(v == "k" or v == "f"):
    #     time = float(pdata[0][2])
    #     timep = float(parent[len(parent) - 1][2])
    #     # print("data: ")
    #     # print(pdata)
    #     # print("parent: ")
    #     # print(parent)
    #     print("Time difference: ",end = "")
    #     print(str(time - timep))
    #     # print()

print("Number of length 1 tracks: " + str(num))