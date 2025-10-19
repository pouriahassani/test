import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
ZOOM = 1
FULL_PARTITIONING = 0
metric = "SSE"
# Load first dataset (EXE)
data_exe = np.loadtxt("EXE_results_biger_range_corrent_power.csv", delimiter=",", skiprows=1)  
charge_vals_exe = data_exe[:, 0]
start_vals_exe = data_exe[:, 1]
if metric == "SSE":
   result_vals_exe = data_exe[:, 3]
if metric == "SST":
   result_vals_exe = data_exe[:, 4]
if metric == "result":
   result_vals_exe = data_exe[:, 2]  

# Load second dataset (FAXE)
data_faxe = np.loadtxt("AXE_results_biger_range_corrent_power.csv", delimiter=",", skiprows=1)  
charge_vals_faxe = data_faxe[:, 0]
start_vals_faxe = data_faxe[:, 1]
if metric == "SSE":
   result_vals_faxe = data_faxe[:, 3]
if metric == "SST":
   result_vals_faxe = data_faxe[:, 4]
if metric == "result":
   result_vals_faxe = data_faxe[:, 2]   

# Define start values range
if FULL_PARTITIONING:
   charge_values = np.arange(0, 20, 0.1)
else:
   charge_values = np.arange(7, 15, 2)




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
      fig, ax_main = plt.subplots(figsize=(10, 6))
      if ZOOM:
         zoom_start_faxe = []
         zoom_result_faxe = []
         zoom_result_exe = []
         zoom_start_exe = []
         first = 0
         last = 0
         if metric == "SSE" or "SST":
            MIN = 100
            MAX = 0
         else:
            MIN = 0
            MAX = 100
         for idx in range(len(filtered_start_faxe)):
            if first ==  1 and last == 0:
               zoom_start_faxe.append(filtered_start_faxe[idx])
               zoom_result_faxe.append(filtered_result_faxe[idx])
               if filtered_result_faxe[idx] == MAX:
                  if all(x == MAX for x in filtered_result_faxe[idx:]): 
                     break

            if first == 0 and last == 0:
               if filtered_result_faxe[idx] < MIN:
                  first = 1
                  zoom_start_faxe.append(filtered_start_faxe[idx])
                  zoom_result_faxe.append(MIN)

         first = 0
         last = 0
         for idx in range(len(filtered_start_exe)):
            if first ==  1 and last == 0:
               zoom_start_exe.append(filtered_start_exe[idx])
               zoom_result_exe.append(filtered_result_exe[idx])
               if filtered_result_exe[idx] == MAX:
                  if all(x == MAX for x in filtered_result_exe[idx:]): 
                     break

            if first == 0 and last == 0:
               if filtered_result_exe[idx] < MIN:
                  first = 1
                  zoom_start_exe.append(filtered_start_exe[idx])
                  zoom_result_exe.append(MIN)
         for idx in range(len(zoom_start_exe)):
            if zoom_start_exe[idx] not in zoom_start_faxe:
               zoom_start_faxe.append(zoom_start_exe[idx])
               zoom_result_faxe.append(100)
         ax_main.plot(filtered_start_exe, filtered_result_exe,   label="E-MPSoC", color = 'r', marker='o', linestyle='-',markersize=3)
         ax_main.plot(filtered_start_faxe, filtered_result_faxe, label=" FAxE",color = 'g', marker='s', linestyle='-',markersize=3) 
         ax_main.set_xlabel("start_window",fontsize=20)
         ax_main.set_ylabel("Partitioning Success Rate (%)", fontsize=20)
         # ax_main.set_title(f"start_window = {start_val_target:.1f}", fontsize=22)
         ax_main.legend(fontsize=19)
         ax_main.grid(True)
         ax_main.tick_params(axis='both', labelsize=16)  # Increase font size for axis ticks
         # Create inset axes
         ax_inset = inset_axes(ax_main, width=5/2, height=4/2,  # Absolute size in inches
                           bbox_to_anchor=(-0.1, 0.3, 0.65, 0.5),  # (x, y, width, height) in figure fraction
                           bbox_transform=ax_main.figure.transFigure)


         # Zoomed-in plot (Inset)
         ax_inset.plot(zoom_start_exe, zoom_result_exe, label="E-MPSoC", color='r', marker='o', linestyle='-', markersize=3)
         ax_inset.plot(zoom_start_faxe, zoom_result_faxe, label="FAxE", color='g', marker='s', linestyle='-', markersize=3)

         # ax_inset.set_xlabel("Battery Charging Rate (P) in mW", fontsize=10)
         # ax_inset.set_ylabel("Partitioning Success Rate (%)", fontsize=10)
         # ax_inset.set_title(f"Zoomed-in (start_window={start_val_target:.1f})", fontsize=12)
         # ax_inset.legend(fontsize=8)
         ax_inset.grid(True)
         ax_inset.tick_params(axis='both', labelsize=16)

         # Draw lines to indicate zoomed-in region
         x1, x2 = zoom_start_faxe[0], zoom_start_exe[-1]  # X range of zoomed-in data
         y1, y2 = -1,101  # Y range of zoomed-in data
         mark_inset(ax_main, ax_inset, loc1=2, loc2=4, fc="lightcyan", ec="slateblue", lw=1,linestyle='--') 
         # Automatically draw lines to indicate the zoomed-in region
         # ax_main.indicate_inset_zoom(ax_inset, 
         #                            # color='blue',      # Set the color of the lines
         #                            linewidth=2,      # Set line thickness
         #                            linestyle='--',   # Set line style to dashed
         #                            edgecolor='none') 
         # ax_main.add_patch(plt.Rectangle((x1, y1), x2-x1, y2-y1, edgecolor="blue", linewidth=1, linestyle="--", fill=False))
         plt.tight_layout()
         filename = str(charge_val_target) + "_CHARGE_" + metric + "_zoomed.pdf"
         plt.savefig(filename, format="pdf", dpi=300)
         plt.show()
    
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

   plt.plot(charge_exe_100,start_exe_100, label="EXE", color = 'r', marker='s', linestyle='--',markersize=3)
   plt.plot(charge_axe_100,start_axe_100, label="FAXE",color = 'g', marker='o', linestyle='-',markersize=3)
   plt.grid(True)
   plt.xlabel("Charging Rate",fontsize=16)
   plt.ylabel("Minimum start window",fontsize=16)
   plt.legend(fontsize=15)  # Increased legend font size
   plt.xticks(fontsize=12)  # Increase tick font size
   plt.yticks(fontsize=12)  # Increase tick font size

   charge_diff = 0
   for idx in range(len(charges_100)):
      charge_diff += (exe_100[idx] - axe_100[idx])/exe_100[idx]*100
   
   print(charge_diff/(len(charges_100)))
   print(len(start_axe_100),len(start_exe_100),len(axe_100))
   # Adjust layout to prevent overlap
   # plt.tight_layout()
   plt.savefig("FIX_CHARGE_FULL_partitioning_100.pdf", format="pdf", dpi=300)
   plt.show()

   plt.plot(charge_exe_95,start_exe_95, label="EXE", color = 'r', marker='s', linestyle='--',markersize=3)
   plt.plot(charge_axe_95,start_axe_95, label="FAXE",color = 'g', marker='o', linestyle='-',markersize=3)
   plt.grid(True)
   plt.xlabel("Charging Rate",fontsize=16)
   plt.ylabel("Minimum start window",fontsize=16)
   plt.legend(fontsize=15)  # Increased legend font size
   plt.xticks(fontsize=12)  # Increase tick font size
   plt.yticks(fontsize=12)  # Increase tick font size

   charge_diff = 0
   for idx in range(len(charges_95)):
      charge_diff += (exe_95[idx] - axe_95[idx])/exe_95[idx]*100
   
   print(charge_diff/(len(charges_95)))
   print(len(start_axe_95),len(start_exe_95),len(axe_95))
   # Adjust layout to prevent overlap
   # plt.tight_layout()
   plt.savefig("FIX_CHARGE_FULL_partitioning_95.pdf", format="pdf", dpi=300)
   plt.show()

   plt.plot(charge_exe_90,start_exe_90, label="EXE", color = 'r', marker='s', linestyle='--',markersize=4)
   plt.plot(charge_axe_90,start_axe_90, label="FAXE",color = 'g', marker='o', linestyle='-',markersize=4)
   plt.grid(True)
   plt.xlabel("Charging Rate",fontsize=16)
   plt.ylabel("Minimum start window",fontsize=16)
   plt.legend(fontsize=15)  # Increased legend font size
   plt.xticks(fontsize=12)  # Increase tick font size
   plt.yticks(fontsize=12)  # Increase tick font size

   charge_diff = 0
   for idx in range(len(charges_90)):
      charge_diff += (exe_90[idx] - axe_90[idx])/exe_90[idx]*100
   
   print(charge_diff/(len(charges_90)))
   print(len(start_axe_90),len(start_exe_90),len(axe_90))
   # Adjust layout to prevent overlap
   # plt.tight_layout()
   plt.savefig("FIX_CHARGE_FULL_partitioning_90.pdf", format="pdf", dpi=300)
   plt.show()

   plt.plot(charge_exe_80,start_exe_80, label="EXE", color = 'r', marker='s', linestyle='--',markersize=4)
   plt.plot(charge_axe_80,start_axe_80, label="FAXE",color = 'g', marker='o', linestyle='-',markersize=4)
   plt.grid(True)
   plt.xlabel("Charging Rate",fontsize=16)
   plt.ylabel("Minimum start window",fontsize=16)
   plt.legend(fontsize=15)  # Increased legend font size
   plt.xticks(fontsize=12)  # Increase tick font size
   plt.yticks(fontsize=12)  # Increase tick font size

   charge_diff = 0
   for idx in range(len(charges_80)):
      charge_diff += (exe_80[idx] - axe_80[idx])/exe_80[idx]*100
   
   print(charge_diff/(len(charges_80)))
   print(len(start_axe_80),len(start_exe_80),len(axe_80))
   # Adjust layout to prevent overlap
   # plt.tight_layout()
   plt.savefig("FIX_CHARGE_FULL_partitioning_80.pdf", format="pdf", dpi=300)
   plt.show()      