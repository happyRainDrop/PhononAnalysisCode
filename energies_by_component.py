import matplotlib.pyplot as plt
import numpy as np

# File path
file_path = "StepData.txt"

# Read the file
with open(file_path, 'r') as file:
    lines = file.readlines()

# Initialize dictionaries to store energies for each ID
cap_energies = []
ind_energies = []
feed_energies = []

# Process the file data
print("Processing...")
for i in range(0, len(lines)-1):

    if lines[i].startswith("New Event"): 
      continue
  
    line = lines[i].strip().split(',')
    prev_line = lines[i-1].strip().split(',')

    if line[5].startswith("kid_cap"):
        energy = float(line[1]) / 4.136
        cap_energies.append(energy)

    elif line[5].startswith("kid_ind"):
        energy = float(line[1]) / 4.136
        ind_energies.append(energy)
    
    elif line[5].startswith("feed"):
        energy = float(line[1]) / 4.136
        feed_energies.append(energy)

    

print("Plotting...")
# Plotting the distributions
cap_bins = 100  # Number of bins for capacitor energy distribution
ind_bins = 100  # Number of bins for inductor energy distribution
feed_bins = 100  # Number of bins for feedline energy distribution

# Capacitor Phonon Energy Distribution
plt.figure()
plt.title("Capacitor Phonon Energy Distribution")
plt.xlabel("Energy")
plt.ylabel("Frequency")
plt.hist(cap_energies, bins=cap_bins, histtype='step')
plt.savefig('Capacitor Phonon Energy Distribution.png')

# Inductor Phonon Energy Distribution
plt.figure()
plt.title("Inductor Phonon Energy Distribution")
plt.xlabel("Energy")
plt.ylabel("Frequency")
plt.hist(ind_energies, bins=ind_bins, histtype='step')
plt.savefig('Inductor Phonon Energy Distribution.png')

# Create a figure for Feedline Phonon Energy Distribution
plt.figure()
plt.title("Feedline Phonon Energy Distribution")
plt.xlabel("Energy")
plt.ylabel("Frequency")
plt.hist(feed_energies, bins=feed_bins, histtype='step')
plt.savefig('Feedline Phonon Energy Distribution.png')

# Display the plots
plt.show()
