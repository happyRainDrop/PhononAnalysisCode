from math import *
import numpy as np
import seaborn as sns
import random
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D

dt = 2000
de = 0.1
gap_energy = 0.1805
numsubgap = 0
subgap_energy = 0.0
total_energy = 0.0
line_data = []
phononids = []
setids = []
phononEnergies = []
phononTimes = []
phononid = 0
phononEnergy = 0.0
phononTime = 0.0
largest_energy = 0.0
largest_time = 0.0
yspace = 20
xspace = 100 / dt

phononData = {}
energyDist = []

xlabel = []
ylabel = []

numLines = 0


print("Collecting data . . . ")
directory = "Data/"
path = directory + "StepData.txt"
f = open(path, "r")
lines = f.readlines()
f.close()

print("Computing . . . ")
#Add energies for each event
for i in range(0, len(lines)):
    line = lines[i]
    if(line == "New Event\n"):
        break
    
    numLines += 1
    line_data = line[:-1].split(",")
    phononid = int(line_data[0])
    phononEnergy = float(line_data[1])
    phononTime = float(line_data[2])
    if(line_data[3][0] != "p"):
        continue
    phononids.append(phononid)
    phononEnergies.append(phononEnergy)
    phononTimes.append(phononTime)
    if(phononEnergy > largest_energy):
        largest_energy = phononEnergy
    total_energy += phononEnergy
    if(phononEnergy < 2 * gap_energy):
        numsubgap += 1
        subgap_energy += phononEnergy
    if(phononTime > largest_time):
        largest_time = phononTime

xlen = int(largest_time / dt)
# xlen = 1000
ylen = int(largest_energy / de)
setids = list(set(phononids))
setids.sort()
for i in range(len(setids)):
    phononData[setids[i]] = [[],[]]

for i in range(len(phononids)):
    phononData[phononids[i]][0].append(phononEnergies[i])
    phononData[phononids[i]][1].append(phononTimes[i])

for i in range(xlen + 1):
    energyDist.append([])
    for j in range(ylen + 1):
        energyDist[i].append(0)

#iterate through all phonons
timea = 0.0
timeb = 0.0
timeaint = 0
timebint = 0
cur_energy = 0.0
energyind = 0
timeind = 0
pdata = []
lenp = 0

# iterate through IDs to see what time interval and energy interval the step belongs in
print("Still Computing . . . ")
idcounter = 0
for ID in phononData:
    idcounter += 1
    if(idcounter % 1000 == 0):
        print(idcounter)
    pdata = phononData[ID]
    lenp = len(pdata[1])
    # iterates throug all steps for each phonon
    # finds the slices of time and the energy that the phonon had at those times and
    #   increases the counter for that grid location
    for i in range(lenp - 1):
        timea = pdata[1][i]
        timeb = pdata[1][i + 1]
        timeaint = floor(timea / dt) * dt
        timebint = floor(timeb / dt) * dt
        cur_energy = pdata[0][i]
        energyind = ylen - int(cur_energy / de)
        # if(timeaint == 0):
        #     energyDist[0][energyind] += 1
        #     # energyDist[0][energyind] += cur_energy
        if(timeaint == timebint):
            continue
        for j in range(timeaint, timebint, dt):
            timeind = int(float(j) / dt)
            energyDist[timeind][energyind] += 1
            # if(timeind < xlen):
            #     energyDist[timeind][energyind] += 1
                # energyDist[timeind][energyind] += cur_energy

# tot_init_energy = 0.0
# for i in range(len(energyDist[0])):
#     tot_init_energy += energyDist[400][i]

tot_init_energy = energyDist[1][0]

# print("Total Initial Energy: " + str(0.001 * tot_init_energy))

print("Plotting . . . ")
print("Proportion of subgap phonons: " + str(float(numsubgap) / numLines))
print("Total Subgap Energy: " + str(subgap_energy) + ", Total Energy: " + str(total_energy))
print("Subgap Energy Fraction: " + str(float(subgap_energy) / total_energy))

rotatedDist = []
for i in range(len(energyDist[0])):
    rotatedDist.append([])
    for j in range(len(energyDist)):
        rotatedDist[i].append(0.0)
        energyDist[j][i] += 1
        rotatedDist[i][j] = log(energyDist[j][i], 10)

ax = sns.heatmap(np.array(rotatedDist), linewidth=0)
ax.set_title(r"Phonon Energy Distribution (logorithmic count) vs Time")
ax.set_xlabel("Time (us)")
ax.set_ylabel("Energy (meV)")

# ax.set_xticks(np.arange(0, xlen, xspace))
ax.set_yticks(np.arange(0, ylen, yspace))

for i in range(ceil(xlen / xspace)):
    xlabel.append(float(xspace * i))
    xlabel[i] *= dt

for i in range(ceil(ylen / yspace)):
    ylabel.append(float(yspace * (ceil(ylen / yspace) - i)))
    ylabel[i] *= de

# ax.set_xticklabels(xlabel)
ax.set_yticklabels(ylabel)
plt.show()
