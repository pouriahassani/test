
import matplotlib.pyplot as plt
import numpy as np

import os
import shutil 
import random
from Node import *
from Prg import *
from Arch import *
from system import *
from Bookie import *
import numpy as np
# Simulation parameters
STEPS = 20  # Number of steps to shift the window of values
# The application's execution time (Ci) will be multiplied by a random value picked from the window of values
# to generate corresponding deadlines and periods.
SHIFT_WINDOW = 0.25 # we shift the window by SHIFT_WINDOW at each step
START_OF_WINDOW = 1 # The lower bound of the window 
WINDOW_BOUND = 5 # The bound of the window. Now the 
# staring window will be [1:6]. In the step number s=n 
# the window will be [n*SHIFT_WINDOW+START_OF_WINDOW,n*SHIFT_WINDOW+START_OF_WINDOW + WINDOW_BOUND ]
ITR_PER_WINDOW = 10 #Number of iterarions per window to reach reliable results
CHARGE_STEPS = 5 #Increase the charging rate in CHARGE_STEPS and see the paritiong sucess rate change
PROGRAMS_INSTANCES = 10
# ~ 4757098
e_mw = 9.175
# ~ a_mw = 4.93
a_mw = 8.735

NONE = 4.25
I1 = 5.07
I2 = 4.76
F_Units_1 = 4.141
F_Units_2 = 4.011

# Power consumption of different core settings

# No multiplication
I0_F0_mw = NONE
# Only Exact Int
I1_F0_mw = I1 
# Only Approximate int
I2_F0_mw = I2
# Only Exact Float
I0_F1_mw = NONE + F_Units_1
# Only approximate Float
I0_F2_mw = NONE + F_Units_2
# Exact Int and Exact Float
I1_F1_mw = I1 + F_Units_1
# Exact Int and Approximate Float
I1_F2_mw = I1 + F_Units_2
# Approximate Int and Exact Float
I2_F1_mw = I2 + F_Units_1
# Approximate Int and Approximate Float
I2_F2_mw = I2 + F_Units_2

WCPC = I1_F1_mw # Worst case power comsumption shows the power cosnsumption of the highest power consuming node

CHARGE_INITIAL = 2000000
CHARGING_RATE = 20
def Correct_Nodes(NODES,prg):
    available_nodes = []
    for node in NODES:
        available_nodes.append(node)
    Correct_nodes = []
    # Prg doesn't have Integer multiplication
    if prg.Int_pref == 0:
        # prg dosn't have float multiplication
        if prg.Float_pref == 0:
            Correct_nodes = available_nodes
            return Correct_nodes
        
        # Prg requires exact Float multiplication
        if prg.Float_pref == 1:
            for node in available_nodes:
                if node.arch.Float_Type == 1:
                    Correct_nodes.append(node)
            return Correct_nodes
        
        # Prg has Float multiplication and it can be approximate
        if prg.Float_pref == 2:
            for node in available_nodes:
                if node.arch.Float_Type != 0:
                    Correct_nodes.append(node)
            return Correct_nodes
        
    # Prg requires exact Integer multiplication
    if prg.Int_pref == 1:
        # prg dosn't have float multiplication
        if prg.Float_pref == 0:
            for node in available_nodes:
                if node.arch.Int_Type == 1:
                    Correct_nodes.append(node)
            return Correct_nodes
        
        # Prg requires exact Float multiplication
        if prg.Float_pref == 1:
            for node in available_nodes:
                if node.arch.Int_Type == 1 and node.arch.Float_Type == 1:
                    Correct_nodes.append(node)
            return Correct_nodes
        
        # Prg has Float multiplication and it can be approximate
        if prg.Float_pref == 2:
            for node in available_nodes:
                if node.arch.Int_Type == 1 and node.arch.Float_Type != 0:
                        Correct_nodes.append(node)
            return Correct_nodes
    # Prg has Integer multiplication and it can be approximate
    if prg.Int_pref == 2:
        # prg dosn't have float multiplication
        if prg.Float_pref == 0:
            for node in available_nodes:
                if node.arch.Int_Type != 0:
                    Correct_nodes.append(node)
            return Correct_nodes
        
        # Prg requires exact Float multiplication
        if prg.Float_pref == 1:
            for node in available_nodes:
                if node.arch.Int_Type != 0 and node.arch.Float_Type == 1:
                    Correct_nodes.append(node)
            return Correct_nodes
        
        # Prg has Float multiplication and it can be approximate
        if prg.Float_pref == 2:
            for node in available_nodes:
                if node.arch.Int_Type != 0 and node.arch.Float_Type != 0:
                        Correct_nodes.append(node)
            return Correct_nodes
    return Correct_nodes


