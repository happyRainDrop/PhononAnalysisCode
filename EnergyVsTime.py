from math import *
from matplotlib import lines
import numpy as np
from numpy.core import numeric
import seaborn as sns
import random as rand
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors

# makes several plots of the total energy vs time, qp energy in the inductors/capacitors/feedline,
# and the flux in and out of the inds, caps, and feedline.

numcols = 0
kid_ids = []
#current = 0 or prototype = 1?
detector = 0
#counts = 0 or energy = 1?
fluxmode = 1

kidPlotConfig = []

if(detector == 0):
    #layout of kid_ids
    kid_ids = [0, 0,  1,  2,  3,  4,  5,  6,  0,  0,
              0,  0,  7,  8,  9,  10, 11, 12, 0,  0,
              0,  0,  13, 14, 15, 16, 17, 18, 0,  0,
              0,  0,  19, 20, 21, 22, 23, 24, 0,  0,
              25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
              35, 36, 37, 38, 39, 40, 41, 42, 43, 44,
              45, 46, 47, 48, 49, 50, 51, 52, 53, 54,
              55, 56, 57, 58, 59, 60, 61, 62, 63, 64,
              0,  65, 66, 67, 68, 69, 70, 71, 72, 0, 
              0,  0,  0,  73, 74, 75, 76, 0,  0,  0,
              0,  0,  0,  77, 78, 79, 80, 0,  0,  0]
    numcols = 10
    num_kids = 80
    kidPlotConfig = [0.03, 0.04, 0.97, 0.96, 0.25, 0.35]
else:
    kid_ids = [16, 0,  9,  0, 
               0,  20, 0,  5, 
               4,  0,  2,  0, 
               0,  11, 0,  15,
               14, 0,  19, 0, 
               0,  6,  0,  7, 
               1,  0,  13, 0, 
               0,  18, 0, 17,
               8,  0,  3,  0, 
               0,  12, 0,  10]
    numcols = 4
    num_kids = 20
    kidPlotConfig = [0.03, 0.04, 0.97, 0.96, 0.1, 0.0]
    # kid_ids = [16, 9, 
    #            20, 5, 
    #            4,  2, 
    #            11, 15,
    #            14, 19,
    #            6,  7, 
    #            1,  13,
    #            18, 17,
    #            8,  3, 
    #            12, 10]
    # kid_ids = [16, 20, 9, 5,
    #            4, 11, 2, 15,
    #            14, 6, 19, 7,
    #            1, 18, 13, 17,
    #            8, 12, 3, 10]
    # numcols = 2

numrows = ceil(len(kid_ids) / float(numcols))

#will not analyze particles after this time
max_time = 1000000
#width of each step of time (ns)
dt = 10
#step time for flux (ns)
fluxdt = 1000
#gap energy for inds
# gap_energy = 0.1805 - 0.0001
gap_energy = 0.1805
# gap_energy = 0.2
# gap_energy = 0.1
# gap_energy = 0.34743
#nionium gap
ngap = 1.395
#qp lifetime for inds
qplife = 438
#edge of graphs for qp energy and flux vs time for inds and caps
max_graph_time = 150
#number of energy bands to seperate the flux into
numFluxBands = 3
#for random colors in flux plots
rSeed = 1394057
#how much darker should outflux's line color be than influx in plots?
darkFactor = 0.75
#primary photon energy
primaryEnergy = 15000
#where is the data?
directory = "Data/"
# directory = "Data/0.008/"
absProb = 0.1
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
maxPhononEnergy = []    # Max energy of any given phonon/time
subpTotal = []          
subniobTotal = []
superpTotal = []

part = []
subp = []
subniob = []
superp = []

# part = np.array([])
# subp = np.array([])
# subniob = np.array([])
# superp = np.array([])

partid = 0
partEnergy = 0.0
partTime = 0.0
partDef = ""
partDeposit = 0.0
partVol = ""
largest_time = 0.0
yspace = 10
xspace = 20
partData = []
xdata = []
fluxdata = []
electrodeData = []
num_events = 0
vol = ""

indEnergy = []
capEnergy = []
feedEnergy = []
substrate = []
mountDeposit = []

qpData = []
qpInd = np.array([])
qpCap = np.array([])
qpIndTotal = np.array([])
qpCapTotal = np.array([])
qpfeed = np.array([])
qpMark = np.array([])
qpEnergy = np.array([])

qpEnergyGain = np.array([])

numqpIndTotal = np.array([])
numqpCapTotal = np.array([])
numqpfeed = np.array([])
numqp = np.array([])

primaryInd = -1
primaryCap = -1
indmax = 0
capmax = 0
highestind = 0
highestcap = 0

totind = 0.0
totcap = 0.0
totfeed = 0.0
totsubstrate = 0.0

event_id = 0
qpcount = 0
qpE = 0.0
qpt = 0.0
deltaGain = 0

influxInd = []
influxCap = []
influxIndTotal = []
influxCapTotal = []
influxfeed = []
outfluxInd = []
outfluxCap = []
outfluxIndTotal = []
outfluxCapTotal = []
outfluxfeed = []

timea = 0.0
timeb = 0.0
timeaint = 0
timebint = 0
cur_energy = 0.0
energyind = 0
timeind = 0
pdata = []
qdata = []
lenp = 0

ind = []
cap = []
feed = []
sub = []
mount = []

Total = []
endTotal = []

xaxis = []

partids.append([])
partEnergies.append([])
partTimes.append([])
partDefs.append([])
partDeposits.append([])
partVols.append([])
partParents.append([])

print("Reading Data . . . ")
# path = directory + "StepData2" + str(absProb) + ".txt"
path = directory + "StepData.txt"
with open(path) as f:
    for line in f:
        if(line == "New Event\n"):
            num_events += 1
            partids.append([])
            partEnergies.append([])
            partTimes.append([])
            partDefs.append([])
            partDeposits.append([])
            partVols.append([])
            partParents.append([])
            endTotal.append(0)
            electrodeData.append([])
            continue
        line_data = line[:-1].split(",")
        partid = int(line_data[0])
        partEnergy = float(line_data[1])
        partTime = float(line_data[2])
        partDef = line_data[3]
        partDeposit = float(line_data[4])
        partVol = line_data[5]
        partids[num_events].append(partid)
        partEnergies[num_events].append(partEnergy)
        partTimes[num_events].append(partTime)
        partDefs[num_events].append(partDef)
        partDeposits[num_events].append(partDeposit)
        partVols[num_events].append(partVol)
        if(len(line_data) > 6):
            partParents[num_events].append(int(line_data[6]))
        else:
            partParents[num_events].append(0)
        if(partTime > largest_time):
            largest_time = partTime

