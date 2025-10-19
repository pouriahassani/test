import numpy as np
import matplotlib.pyplot as plt

# Load first dataset (EXE)
data_exe = np.loadtxt("output_data_EXE_fit_1_battery_Correct_power.csv", delimiter=",", skiprows=1)  
charge_vals_exe = data_exe[:, 0]
start_vals_exe = data_exe[:, 1]
result_vals_exe = data_exe[:, 2]

# Load second dataset (FAXE)
data_faxe = np.loadtxt("output_data_AXE_fit_1_battery_Correct_power.csv", delimiter=",", skiprows=1)  
charge_vals_faxe = data_faxe[:, 0]
start_vals_faxe = data_faxe[:, 1]
result_vals_faxe = data_faxe[:, 2]

# Define charge values range
charge_values = np.arange(0, 568, 8)
n_rows = int(np.ceil(len(charge_values) / 3))  # Determine rows for 3 columns layout

fig, axes = plt.subplots(n_rows, 3, figsize=(15, 5 * n_rows))
axes = axes.flatten()  # Flatten to easily iterate
diff = 0
len_data = 0
# Loop through charge values and plot in separate subplots
for i, charge_val_target in enumerate(charge_values):
    # Filter data for EXE
    mask_exe = np.abs(charge_vals_exe - charge_val_target) <= 0.01
    filtered_start_exe = start_vals_exe[mask_exe]
    filtered_result_exe = result_vals_exe[mask_exe]
    
    # Filter data for FAXE
    mask_faxe = np.abs(charge_vals_faxe - charge_val_target) <= 0.01
    filtered_start_faxe = start_vals_faxe[mask_faxe]
    filtered_result_faxe = result_vals_faxe[mask_faxe]
    for idx in range(len(filtered_start_faxe)):
        diff += ( filtered_result_faxe[idx] - filtered_result_exe[idx])
        len_data +=1
    # ax = axes[i]
    # ax.plot(filtered_start_exe, filtered_result_exe, label="EXE", marker='o', linestyle='-')
    # ax.plot(filtered_start_faxe, filtered_result_faxe, label="FAXE", marker='s', linestyle='--')
    # ax.set_xlabel("Start Window of the application deadlines")
    # ax.set_ylabel("Partitioning success rate")
    # ax.set_title(f"Charge rate = {charge_val_target:.1f}")
    # ax.legend()
    # ax.grid(True)
print(diff,len_data)
print(diff/len_data )
# Adjust layout to prevent overlap
# plt.tight_layout()
# plt.savefig("partitioning_success_rate_all.jpg", format="jpg", dpi=300)
# plt.show()

