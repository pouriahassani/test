import numpy as np
import matplotlib.pyplot as plt

# Load first dataset
data_exe = np.loadtxt("10_apps_EXE_Results_fit_1_battery_5_41_4e.csv", delimiter=",", skiprows=1)  
charge_vals_exe = data_exe[:, 0]
start_vals_exe = data_exe[:, 1]
result_vals_exe = data_exe[:, 2]

# Load second dataset
data_faxe = np.loadtxt("10_apps_AXE_Results_fit_1_battery_5_41_4e.csv", delimiter=",", skiprows=1)  
charge_vals_faxe = data_faxe[:, 0]
start_vals_faxe = data_faxe[:, 1]
result_vals_faxe = data_faxe[:, 2]


# mask the data


# mask = (charge_vals_faxe >= 8) & (charge_vals_faxe <= 15) & (result_vals_faxe<100) & (result_vals_faxe>0)
# charge_vals_exe = charge_vals_exe[mask]
# result_vals_exe = result_vals_exe[mask]
# start_vals_exe = start_vals_exe[mask]
# # Apply the mask to filter the values
# charge_vals_faxe = charge_vals_faxe[mask]
# result_vals_faxe = result_vals_faxe[mask]
# start_vals_faxe = start_vals_faxe[mask]

# mask = (start_vals_exe >= 6) & (start_vals_exe <= 15) & (result_vals_exe<100) & (result_vals_exe>0)
# charge_vals_exe = charge_vals_exe[mask]
# result_vals_exe = result_vals_exe[mask]
# start_vals_exe = start_vals_exe[mask]
# # Apply the mask to filter the values
# charge_vals_faxe = charge_vals_faxe[mask]
# result_vals_faxe = result_vals_faxe[mask]
# start_vals_faxe = start_vals_faxe[mask]

# Create figure with two subplots
fig = plt.figure(figsize=(14, 6))

# First subplot (EXE)
ax1 = fig.add_subplot(121, projection='3d')
ax1.scatter(charge_vals_exe, start_vals_exe, result_vals_exe, c=result_vals_exe, cmap='viridis', marker='o')
ax1.set_xlabel('Charge')
ax1.set_ylabel('Start')
ax1.set_zlabel('Result')
ax1.set_title('EXE Data')

# Second subplot (FAXE)
ax2 = fig.add_subplot(122, projection='3d')
ax2.scatter(charge_vals_faxe, start_vals_faxe, result_vals_faxe, c=result_vals_faxe, cmap='plasma', marker='o')
ax2.set_xlabel('Charge')
ax2.set_ylabel('Start')
ax2.set_zlabel('Result')
ax2.set_title('FAXE Data')

# Show the figure
plt.tight_layout()
plt.show()