#get QP data
# path = directory + "ElectrodeData2" + str(absProb) + ".txt"
path = directory + "ElectrodeData.txt"
with open(path) as f:
    for line in f:
        if(line == "New Event\n"):
            qpcount = 0
            event_id += 1
            continue
        line_data = line[:-1].split("|")
        line_data0 = line_data[0].split(",")
        electrodeData[event_id].append([])
        electrodeData[event_id][qpcount].append([])
        electrodeData[event_id][qpcount][0].append(float(line_data0[0]))
        electrodeData[event_id][qpcount][0].append(line_data0[1])
        qp_line_data = line_data[1][:-1].split(",")
        electrodeData[event_id][qpcount].append([])
        electrodeData[event_id][qpcount][1].append([])
        electrodeData[event_id][qpcount][1].append([])
        electrodeData[event_id][qpcount][1].append([])
        for j in range(int(len(qp_line_data) / 3)):
            qpId = int(qp_line_data[3 * j + 0])
            qpE = float(qp_line_data[3 * j + 1])
            qpt = float(qp_line_data[3 * j + 2])
            electrodeData[event_id][qpcount][1][0].append(qpId)
            electrodeData[event_id][qpcount][1][1].append(qpE)
            electrodeData[event_id][qpcount][1][2].append(qpt)
        lineGainData = line_data[2][:-1].split(",")
        electrodeData[event_id][qpcount].append([])
        for j in range(int(len(lineGainData) / 2)):
            qpt = float(lineGainData[2 * j + 0])
            deltaGain = int(lineGainData[2 * j + 1])
            electrodeData[event_id][qpcount][2].append(qpt)
            electrodeData[event_id][qpcount][2].append(deltaGain)
        qpcount += 1

# xlen = int(largest_time / dt). It's the number of time bins we have
xlen = min(int(largest_time / dt), int(max_time / dt) - 1)
fluxlen = min(int(largest_time / fluxdt), int(max_time / fluxdt) - 1)
# xlen = 1000

print("Organizing QP Data . . . ")
#organize info about each qp
setids = []
for i in range(num_events):
    qpData.append([])
    # print(i)
    for j in range(len(electrodeData[i])):
        qpData[i].append([])
        qpData[i][j].append(electrodeData[i][j][0])
        qpData[i][j].append({})
        setids = list(set(electrodeData[i][j][1][0]))
        # setids.sort()
        for k in range(len(setids)):
            qpData[i][j][1][setids[k]] = [[], []]

for i in range(num_events):
    for j in range(len(electrodeData[i])):
        # print(partEnergies[i][j])
        qpData[i][j].append(electrodeData[i][j][0])
        qpData[i][j].append(electrodeData[i][j][1])
        for k in range(int(len(electrodeData[i][j][1][0]))):
            qpId = electrodeData[i][j][1][0][k]
            qpE = electrodeData[i][j][1][1][k]
            qpt = electrodeData[i][j][1][2][k]
            qpData[i][j][1][qpId][0].append(qpE)
            qpData[i][j][1][qpId][1].append(qpt)

print("Organizing Particle Data . . . ")
#organize info about each phonon
setids = []
for i in range(num_events):
    partData.append({})
    setids = list(set(partids[i]))
    setids.sort()
    for j in range(len(setids)):
        partData[i][setids[j]] = [[], [], [], [], []]

for i in range(num_events):
    for j in range(len(partids[i])):
        # print(partEnergies[i][j])
        partData[i][partids[i][j]][0].append(partEnergies[i][j])
        partData[i][partids[i][j]][1].append(partTimes[i][j])
        partData[i][partids[i][j]][2].append(partDefs[i][j])
        partData[i][partids[i][j]][3].append(partVols[i][j])
        partData[i][partids[i][j]][4].append(partDeposits[i][j])

for i in range(num_kids):
    influxInd.append([])
    influxCap.append([])
    outfluxInd.append([])
    outfluxCap.append([])
    for j in range(numFluxBands + 1):
        influxInd[i].append([])
        influxCap[i].append([])
        outfluxInd[i].append([])
        outfluxCap[i].append([])
        for k in range(fluxlen + 1):
            influxInd[i][j].append(0)
            influxCap[i][j].append(0)
            outfluxInd[i][j].append(0)
            outfluxCap[i][j].append(0)
for i in range(numFluxBands + 1):
    influxIndTotal.append([])
    influxCapTotal.append([])
    influxfeed.append([])
    outfluxIndTotal.append([])
    outfluxCapTotal.append([])
    outfluxfeed.append([])
    for j in range(fluxlen + 1):
        influxIndTotal[i].append(0)
        influxCapTotal[i].append(0)
        influxfeed[i].append(0)
        outfluxIndTotal[i].append(0)
        outfluxCapTotal[i].append(0)
        outfluxfeed[i].append(0)

