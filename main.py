import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read Excel into a pandas data frame
photo_frame = pd.read_excel("photometry.xlsx")

# Convert to numpy array for easier indexing
photo_array = photo_frame.to_numpy()

# Timestamps in first column
time_values = photo_array[:,0]

# Calcium measurements in columns from 2 until the last
calcium = photo_array[:,1:]

print(f"Array shape is {np.shape(photo_array)}")

# Average all calcium values in each column
m1 = np.mean(calcium, axis = 0)
num_trials = np.size(m1)
print(f"Calculated average for {num_trials} trials, one in each column")

# Average all values in each row
m2 = np.mean(calcium, axis = 1)
print(f"Calculated average for {np.size(m2)} time points, one in each row")

plt.plot(time_values, calcium, linewidth=0.5)
plt.xlabel("Time after cue onset (s)")
plt.title("Calcium measurements for each trial")

# Create new figure, otherwise plots will overlap on same one
plt.figure()
plt.plot(time_values, m2)
plt.xlabel("Time after cue onset (s)")
plt.title(f"Calcium measurements averaged across all {num_trials} trials")