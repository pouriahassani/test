import numpy as np
import matplotlib.pyplot as plt

# Load first dataset (EXE)
data_exe = np.loadtxt("output_data_EXE_fit_battery_Correct_power.csv", delimiter=",", skiprows=1)  
charge_vals_exe = data_exe[:, 0]
start_vals_exe = data_exe[:, 1]
result_vals_exe = data_exe[:, 2]

# Load second dataset (FAXE)
data_faxe = np.loadtxt("output_data_AXE_fit_battery_Correct_power.csv", delimiter=",", skiprows=1)  
charge_vals_faxe = data_faxe[:, 0]
start_vals_faxe = data_faxe[:, 1]
result_vals_faxe = data_faxe[:, 2]

# Choose the specific charge_val to filter
charge_val_target = 0.5 # Change this to your desired charge_val

# Filter data for EXE
mask_exe = charge_vals_exe == charge_val_target
filtered_start_exe = start_vals_exe[mask_exe]
filtered_result_exe = result_vals_exe[mask_exe]

# Filter data for FAXE
mask_faxe = charge_vals_faxe == charge_val_target
filtered_start_faxe = start_vals_faxe[mask_faxe]
filtered_result_faxe = result_vals_faxe[mask_faxe]

# Plot the filtered data
plt.figure(figsize=(8, 6))
plt.plot(filtered_start_exe, filtered_result_exe, label="EXE", marker='o', linestyle='-')
plt.plot(filtered_start_faxe, filtered_result_faxe, label="FAXE", marker='s', linestyle='--')

# Labels and title
plt.xlabel("Start Window of the application deadlines")
plt.ylabel("Partitioning success rate")
plt.title(f"Partitioning success rate for battery charging rate of {charge_val_target}")
plt.legend()
plt.grid(True)
plt.savefig("partitioning_success_rate_"+str(charge_val_target)+".jpg", format="jpg", dpi=300)
# Show the plot
plt.show()
