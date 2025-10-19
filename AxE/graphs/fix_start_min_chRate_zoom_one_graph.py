import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
import csv
ZOOM = 1
FULL_PARTITIONING = 0
# Load first dataset (EXE)
data_exe = np.loadtxt("EXE_results_biger_range_corrent_power.csv", delimiter=",", skiprows=1)  
charge_vals_exe = data_exe[:, 0]
start_vals_exe = data_exe[:, 1]
result_vals_exe = data_exe[:, 2]

# Load second dataset (FAXE)
data_faxe = np.loadtxt("AXE_results_biger_range_corrent_power.csv", delimiter=",", skiprows=1)  
charge_vals_faxe = data_faxe[:, 0]
start_vals_faxe = data_faxe[:, 1]
result_vals_faxe = data_faxe[:, 2]

# Define start values range
if FULL_PARTITIONING:
   start_values = np.arange(1, 21, 0.1)
else:
   if not ZOOM:
      start_values = np.arange(8, 24, 4)
      n_rows = int(np.ceil(len(start_values) / 2))  # Determine rows for 3 columns layout
      fig, axes = plt.subplots(n_rows, 2, figsize=(20, 5 * n_rows))
      axes = axes.flatten()  # Flatten to easily iterate
   if ZOOM:
      start_values = np.arange(8,24, 4)
      

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
for i, start_val_target in enumerate(start_values):
    # Filter data for EXE
    mask_exe = np.abs(start_vals_exe - start_val_target) <= 0.02 
    filtered_charge_exe = charge_vals_exe[mask_exe]
    filtered_result_exe = result_vals_exe[mask_exe]

    mask_exe = (filtered_charge_exe <=20)
    filtered_charge_exe = filtered_charge_exe[mask_exe]
    filtered_result_exe = filtered_result_exe[mask_exe]
    
    # Filter data for FAXE
    mask_faxe = np.abs(start_vals_faxe - start_val_target) <= 0.02
    filtered_charge_faxe = charge_vals_faxe[mask_faxe]
    filtered_result_faxe = result_vals_faxe[mask_faxe]

        # Filter data for FAXE
    mask_faxe = (filtered_charge_faxe <=20)
    filtered_charge_faxe = filtered_charge_faxe[mask_faxe]
    filtered_result_faxe = filtered_result_faxe[mask_faxe]

    if  not FULL_PARTITIONING:
      
      if ZOOM:
         fig, ax_main = plt.subplots(figsize=(12, 6))
         zoom_charge_faxe = []
         zoom_result_faxe = []
         zoom_result_exe = []
         zoom_charge_exe = []
         first = 0
         last = 0
         for idx in range(len(filtered_charge_faxe)):
            if first ==  1 and last == 0:
               zoom_charge_faxe.append(filtered_charge_faxe[idx])
               zoom_result_faxe.append(filtered_result_faxe[idx])
               if filtered_result_faxe[idx] == 100:
                  if all(x == 100 for x in filtered_result_faxe[idx:]): 
                     break
                  

            if first == 0 and last == 0:
               if filtered_result_faxe[idx] > 0:
                  first = 1
                  print(filtered_charge_faxe[idx])
                  zoom_charge_faxe.append(filtered_charge_faxe[idx-1])
                  zoom_result_faxe.append(0)
                  zoom_charge_faxe.append(filtered_charge_faxe[idx])
                  zoom_result_faxe.append(filtered_result_faxe[idx])

         first = 0
         last = 0
         for idx in range(len(filtered_charge_exe)):
            if first ==  1 and last == 0:
               zoom_charge_exe.append(filtered_charge_exe[idx])
               zoom_result_exe.append(filtered_result_exe[idx])
               if filtered_result_exe[idx] == 100:
                  if all(x == 100 for x in filtered_result_exe[idx:]): 
                     break

            if first == 0 and last == 0:
               if filtered_result_exe[idx] > 0:
                  first = 1
                  print(filtered_charge_exe[idx])
                  zoom_charge_exe.append(filtered_charge_exe[idx-1])
                  zoom_result_exe.append(0)
                  zoom_charge_exe.append(filtered_charge_exe[idx])
                  zoom_result_exe.append(filtered_result_exe[idx])
         for idx in range(len(zoom_charge_exe)):
            if zoom_charge_exe[idx] not in zoom_charge_faxe:
               zoom_charge_faxe.append(zoom_charge_exe[idx])
               zoom_result_faxe.append(100)
         zoom_result_exe_1 = []
         zoom_charge_exe_1 = []
         for idx in range(len(zoom_charge_faxe)):
            if zoom_charge_faxe[idx] not in zoom_charge_exe:
               zoom_charge_exe_1.append(zoom_charge_faxe[idx])
               zoom_result_exe_1.append(0)
         zoom_charge_exe = zoom_charge_exe_1 + zoom_charge_exe
         zoom_result_exe = zoom_result_exe_1  + zoom_result_exe
         ax_main.plot(filtered_charge_exe, filtered_result_exe,   label="E-MPSoC", color = 'r', marker='o', linestyle='-',markersize=3)
         ax_main.plot(filtered_charge_faxe, filtered_result_faxe, label=" FAxE",color = 'g', marker='s', linestyle='-',markersize=3) 
         ax_main.set_xlabel("Battery Charging Rate (P) in mW",fontsize=24)
         ax_main.set_ylabel("Partitioning Success Rate (%)", fontsize=24)
         # ax_main.set_title(f"start_window = {start_val_target:.1f}", fontsize=22)
         ax_main.legend(fontsize=24)
         ax_main.grid(True)
         ax_main.tick_params(axis='both', labelsize=20)  # Increase font size for axis ticks
         # Create inset axes
         ax_inset = inset_axes(ax_main, width=5/2, height=4/2,  # Absolute size in inches
                           bbox_to_anchor=(0.3, 0.3, 0.65, 0.5),  # (x, y, width, height) in figure fraction
                           bbox_transform=ax_main.figure.transFigure)

         x_min = zoom_charge_faxe[0] -1
         x_max = zoom_charge_faxe[0]+3  # Change these as needed
         zoom_charge_exe_1 = zoom_charge_exe.copy()
         zoom_result_exe_1 = zoom_result_exe.copy()
         for i in range(40):
            if x_min + i*0.1  < zoom_charge_exe[0]:
               zoom_charge_exe_1.insert(i,x_min + i*0.1)
               zoom_result_exe_1.insert(0,0)
            if x_min + i*0.1  > zoom_charge_exe[-1]:
               zoom_charge_exe_1.append(x_min + i*0.1)
               zoom_result_exe_1.append(100)


         zoom_charge_faxe_1 = zoom_charge_faxe.copy()
         zoom_result_faxe_1 = zoom_result_faxe.copy()

         for i in range(40):
            if x_min + i*0.1  < zoom_charge_faxe[0]:
               zoom_charge_faxe_1.insert(i,x_min + i*0.1)
               zoom_result_faxe_1.insert(0,0)
            if x_min + i*0.1  > zoom_charge_faxe[-1]:
               zoom_charge_faxe_1.append(x_min + i*0.1)
               zoom_result_faxe_1.append(100)         
         # Zoomed-in plot (Inset)
         ax_inset.plot(zoom_charge_exe_1, zoom_result_exe_1, label="E-MPSoC", color='r', marker='o', linestyle='-', markersize=3)
         ax_inset.plot(zoom_charge_faxe_1, zoom_result_faxe_1, label="FAxE", color='g', marker='s', linestyle='-', markersize=3)
         ax_inset.grid(True)

         # For each axis (e.g., ax_inset, ax_main, etc.)
         xticks = np.arange(x_min, x_max + 1, 1)
         yticks = np.arange(0, 101, 20)
         ax_inset.set_xlim(x_min, x_max)
         ax_inset.set_xticks(xticks)
         ax_inset.set_yticks(yticks)


         ax_inset.tick_params(axis='both', labelsize=12)

         # Draw lines to indicate zoomed-in region
         x1, x2 = zoom_charge_faxe[0], zoom_charge_exe[-1]  # X range of zoomed-in data
         y1, y2 = -1,101  # Y range of zoomed-in data
         mark_inset(ax_main, ax_inset, loc1=2, loc2=4, fc="lightcyan", ec="slateblue", lw=1,linestyle='--') 
         plt.tight_layout()
         filename = str(start_val_target) + "_START_partitioning_success_rate_zoomed.pdf"
         plt.savefig(filename, format="pdf", dpi=300)
         plt.show()

         filename_AXE_all = str(start_val_target) + "_AXE_START_success_rate_all.csv"
         filename_AXE_zoomed = str(start_val_target) + "_AXE_START_success_rate_zoomed.csv"
         filename_EXE_all = str(start_val_target) + "_EXE_START_success_rate_all.csv"
         filename_EXE_zoomed = str(start_val_target) + "_EXE_START_success_rate_zoomed.csv"
         with open(filename_AXE_all, mode="w", newline="") as file:
            writer = csv.writer(file)
            # Writing the header
            writer.writerow(["charging_rate", "suucess_rate"])
            # Writing data in a loop
            for idx in range(len(filtered_charge_faxe)):
               writer.writerow([filtered_charge_faxe[idx], filtered_result_faxe[idx]])
         print(f"Data successfully written to {filename_AXE_all}")

         with open(filename_EXE_all, mode="w", newline="") as file:
            writer = csv.writer(file)
            # Writing the header
            writer.writerow(["charging_rate", "suucess_rate"])
            # Writing data in a loop
            for idx in range(len(filtered_charge_exe)):
               writer.writerow([filtered_charge_exe[idx], filtered_result_exe[idx]])
         print(f"Data successfully written to {filename_EXE_all}")  
         
         with open(filename_AXE_zoomed, mode="w", newline="") as file:
            writer = csv.writer(file)
            # Writing the header
            writer.writerow(["charging_rate", "suucess_rate"])
            # Writing data in a loop
            for idx in range(len(zoom_charge_faxe_1)):
               writer.writerow([zoom_charge_faxe_1[idx], zoom_result_faxe_1[idx]])
         print(f"Data successfully written to {filename_AXE_zoomed}")
         
         with open(filename_EXE_zoomed, mode="w", newline="") as file:
            writer = csv.writer(file)
            # Writing the header
            writer.writerow(["charging_rate", "suucess_rate"])
            # Writing data in a loop
            for idx in range(len(zoom_charge_exe_1)):
               writer.writerow([zoom_charge_exe_1[idx], zoom_result_exe_1[idx]])
         print(f"Data successfully written to {filename_EXE_zoomed}")                    


    
   # FULL partitioning comparissionz
    if FULL_PARTITIONING:
      for idx in range(len(filtered_charge_faxe)):
         diff += ( filtered_result_faxe[idx] - filtered_result_exe[idx])
         len_data +=1
      for idx in range(len(filtered_charge_faxe)):
         if filtered_result_faxe[idx] >= 95:
            start_axe_95.append(start_val_target)
            charge_axe_95.append(filtered_charge_faxe[idx])
            break
      for idx in range(len(filtered_charge_exe)):
         if filtered_result_exe[idx] >= 95:
            start_exe_95.append(start_val_target)
            charge_exe_95.append(filtered_charge_exe[idx])
            break
      for idx in range(len(filtered_charge_faxe)):
         if filtered_result_faxe[idx] >= 90:
            start_axe_90.append(start_val_target)
            charge_axe_90.append(filtered_charge_faxe[idx])
            break
      for idx in range(len(filtered_charge_exe)):
         if filtered_result_exe[idx] >= 90:
            start_exe_90.append(start_val_target)
            charge_exe_90.append(filtered_charge_exe[idx])
            break
      for idx in range(len(filtered_charge_exe)):
         if filtered_result_exe[idx] >= 100:
            start_exe_100.append(start_val_target)
            charge_exe_100.append(filtered_charge_exe[idx])
            break         
      for idx in range(len(filtered_charge_faxe)):
         if filtered_result_faxe[idx] >= 100:
            start_axe_100.append(start_val_target)
            charge_axe_100.append(filtered_charge_faxe[idx])
            break
      for idx in range(len(filtered_charge_exe)):
         if filtered_result_exe[idx] >= 80:
            start_exe_80.append(start_val_target)
            charge_exe_80.append(filtered_charge_exe[idx])
            break        
      for idx in range(len(filtered_charge_faxe)):
         if filtered_result_faxe[idx] >= 80:
            start_axe_80.append(start_val_target)
            charge_axe_80.append(filtered_charge_faxe[idx])
            break                     
