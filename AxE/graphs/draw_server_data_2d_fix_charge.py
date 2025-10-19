import numpy as np
import matplotlib.pyplot as plt

# Load first dataset (EXE)
data_exe = np.loadtxt("EXE_results.csv", delimiter=",", skiprows=1)  
charge_vals_exe = data_exe[:, 0]
start_vals_exe = data_exe[:, 1]
result_vals_exe = data_exe[:, 4]

# Load second dataset (FAXE)
data_faxe = np.loadtxt("AXE_results.csv", delimiter=",", skiprows=1)  
charge_vals_faxe = data_faxe[:, 0]
start_vals_faxe = data_faxe[:, 1]
result_vals_faxe = data_faxe[:, 4]

# Define start values range
charge_values = np.arange(1, 10, 1)
n_rows = int(np.ceil(len(charge_values) / 3))  # Determine rows for 3 columns layout

fig, axes = plt.subplots(n_rows, 3, figsize=(15, 5 * n_rows))
axes = axes.flatten()  # Flatten to easily iterate
diff = 0
len_data = 0
start_axe_100 = []
charge_axe_100 = []
start_exe_100 = []
charge_exe_100 = []
# Loop through start values and plot in separate subplots
for i, charge_val_target in enumerate(charge_values):
    # Filter data for EXE
    mask_exe = np.abs(charge_vals_exe - charge_val_target) <= 0.02
    filtered_start_exe = start_vals_exe [mask_exe]
    filtered_result_exe = result_vals_exe[mask_exe]
    
    # Filter data for FAXE
    mask_faxe = np.abs(charge_vals_faxe - charge_val_target) <= 0.02
    filtered_start_faxe = start_vals_faxe[mask_faxe]
    filtered_result_faxe = result_vals_faxe[mask_faxe]

    # mask = (filtered_charge_exe >= 2) & (filtered_charge_exe <= 10)
    # filtered_charge_exe = filtered_charge_exe[mask]
    # filtered_result_exe = filtered_result_exe[mask]
    # # Apply the mask to filter the values
    # filtered_charge_faxe = filtered_charge_faxe[mask]
    # filtered_result_faxe = filtered_result_faxe[mask]
    # print(charge_val_target)
    # print(filtered_result_faxe)
    # print(filtered_result_exe)
    for idx in range(len(filtered_start_faxe)):
        diff += ( filtered_result_faxe[idx] - filtered_result_exe[idx])
        len_data +=1
    for idx in range(len(filtered_start_faxe)):
      if filtered_result_faxe[idx] >= 95:
         start_axe_100.append(filtered_start_faxe[idx])
         charge_axe_100.append(charge_val_target)
         break
    for idx in range(len(filtered_start_exe)):
      if filtered_result_exe[idx] >= 95:
         start_exe_100.append(filtered_start_exe[idx])
         charge_exe_100.append(charge_val_target)
         break
    ax = axes[i]
    ax.plot(filtered_start_exe, filtered_result_exe, label="EXE", marker='o', linestyle='-')
    ax.plot(filtered_start_faxe, filtered_result_faxe, label="FAXE", marker='s', linestyle='--')
    ax.set_xlabel("Battery Charging Rate")
    ax.set_ylabel("Partitioning success rate")
    ax.set_title(f"Start value = {charge_val_target:.1f}")
    ax.legend()
    ax.grid(True)
print(diff,len_data)
print(diff/len_data )
charges_100 = []
exe_100 = []
axe_100 = []
for idx,charge_100 in enumerate(charge_axe_100):
   if idx<len(charge_exe_100):
    if charge_exe_100[idx] == charge_100:
        exe_100.append(start_exe_100[idx])
        axe_100.append(start_axe_100[idx])
        charges_100.append(charge_100)
print(charges_100)
print(axe_100)
print(exe_100)

# filtered_x = [xi for xi in start_axe_100 if xi < 10]
# filtered_y = [charge_axe_100[i] for i in range(len(start_axe_100)) if start_axe_100[i] < 10]
# plt.plot(filtered_x, filtered_y, label="FAXE", marker='o', linestyle='-')
# filtered_x = [xi for xi in start_exe_100 if xi < 10]
# filtered_y = [charge_exe_100[i] for i in range(len(start_exe_100)) if start_exe_100[i] < 10]

# plt.plot(charge_axe_100, start_axe_100, label="FAXE", marker='o', linestyle='-')
# plt.plot(charge_exe_100, start_exe_100, label="EXE", marker='s', linestyle='--')
# plt.xlabel("start window")
# plt.ylabel("Charging rate when the partitioning reaches 100%")
# plt.legend()
# plt.show()
# charge_diff = 0
# for idx in range(len(charges_100)):
#    charge_diff += (exe_100[idx] - axe_100[idx])/exe_100[idx]*100
  
# print(charge_diff/(len(charges_100)))
# print(charge_diff/len(charge_axe_100))
# Adjust layout to prevent overlap
plt.tight_layout()
plt.savefig("partitioning_success_rate_all.jpg", format="jpg", dpi=300)
plt.show()