def calculate_SSE(node,program,system):
    prgs = []
    for prg in node.prgs:
        prgs.append(prg)
    prgs.append(program)
    deadlines = []
    releases = []
    SSE = []
    for prg in prgs:
        deadlines.append(prg.deadline)
        releases.append(prg.release)
    min_SSE_T1T2 = float("inf")
    for release in releases:
        for deadline in deadlines:
            if deadline >= release:
                available_charge = system.charge_initial + system.charging_rate*(deadline - release)
                g_release_deadline = 0
                for prg in prgs:
                    if prg.release >= release and prg.deadline <= deadline:
                        g_release_deadline += prg.get_c(node.arch.get_i()) * node.arch.get_power()
                sse_t1t2 = available_charge - g_release_deadline
                if min_SSE_T1T2 > sse_t1t2:
                    g = g_release_deadline
                    C_EP = available_charge
    return g/C_EP
                    
def calculate_SST(node,program,system):
    prgs = []
    for prg in node.prgs:
        prgs.append(prg)
    prgs.append(program)
    deadlines = []
    releases = []
    for prg in prgs:
        deadlines.append(prg.deadline)
        releases.append(prg.release)
    min_SST_T1T2 = float("inf")
    for release in releases:
        for deadline in deadlines:
            if deadline >= release:
                available_time = deadline - release
                h_release_deadline = 0
                for prg in prgs:
                    if prg.release >= release and prg.deadline <= deadline:
                        h_release_deadline += prg.get_c(node.arch.get_i()) 
                sst_t1t2 = available_time - h_release_deadline
                if min_SST_T1T2 > sst_t1t2:
                    h = h_release_deadline
                    t1_t2 = available_time
    return h/t1_t2                   


def partition(prgs, system):
    # sort the prgs using their worst case power consumption
    prgs = sorted(prgs, key=lambda Prg: Prg.get_c(0) * WCPC,reverse=True)
    for prg in prgs:
        correct_nodes = Correct_Nodes(system.nodes,prg)
        NODESS = Correct_Nodes(system.nodes,prg)
        for node in correct_nodes:
            node.arch.potential_sse = calculate_SSE(node,prg,system)
            node.arch.potential_sst = calculate_SST(node,prg,system)
            if node.arch.potential_sse > 1 or node.arch.potential_sst > 1:
                correct_nodes.remove(node)
        if not correct_nodes:
            return 0
        candidate_nodes = []
        for node in correct_nodes:
            if abs(node.arch.potential_sse - node.arch.potential_sst) < abs(node.arch.sse - node.arch.sst):
                candidate_nodes.append(node)
        if not candidate_nodes: 
            correct_nodes.sort(key=lambda Node:Node.arch.get_power()) 
            correct_nodes[0].prgs.append(prg) 
            correct_nodes[0].arch.sse = correct_nodes[0].arch.potential_sse
            correct_nodes[0].arch.sst = correct_nodes[0].arch.potential_sst
        else:
            candidate_nodes.sort(key=lambda Node:Node.arch.get_power()) 
            candidate_nodes[0].prgs.append(prg) 
            candidate_nodes[0].arch.sse = candidate_nodes[0].arch.potential_sse
            candidate_nodes[0].arch.sst = candidate_nodes[0].arch.potential_sst
    return 1
                
        