# print("start_axe_100 " , start_axe_100)
# print("charge_axe_100 ", charge_axe_100)
# print("start_exe_100 ", start_exe_100)
# print("charge_exe_100" , charge_exe_100)

print(len(start_axe_100))
print(len(charge_axe_100))
print(len(charge_exe_100))
if not FULL_PARTITIONING:
   # if ZOOM:
   #    plt.tight_layout()
   #    plt.savefig("FIXED_START_partitioning_success_rate_zoomed.pdf", format="pdf", dpi=300)
   #    plt.show()
   if not ZOOM:
      plt.tight_layout()
      plt.savefig("FIXED_START_partitioning_success_rate_all.pdf", format="pdf", dpi=300)
      plt.show()

if FULL_PARTITIONING:
   print(diff,len_data)
   print(diff/len_data )
   starts_100 = []
   exe_100 = []
   axe_100 = []
   starts_95 = []
   exe_95 = []
   axe_95 = []
   starts_90 = []
   exe_90 = []
   axe_90 = []
   starts_80 = []
   exe_80 = []
   axe_80 = []   
   for idx_axe,axet_95 in enumerate(start_axe_95):
         # if axet_100 >21:
         #    break
         for idx_exe,exet_95 in enumerate(start_exe_95):
            if np.abs(axet_95 - exet_95)<=0.05:
               exe_95.append(charge_exe_95[idx_exe])
               axe_95.append(charge_axe_95[idx_axe])
               starts_95.append(exet_95)
               break
   for idx_axe,axet_90 in enumerate(start_axe_90):
         # if axet_100 >21:
         #    break
         for idx_exe,exet_90 in enumerate(start_exe_90):
            if np.abs(axet_90 - exet_90)<=0.05:
               exe_90.append(charge_exe_90[idx_exe])
               axe_90.append(charge_axe_90[idx_axe])
               starts_90.append(exet_90)
               break
   for idx_axe,axet_100 in enumerate(start_axe_100):
         # if axet_100 >21:
         #    break
         for idx_exe,exet_100 in enumerate(start_exe_100):
            if np.abs(axet_100 - exet_100)<=0.05:
               exe_100.append(charge_exe_100[idx_exe])
               axe_100.append(charge_axe_100[idx_axe])
               starts_100.append(exet_100)
               break    

   for idx_axe,axet_80 in enumerate(start_axe_80):
         # if axet_80 >21:
         #    break
         for idx_exe,exet_80 in enumerate(start_exe_80):
            if np.abs(axet_80 - exet_80)<=0.05:
               exe_80.append(charge_exe_80[idx_exe])
               axe_80.append(charge_axe_80[idx_axe])
               starts_80.append(exet_80)
               break                                 
   # for idx_axe,axet_100 in enumerate(start_axe_100):
   #       if axet_100 >15:
   #          break
   #       if axet_100 not in starts_100:
   #             exe_100.append(50)
   #             axe_100.append(charge_axe_100[idx_axe])
   #             starts_100.append(axet_100)
   # for idx_exe,exet_100 in enumerate(start_exe_100):
   #       if exet_100 >15:
   #          break
   #       if exet_100 not in starts_100:
   #             exe_100.append(charge_exe_100[idx_exe])
   #             axe_100.append(50)
   #             starts_100.append(exet_100)
               
   print(len(starts_100))
   # print(axe_100)
   # print(exe_100)

   plt.plot(start_exe_100, charge_exe_100, label="E-MPSoC", color = 'r', marker='s', linestyle='--',markersize=3)
   plt.plot(start_axe_100, charge_axe_100, label="F-AxE",color = 'g', marker='o', linestyle='-',markersize=3)
   # Adding grid lines


   plt.grid(True)
   plt.xlabel("start_window", fontsize=16)  # Increased font size
   plt.ylabel("Minimum Charging Rate (P) in mW", fontsize=16)  # Increased font size
   plt.legend(fontsize=15)  # Increased legend font size
   plt.xticks(fontsize=12)  # Increase tick font size
   plt.yticks(fontsize=12)  # Increase tick font size

   charge_diff = 0
   for idx in range(len(starts_100)):
      charge_diff += (exe_100[idx] - axe_100[idx])/exe_100[idx]*100
   
   print(charge_diff/(len(starts_100)))
   print(len(charge_axe_100),len(charge_exe_100),len(axe_100))
   # Adjust layout to prevent overlap
   # plt.tight_layout()
   plt.savefig("FULL_partitioning_CHARGE_100.pdf", format="pdf", dpi=300)
   plt.show()



   plt.plot(start_exe_95, charge_exe_95, label="E-MPSoC", color = 'r', marker='s', linestyle='--',markersize=3)
   plt.plot(start_axe_95, charge_axe_95, label="F-AxE",color = 'g', marker='o', linestyle='-',markersize=3)
   # # Adding grid lines

   plt.grid(True)
   plt.xlabel("start_window", fontsize=16)  # Increased font size
   plt.ylabel("Minimum Charging Rate (P) in mW", fontsize=16)  # Increased font size
   plt.legend(fontsize=15)  # Increased legend font size
   plt.xticks(fontsize=12)  # Increase tick font size
   plt.yticks(fontsize=12)  # Increase tick font size

   charge_diff = 0
   for idx in range(len(starts_95)):
      charge_diff += (exe_95[idx] - axe_95[idx])/exe_95[idx]*100
   
   print(charge_diff/(len(starts_95)))
   print(len(charge_axe_95),len(charge_exe_95),len(axe_95))
   # Adjust layout to prevent overlap
   # plt.tight_layout()
   plt.savefig("FULL_partitioning_CHARGE_95.pdf", format="pdf", dpi=300)
   plt.show()





   plt.plot(start_exe_90, charge_exe_90, label="E-MPSoC", color = 'r', marker='s', linestyle='--',markersize=3)
   plt.plot(start_axe_90, charge_axe_90, label="F-AxE",color = 'g', marker='o', linestyle='-',markersize=3)
   # # Adding grid lines

   plt.grid(True)
   plt.xlabel("start_window", fontsize=16)  # Increased font size
   plt.ylabel("Minimum Charging Rate (P) in mW", fontsize=16)  # Increased font size
   plt.legend(fontsize=15)  # Increased legend font size
   plt.xticks(fontsize=12)  # Increase tick font size
   plt.yticks(fontsize=12)  # Increase tick font size

   charge_diff = 0
   for idx in range(len(starts_90)):
      charge_diff += (exe_90[idx] - axe_90[idx])/exe_90[idx]*100
   
   print(charge_diff/(len(starts_90)))
   print(len(charge_axe_90),len(charge_exe_90),len(axe_90))
   # Adjust layout to prevent overlap
   # plt.tight_layout()
   plt.savefig("FULL_partitioning_CHARGE_90.pdf", format="pdf", dpi=300)
   plt.show()



   plt.plot(start_exe_80, charge_exe_80, label="E-MPSoC", color = 'r', marker='s', linestyle='--',markersize=3)
   plt.plot(start_axe_80, charge_axe_80, label="F-AxE",color = 'g', marker='o', linestyle='-',markersize=3)
   # # Adding grid lines

   plt.grid(True)
   plt.xlabel("start_window", fontsize=16)  # Increased font size
   plt.ylabel("Minimum Charging Rate (P) in mW", fontsize=16)  # Increased font size
   plt.legend(fontsize=15)  # Increased legend font size
   plt.xticks(fontsize=12)  # Increase tick font size
   plt.yticks(fontsize=12)  # Increase tick font size

   charge_diff = 0
   for idx in range(len(starts_80)):
      charge_diff += (exe_80[idx] - axe_80[idx])/exe_80[idx]*100
   
   print(charge_diff/(len(starts_80)))
   print(len(charge_axe_80),len(charge_exe_80),len(axe_80))
   # Adjust layout to prevent overlap
   # plt.tight_layout()
   plt.savefig("FULL_partitioning_CHARGE_80.pdf", format="pdf", dpi=300)
   plt.show()
   axe_start_avg_80 = sum(axe_80)/len(starts_80)      
   exe_start_avg_80 = sum(exe_80)/len(starts_80)     
   print("axe_avg_80", axe_start_avg_80)    
   print("exe_avg_80", exe_start_avg_80)
   print("diff", (exe_start_avg_80 - axe_start_avg_80) / exe_start_avg_80)
   axe_start_avg_90 = sum(axe_90)/len(starts_90)      
   exe_start_avg_90 = sum(exe_90)/len(starts_90)     
   print("axe_avg_90", axe_start_avg_90)    
   print("exe_avg_90", exe_start_avg_90)
   print("diff", (exe_start_avg_90 - axe_start_avg_90) / exe_start_avg_90)
   axe_start_avg_95 = sum(axe_95)/len(starts_95)      
   exe_start_avg_95 = sum(exe_95)/len(starts_95)     
   print("axe_avg_95", axe_start_avg_95)    
   print("exe_avg_95", exe_start_avg_95)
   print("diff", (exe_start_avg_95 - axe_start_avg_95) / exe_start_avg_95)
   axe_start_avg_100 = sum(axe_100)/len(starts_100)      
   exe_start_avg_100 = sum(exe_100)/len(starts_100)     
   print("axe_avg_100", axe_start_avg_100)    
   print("exe_avg_100", exe_start_avg_100)
   print("diff", (exe_start_avg_100- axe_start_avg_100) / exe_start_avg_100)

   filename_AXE_80 = "FIX_START_AXE_FULL_partitioning_80.csv"
   filename_AXE_90 = "FIX_START_AXE_FULL_partitioning_90.csv"
   filename_AXE_95 = "FIX_START_AXE_FULL_partitioning_95.csv"
   filename_AXE_100 ="FIX_START_AXE_FULL_partitioning_100.csv"
   filename_EXE_80 = "FIX_START_EXE_FULL_partitioning_80.csv"
   filename_EXE_90 = "FIX_START_EXE_FULL_partitioning_90.csv"
   filename_EXE_95 = "FIX_START_EXE_FULL_partitioning_95.csv"
   filename_EXE_100 ="FIX_START_EXE_FULL_partitioning_100.csv"
   # Writing to CSV file
   with open(filename_AXE_80, mode="w", newline="") as file:
      writer = csv.writer(file)
      
      # Writing the header
      writer.writerow(["x", "y_faxe"])
      
      # Writing data in a loop
      for idx in range(len(start_axe_80)):
         writer.writerow([start_axe_80[idx], charge_axe_80[idx]])

   print(f"Data successfully written to {filename_AXE_80}")

   with open(filename_AXE_90, mode="w", newline="") as file:
      writer = csv.writer(file)
      
      # Writing the header
      writer.writerow(["x", "y_faxe"])
      
      # Writing data in a loop
      for idx in range(len(start_axe_90)):
         writer.writerow([start_axe_90[idx], charge_axe_90[idx]])

   print(f"Data successfully written to {filename_AXE_90}")



   with open(filename_AXE_95, mode="w", newline="") as file:
      writer = csv.writer(file)
      
      # Writing the header
      writer.writerow(["x", "y_faxe"])
      
      # Writing data in a loop
      for idx in range(len(start_axe_95)):
         writer.writerow([start_axe_95[idx], charge_axe_95[idx]])

   print(f"Data successfully written to {filename_AXE_95}")

   with open(filename_AXE_100, mode="w", newline="") as file:
      writer = csv.writer(file)
      
      # Writing the header
      writer.writerow(["x", "y_faxe"])
      
      # Writing data in a loop
      for idx in range(len(start_axe_100)):
         writer.writerow([start_axe_100[idx], charge_axe_100[idx]])

   print(f"Data successfully written to {filename_AXE_100}")  

   with open(filename_EXE_80, mode="w", newline="") as file:
      writer = csv.writer(file)
      
      # Writing the header
      writer.writerow(["x", "exe"])
      
      # Writing data in a loop
      for idx in range(len(start_exe_80)):
         writer.writerow([start_exe_80[idx], charge_exe_80[idx]])

   print(f"Data successfully written to {filename_EXE_80}")

   with open(filename_EXE_90, mode="w", newline="") as file:
      writer = csv.writer(file)
      
      # Writing the header
      writer.writerow(["x", "exe"])
      
      # Writing data in a loop
      for idx in range(len(start_exe_90)):
         writer.writerow([start_exe_90[idx], charge_exe_90[idx]])

   print(f"Data successfully written to {filename_EXE_90}")



   with open(filename_EXE_95, mode="w", newline="") as file:
      writer = csv.writer(file)
      
      # Writing the header
      writer.writerow(["x", "exe"])
      
      # Writing data in a loop
      for idx in range(len(start_exe_95)):
         writer.writerow([start_exe_95[idx], charge_exe_95[idx]])

   print(f"Data successfully written to {filename_EXE_95}")

   with open(filename_EXE_100, mode="w", newline="") as file:
      writer = csv.writer(file)
      
      # Writing the header
      writer.writerow(["x", "exe"])
      
      # Writing data in a loop
      for idx in range(len(start_exe_100)):
         writer.writerow([start_exe_100[idx], charge_exe_100[idx]])

   print(f"Data successfully written to {filename_EXE_100}")  