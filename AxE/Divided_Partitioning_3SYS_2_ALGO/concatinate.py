import sys
import os

# Define the base output directory and cumulative result files
output_dir = "OUTPUT"
axe_MIN_SSE_filename = os.path.join("./", "AXE_MIN_SSE_results.csv")
exe_MIN_SSE_filename = os.path.join("./", "EXE_MIN_SSE_results.csv")
axe_MIN_SST_filename = os.path.join("./",  "AXE_MIN_SST_results.csv")
exe_MIN_SST_filename = os.path.join("./",  "EXE_MIN_SST_results.csv")
axe_NP_filename = os.path.join("./",      "AXE_NP_results.csv")
exe_NP_filename = os.path.join("./",      "EXE_NP_results.csv")
FULL_MIN_SSE_filename = os.path.join("./","FULL_MIN_SSE_results.csv")
FULL_MIN_SST_filename = os.path.join("./","FULL_MIN_SST_results.csv")
FULL_NP_filename = os.path.join("./",     "FULL_NP_results.csv")


# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Define headers (update these if necessary)
axe_MIN_SSE_header = "Charging Rate,Start Window,Result,SSE,SST"  # Header for axe_MIN_SSE results
exe_MIN_SSE_header = "Charging Rate,Start Window,Result,SSE,SST"  # Header for exe_MIN_SSE results
FULL_MIN_SSE_header = "Charging Rate,Start Window,Result,SSE,SST"  # Header for FULL_MIN_SSE results
# Write header to the cumulative files if they do not exist or are empty
if not os.path.exists(axe_MIN_SSE_filename) or os.path.getsize(axe_MIN_SSE_filename) == 0:
    with open(axe_MIN_SSE_filename, "w") as f:
        f.write(axe_MIN_SSE_header + "\n")

if not os.path.exists(exe_MIN_SSE_filename) or os.path.getsize(exe_MIN_SSE_filename) == 0:
    with open(exe_MIN_SSE_filename, "w") as f:
        f.write(exe_MIN_SSE_header + "\n")

if not os.path.exists(FULL_MIN_SSE_filename) or os.path.getsize(FULL_MIN_SSE_filename) == 0:
    with open(FULL_MIN_SSE_filename, "w") as f:
        f.write(FULL_MIN_SSE_header + "\n")

# Define headers (update these if necessary)
axe_MIN_SST_header = "Charging Rate,Start Window,Result,SSE,SST"  # Header for axe_MIN_SST results
exe_MIN_SST_header = "Charging Rate,Start Window,Result,SSE,SST"  # Header for exe_MIN_SST results
FULL_MIN_SST_header = "Charging Rate,Start Window,Result,SSE,SST"  # Header for FULL_MIN_SST results
# Write header to the cumulative files if they do not exist or are empty
if not os.path.exists(axe_MIN_SST_filename) or os.path.getsize(axe_MIN_SST_filename) == 0:
    with open(axe_MIN_SST_filename, "w") as f:
        f.write(axe_MIN_SST_header + "\n")

if not os.path.exists(exe_MIN_SST_filename) or os.path.getsize(exe_MIN_SST_filename) == 0:
    with open(exe_MIN_SST_filename, "w") as f:
        f.write(exe_MIN_SST_header + "\n")

if not os.path.exists(FULL_MIN_SST_filename) or os.path.getsize(FULL_MIN_SST_filename) == 0:
    with open(FULL_MIN_SST_filename, "w") as f:
        f.write(FULL_MIN_SST_header + "\n")

# Define headers (update these if necessary)
axe_NP_header = "Charging Rate,Start Window,Result,SSE,SST"  # Header for axe_NP results
exe_NP_header = "Charging Rate,Start Window,Result,SSE,SST"  # Header for exe_NP results
FULL_NP_header = "Charging Rate,Start Window,Result,SSE,SST"  # Header for FULL_NP results
# Write header to the cumulative files if they do not exist or are empty
if not os.path.exists(axe_NP_filename) or os.path.getsize(axe_NP_filename) == 0:
    with open(axe_NP_filename, "w") as f:
        f.write(axe_NP_header + "\n")

