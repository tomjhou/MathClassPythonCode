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

# Plot each trial
plt.plot(time_values, calcium, linewidth=0.5)
plt.xlabel("Time after cue onset (s)")
plt.title("Calcium measurements for each trial")

# Create new figure, otherwise plots will overlap on same one
plt.figure()

# Plot average across trials
# Average all values in each row
row_means = np.mean(calcium, axis = 1)
plt.plot(time_values, row_means)
plt.xlabel("Time after cue onset (s)")
plt.title(f"Calcium measurements averaged across all {np.shape(calcium)[1]} trials")