fluxBandId = 0
#calculate flux of phonons in and out of the KIDs and feedline
for i in range(num_events):
    print("Analyzing Event " + str(i + 1) + " Flux . . .")
    for j in range(len(partids[i])):
        vol = partVols[i][j]
        time = partTimes[i][j]
        if(time >= max_time):
            continue
        timeind = int(time / fluxdt)
        partEnergy = partEnergies[i][j]
        partDef = partDefs[i][j]
        partid = partids[i][j]
        if(partDef[0] != "p"):
            continue
        if(partEnergy >= 2 * ngap):
            fluxBandId = 2
        elif(partEnergy >= 2 * gap_energy):
            fluxBandId = 1
        else:
            fluxBandId = 0
        if(fluxmode == 0):
            partEnergy = 1
        if(partParents[i][j] != 0):
            parentid = partParents[i][j]
            parentvol = partData[i][parentid][3][len(partData[i][parentid][3]) - 1]
            partDef = partData[i][parentid][2][0]
            if(partDef[0] != "p"):
                continue
            if(parentvol[0] == "k"):
                kid_id=int(parentvol[7:len(parentvol)])
                if(parentvol[4] == "i"):
                    outfluxInd[kid_id][fluxBandId][timeind] += partEnergy
                    outfluxIndTotal[fluxBandId][timeind] += partEnergy
                    outfluxInd[kid_id][numFluxBands][timeind] += partEnergy
                    outfluxIndTotal[numFluxBands][timeind] += partEnergy
                elif(parentvol[4] == "c"):
                    outfluxCap[kid_id][fluxBandId][timeind] += partEnergy
                    outfluxCapTotal[fluxBandId][timeind] += partEnergy
                    outfluxCap[kid_id][numFluxBands][timeind] += partEnergy
                    outfluxCapTotal[numFluxBands][timeind] += partEnergy
                else:
                    print("Unrecognized Volume")
            elif(parentvol[0] == "f"):
                outfluxfeed[fluxBandId][timeind] += partEnergy
                outfluxfeed[numFluxBands][timeind] += partEnergy
        else:
            partEnergy = partData[i][partid][0][len(partData[i][partid][0]) - 2]
            if(partEnergy  >= 2 * ngap):
                fluxBandId = 2
            elif(partEnergy >= 2 * gap_energy):
                fluxBandId = 1
            else:
                fluxBandId = 0
            if(partEnergies[i][j] != 0.0):
                continue
            if(vol[0] == "k"):
                kid_id=int(vol[7:len(vol)])
                if(vol[4] == "i"):
                    influxInd[kid_id][fluxBandId][timeind] += partEnergy
                    influxIndTotal[fluxBandId][timeind] += partEnergy
                    influxInd[kid_id][numFluxBands][timeind] += partEnergy
                    influxIndTotal[numFluxBands][timeind] += partEnergy
                elif(vol[4] == "c"):
                    influxCap[kid_id][fluxBandId][timeind] += partEnergy
                    influxCapTotal[fluxBandId][timeind] += partEnergy
                    influxCap[kid_id][numFluxBands][timeind] += partEnergy
                    influxCapTotal[numFluxBands][timeind] += partEnergy
                else:
                    print("Unrecognized Volume")
            elif(vol[0] == "f"):
                influxfeed[fluxBandId][timeind] += partEnergy
                influxfeed[numFluxBands][timeind] += partEnergy


for i in range(num_kids):
    for j in range(numFluxBands + 1):
        for k in range(fluxlen + 1):
            influxInd[i][j][k] /= float(num_events)
            influxCap[i][j][k] /= float(num_events)
            outfluxInd[i][j][k] /= float(num_events)
            outfluxCap[i][j][k] /= float(num_events)

highest_flux = 0
for i in range(numFluxBands + 1):
    for j in range(fluxlen + 1):
        influxIndTotal[i][j] /= float(num_events)
        influxCapTotal[i][j] /= float(num_events)
        influxfeed[i][j] /= float(num_events)
        outfluxIndTotal[i][j] /= float(num_events)
        outfluxCapTotal[i][j] /= float(num_events)
        outfluxfeed[i][j] /= float(num_events)

for i in range(fluxlen + 1):
    if(influxIndTotal[numFluxBands][i] > highest_flux):
        highest_flux = influxIndTotal[numFluxBands][i]
    if(influxCapTotal[numFluxBands][i] > highest_flux):
        highest_flux = influxCapTotal[numFluxBands][i]
    if(influxfeed[numFluxBands][i] > highest_flux):
        highest_flux = influxfeed[numFluxBands][i]
    if(outfluxIndTotal[numFluxBands][i] > highest_flux):
        highest_flux = outfluxIndTotal[numFluxBands][i]
    if(outfluxCapTotal[numFluxBands][i] > highest_flux):
        highest_flux = outfluxCapTotal[numFluxBands][i]
    if(outfluxfeed[numFluxBands][i] > highest_flux):
        highest_flux = outfluxfeed[numFluxBands][i]

for i in range(fluxlen + 1):
    fluxdata.append(0.001 * i * fluxdt)

for i in range(xlen + 1):
    partTotal.append(0)
    maxPhononEnergy.append(0)
    subniobTotal.append(0)
    subpTotal.append(0)
    superpTotal.append(0)
    xdata.append(0.001 * i * dt)


#analyze qps
qpInd = np.zeros((num_kids,xlen + 1))
qpCap = np.zeros((num_kids,xlen + 1))

numqpInd = np.zeros((num_kids,xlen + 1))
numqpCap = np.zeros((num_kids,xlen + 1))

qpIndTotal = np.zeros(xlen + 1)
qpCapTotal = np.zeros(xlen + 1)
qpfeed = np.zeros(xlen + 1)
qpMark = np.zeros(xlen + 1)
qpEnergy = np.zeros(xlen + 1)
numqpIndTotal = np.zeros(xlen + 1)
numqpCapTotal = np.zeros(xlen + 1)
numqpfeed = np.zeros(xlen + 1)
numqp = np.zeros(xlen + 1)


# for i in range(xlen + 1):
#     qpIndTotal = np.append(qpIndTotal, [0])
#     qpCapTotal = np.append(qpCapTotal, [0])
#     qpfeed = np.append(qpfeed, [0])
#     qpEnergy = np.append(qpEnergy, [0])

#     numqpIndTotal = np.append(numqpIndTotal, [0])
#     numqpCapTotal = np.append(numqpCapTotal, [0])
#     numqpfeed = np.append(numqpfeed, [0])
#     numqp = np.append(numqp, [0])


# for i in range(num_events):
#     print("Analyzing Event " + str(i + 1) + " Particles . . .")
#     for j in range(len(qpData[i])):
#         time = qpData[i][j][0][0]
#         vol = qpData[i][j][0][1]
#         for ID in qpData[i][j][1]:
#             print(ID)
#             # print(qpData[i][j][1][1])
#             print(qpData[i][j][1][ID])