# Create the architecture and assign Names and power
arch_I0_F0      = Arch( 0,I0_F0_mw,0,0 )            # No multiplication
arch_I1_F0      = Arch( 0,I1_F0_mw,1,0 )            # Only Exact Int
arch_I2_F0      = Arch( 1,I2_F0_mw,2,0 )            # Only Approximate int
arch_I0_F1      = Arch( 0,I0_F1_mw,0,1 )            # Only Exact Float
arch_I0_F2      = Arch( 0,I0_F2_mw,0,2 )            # Only approximate Float
arch_I1_F1      = Arch( 0,I1_F1_mw,1,1 )            # Exact Int and Exact Float
arch_I1_F2      = Arch( 0,I1_F2_mw,1,2 )            # Exact Int and Approximate Float
arch_I2_F1      = Arch( 1,I2_F1_mw,2,1 )            # Approximate Int and Exact Float
arch_I2_F2      = Arch( 1,I2_F2_mw,2,2 )            # Approximate Int and Approximate Float



archs = [arch_I0_F0,
         arch_I1_F0,
         arch_I2_F0,
         arch_I0_F1,
         arch_I0_F2,
         arch_I1_F1,
         arch_I1_F2,
         arch_I2_F1,
         arch_I2_F2]
arch_EXE = [arch_I0_F0,
         arch_I1_F0,
         arch_I1_F0,
         arch_I0_F1,
         arch_I0_F1,
         arch_I1_F1,
         arch_I1_F1,
         arch_I1_F1,
         arch_I1_F1]
# SYSTEM = system( "FF", "FF", archs, CHARGE_INITIAL, CHARGING_RATE ) 
SYSTEM = system( "FF", "FF", archs_EXE, CHARGE_INITIAL, CHARGING_RATE ) 
# configurations = []
# configurations.append( Configuration( "FF", "FF", archs ) )
# configurations.append( Configuration( "BF", "BF", archs ) )
# configurations.append( Configuration( "WF", "WF", archs ) )
#configurations.append( Configuration( 1, "10", [arch_a, arch_e] ) )
# ~ configurations.append( Configuration( 2, "11", [arch_a, arch_a] ) )

prgs = []

# ~ prgs.append( Prg( 10, "sharpen_mul"  , 95.57   , 78.07   ) )
# ~ prgs.append( Prg(  9, "qsort"        , 26.93   , 5.22    ) )
# ~ prgs.append( Prg(  8, "grayscale"    , 89.83   , 25.55   ) )
# ~ prgs.append( Prg(  7, "aes"          , 1651.60 , 1651.60 ) )
# ~ prgs.append( Prg(  6, "blowfish"     , 397.57  , 397.57  ) )
# ~ prgs.append( Prg(  5, "square_mmult" , 9.61    , 7.67    ) )
# ~ prgs.append( Prg(  4, "sha256"       , 50.50   , 50.44   ) )
# ~ prgs.append( Prg(  3, "primes"       , 2.69    , 2.69    ) )
# ~ prgs.append( Prg(  2, "norx"         , 57.09   , 57.09   ) )
# ~ prgs.append( Prg(  1, "msort"        , 21.45   , 21.45   ) )
# ~ prgs.append( Prg(  0, "dhrystone"    , 26.63   , 26.52   ) )

