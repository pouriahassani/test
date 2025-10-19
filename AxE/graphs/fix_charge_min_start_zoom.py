import numpy as np
import matplotlib.pyplot as plt
ZOOM = 0
FULL_PARTITIONING = 1
# Load first dataset (EXE)
data_exe = np.loadtxt("EXE_results_bigger_range.csv", delimiter=",", skiprows=1)  
charge_vals_exe = data_exe[:, 0]
start_vals_exe = data_exe[:, 1]
result_vals_exe = data_exe[:, 2]

# Load second dataset (FAXE)
data_faxe = np.loadtxt("AXE_results_bigger_range.csv", delimiter=",", skiprows=1)  
charge_vals_faxe = data_faxe[:, 0]
start_vals_faxe = data_faxe[:, 1]
result_vals_faxe = data_faxe[:, 2]

# Define start values range
if FULL_PARTITIONING:
   charge_values = np.arange(0, 20, 0.1)
   figsize=(15, 10)
else:
   charge_values = np.arange(7, 15, 2)
   n_rows = int(np.ceil(len(charge_values) / 2))  # Determine rows for 3 columns layout
   fig, axes = plt.subplots(n_rows, 2, figsize=(15, 5 * n_rows))
   axes = axes.flatten()  # Flatten to easily iterate



diff = 0
len_data = 0
start_axe_100 = []
charge_axe_100 = []
start_exe_100 = []
charge_exe_100 = []
start_axe_95 = []
charge_axe_95 = []
start_exe_95 = []
charge_exe_95 = []
start_axe_90 = []
charge_axe_90 = []
start_exe_90 = []
charge_exe_90 = []
start_axe_80 = []
charge_axe_80 = []
start_exe_80 = []
charge_exe_80 = []
# Loop through start values and plot in separate subplots
for i, charge_val_target in enumerate(charge_values):
    # Filter data for EXE
    mask_exe = np.abs(charge_vals_exe - charge_val_target) <= 0.02
    filtered_start_exe = start_vals_exe[mask_exe]
    filtered_result_exe = result_vals_exe[mask_exe]

    mask_exe = (filtered_start_exe <= 21)
    filtered_start_exe = filtered_start_exe[mask_exe]
    filtered_result_exe = filtered_result_exe[mask_exe]
    
    # Filter data for FAXE
    mask_faxe = np.abs(charge_vals_faxe - charge_val_target) <= 0.02
    filtered_start_faxe = start_vals_faxe[mask_faxe]
    filtered_result_faxe = result_vals_faxe[mask_faxe]

    mask_faxe = (filtered_start_faxe <= 21)
    filtered_start_faxe = filtered_start_faxe[mask_faxe]
    filtered_result_faxe = filtered_result_faxe[mask_faxe]

    if  not FULL_PARTITIONING:
      ax = axes[i]
      if ZOOM:
         zoom_start_faxe = []
         zoom_result_faxe = []
         zoom_result_exe = []
         zoom_start_exe = []
         first = 0
         last = 0
         for idx in range(len(filtered_start_faxe)):
            if first ==  1 and last == 0:
               if filtered_result_faxe[idx] == 100:
                  zoom_start_faxe.append(filtered_start_faxe[idx])
                  zoom_result_faxe.append(100)
                  break
               zoom_start_faxe.append(filtered_start_faxe[idx])
               zoom_result_faxe.append(filtered_result_faxe[idx])
            if first == 0 and last == 0:
               if filtered_result_faxe[idx] > 0:
                  first = 1
                  zoom_start_faxe.append(filtered_start_faxe[idx])
                  zoom_result_faxe.append(0)

         first = 0
         last = 0
         for idx in range(len(filtered_start_exe)):
            if first ==  1 and last == 0:
               if filtered_result_exe[idx] == 100:
                  zoom_start_exe.append(filtered_start_exe[idx])
                  zoom_result_exe.append(100)
                  break
               zoom_start_exe.append(filtered_start_exe[idx])
               zoom_result_exe.append(filtered_result_exe[idx])
            if first == 0 and last == 0:
               if filtered_result_exe[idx] > 0:
                  first = 1
                  zoom_start_exe.append(filtered_start_exe[idx])
                  zoom_result_exe.append(0)
         ax.plot(zoom_start_exe,  zoom_result_exe, label="EXE",  color = 'r',marker='o', linestyle='-',markersize=5)
         ax.plot(zoom_start_faxe, zoom_result_faxe, label="FAXE",color = 'g',marker='s', linestyle='-',markersize=5)
         ax.set_xlabel("Start Window", fontsize=20)
         ax.set_ylabel("Partitioning Success Rate (%)", fontsize=20)
         ax.set_title(f"Charging Rate (P) = {charge_val_target:.1f} mW", fontsize=22)
         ax.legend(fontsize=19)
         ax.grid(True)
         ax.tick_params(axis='both', labelsize=16)  # Increase font size for axis ticks
      if not ZOOM:
         ax.plot(filtered_start_exe, filtered_result_exe,   label="E-MPSoC", color = 'r', marker='o', linestyle='-',markersize=3)
         ax.plot(filtered_start_faxe, filtered_result_faxe, label="AxE-F",color = 'g', marker='s', linestyle='-',markersize=3)
         ax.set_xlabel("Start Window", fontsize=20)
         ax.set_ylabel("Partitioning Success Rate (%)", fontsize=20)
         ax.set_title(f"Charging Rate (P) = {charge_val_target:.1f} mW", fontsize=22)
         ax.legend(fontsize=19)
         ax.grid(True)

         ax.tick_params(axis='both', labelsize=16)  # Increase font size for axis ticks
    
   # FULL partitioning comparissionz
    if FULL_PARTITIONING:
      for idx in range(len(filtered_start_faxe)):
         diff += ( filtered_result_faxe[idx] - filtered_result_exe[idx])
         len_data +=1

      for idx in range(len(filtered_start_faxe)):
         if filtered_result_faxe[idx] >= 100:
            start_axe_100.append(filtered_start_faxe[idx])
            charge_axe_100.append(charge_val_target)
            break
      for idx in range(len(filtered_start_exe)):
         if filtered_result_exe[idx] >= 100:
            start_exe_100.append(filtered_start_exe[idx])
            charge_exe_100.append(charge_val_target)
            break 

      for idx in range(len(filtered_start_faxe)):
         if filtered_result_faxe[idx] >= 95:
            start_axe_95.append(filtered_start_faxe[idx])
            charge_axe_95.append(charge_val_target)
            break
      for idx in range(len(filtered_start_exe)):
         if filtered_result_exe[idx] >= 95:
            start_exe_95.append(filtered_start_exe[idx])
            charge_exe_95.append(charge_val_target)
            break       

      for idx in range(len(filtered_start_faxe)):
         if filtered_result_faxe[idx] >= 90:
            start_axe_90.append(filtered_start_faxe[idx])
            charge_axe_90.append(charge_val_target)
            break
      for idx in range(len(filtered_start_exe)):
         if filtered_result_exe[idx] >= 90:
            start_exe_90.append(filtered_start_exe[idx])
            charge_exe_90.append(charge_val_target)
            break                   

      for idx in range(len(filtered_start_faxe)):
         if filtered_result_faxe[idx] >= 80:
            start_axe_80.append(filtered_start_faxe[idx])
            charge_axe_80.append(charge_val_target)
            break
      for idx in range(len(filtered_start_exe)):
         if filtered_result_exe[idx] >= 80:
            start_exe_80.append(filtered_start_exe[idx])
            charge_exe_80.append(charge_val_target)
            break

