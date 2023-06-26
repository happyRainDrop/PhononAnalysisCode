from math import *
import numpy as np
import seaborn as sns
import random
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors

data = []
xData = []
yData = []
zData = []
colData = []

fraction = 0.01

#this requires that the step data is organized like this: id, .., .., \n
print("Collecting data . . . ")
directory = "Data/"
path = directory + "ReflData.txt"
f = open(path, "r")
data = f.read().split(",")
f.close()

print("Reading Data . . . ")
for i in range(int(len(data) / 4)):
    if(int(data[4 * i + 3]) == 1):
        if(random.random() > fraction):
            continue
    xData.append(float(data[4 * i + 0]))
    yData.append(float(data[4 * i + 1]))
    zData.append(float(data[4 * i + 2]))
    if(int(data[4 * i + 3]) == 1):
        colData.append((0, 0, 1))
    else:
        colData.append((1, 0, 0))


# for i in range(int(len(data) / 4)):
#     if(int(data[4 * i + 3]) == 0):
#         xData.append(float(data[4 * i + 0]))
#         yData.append(float(data[4 * i + 1]))
#         zData.append(float(data[4 * i + 2]))
#         if(int(data[4 * i + 3]) == 1):
#             colData.append((0, 0, 1))
#         else:
#             colData.append((1, 0, 0))


# for i in range(int(len(data) / 4)):
#     if(float(data[4 * i + 2]) < 0.):
#         if(random.random() > fraction):
#             continue
#     xData.append(float(data[4 * i + 0]))
#     yData.append(float(data[4 * i + 1]))
#     zData.append(float(data[4 * i + 2]))
#     if(float(data[4 * i + 2]) < 0.):
#         colData.append((0, 0, 1))
#     else:
#         colData.append((1, 0, 0))


for i in range(len(xData)):
    x = xData[i]
    y = yData[i]
    z = zData[i]

    if(fabs(sqrt(x * x + y * y + z * z) - 1) > 0.00001):
        print(str(x) + "," + str(y) + "," + str(z))


print("Plotting . . . ")
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.title("Reflected Phonon Directions")
ax.scatter(xData, yData, zData, c = colData)
plt.show()