if not os.path.exists(exe_NP_filename) or os.path.getsize(exe_NP_filename) == 0:
    with open(exe_NP_filename, "w") as f:
        f.write(exe_NP_header + "\n")

if not os.path.exists(FULL_NP_filename) or os.path.getsize(FULL_NP_filename) == 0:
    with open(FULL_NP_filename, "w") as f:
        f.write(FULL_NP_header + "\n")



# Open the cumulative result files in append mode
with open(axe_MIN_SSE_filename, "a") as axe_MIN_SSE_file, open(exe_MIN_SSE_filename, "a") as exe_MIN_SSE_file:
    for start_charge in range(0, 50):  # Run for 50 iterations (adjust as needed)
        # Generate the specific test filenames based on start_charge
        Start_Charge = float(start_charge)
        axe_MIN_SSE_test_filename = os.path.join(output_dir, f"axe_MIN_SSE_{Start_Charge}.csv")
        exe_MIN_SSE_test_filename = os.path.join(output_dir, f"exe_MIN_SSE_{Start_Charge}.csv")

        # Append contents from the axe_MIN_SSE test file, skipping its header
        if os.path.exists(axe_MIN_SSE_test_filename):
            with open(axe_MIN_SSE_test_filename, 'r') as f_axe_MIN_SSE:
                lines = f_axe_MIN_SSE.readlines()
                if len(lines) > 1:
                    print(lines[0])
                    axe_MIN_SSE_file.writelines(lines[1:])  # Skip the first line (header)
        
        # Append contents from the exe_MIN_SSE test file, skipping its header
        if os.path.exists(exe_MIN_SSE_test_filename):
            with open(exe_MIN_SSE_test_filename, 'r') as f_exe_MIN_SSE:
                lines = f_exe_MIN_SSE.readlines()
                if len(lines) > 1:
                    exe_MIN_SSE_file.writelines(lines[1:])  # Skip the first line (header)
        
        sys.stdout.flush()  # Ensure output is flushed immediately

print(f"Results successfully appended to {axe_MIN_SSE_filename} and {exe_MIN_SSE_filename}")

with open(axe_MIN_SST_filename, "a") as axe_MIN_SST_file, open(exe_MIN_SST_filename, "a") as exe_MIN_SST_file:
    for start_charge in range(0, 50):  # Run for 50 iterations (adjust as needed)
        # Generate the specific test filenames based on start_charge
        Start_Charge = float(start_charge)
        axe_MIN_SST_test_filename = os.path.join(output_dir, f"axe_MIN_SST_{Start_Charge}.csv")
        exe_MIN_SST_test_filename = os.path.join(output_dir, f"exe_MIN_SST_{Start_Charge}.csv")

        # Append contents from the axe_MIN_SST test file, skipping its header
        if os.path.exists(axe_MIN_SST_test_filename):
            with open(axe_MIN_SST_test_filename, 'r') as f_axe_MIN_SST:
                lines = f_axe_MIN_SST.readlines()
                if len(lines) > 1:
                    print(lines[0])
                    axe_MIN_SST_file.writelines(lines[1:])  # Skip the first line (header)
        
        # Append contents from the exe_MIN_SST test file, skipping its header
        if os.path.exists(exe_MIN_SST_test_filename):
            with open(exe_MIN_SST_test_filename, 'r') as f_exe_MIN_SST:
                lines = f_exe_MIN_SST.readlines()
                if len(lines) > 1:
                    exe_MIN_SST_file.writelines(lines[1:])  # Skip the first line (header)
        
        sys.stdout.flush()  # Ensure output is flushed immediately

print(f"Results successfully appended to {axe_MIN_SST_filename} and {exe_MIN_SST_filename}")