for i in range(num_events):
    print("Analyzing Event " + str(i + 1) + " QPs . . .")
    for j in range(len(qpData[i])):
        time = qpData[i][j][0][0]
        vol = qpData[i][j][0][1]
        for ID in qpData[i][j][1]:
            qdata = qpData[i][j][1][ID]
            lenp = len(qdata[1])
            # iterates throug all steps for each qp
            # finds the slices of time and the energy that the qp had at those times and
            #   increases the energy for that grid location by the energy of the qp
            for k in range(lenp - 1):
                timea = qdata[1][k] + time
                timeb = qdata[1][k + 1] + time
                timeaint = floor(timea / dt)
                timebint = floor(timeb / dt)
                qpE = qdata[0][k]
                if(timeaint == timebint):
                    continue                
                timebint = min(timebint, (xlen + 1))
                if(vol[0] == "k"):
                    kid_id=int(vol[7:len(vol)])
                    if(vol[4] == "i"):
                        qpInd[kid_id][timeaint:timebint] += qpE
                        qpIndTotal[timeaint:timebint] += qpE
                        numqpIndTotal[timeaint:timebint] += 1
                        numqpInd[kid_id][timeaint:timebint] += 1
                    elif(vol[4] == "c"):
                        qpCap[kid_id][timeaint:timebint] += qpE
                        qpCapTotal[timeaint:timebint] += qpE
                        numqpCap[kid_id][timeaint:timebint] += 1
                    else:
                            print("Unrecognized Volume")
                elif(vol[0] == "f"):
                    qpfeed[timeaint:timebint] += qpE
                    numqpfeed[timeaint:timebint] += 1
                elif(vol[0] == "m"):
                    qpMark[timeaint:timebint] += qpE
                else:
                    print("Unrecognized Volume")
                qpEnergy[timeaint:timebint] += qpE
                numqp[timeaint:timebint] += 1
    endTotal[i] += qpEnergy[xlen]


# account for energy losses / gains in film
qpEnergyGain = np.zeros(xlen + 1)
for i in range(num_events):
    for j in range(len(electrodeData[i])):
        for k in range(int(len(electrodeData[i][j][2]) / 2)):
            time = electrodeData[i][j][2][2 * k + 0] + electrodeData[i][j][0][0]
            deltaGain = electrodeData[i][j][2][2 * k + 1]
            timeind = floor(time / dt)
            timeind = min(timeind, xlen)
            qpEnergyGain[timeind] += deltaGain
qpEnergyGain = np.cumsum(qpEnergyGain) * gap_energy
qpEnergyGain /= float(num_events)

# iterate through IDs to see what time interval and energy interval the step belongs in
for i in range(num_events):
    part = np.array([])
    maxPart = np.array([])  # The maximum phonon energy
    subp = np.array([])
    subniob = np.array([])
    superp = np.array([])

    print("Analyzing Event " + str(i + 1) + " Particles . . .")
    for j in range(xlen + 1):
        part = np.append(part, [0])
        maxPart = np.append(part, [0])
        subniob = np.append(subniob, [0])
        subp = np.append(subp, [0])
        superp = np.append(superp, [0])
    for ID in partData[i]:
        pdata = partData[i][ID]
        lenp = len(pdata[1])
        # iterates throug all steps for each phonon
        # finds the slices of time and the energy that the phonon had at those times and
        #   increases the counter for that grid location
        for j in range(lenp - 1):
            timea = pdata[1][j]
            timeb = pdata[1][j + 1]
            timeaint = floor(timea / dt)
            timebint = floor(timeb / dt)
            cur_energy = pdata[0][j]
            partDef = pdata[2][j]
            if(timeaint == timebint):
                continue
            
            timebint = min(timebint, (xlen + 1))
            part[timeaint:timebint] += cur_energy

            maxPart[timeaint:timebint] = max(max(maxPart[timeaint:timebint]), cur_energy)

            if(cur_energy  >= 2 * ngap):
                superp[timeaint:timebint] += cur_energy
            elif(cur_energy >= 2 * gap_energy):
                subniob[timeaint:timebint] += cur_energy
            else:
                subp[timeaint:timebint] += cur_energy
    
    endTotal[i] += part[xlen]
    for j in range(xlen + 1):
        partTotal[j] += part[j]         #The total phonon energy = 
        superpTotal[j] += superp[j]     #supergap niobium +
        subniobTotal[j] += subniob[j]   #Supergap(aluminum) to Subgap(niobium) Energy +
        subpTotal[j] += subp[j]         #Subgap (aluminum) energy

        maxPhononEnergy[j] += maxPart[j]


#for energy deposits
for i in range(xlen + 1):
    indEnergy.append(0)
    capEnergy.append(0)
    feedEnergy.append(0)
    substrate.append(0)
    mountDeposit.append(0)

for i in range(num_events):
    ind = []
    cap = []
    feed = []
    sub = []
    mount = []
    for j in range(xlen + 1):
        ind.append(0)
        cap.append(0)
        feed.append(0)
        sub.append(0)
        mount.append(0)
    for j in range(len(partDeposits[i])):
        partDeposit = partDeposits[i][j]
        time = partTimes[i][j]
        timeind = int(float(time) / dt)
        if(timeind > xlen):
            continue
        partVol = partVols[i][j]
        if(partVol[0] == "k"):
            if(partVol[4] == "i"):
                ind[timeind] += partDeposit
            elif(partVol[4] == "c"):
                cap[timeind] += partDeposit
            else:
                print("Unrecognized Volume")
        elif(partVol[0] == "f"):
            feed[timeind] += partDeposit
        elif(partVol[0] == "W"):
            sub[timeind] += partDeposit
        elif(partVol[0] == "m"):
            mount[timeind] += partDeposit
        elif(partVol[0] != "T"):
            print("Unrecognized Volume")

    totind = 0.0
    totcap = 0.0
    totfeed = 0.0
    totsubstrate = 0.0
    totmount = 0.0
    for j in range(xlen + 1):
        totind += ind[j]
        totcap += cap[j]
        totfeed += feed[j]
        totsubstrate += sub[j]
        totmount += mount[j]
        ind[j] = totind
        cap[j] = totcap
        feed[j] = totfeed
        sub[j] = totsubstrate
        mount[j] = totmount
    
    endTotal[i] += ind[xlen]
    endTotal[i] += cap[xlen]
    endTotal[i] += feed[xlen]
    endTotal[i] += sub[xlen]
    endTotal[i] += mount[xlen]
    
    for j in range(xlen + 1):
        indEnergy[j] += ind[j]
        capEnergy[j] += cap[j]
        feedEnergy[j] += feed[j]
        substrate[j] += sub[j]
        mountDeposit[j] += mount[j]

for i in range(num_events):
    print("\nEvent " + str(i + 1) + " Final Total Energy: " + str(endTotal[i])[0:9], end="")
    if(endTotal[i] > 15000):
        print("    *Does not conserve energy", end="")

print()

