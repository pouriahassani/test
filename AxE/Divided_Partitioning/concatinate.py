import sys
import os

# Define the base output directory and cumulative result files
output_dir = "OUTPUT"
axe_filename = os.path.join("./", "AXE_results.csv")
exe_filename = os.path.join("./", "EXE_results.csv")

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Define headers (update these if necessary)
axe_header = "Charging Rate,Start Window,Result,SSE,SST"  # Header for AXE results
exe_header = "Charging Rate,Start Window,Result,SSE,SST"  # Header for EXE results

# Write header to the cumulative files if they do not exist or are empty
if not os.path.exists(axe_filename) or os.path.getsize(axe_filename) == 0:
    with open(axe_filename, "w") as f:
        f.write(axe_header + "\n")

if not os.path.exists(exe_filename) or os.path.getsize(exe_filename) == 0:
    with open(exe_filename, "w") as f:
        f.write(exe_header + "\n")

# Open the cumulative result files in append mode
with open(axe_filename, "a") as axe_file, open(exe_filename, "a") as exe_file:
    for start_charge in range(0, 50):  # Run for 50 iterations (adjust as needed)
        # Generate the specific test filenames based on start_charge
        Start_Charge = float(start_charge*2)
        axe_test_filename = os.path.join(output_dir, f"AXE_{Start_Charge}.csv")
        exe_test_filename = os.path.join(output_dir, f"EXE_{Start_Charge}.csv")

        # Append contents from the AXE test file, skipping its header
        if os.path.exists(axe_test_filename):
            with open(axe_test_filename, 'r') as f_axe:
                lines = f_axe.readlines()
                if len(lines) > 1:
                    print(lines[0])
                    axe_file.writelines(lines[1:])  # Skip the first line (header)
        
        # Append contents from the EXE test file, skipping its header
        if os.path.exists(exe_test_filename):
            with open(exe_test_filename, 'r') as f_exe:
                lines = f_exe.readlines()
                if len(lines) > 1:
                    exe_file.writelines(lines[1:])  # Skip the first line (header)
        
        sys.stdout.flush()  # Ensure output is flushed immediately

print(f"Results successfully appended to {axe_filename} and {exe_filename}")
