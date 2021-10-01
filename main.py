
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read Excel into a pandas data frame

print('Reading Excel file...')
photo_frame = pd.io.excel.read_excel("photometry.xlsx")
print(f'Done reading file. Obtained array with shape {np.shape(photo_frame)}')

# Convert to numpy array for easier indexing
photo_array = photo_frame.to_numpy()

# Extract timestamps from first column
time_values = photo_array[:,0]

# Extract calcium measurements from columns 2 until end
calcium = photo_array[:,1:]

# Plot each trial as a separate line
plt.plot(time_values, calcium, linewidth=0.5)
# Add x-axis label
plt.xlabel("Time after cue onset (s)")
# Add title
plt.title("Calcium measurements for each trial")

# Now create new figure, otherwise subsequent plots will overlap previous
plt.figure()

# Average all values for each time point
row_means = np.mean(calcium, axis = 1)
# Plot average across trials
plt.plot(time_values, row_means)
plt.xlabel("Time after cue onset (s)")
plt.title(f"Calcium measurements averaged across all {np.shape(calcium)[1]} trials")

# If you haven't selected "run with Python console" option, you need this or else plot will close as soon as program completes.
plt.show()