for i in range(xlen + 1):
    indEnergy[i] /= float(num_events)
    capEnergy[i] /= float(num_events)
    feedEnergy[i] /= float(num_events)
    substrate[i] /= float(num_events)

    mountDeposit[i] /= float(num_events)

    subpTotal[i] /= float(num_events)
    subniobTotal[i] /= float(num_events)
    superpTotal[i] /= float(num_events)
    partTotal[i] /= float(num_events)
    maxPhononEnergy[i] /= float(num_events)

    qpEnergy[i] /= float(num_events)
    qpIndTotal[i] /= float(num_events)
    qpCapTotal[i] /= float(num_events)
    qpfeed[i] /= float(num_events)

    numqp[i] /= float(num_events)
    numqpIndTotal[i] /= float(num_events)
    numqpCapTotal[i] /= float(num_events)
    numqpfeed[i] /= float(num_events)

for i in range(num_kids):
    for j in range(xlen + 1):
        qpInd[i][j] /= float(num_events)
        qpCap[i][j] /= float(num_events)

for i in range(xlen + 1):
    Total.append(0)
    Total[i] += partTotal[i]

    # Total[i] -= indEnergy[i]
    # Total[i] -= capEnergy[i]
    # Total[i] -= feedEnergy[i]
    Total[i] += substrate[i]

    Total[i] += mountDeposit[i]

    Total[i] += qpEnergy[i]

    Total[i] -= qpEnergyGain[i]

for i in range(num_kids):
    indmax = 0
    capmax = 0
    for j in range(xlen + 1):
        if(qpInd[i][j] > indmax):
            indmax = qpInd[i][j]
        if(qpCap[i][j] > capmax):
            capmax = qpCap[i][j]
    if(indmax > highestind):
        primaryInd = i
        highestind = indmax
    if(capmax > highestcap):
        primaryCap = i
        highestcap = capmax

qpLifeData = np.array([])
qpLifexData = np.array([])
phononLifeData = np.array([])
qpLifeInterval = [20, 50]
phononLifeInterval = [120, 250]
#Calculate phonon lifetime and qp lifetime
# for i in range(int(qpLifeInterval[0] / dt), int(qpLifeInterval[1] / dt))
timeaint = int(float(qpLifeInterval[0]) * 1000.0 / dt)
timebint = int(float(qpLifeInterval[1]) * 1000.0 / dt)
qpLifeData = qpInd[primaryInd][timeaint:timebint]
qpLifeData = np.log(qpLifeData + 0.001)
qpLifexData = np.array(range(timeaint, timebint)) * dt / 1000.0
qpm, qpb = np.polyfit(qpLifexData, qpLifeData, 1)

timeaint = int(float(phononLifeInterval[0]) * 1000.0 / dt)
timebint = int(float(phononLifeInterval[1]) * 1000.0 / dt)
phononLifeData = np.zeros(timebint - timeaint)
for i in range(num_kids):
    phononLifeData = np.add(phononLifeData, qpInd[i][timeaint:timebint] + 0.001)

phononLifeData = np.log(phononLifeData / float(num_kids))

phononLifexData = np.array(range(timeaint, timebint)) * dt / 1000.0
phononm, phononb = np.polyfit(phononLifexData, phononLifeData, 1)



print("QP Lifetime: " + str(-1.0 / qpm) + " us")
print("Phonon Lifetime: " + str(-1.0 / phononm) + " us")

maxIndEnergy = np.amax(qpIndTotal)
print("Max Ind Energy: " + str(maxIndEnergy) + ", Fraction: " + str(float(maxIndEnergy) / primaryEnergy))

print("Primary Inductor : " + str(primaryInd + 1))
print("Primary Capacitor : " + str(primaryCap + 1))

print("Plotting . . . ")

ax = plt.subplot(111)
# plt.title(r"Total Energy vs Time" + " (" + str(absProb) + ") ")
plt.title(r"Total Energy vs Time")
plt.xlabel("Time (μs)")
plt.ylabel("Energy (meV)")

plt.plot(xdata, Total, label="Total Energy")

plt.plot(xdata, partTotal, label="Total Particle Energy")
plt.plot(xdata, maxPhononEnergy, label="Maximum energy of any phonon")
plt.plot(xdata, subpTotal, label="Subgap(aluminum) Energy")
plt.plot(xdata, subniobTotal, label="Supergap(aluminum) to Subgap(niobium) Energy")
plt.plot(xdata, superpTotal, label="Supergap(niobium) Energy")

# plt.plot(xdata, indEnergy, label="Inductor Energy Deposit")
# plt.plot(xdata, capEnergy, label="Capacitor Energy Deposit")
# plt.plot(xdata, feedEnergy, label="Feedline Energy Deposit")

plt.plot(xdata, substrate, label="Substrate Energy Deposit")

plt.plot(xdata, qpEnergy, label="Quasiparticle Energy")
plt.plot(xdata, qpIndTotal, label="Inductor Quasiparticle Energy")
plt.plot(xdata, qpCapTotal, label="Capacitor Quasiparticle Energy")
plt.plot(xdata, qpfeed, label="Feedline Quasiparticle Energy")

plt.plot(xdata, qpEnergyGain, label="QP Energy Gain")

plt.plot(xdata, mountDeposit, label="Mount Energy Deposit")

plt.plot(xdata, qpMark, label="Markings Quasiparticle Energy")
leg = plt.legend(loc='upper right', shadow=True, fancybox=True)
leg.get_frame().set_alpha(0.5)
plt.show()


plt.title(r"Total Energy vs Time (Semi-Log)")
plt.xlabel("Time (μs)")
plt.ylabel("Energy (meV)")

plt.yscale("log", base = np.e)

yticksE = []
ylabelsE = []
for i in range(-4, int(np.log(primaryEnergy)) + 2):
    yticksE.append(np.exp(i))
    ylabelsE.append("e^" + str(i))
plt.yticks(yticksE, ylabelsE)

plt.plot(xdata, Total, label="Total Energy")

plt.plot(xdata, partTotal, label="Total Particle Energy")
plt.plot(xdata, subpTotal, label="Subgap(aluminum) Energy")
plt.plot(xdata, subniobTotal, label="Supergap(aluminum) to Subgap(niobium) Energy")
plt.plot(xdata, superpTotal, label="Supergap(niobium) Energy")

plt.plot(xdata, substrate, label="Substrate Energy Deposit")

plt.plot(xdata, qpEnergy, label="Quasiparticle Energy")
plt.plot(xdata, qpIndTotal, label="Inductor Quasiparticle Energy")
plt.plot(xdata, qpCapTotal, label="Capacitor Quasiparticle Energy")
plt.plot(xdata, qpfeed, label="Feedline Quasiparticle Energy")