print(len(charge_axe_100))
print(len(charge_exe_100))
print(len(start_axe_100))
print("start_axe_100 " , start_axe_100)
print("charge_axe_100 ", charge_axe_100)
print("start_exe_100 ", start_exe_100)
print("charge_exe_100" , charge_exe_100)
if not FULL_PARTITIONING:
   if ZOOM:
      plt.tight_layout()
      plt.savefig("FIXED_CHARGE_partitioning_success_rate_zoomed.pdf", format="pdf", dpi=300)
      plt.show()
   if not ZOOM:
      plt.tight_layout()
      plt.savefig("FIXED_CHARGE_partitioning_success_rate_all.pdf", format="pdf", dpi=300)
      plt.show()

if FULL_PARTITIONING:
   print(diff,len_data)
   print(diff/len_data )
   charges_100 = []
   exe_100 = []
   axe_100 = []
   charges_95 = []
   exe_95 = []
   axe_95 = []
   charges_90 = []
   exe_90 = []
   axe_90 = []
   charges_80 = []
   exe_80 = []
   axe_80 = []

   for idx_axe,axet_100 in enumerate(charge_axe_100):
         for idx_exe,exet_100 in enumerate(charge_exe_100):
            if axet_100 == exet_100:
               exe_100.append(start_exe_100[idx_exe])
               axe_100.append(start_axe_100[idx_axe])
               charges_100.append(exet_100)
               break

   for idx_axe,axet_95 in enumerate(charge_axe_95):
         for idx_exe,exet_95 in enumerate(charge_exe_95):
            if axet_95 == exet_95:
               exe_95.append(start_exe_95[idx_exe])
               axe_95.append(start_axe_95[idx_axe])
               charges_95.append(exet_95)
               break     

   for idx_axe,axet_90 in enumerate(charge_axe_90):
         for idx_exe,exet_90 in enumerate(charge_exe_90):
            if axet_90 == exet_90:
               exe_90.append(start_exe_90[idx_exe])
               axe_90.append(start_axe_90[idx_axe])
               charges_90.append(exet_90)
               break   

   for idx_axe,axet_80 in enumerate(charge_axe_80):
         for idx_exe,exet_80 in enumerate(charge_exe_80):
            if axet_80 == exet_80:
               exe_80.append(start_exe_80[idx_exe])
               axe_80.append(start_axe_80[idx_axe])
               charges_80.append(exet_80)
               break                              
   # print(starts_100)
   print(len(axe_100))
   print(len(exe_100))
   # plt.figure(figsize=(15, 10))
   plt.plot(charge_exe_100,start_exe_100, label="E-MPSoC", color = 'r', marker='s', linestyle='-',markersize=3)
   plt.plot(charge_axe_100,start_axe_100, label="AXE-F",color = 'g', marker='o', linestyle='-',markersize=3)
   plt.grid(True)
   plt.xlabel("Charging Rate",fontsize=16)
   plt.ylabel("Minimum start window",fontsize=16)
   plt.legend(fontsize=19)  # Increased legend font size
   plt.xticks(fontsize=16)  # Increase tick font size
   plt.yticks(fontsize=16)  # Increase tick font size

   charge_diff = 0
   for idx in range(len(charges_100)):
      charge_diff += (exe_100[idx] - axe_100[idx])/exe_100[idx]*100
   
   print(charge_diff/(len(charges_100)))
   print(len(start_axe_100),len(start_exe_100),len(axe_100))
   # Adjust layout to prevent overlap
   # plt.tight_layout()
   plt.savefig("FIX_CHARGE_FULL_partitioning_100.pdf", format="pdf", dpi=300)
   plt.show()


   # plt.figure(figsize=(15, 10))
   plt.plot(charge_exe_95,start_exe_95, label="E-MPSoC", color = 'r', marker='s', linestyle='-',markersize=3)
   plt.plot(charge_axe_95,start_axe_95, label="AXE-F",color = 'g', marker='o', linestyle='-',markersize=3)
   plt.grid(True)
   plt.xlabel("Charging Rate",fontsize=16)
   plt.ylabel("Minimum start window",fontsize=16)
   plt.legend(fontsize=19)  # Increased legend font size
   plt.xticks(fontsize=16)  # Increase tick font size
   plt.yticks(fontsize=16)  # Increase tick font size

   charge_diff = 0
   for idx in range(len(charges_95)):
      charge_diff += (exe_95[idx] - axe_95[idx])/exe_95[idx]*100
   
   print(charge_diff/(len(charges_95)))
   print(len(start_axe_95),len(start_exe_95),len(axe_95))
   # Adjust layout to prevent overlap
   # plt.tight_layout()
   plt.savefig("FIX_CHARGE_FULL_partitioning_95.pdf", format="pdf", dpi=300)
   plt.show()


   # plt.figure(figsize=(15, 10))
   plt.plot(charge_exe_90,start_exe_90, label="E-MPSoC", color = 'r', marker='s', linestyle='-',markersize=3)
   plt.plot(charge_axe_90,start_axe_90, label="AXE-F",color = 'g', marker='o', linestyle='-',markersize=3)
   plt.grid(True)
   plt.xlabel("Charging Rate",fontsize=16)
   plt.ylabel("Minimum start window",fontsize=16)
   plt.legend(fontsize=19)  # Increased legend font size
   plt.xticks(fontsize=16)  # Increase tick font size
   plt.yticks(fontsize=16)  # Increase tick font size

   charge_diff = 0
   for idx in range(len(charges_90)):
      charge_diff += (exe_90[idx] - axe_90[idx])/exe_90[idx]*100
   
   print(charge_diff/(len(charges_90)))
   print(len(start_axe_90),len(start_exe_90),len(axe_90))
   # Adjust layout to prevent overlap
   # plt.tight_layout()
   plt.savefig("FIX_CHARGE_FULL_partitioning_90.pdf", format="pdf", dpi=300)
   plt.show()



   # plt.figure(figsize=(15, 10))
   plt.plot(charge_exe_80,start_exe_80, label="E-MPSoC", color = 'r', marker='s', linestyle='-',markersize=3)
   plt.plot(charge_axe_80,start_axe_80, label="AXE-F",color = 'g', marker='o', linestyle='-',markersize=3)
   plt.grid(True)
   plt.xlabel("Charging Rate",fontsize=16)
   plt.ylabel("Minimum start window",fontsize=16)
   plt.legend(fontsize=19)  # Increased legend font size
   plt.xticks(fontsize=16)  # Increase tick font size
   plt.yticks(fontsize=16)  # Increase tick font size

   charge_diff = 0
   for idx in range(len(charges_80)):
      charge_diff += (exe_80[idx] - axe_80[idx])/exe_80[idx]*100
   
   print(charge_diff/(len(charges_80)))
   print(len(start_axe_80),len(start_exe_80),len(axe_80))
   # Adjust layout to prevent overlap
   # plt.tight_layout()
   plt.savefig("FIX_CHARGE_FULL_partitioning_80.pdf", format="pdf", dpi=300)
   plt.show()      