# ~ prgs.append( Prg(  0, "dhrystone"    , 26.63   , 26.52   ) )
# ~ prgs.append( Prg(  1, "msort"        , 21.45   , 21.45   ) )
# ~ prgs.append( Prg(  2, "norx"         , 57.09   , 57.09   ) )
# ~ prgs.append( Prg(  3, "primes"       , 2.69    , 2.69    ) )
# ~ prgs.append( Prg(  4, "sha256"       , 50.50   , 50.44   ) )
# ~ prgs.append( Prg(  5, "square_mmult" , 9.61    , 7.67    ) )
# ~ prgs.append( Prg(  6, "blowfish"     , 397.57  , 397.57  ) )
# ~ prgs.append( Prg(  7, "aes"          , 1651.60 , 1651.60 ) )
# ~ prgs.append( Prg(  8, "grayscale"    , 89.83   , 25.55   ) )
# ~ prgs.append( Prg(  9, "qsort"        , 26.93   , 5.22    ) )
# ~ prgs.append( Prg( 10, "sharpen_mul"  , 95.57   , 78.07   ) )
# #######
prgs.append( Prg(  0, "susan"        , 146710  , 144603.93 ,146710  , 144603.93  , 2,2 ) )
prgs.append( Prg(  9, "dhrystone"    , 26.63   , 26.52     ,26.63   , 26.52      , 2,0 ) )
prgs.append( Prg( 10, "sharpen_mul"  , 95.57   , 78.07     ,95.57   , 78.07      , 2,0 ) )
prgs.append( Prg( 11, "square_mmult" , 9.61    , 7.67      ,9.61    , 7.67       , 2,0 ) )
prgs.append( Prg( 12, "grayscale"    , 89.83   , 25.55     ,89.83   , 25.55      , 2,0 ) )
prgs.append( Prg(  1, "FFT"          , 709308  , 709308    ,709308  , 709308     , 0,2    ) )
prgs.append( Prg(  2, "basicmath"    , 55010   , 55010     ,55010   , 55010      , 1,1  ) )
prgs.append( Prg(  3, "crc32"        , 23686   , 23686     ,23686   , 23686      , 0,0    ) )
prgs.append( Prg(  4, "aes"          , 1651.60 , 1651.60   ,1651.60 , 1651.60    , 0,0    ) )
prgs.append( Prg(  5, "stringsearch" , 530     , 530       ,530     , 530        , 0,0    ) )
prgs.append( Prg(  6, "blowfish"     , 397.57  , 397.57    ,397.57  , 397.57     , 0,0    ) )
prgs.append( Prg(  7, "sha256"       , 50.50   , 50.44     ,50.50   , 50.44      , 1,0  ) )
prgs.append( Prg(  8, "qsort"        , 26.93   , 5.22      ,26.93   , 5.22       , 1,0  ) )
prgs.append( Prg( 13, "msort"        , 21.45   , 21.45     ,21.45   , 21.45      , 0,0    ) )
prgs.append( Prg( 14, "norx"         , 57.09   , 57.09     ,57.09   , 57.09      , 0,0    ) )
prgs.append( Prg( 15, "primes"       , 2.69    , 2.69      ,2.69    , 2.69       , 0,0    ) )
prgs = PROGRAMS_INSTANCES*prgs

# Create class bookie to save the results
record = Bookie()
# The new partitioning algorithm
# Set the deadline and period of the applications
for charge_step in range(CHARGE_STEPS):
    SYSTEM.charging_rate = CHARGING_RATE*charge_step
    for step in range(STEPS):
        start_window = START_OF_WINDOW + step * SHIFT_WINDOW
        end_window = START_OF_WINDOW + step * SHIFT_WINDOW + WINDOW_BOUND
        partition_result = 0
        for iteration in range(ITR_PER_WINDOW):
            for prg in prgs:
                # generate a random number to multiply with the application's Ci and generate the deadline for it
                RAND = random.uniform(start_window, end_window)
                # set the deadline of the applications
                prg.set_deadline(RAND)
            partition_result += partition(prgs, SYSTEM)
            SYSTEM.reset_nodes()
        print(partition_result)
        record.record_entry_2_deep(start_window,SYSTEM.charging_rate,partition_result)

# Convert dictionary into lists
charge_vals = []  # X-axis (charge)
start_vals = []   # Y-axis (start)
result_vals = []  # Z-axis (result)
for  start, inner_dict in record.record.items():
    for charge , result in inner_dict.items():
        charge_vals.append(charge)
        start_vals.append(start)
        result_vals.append(result)

# Convert lists to NumPy arrays
charge_vals = np.array(charge_vals)
start_vals = np.array(start_vals)
result_vals = np.array(result_vals)


# Stack arrays into columns and save to a CSV file
data = np.column_stack((charge_vals, start_vals, result_vals))

# Save to a text file
np.savetxt("output_data_EXE.csv", data, delimiter=",", header="Charge,Start,Result", comments='')

# Create 3D figure
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot as scatter plot
ax.scatter(charge_vals, start_vals, result_vals, c=result_vals, cmap='viridis', marker='o')

# Labels
ax.set_xlabel('Charge')
ax.set_ylabel('Start')
ax.set_zlabel('Result')
ax.set_title('3D Visualization of Charge vs. Start vs. Result')

plt.show()


        