with open(axe_NP_filename, "a") as axe_NP_file, open(exe_NP_filename, "a") as exe_NP_file:
    for start_charge in range(0, 50):  # Run for 50 iterations (adjust as needed)
        # Generate the specific test filenames based on start_charge
        Start_Charge = float(start_charge)
        axe_NP_test_filename = os.path.join(output_dir, f"axe_NP_{Start_Charge}.csv")
        exe_NP_test_filename = os.path.join(output_dir, f"exe_NP_{Start_Charge}.csv")

        # Append contents from the axe_NP test file, skipping its header
        if os.path.exists(axe_NP_test_filename):
            with open(axe_NP_test_filename, 'r') as f_axe_NP:
                lines = f_axe_NP.readlines()
                if len(lines) > 1:
                    print(lines[0])
                    axe_NP_file.writelines(lines[1:])  # Skip the first line (header)
        
        # Append contents from the exe_NP test file, skipping its header
        if os.path.exists(exe_NP_test_filename):
            with open(exe_NP_test_filename, 'r') as f_exe_NP:
                lines = f_exe_NP.readlines()
                if len(lines) > 1:
                    exe_NP_file.writelines(lines[1:])  # Skip the first line (header)
        
        sys.stdout.flush()  # Ensure output is flushed immediately

print(f"Results successfully appended to {axe_NP_filename} and {exe_NP_filename}")

with open(FULL_MIN_SST_filename, "a") as FULL_MIN_SST_file:
    for start_charge in range(0, 50):  # Run for 50 iterations (adjust as needed)
        # Generate the specific test filenames based on start_charge
        Start_Charge = float(start_charge)
        FULL_MIN_SST_test_filename = os.path.join(output_dir, f"FULL_MIN_SST_{Start_Charge}.csv")

        # Append contents from the FULL_MIN_SST test file, skipping its header
        if os.path.exists(FULL_MIN_SST_test_filename):
            with open(FULL_MIN_SST_test_filename, 'r') as f_FULL_MIN_SST:
                lines = f_FULL_MIN_SST.readlines()
                if len(lines) > 1:
                    print(lines[0])
                    FULL_MIN_SST_file.writelines(lines[1:])  # Skip the first line (header)
        
        sys.stdout.flush()  # Ensure output is flushed immediately

print(f"Results successfully appended to {FULL_MIN_SST_filename} and {exe_MIN_SST_filename}")

with open(FULL_MIN_SSE_filename, "a") as FULL_MIN_SSE_file:
    for start_charge in range(0, 50):  # Run for 50 iterations (adjust as needed)
        # Generate the specific test filenames based on start_charge
        Start_Charge = float(start_charge)
        FULL_MIN_SSE_test_filename = os.path.join(output_dir, f"FULL_MIN_SSE_{Start_Charge}.csv")

        # Append contents from the FULL_MIN_SSE test file, skipping its header
        if os.path.exists(FULL_MIN_SSE_test_filename):
            with open(FULL_MIN_SSE_test_filename, 'r') as f_FULL_MIN_SSE:
                lines = f_FULL_MIN_SSE.readlines()
                if len(lines) > 1:
                    print(lines[0])
                    FULL_MIN_SSE_file.writelines(lines[1:])  # Skip the first line (header)
        
        sys.stdout.flush()  # Ensure output is flushed immediately

print(f"Results successfully appended to {FULL_MIN_SSE_filename} and {exe_MIN_SST_filename}")

with open(FULL_NP_filename, "a") as FULL_NP_file:
    for start_charge in range(0, 50):  # Run for 50 iterations (adjust as needed)
        # Generate the specific test filenames based on start_charge
        Start_Charge = float(start_charge)
        FULL_NP_test_filename = os.path.join(output_dir, f"FULL_NP_{Start_Charge}.csv")

        # Append contents from the FULL_NP test file, skipping its header
        if os.path.exists(FULL_NP_test_filename):
            with open(FULL_NP_test_filename, 'r') as f_FULL_NP:
                lines = f_FULL_NP.readlines()
                if len(lines) > 1:
                    print(lines[0])
                    FULL_NP_file.writelines(lines[1:])  # Skip the first line (header)
        
        sys.stdout.flush()  # Ensure output is flushed immediately

print(f"Results successfully appended to {FULL_NP_filename} and {exe_MIN_SST_filename}")