plt.plot(xdata, mountDeposit, label="Mount Energy Deposit")

plt.plot(xdata, qpMark, label="Markings Quasiparticle Energy")
leg = plt.legend(loc='upper right', shadow=True, fancybox=True)
leg.get_frame().set_alpha(0.5)
plt.show()


# plt.title(r"Total Energy vs Time (Log-Log)")
# plt.xlabel("Time (μs)")
# plt.ylabel("Energy (meV)")

# plt.xscale("log")
# plt.yscale("log")

# plt.plot(xdata, Total, label="Total Energy")

# plt.plot(xdata, partTotal, label="Total Particle Energy")
# plt.plot(xdata, subpTotal, label="Subgap(aluminum) Energy")
# plt.plot(xdata, subniobTotal, label="Supergap(aluminum) to Subgap(niobium) Energy")
# plt.plot(xdata, superpTotal, label="Supergap(niobium) Energy")

# plt.plot(xdata, substrate, label="Substrate Energy Deposit")

# plt.plot(xdata, qpEnergy, label="Quasiparticle Energy")
# plt.plot(xdata, qpIndTotal, label="Inductor Quasiparticle Energy")
# plt.plot(xdata, qpCapTotal, label="Capacitor Quasiparticle Energy")
# plt.plot(xdata, qpfeed, label="Feedline Quasiparticle Energy")
# leg = plt.legend(loc='upper right', shadow=True, fancybox=True)
# leg.get_frame().set_alpha(0.5)
# plt.show()


#plot of all inductor qp energy vs time.
defaultHandle, = plt.plot([0], [0], color = (0, 0, 0, 0))
indLines = []
indLabels = []
for i in range(num_kids):
    indLines.append(0)
    indLabels.append(str(i))
plt.title(r"QP Energy for each Inductor vs Time")
plt.xlabel("Time (μs)")
plt.ylabel("Energy (meV)")

for i in range(num_kids):
    indLines[i], = plt.plot(xdata, qpInd[i], label=str(i + 1), color=matplotlib.colors.hsv_to_rgb((0.9 * float(i) / num_kids, 1, 1)))
    # plt.plot(xdata, qpInd[i], label=str(i + 1), color=matplotlib.colors.hsv_to_rgb((float(i) / num_kids, 1, 1)))

indHandles = []
kidLegend = []
for i in range(len(kid_ids)):
    indHandles.append(0)
    kidLegend.append(0)
for i in range(len(kid_ids)):
    if(kid_ids[i] == 0):
        indHandles[i] = defaultHandle
        kidLegend[i] = ""
    else:
        indHandles[i] = indLines[kid_ids[i] - 1]
        kidLegend[i] = str(kid_ids[i])
indHandles2 = []
kidLegend2 = []
for i in range(len(kid_ids)):
    indHandles2.append(0)
    kidLegend2.append(0)
for i in range(numcols):
    for j in range(numrows):
        indHandles2[i * numrows + j] = indHandles[j * numcols + i]
        kidLegend2[i * numrows + j] = kidLegend[j * numcols + i]
indHandles = indHandles2
kidLegend = kidLegend2

leg = plt.legend(indHandles, kidLegend, loc='upper right', ncol = numcols, shadow=True, fancybox=True, handlelength=1.0, fontsize='small', columnspacing=0.5)
leg.get_frame().set_alpha(0.5)
plt.show()


#plot of all inductor qp energy vs time (Semi-Log).
plt.title(r"QP Energy for each Inductor vs Time (Semi-Log)")
plt.xlabel("Time (μs)")
plt.ylabel("Energy (meV)")
plt.yscale("log", base = np.e)
plt.yticks(yticksE, ylabelsE)
for i in range(num_kids):
    indLines[i], = plt.plot(xdata, qpInd[i], label=str(i + 1), color=matplotlib.colors.hsv_to_rgb((0.9 * float(i) / num_kids, 1, 1)))
    # plt.plot(xdata, qpInd[i], label=str(i + 1), color=matplotlib.colors.hsv_to_rgb((float(i) / num_kids, 1, 1)))


plt.plot(qpLifexData, np.exp(qpm * qpLifexData + qpb), color = (0, 0, 0))
plt.plot(phononLifexData, np.exp(phononm * phononLifexData + phononb), color = (0, 0, 0))



leg = plt.legend(indHandles, kidLegend, loc='upper right', ncol = numcols, shadow=True, fancybox=True, handlelength=1.0, fontsize='small', columnspacing=0.5)
leg.get_frame().set_alpha(0.5)
plt.show()

# #num qps in each ind vs time
# plt.title(r"Inductor QP Count vs Time (Semi-Log)")
# plt.xlabel("Time (μs)")
# plt.ylabel("Count")
# for i in range(num_kids):
#     indLines[i], = plt.plot(xdata, numqpInd[i], label=str(i + 1), color=matplotlib.colors.hsv_to_rgb((0.9 * float(i) / num_kids, 1, 1)))
#     # plt.plot(xdata, qpInd[i], label=str(i + 1), color=matplotlib.colors.hsv_to_rgb((float(i) / num_kids, 1, 1)))
# leg = plt.legend(indHandles, kidLegend, loc='upper right', ncol = numcols, shadow=True, fancybox=True, handlelength=1.0, fontsize='small', columnspacing=0.5)
# leg.get_frame().set_alpha(0.5)
# plt.show()


# #plot of all capacitor qp energy vs time.
# plt.title(r"QP Energy for each Capacitor vs Time")
# plt.xlabel("Time (μs)")
# plt.ylabel("Energy (meV)")

# for i in range(num_kids):
#     # indLines[i], = plt.plot(xdata, qpCap[i], label=str(i + 1), color=matplotlib.colors.hsv_to_rgb((0.9 * float(i) / num_kids, 1, 1)))
#     plt.plot(xdata, qpCap[i], label=str(i + 1), color=matplotlib.colors.hsv_to_rgb((0.9 * float(i) / num_kids, 1, 1)))

# leg = plt.legend(indHandles, kidLegend, loc='upper right', ncol = numcols, shadow=True, fancybox=True, handlelength=1.0, fontsize='small', columnspacing=0.5)
# leg.get_frame().set_alpha(0.5)
# plt.show()


mpxTickLabels = [0, max_graph_time]
#plot of each individual inductor qp energy vs time
fig, axs = plt.subplots(numrows, numcols)
mng = plt.get_current_fig_manager()
mng.set_window_title('Inductor QP energy vs Time (logorithmic)')

