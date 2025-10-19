import numpy as np
import matplotlib.pyplot as plt

# Load first dataset (EXE)
data_exe = np.loadtxt("output_data_EXE_fit_battery_Wrong_power.csv", delimiter=",", skiprows=1)  
charge_vals_exe = data_exe[:, 0]
start_vals_exe = data_exe[:, 1]
result_vals_exe = data_exe[:, 2]

# Load second dataset (FAXE)
data_faxe = np.loadtxt("output_data_AXE_fit_battery_Wrong_power.csv", delimiter=",", skiprows=1)  
charge_vals_faxe = data_faxe[:, 0]
start_vals_faxe = data_faxe[:, 1]
result_vals_faxe = data_faxe[:, 2]




# Plot the filtered data
# Create figure


# Loop through charge values from 1 to 2 with 0.1 step
for start_val_target in np.arange(1, 6, 0.2):
    # Filter data for EXE
    plt.figure(figsize=(10, 6))
    mask_exe = np.abs(start_vals_faxe - start_val_target) <= 0.01
    filtered_start_exe = charge_vals_exe[mask_exe]
    filtered_result_exe = result_vals_exe[mask_exe]
    
    # Filter data for FAXE
    mask_faxe = np.abs(start_vals_faxe - start_val_target) <= 0.01
    filtered_start_faxe = charge_vals_faxe[mask_faxe]
    filtered_result_faxe = result_vals_faxe[mask_faxe]
    
    # Plot the filtered data
    plt.plot(filtered_start_exe, filtered_result_exe, label=f"EXE (Start={start_val_target:.1f})", marker='o', linestyle='-')
    plt.plot(filtered_start_faxe, filtered_result_faxe, label=f"FAXE (Start={start_val_target:.1f})", marker='s', linestyle='--')

    # Labels and title
    plt.xlabel("Charging Rate")
    plt.ylabel("Partitioning success rate")
    plt.title(f"Partitioning success rate for start window of {start_val_target}")
    plt.legend()
    plt.grid(True)
    # plt.savefig("partitioning_success_rate_"+str(charge_val_target)+".jpg", format="jpg", dpi=300)
    # Show the plot
    plt.show()
