import pandas as pd
import matplotlib.pyplot as plt

# Define the file paths for the two CSV files
file1 = 'AXE_10.0.csv'  # Replace with your first CSV file path
file2 = 'EXE_10.0.csv'  # Replace with your second CSV file path

# Read the CSV files into DataFrames
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Create a figure with two 3D subplots
fig, (ax1, ax2) = plt.subplots(1, 2, subplot_kw={'projection': '3d'}, figsize=(14, 6))

# Plot the first dataset
ax1.scatter(df1['Charging Rate'], df1['Start Window'], df1['Result'], c='b', marker='o')
ax1.set_title('Dataset 1')
ax1.set_xlabel('Charging Rate')
ax1.set_ylabel('Start Window')
ax1.set_zlabel('Result')

# Plot the second dataset
ax2.scatter(df2['Charging Rate'], df2['Start Window'], df2['Result'], c='r', marker='^')
ax2.set_title('Dataset 2')
ax2.set_xlabel('Charging Rate')
ax2.set_ylabel('Start Window')
ax2.set_zlabel('Result')

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plots
plt.show()