current_id = 0
for i in range(numcols):
    for j in range(numrows):
        current_id = kid_ids[j * numcols + i] - 1
        if(current_id != - 1):
            axs[j][i].set_yscale("log")
            axs[j][i].set(ylim = (1, highestind + 100))
            axs[j][i].set(xlim = (0, max_graph_time))
            axs[j][i].set_xticks([0, max_graph_time])
            axs[j][i].set_xticklabels(mpxTickLabels)
            axs[j][i].plot(xdata, qpInd[current_id])
            axs[j][i].set_title(str(current_id + 1))
        else:
            axs[j][i].grid(False)
            axs[j][i].axis("off")

plt.subplots_adjust(left = kidPlotConfig[0], bottom = kidPlotConfig[1], right = kidPlotConfig[2],
                    top = kidPlotConfig[3], wspace = kidPlotConfig[4], hspace = kidPlotConfig[5])
plt.xlabel("Time (μs)")
plt.ylabel("Energy (meV)")
plt.show()



# #plot of each individual capacitor qp energy vs time
# fig, axs = plt.subplots(numrows, numcols)
# mng = plt.get_current_fig_manager()
# mng.set_window_title('Capacitor QP energy vs Time (logorithmic)')

# current_id = 0
# for i in range(numcols):
#     for j in range(numrows):
#         current_id = kid_ids[j * numcols + i] - 1
#         if(current_id != - 1):
#             axs[j][i].set_yscale("log")
#             axs[j][i].set(ylim = (1, highestcap + 100))
#             axs[j][i].set(xlim = (0, max_graph_time))
#             axs[j][i].set_xticks([0, max_graph_time])
#             axs[j][i].set_xticklabels(mpxTickLabels)
#             axs[j][i].plot(xdata, qpCap[current_id])
#             axs[j][i].set_title(str(current_id + 1))
#         else:
#             axs[j][i].grid(False)
#             axs[j][i].axis("off")

# plt.subplots_adjust(left = kidPlotConfig[0], bottom = kidPlotConfig[1], right = kidPlotConfig[2],
#                     top = kidPlotConfig[3], wspace = kidPlotConfig[4], hspace = kidPlotConfig[5])
# plt.xlabel("Time (μs)")
# plt.ylabel("Energy (meV)")
# plt.show()


#Total Flux Graph
plt.title(r"Flux vs Time")
plt.xlabel("Time (μs)")
plt.ylabel("Flux (meV/μs)")
plt.plot(fluxdata, influxIndTotal[numFluxBands], label="Inductor Influx")
plt.plot(fluxdata, outfluxIndTotal[numFluxBands], label="Inductor Outflux")
plt.plot(fluxdata, influxCapTotal[numFluxBands], label="Capacitor Influx")
plt.plot(fluxdata, outfluxCapTotal[numFluxBands], label="Capacitor Outflux")
plt.plot(fluxdata, influxfeed[numFluxBands], label="Feedline Influx")
plt.plot(fluxdata, outfluxfeed[numFluxBands], label="Feedline Outflux")
leg = plt.legend(loc='upper right', shadow=True, fancybox=True)
leg.get_frame().set_alpha(0.5)
plt.show()

#Inductor Flux Graph
plt.title(r"Inductor Flux vs Time")
plt.xlabel("Time (μs)")
plt.ylabel("Flux (meV/μs)")

plotCols = [(0, 255, 0), (255, 60, 0), (226, 0, 226), (50, 50, 255)]
darkPlotCols = []
for i in range(len(plotCols)):
    plotCols[i] = (plotCols[i][0] / 255.0, plotCols[i][1] / 255.0, plotCols[i][2] / 255.0)
    darkPlotCols.append((plotCols[i][0] * darkFactor, plotCols[i][1] * darkFactor, plotCols[i][2] * darkFactor))

plt.plot(fluxdata, influxIndTotal[0], label="Subgap(aluminum) Inductor Influx", color = plotCols[0])
plt.plot(fluxdata, outfluxIndTotal[0], label="Subgap(aluminum) Inductor Outflux", color = darkPlotCols[0])
plt.plot(fluxdata, influxIndTotal[1], label="Supergap(aluminum) to Subgap(niobium) Inductor Influx", color = plotCols[1])
plt.plot(fluxdata, outfluxIndTotal[1], label="Supergap(aluminum) to Subgap(niobium) Inductor Outflux", color = darkPlotCols[1])
plt.plot(fluxdata, influxIndTotal[2], label="Supergap(niobium) Inductor Influx", color = plotCols[2])
plt.plot(fluxdata, outfluxIndTotal[2], label="Supergap(niobium) Inductor Outflux", color = darkPlotCols[2])
plt.plot(fluxdata, influxIndTotal[numFluxBands], label="Total Inductor Influx", color = plotCols[3])
plt.plot(fluxdata, outfluxIndTotal[numFluxBands], label="Total Inductor Outflux", color = darkPlotCols[3])
leg = plt.legend(loc='upper right', shadow=True, fancybox=True)
leg.get_frame().set_alpha(0.5)
plt.show()


#Capacitor Flux Graph
plt.title(r"Capacitor Flux vs Time")
plt.xlabel("Time (μs)")
plt.ylabel("Flux (meV/μs)")
rand.seed(rSeed)
plt.plot(fluxdata, influxCapTotal[0], label="Subgap(aluminum) Capacitor Influx", color = plotCols[0])
plt.plot(fluxdata, outfluxCapTotal[0], label="Subgap(aluminum) Capacitor Outflux", color = darkPlotCols[0])
plt.plot(fluxdata, influxCapTotal[1], label="Supergap(aluminum) to Subgap(niobium) Capacitor Influx", color = plotCols[1])
plt.plot(fluxdata, outfluxCapTotal[1], label="Supergap(aluminum) to Subgap(niobium) Capacitor Outflux", color = darkPlotCols[1])
plt.plot(fluxdata, influxCapTotal[2], label="Supergap(niobium) Capacitor Influx", color = plotCols[2])
plt.plot(fluxdata, outfluxCapTotal[2], label="Supergap(niobium) Capacitor Outflux", color = darkPlotCols[2])
plt.plot(fluxdata, influxCapTotal[numFluxBands], label="Total Capacitor Influx", color = plotCols[3])
plt.plot(fluxdata, outfluxCapTotal[numFluxBands], label="Total Capacitor Outflux", color = darkPlotCols[3])
leg = plt.legend(loc='upper right', shadow=True, fancybox=True)
leg.get_frame().set_alpha(0.5)
plt.show()


