from math import *
import numpy as np
import seaborn as sns
import random
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D

max_time = 5000000
dt = 2000
gap_energy = 0.1805
ngap = 1.395
line_data = []
partids = []
setids = []
partEnergies = []
partTimes = []
partDefs = []
partDeposits = []
partVols = []
partParents = []

partTotal = []
subpTotal = []
subniobTotal = []
superpTotal = []

partid = 0
partEnergy = 0.0
partTime = 0.0
partDef = ""
partDeposit = 0.0
partVol = ""
partParent = 0
largest_time = 0.0
yspace = 10
xspace = 20
partData = {}
xdata = []

indEnergy = []
capEnergy = []
feedEnergy = []
substrate = []
other = []
otherTotal = []

Total = []

def GetPartGroup(energy):
    if(energy  > 2 * ngap):
        return 0
    elif(energy > 2 * gap_energy):
        return 1
    else:
        return 2

print("Collecting data . . . ")
directory = "Data/"
path = directory + "StepData.txt"
f = open(path, "r")
steplines = f.readlines()
f.close()

print("Reading Data . . . ")
#Add energies for each event
#For particle energies
for i in range(0, len(steplines)):
    line = steplines[i]
    if(line == "New Event\n"):
        break

    line_data = line[:-1].split(",")
    partid = int(line_data[0])
    partEnergy = float(line_data[1])
    partTime = float(line_data[2])
    partDef = line_data[3]
    partDeposit = float(line_data[4])
    partVol = line_data[5]
    partParent = 0
    if(len(line_data) > 6):
        partParent = int(line_data[6])

    partids.append(partid)
    partEnergies.append(partEnergy)
    partTimes.append(partTime)
    partDefs.append(partDef)
    partDeposits.append(partDeposit)
    partVols.append(partVol)
    partParents.append(partParent)

    if(partTime > largest_time):
        largest_time = partTime

# xlen = int(largest_time / dt)
xlen = min(int(largest_time / dt), int(max_time / dt) - 1)
# xlen = 1000
setids = list(set(partids))
setids.sort()
for i in range(len(setids)):
    partData[setids[i]] = [[],[],[]]

for i in range(len(partids)):
    partid = partids[i]
    partData[partid][0].append(partEnergies[i])
    partData[partid][1].append(partTimes[i])
    partData[partid][2].append(partDefs[i])

#get parent ids for all particles
for i in range(len(partParents)):
    partParent = partParents[i]
    partid = partids[i]
    partData[partid].append(partParent)

for i in range(3):
    partTotal.append([])
    subniobTotal.append([])
    subpTotal.append([])
    superpTotal.append([])
    otherTotal.append([])
    xdata.append([])
    for j in range(xlen + 1):
        partTotal[i].append(0)
        subniobTotal[i].append(0)
        subpTotal[i].append(0)
        superpTotal[i].append(0)
        otherTotal[i].append(0)
        xdata[i].append(0.001 * j * dt)

#for energy deposits
for i in range(3):
    indEnergy.append([])
    capEnergy.append([])
    feedEnergy.append([])
    substrate.append([])
    other.append([])
    for j in range(xlen + 1):
        indEnergy[i].append(0)
        capEnergy[i].append(0)
        feedEnergy[i].append(0)
        substrate[i].append(0)
        other[i].append(0)

group = 0
for i in range(len(partDeposits)):
    partDeposit = partDeposits[i]
    partid = partids[i]
    partDef = partDefs[i]
    particle = partData[partid]
    time = partTimes[i]
    timeind = int(float(time) / dt)
    partEnergy = particle[0][len(particle[0]) - 2]
    group = GetPartGroup(partEnergy)
    if(timeind > xlen):
        continue
    if(partDef[0] != "p"):
        continue
    partVol = partVols[i]
    # if(group == 1 and partDeposit != 0):
    #     print(partDeposit)
    if(partVol[0] == "k"):
        if(partVol[4] == "i"):
            indEnergy[group][timeind] += partDeposit
        elif(partVol[4] == "c"):
            capEnergy[group][timeind] += partDeposit
        else:
            other[group][timeind] += partDeposit
            # print("Unrecognized Volume")
    elif(partVol[0] == "f"):
        feedEnergy[group][timeind] += partDeposit
    elif(partVol[0] == "W"):
        substrate[group][timeind] += partDeposit
    elif(partVol[0] != "T"):
        other[group][timeind] += partDeposit
        # print("Unrecognized Volume")