#Feedline Flux Graph
plt.title(r"Feedline Flux vs Time")
plt.xlabel("Time (μs)")
plt.ylabel("Flux (meV/μs)")
plt.plot(fluxdata, influxfeed[0], label="Subgap(aluminum) Feedline Influx", color = plotCols[0])
plt.plot(fluxdata, outfluxfeed[0], label="Subgap(aluminum) Feedline Outflux", color = darkPlotCols[0])
plt.plot(fluxdata, influxfeed[1], label="Supergap(aluminum) to Subgap(niobium) Feedline Influx", color = plotCols[1])
plt.plot(fluxdata, outfluxfeed[1], label="Supergap(aluminum) to Subgap(niobium) Feedline Outflux", color = darkPlotCols[1])
plt.plot(fluxdata, influxfeed[2], label="Supergap(niobium) Feedline Influx", color = plotCols[2])
plt.plot(fluxdata, outfluxfeed[2], label="Supergap(niobium) Feedline Outflux", color = darkPlotCols[2])
plt.plot(fluxdata, influxfeed[numFluxBands], label="Total Feedline Influx", color = plotCols[3])
plt.plot(fluxdata, outfluxfeed[numFluxBands], label="Total Feedline Outflux", color = darkPlotCols[3])
leg = plt.legend(loc='upper right', shadow=True, fancybox=True)
leg.get_frame().set_alpha(0.5)
plt.show()


#single plot of each inductor flux vs time
plt.title(r"Flux for each Inductor vs Time")
plt.xlabel("Time (μs)")
plt.ylabel("Flux (meV/μs)")
for i in range(num_kids):
    plt.plot(fluxdata, influxInd[i][numFluxBands], color=matplotlib.colors.hsv_to_rgb((0.9 * float(i) / num_kids, 1, 1)))
    # plt.plot(fluxdata, outfluxInd[i], color=matplotlib.colors.hsv_to_rgb((0.9 * float(i) / num_kids, 1, 0.5)))
leg = plt.legend(indHandles, kidLegend, loc='upper right', ncol = numcols, shadow=True, fancybox=True, handlelength=1.0, fontsize='small', columnspacing=0.5)
leg.get_frame().set_alpha(0.5)
plt.show()

# #single plot of each capacitor flux vs time
# plt.title(r"Flux for each Capacitor vs Time")
# plt.xlabel("Time (μs)")
# plt.ylabel("Flux (meV/μs)")
# for i in range(num_kids):
#     plt.plot(fluxdata, influxCap[i][numFluxBands], color=matplotlib.colors.hsv_to_rgb((0.9 * float(i) / num_kids, 1, 1)))
#     # plt.plot(fluxdata, outfluxInd[i], color=matplotlib.colors.hsv_to_rgb((0.9 * float(i) / num_kids, 1, 0.5)))
# leg = plt.legend(indHandles, kidLegend, loc='upper right', ncol = numcols, shadow=True, fancybox=True, handlelength=1.0, fontsize='small', columnspacing=0.5)
# leg.get_frame().set_alpha(0.5)
# plt.show()

#multiple plots of each individual inductor flux vs time
fluxHandles = [0, 0]
fluxLabels = ["influx", "outflux"]
fig, axs = plt.subplots(numrows, numcols)
mng = plt.get_current_fig_manager()
mng.set_window_title('Inductor Flux vs Time (logorithmic)')
current_id = 0
for i in range(numcols):
    for j in range(numrows):
        current_id = kid_ids[j * numcols + i] - 1
        if(current_id != - 1):
            axs[j][i].set_yscale("log")
            axs[j][i].set(ylim = (1, highest_flux + 100))
            axs[j][i].set(xlim = (0, max_graph_time))
            axs[j][i].set_xticks([0, max_graph_time])
            axs[j][i].set_xticklabels(mpxTickLabels)
            fluxHandles[0], = axs[j][i].plot(fluxdata, influxInd[current_id][numFluxBands])
            fluxHandles[1], = axs[j][i].plot(fluxdata, outfluxInd[current_id][numFluxBands])
            axs[j][i].set_title(str(current_id + 1))
        else:
            axs[j][i].grid(False)
            axs[j][i].axis("off")

axs[numrows - 1][numcols - 1].legend(fluxHandles, fluxLabels, loc='upper right')
plt.subplots_adjust(left = kidPlotConfig[0], bottom = kidPlotConfig[1], right = kidPlotConfig[2],
                    top = kidPlotConfig[3], wspace = kidPlotConfig[4], hspace = kidPlotConfig[5])
plt.xlabel("Time (μs)")
plt.ylabel("Flux (meV/μs)")
plt.show()

# #plot of each individual capacitor flux vs time
# fig, axs = plt.subplots(numrows, numcols)
# mng = plt.get_current_fig_manager()
# mng.set_window_title('Capacitor Flux vs Time (logorithmic)')

# current_id = 0
# for i in range(numcols):
#     for j in range(numrows):
#         current_id = kid_ids[j * numcols + i] - 1
#         if(current_id != - 1):
#             axs[j][i].set_yscale("log")
#             axs[j][i].set(ylim = (1, highest_flux + 100))
#             axs[j][i].set(xlim = (0, max_graph_time))
#             axs[j][i].set_xticks([0, max_graph_time])
#             axs[j][i].set_xticklabels(mpxTickLabels)
#             fluxHandles[0], = axs[j][i].plot(fluxdata, influxCap[current_id][numFluxBands], color='b')
#             fluxHandles[1], = axs[j][i].plot(fluxdata, outfluxCap[current_id][numFluxBands], color='c')
#             axs[j][i].set_title(str(current_id + 1))
#         else:
#             axs[j][i].grid(False)
#             axs[j][i].axis("off")

# axs[numrows - 1][numcols - 1].legend(fluxHandles, fluxLabels, loc='upper right')
# plt.subplots_adjust(left = kidPlotConfig[0], bottom = kidPlotConfig[1], right = kidPlotConfig[2],
#                     top = kidPlotConfig[3], wspace = kidPlotConfig[4], hspace = kidPlotConfig[5])
# plt.xlabel("Time (μs)")
# plt.ylabel("Flux (meV/μs)")
# plt.show()