parent_group = 0
parent_particle = []
particle = []
for ID in partData:
    particle = partData[ID]
    partParent = particle[3]
    if(partParent != 0):
        partEnergy = particle[0][0]
        partTime = particle[1][0]
        partDef = particle[2][0]
        timeind = int(float(partTime) / dt)
        if(partDef[0] == "p"):
            group = GetPartGroup(partEnergy)
            parent_particle = partData[partParent]
            parent_group = GetPartGroup(parent_particle[0][0])
            if(parent_group != group):
                if(group == 0):
                    superpTotal[parent_group][timeind] += partEnergy
                elif(group == 1):
                    subniobTotal[parent_group][timeind] += partEnergy
                else:
                    subpTotal[parent_group][timeind] += partEnergy

cdf = True
if(cdf):
    for i in range(3):
        totind = 0.0
        totcap = 0.0
        totfeed = 0.0
        totsubstrate = 0.0
        totsuper = 0.0
        totsubniob = 0.0
        totsub = 0.0
        totother = 0.0
        Total.append([])
        for j in range(xlen + 1):
            totind += indEnergy[i][j]
            totcap += capEnergy[i][j]
            totfeed += feedEnergy[i][j]
            totsubstrate += substrate[i][j]
            totsuper += superpTotal[i][j]
            totsubniob += subniobTotal[i][j]
            totsub += subpTotal[i][j]
            totother += other[i][j]
            indEnergy[i][j] = totind
            capEnergy[i][j] = totcap
            feedEnergy[i][j] = totfeed
            substrate[i][j] = totsubstrate
            superpTotal[i][j] = totsuper
            subniobTotal[i][j] = totsubniob
            subpTotal[i][j] = totsub
            otherTotal[i][j] = totother

for i in range(3):
    Total.append([])

    for j in range(xlen + 1):
        partTotal[i][j] += subpTotal[i][j]
        partTotal[i][j] += subniobTotal[i][j]
        partTotal[i][j] += superpTotal[i][j]

    for j in range(xlen + 1):
        Total[i].append(0)
        Total[i][j] += partTotal[i][j]

        Total[i][j] += indEnergy[i][j]
        Total[i][j] += capEnergy[i][j]
        Total[i][j] += feedEnergy[i][j]
        Total[i][j] += substrate[i][j]
        Total[i][j] += otherTotal[i][j]

fig, axs = plt.subplots(3)
fig.canvas.set_window_title('Differential Energy Transfer vs Time (logorithmic)')

axs[0].set_title(r"Super Nb Gap Energy Transfer vs Time")
axs[1].set_title(r"Super Al Gap Energy Transfer vs Time")
axs[2].set_title(r"Subgap Energy Transfer vs Time")


for i in range(3):
    axs[i].set_xlabel("Time (μs)")
    axs[i].set_ylabel("Energy (meV)")

    axs[i].plot(xdata[i], Total[i], label="Total Energy")

    axs[i].plot(xdata[i], partTotal[i], label="Total Particle Energy")
    axs[i].plot(xdata[i], subpTotal[i], label="Subgap(Al) Energy")
    axs[i].plot(xdata[i], subniobTotal[i], label="Supergap(Al) to Subgap(Nb) Energy")
    axs[i].plot(xdata[i], superpTotal[i], label="Supergap(Nb) Energy")

    axs[i].plot(xdata[i], substrate[i], label="Substrate Energy Deposit")
    axs[i].plot(xdata[i], otherTotal[i], label="Other Energy Deposit")


    leg = axs[i].legend(loc='upper right', shadow=True, fancybox=True)
    leg.get_frame().set_alpha(1.0)


plt.show()

fig, axs = plt.subplots(3)
fig.canvas.set_window_title('Total Energy Transfer')
axs[0].set_title(r"Super Nb Gap Total Energy Transferred")
axs[1].set_title(r"Super Al Gap Total Energy Transferred")
axs[2].set_title(r"Subgap Total Energy Transferred")
for i in range(3):
    labels = ["Substrate Energy Depsosit", "Subgap(Al) Energy", "Subgap(Nb) energy",
              "Supergap(Nb) energy", "Other Energy Deposit", "Total"]
    sizes = []
    sizes.append(substrate[i][len(substrate[i]) - 1])
    sizes.append(subpTotal[i][len(subpTotal[i]) - 1])
    sizes.append(subniobTotal[i][len(subniobTotal[i]) - 1])
    sizes.append(superpTotal[i][len(superpTotal[i]) - 1])
    sizes.append(otherTotal[i][len(otherTotal[i]) - 1])
    sizes.append(Total[i][len(Total[i]) - 1])

    axs[i].bar(labels, sizes)
    axs[i].set_ylabel("Energy (meV)")

plt.show()