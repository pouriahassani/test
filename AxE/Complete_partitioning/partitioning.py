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

test = 1
# Simulation parameters
if test == 1:
    STEPS = 1  # Number of steps to shift the window of values
    # The application's execution time (Ci) will be multiplied by a random value picked from the window of values
    # to generate corresponding deadlines and periods.
    SHIFT_WINDOW = 1 # we shift the window by SHIFT_WINDOW at each step
    START_OF_WINDOW = 16 # The lower bound of the window 
    WINDOW_BOUND = 5 # The bound of the window. Now the 
    # staring window will be [1:6]. In the step number s=n 
    # the window will be [n*SHIFT_WINDOW+START_OF_WINDOW,n*SHIFT_WINDOW+START_OF_WINDOW + WINDOW_BOUND ]
    ITR_PER_WINDOW = 5 #Number of iterarions per window to reach reliable results
    CHARGE_STEPS = 2 #Increase the charging rate in CHARGE_STEPS and see the paritiong sucess rate change
    CHARGING_RATE = 10.5
    CHARGE_INITIAL = 2000

if test == 0:
    STEPS = 200  # Number of steps to shift the window of values
    # The application's execution time (Ci) will be multiplied by a random value picked from the window of values
    # to generate corresponding deadlines and periods.
    SHIFT_WINDOW = 0.1 # we shift the window by SHIFT_WINDOW at each step
    START_OF_WINDOW = 1 # The lower bound of the window 
    WINDOW_BOUND = 5 # The bound of the window. Now the 
    # staring window will be [1:6]. In the step number s=n 
    # the window will be [n*SHIFT_WINDOW+START_OF_WINDOW,n*SHIFT_WINDOW+START_OF_WINDOW + WINDOW_BOUND ]
    ITR_PER_WINDOW = 100 #Number of iterarions per window to reach reliable results
    CHARGE_STEPS = 500 #Increase the charging rate in CHARGE_STEPS and see the paritiong sucess rate change
    CHARGING_RATE = 0.1
    CHARGE_INITIAL = 2000

# ~ 4757098
e_mw = 9.175
# ~ a_mw = 4.93
a_mw = 8.735

NONE = 4.25
I1 = 5.07
I2 = 4.76
F_Units_1 = 4.141
F_Units_2 = 3.135

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


# Create the architecture and assign Names and power
AXE_arch_I0_F0      = Arch( 0,I0_F0_mw,0,0 )            # No multiplication
AXE_arch_I1_F0      = Arch( 0,I1_F0_mw,1,0 )            # Only Exact Int
AXE_arch_I2_F0      = Arch( 1,I2_F0_mw,2,0 )            # Only Approximate int
AXE_arch_I0_F1      = Arch( 0,I0_F1_mw,0,1 )            # Only Exact Float
AXE_arch_I0_F2      = Arch( 0,I0_F2_mw,0,2 )            # Only approximate Float
AXE_arch_I1_F1      = Arch( 0,I1_F1_mw,1,1 )            # Exact Int and Exact Float
AXE_arch_I1_F2      = Arch( 0,I1_F2_mw,1,2 )            # Exact Int and Approximate Float
AXE_arch_I2_F1      = Arch( 1,I2_F1_mw,2,1 )            # Approximate Int and Exact Float
AXE_arch_I2_F2      = Arch( 1,I2_F2_mw,2,2 )            # Approximate Int and Approximate Float

# Create the architecture and assign Names and power
EXE_arch_I0_F0_0      = Arch( 0,I0_F0_mw,0,0 )            # No multiplication
EXE_arch_I1_F0_0      = Arch( 0,I1_F0_mw,1,0 )            # Only Exact Int
EXE_arch_I1_F0_1      = Arch( 0,I1_F0_mw,1,0 )            # Only Approximate int
EXE_arch_I0_F1_0      = Arch( 0,I0_F1_mw,0,1 )            # Only Exact Float
EXE_arch_I0_F1_1      = Arch( 0,I0_F1_mw,0,1 )            # Only approximate Float
EXE_arch_I1_F1_0      = Arch( 0,I1_F1_mw,1,1 )            # Exact Int and Exact Float
EXE_arch_I1_F1_1      = Arch( 0,I1_F1_mw,1,1 )            # Exact Int and Approximate Float
EXE_arch_I1_F1_2      = Arch( 0,I1_F1_mw,1,1 )            # Approximate Int and Exact Float
EXE_arch_I1_F1_3      = Arch( 0,I1_F1_mw,1,1 )            # Approximate Int and Approximate Float



AXE_archs = [  AXE_arch_I0_F0,
               AXE_arch_I1_F0,
               AXE_arch_I2_F0,
               AXE_arch_I0_F1,
               AXE_arch_I0_F2,
               AXE_arch_I1_F1,
               AXE_arch_I1_F2,
               AXE_arch_I2_F1,
               AXE_arch_I2_F2]

EXE_archs  = [  EXE_arch_I0_F0_0 , 
               EXE_arch_I1_F0_0 , 
               EXE_arch_I1_F0_1 , 
               EXE_arch_I0_F1_0 , 
               EXE_arch_I0_F1_1 , 
               EXE_arch_I1_F1_0 , 
               EXE_arch_I1_F1_1 , 
               EXE_arch_I1_F1_2 , 
               EXE_arch_I1_F1_3 ]

# Create the EXACT AND APPROXIMATE SYSTEMS 
SYSTEM_AXE = system( "AXE" , AXE_archs ) 
SYSTEM_EXE = system( "EXE" , EXE_archs ) 
power_a = 0
for node in SYSTEM_AXE.nodes:
    print(node.name, " :",node.arch.power)

# Create class bookie to save the results
BOOKIE_AXE = Bookie()
BOOKIE_EXE = Bookie()
# The new partitioning algorithm
# Set the deadline and period of the applications

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
    if program.Int_pref == 2 and node.arch.Int_Type == 2:
        EXECUTION_TIME = program.APPROX_TIME
    else:
        EXECUTION_TIME = program.EXACT_TIME

    min_SSE_T1T2 = float("inf")
    
    for prg in system.prgs:
        if program.release >= prg.release and program.deadline <= prg.deadline:
            potential_g = prg.g
            AVAILABLE_CHARGE = system.CHARGING_INITIAL + system.CHARGING_RATE*(prg.deadline - prg.release)
            potential_g += EXECUTION_TIME*node.arch.power
            potential_sse = AVAILABLE_CHARGE - potential_g
            if potential_sse < min_SSE_T1T2:
                min_SSE_T1T2 = potential_sse
    
    g1 = EXECUTION_TIME*node.arch.power
    AVAILABLE_CHARGE = system.CHARGING_INITIAL + system.CHARGING_RATE*(program.deadline - program.release)
    for prg in system.prgs:
        if prg.release >= program.release and prg.deadline <= program.deadline:
            g1 += prg.power

    if AVAILABLE_CHARGE - g1 < min_SSE_T1T2:
        min_SSE_T1T2 = AVAILABLE_CHARGE - g1

    return min_SSE_T1T2

def calculate_SST(node,program,system):
    if program.Int_pref == 2 and node.arch.Int_Type == 2:
        EXECUTION_TIME = program.APPROX_TIME
    else:
        EXECUTION_TIME = program.EXACT_TIME

    min_SST_T1T2 = float("inf")
    
    for prg in node.prgs:
        if program.release >= prg.release and program.deadline <= prg.deadline:
            potential_h = prg.h
            AVAILABLE_TIME = prg.deadline - prg.release
            potential_h += EXECUTION_TIME
            potential_sst = AVAILABLE_TIME - potential_h
            if potential_sst < min_SST_T1T2:
                min_SST_T1T2 = potential_sst
    
    h1 = EXECUTION_TIME
    AVAILABLE_TIME = program.deadline - program.release
    for prg in system.prgs:
        if prg.release >= program.release and prg.deadline <= program.deadline:
            h1 += prg.time

    if AVAILABLE_TIME - h1 < min_SST_T1T2:
        min_SST_T1T2 = AVAILABLE_TIME - h1

    return min_SST_T1T2

def Choose_node(prg,Candidate_nodes,system):
    if prg.Int_pref == 0 and prg.Float_pref == 0:
        for node in Candidate_nodes:
            if node.arch.Int_Type == 0 and node.arch.Float_Type == 0:
                return node
        for node in Candidate_nodes:
            if node.arch.Int_Type == 2 and node.arch.Float_Type == 0:
                return node
        for node in Candidate_nodes:
            if node.arch.Int_Type == 0 and node.arch.Float_Type == 2:
                return node
        for node in Candidate_nodes:
            if node.arch.Int_Type == 2 and node.arch.Float_Type == 2:
                return node
        for node in Candidate_nodes:    
            if node.arch.Int_Type == 0 and node.arch.Float_Type == 1:
                return node    
        for node in Candidate_nodes:
            if node.arch.Int_Type == 2 and node.arch.Float_Type == 1:
                return node
        for node in Candidate_nodes:    
            if node.arch.Int_Type == 1 and node.arch.Float_Type == 0:
                return node
        for node in Candidate_nodes:
            if node.arch.Int_Type == 1 and node.arch.Float_Type == 2:
                return node
        for node in Candidate_nodes:
            if node.arch.Int_Type == 1 and node.arch.Float_Type == 1:
                return node
                
    if prg.Int_pref == 2 and prg.Float_pref == 0:
        for node in Candidate_nodes:                
            if node.arch.Int_Type == 2 and node.arch.Float_Type == 0:
                return node
        for node in Candidate_nodes:
            if node.arch.Int_Type == 2 and node.arch.Float_Type == 2:
                return node  
        for node in Candidate_nodes:
            if node.arch.Int_Type == 2 and node.arch.Float_Type == 1:
                return node
        for node in Candidate_nodes:    
            if node.arch.Int_Type == 1 and node.arch.Float_Type == 0:
                return node
        for node in Candidate_nodes:
            if node.arch.Int_Type == 1 and node.arch.Float_Type == 2:
                return node
        for node in Candidate_nodes:    
            if node.arch.Int_Type == 1 and node.arch.Float_Type == 1:
                return node
                
    if prg.Int_pref == 0 and prg.Float_pref == 2:
        for node in Candidate_nodes:                
            if node.arch.Int_Type == 0 and node.arch.Float_Type == 2:
                return node
        for node in Candidate_nodes:
            if node.arch.Int_Type == 2 and node.arch.Float_Type == 2:
                return node
        for node in Candidate_nodes:                
            if node.arch.Int_Type == 0 and node.arch.Float_Type == 1:
                return node    
        for node in Candidate_nodes:
            if node.arch.Int_Type == 2 and node.arch.Float_Type == 1:
                return node
        for node in Candidate_nodes:
            if node.arch.Int_Type == 1 and node.arch.Float_Type == 2:
                return node
        for node in Candidate_nodes:    
            if node.arch.Int_Type == 1 and node.arch.Float_Type == 1:
                return node                

    if prg.Int_pref == 1 and prg.Float_pref == 0:
        for node in Candidate_nodes:                
            if node.arch.Int_Type == 1 and node.arch.Float_Type == 0:
                return node
        for node in Candidate_nodes:
            if node.arch.Int_Type == 1 and node.arch.Float_Type == 2:
                return node
        for node in Candidate_nodes:
            if node.arch.Int_Type == 1 and node.arch.Float_Type == 1:
                return node          

    if prg.Int_pref == 0 and prg.Float_pref == 1:
        for node in Candidate_nodes:                
            if node.arch.Int_Type == 0 and node.arch.Float_Type == 1:
                return node    
        for node in Candidate_nodes:
            if node.arch.Int_Type == 2 and node.arch.Float_Type == 1:
                return node
        for node in Candidate_nodes:
            if node.arch.Int_Type == 1 and node.arch.Float_Type == 1:
                return node        

    if prg.Int_pref == 2 and prg.Float_pref == 1:
        for node in Candidate_nodes:  
            if node.arch.Int_Type == 2 and node.arch.Float_Type == 1:
                return node
        for node in Candidate_nodes:
            if node.arch.Int_Type == 1 and node.arch.Float_Type == 1:
                return node 

    if prg.Int_pref == 1 and prg.Float_pref == 2:
        for node in Candidate_nodes:
            if node.arch.Int_Type == 1 and node.arch.Float_Type == 2:
                return node
        for node in Candidate_nodes:
            if node.arch.Int_Type == 1 and node.arch.Float_Type == 1:
                return node   

    if prg.Int_pref == 1 and prg.Float_pref == 1:
        for node in Candidate_nodes:
            if node.arch.Int_Type == 1 and node.arch.Float_Type == 1:
                return node                                                          
                
    if prg.Int_pref == 2 and prg.Float_pref == 2:
        for node in Candidate_nodes:
            if node.arch.Int_Type == 2 and node.arch.Float_Type == 2:
                return node   
        for node in Candidate_nodes:
            if node.arch.Int_Type == 2 and node.arch.Float_Type == 1:
                return node
        for node in Candidate_nodes:
            if node.arch.Int_Type == 1 and node.arch.Float_Type == 2:
                return node
        for node in Candidate_nodes:
            if node.arch.Int_Type == 1 and node.arch.Float_Type == 1:
                return node    
    print("error happened in Choose_node")
    exit()            
                

def assign_node(node,program,system):
    if program.Int_pref == 2 and node.arch.Int_Type == 2:
        EXECUTION_TIME = program.APPROX_TIME
    else:
        EXECUTION_TIME = program.EXACT_TIME

    program.time = EXECUTION_TIME
    program.power = EXECUTION_TIME * node.arch.power
    program.g = program.power
    program.h = program.time

    for prg in system.prgs:
        if program.release >= prg.release and program.deadline <= prg.deadline:
            prg.g += program.power
    

    for prg in system.prgs:
        if prg.release >= program.release and prg.deadline <= program.deadline:
            program.g += prg.power


    for prg in node.prgs:
        if program.release >= prg.release and program.deadline <= prg.deadline:
            prg.h += program.time
    
    for prg in node.prgs:
        if prg.release >= program.release and prg.deadline <= program.deadline:
            program.h += prg.time

    node.prgs.append(program)
    system.prgs.append(program)


def partition(prgs, system):
    # sort the prgs using their worst case power consumption
    prgs = sorted(prgs, key=lambda Prg: Prg.EXACT_TIME,reverse=True)
    for prg in prgs:
        correct_nodes = Correct_Nodes(system.nodes,prg)
        candidate_nodes = []
        failed_sse = 0
        failed_sst = 0
        for node in correct_nodes:
            potential_sse = calculate_SSE(node,prg,system)
            potential_sst = calculate_SST(node,prg,system)

            if potential_sse < 0:
                failed_sse +=1
            if potential_sst < 0:
                failed_sst +=1

            if potential_sse > 0 and potential_sst > 0:
                candidate_nodes.append(node)
        if not candidate_nodes:
            system.SSE += failed_sse/len(correct_nodes)
            system.SST += failed_sst/len(correct_nodes)
            return 0

        node = Choose_node(prg,candidate_nodes,system)
        assign_node(node,prg,system)
    system.SSE += failed_sse/len(correct_nodes)
    system.SST += failed_sst/len(correct_nodes)
    return 1  


for charge_step in range(CHARGE_STEPS):
    SYSTEM_AXE.CHARGING_RATE = CHARGING_RATE * charge_step
    SYSTEM_AXE.CHARGING_INITIAL = CHARGE_INITIAL
    SYSTEM_EXE.CHARGING_RATE = CHARGING_RATE * charge_step
    SYSTEM_EXE.CHARGING_INITIAL = CHARGE_INITIAL
    EXE_FULL_PARTITIONING = 0
    AXE_FULL_PARTITIONING = 0


    for step in range(STEPS):
        start_window = START_OF_WINDOW + step * SHIFT_WINDOW
        end_window   = start_window + WINDOW_BOUND
        AXE_partition_result = 0
        EXE_partition_result = 0
        SYSTEM_AXE.SSE = 0
        SYSTEM_AXE.SST = 0
        SYSTEM_EXE.SSE = 0
        SYSTEM_EXE.SST = 0
        if EXE_FULL_PARTITIONING >=3 and AXE_FULL_PARTITIONING >= 3:
            BOOKIE_AXE.record_entry(start_window,SYSTEM_AXE.CHARGING_RATE,100,0,0)
            BOOKIE_EXE.record_entry(start_window,SYSTEM_EXE.CHARGING_RATE,100,0,0)
        else:
            for iteration in range(ITR_PER_WINDOW):
                for prg in PRGS:
                    # generate a random number to multiply with the application's Ci and generate the deadline for it
                    RAND = random.uniform(start_window, end_window)
                    # set the deadline of the applications
                    prg.deadline = RAND*prg.EXACT_TIME
                AXE_partition_result += partition(PRGS, SYSTEM_AXE)
                for prg in PRGS:
                    prg.reset()
                SYSTEM_AXE.reset()

                EXE_partition_result += partition(PRGS, SYSTEM_EXE)
                for prg in PRGS:
                    prg.reset()
                SYSTEM_EXE.reset()
            if EXE_partition_result == ITR_PER_WINDOW:
                EXE_FULL_PARTITIONING +=1

            if AXE_partition_result == ITR_PER_WINDOW:
                AXE_FULL_PARTITIONING +=1
            BOOKIE_AXE.record_entry(start_window,SYSTEM_AXE.CHARGING_RATE,AXE_partition_result*100/ITR_PER_WINDOW,
                                    SYSTEM_AXE.SSE*100/ITR_PER_WINDOW,SYSTEM_AXE.SST*100/ITR_PER_WINDOW)
            BOOKIE_EXE.record_entry(start_window,SYSTEM_EXE.CHARGING_RATE,EXE_partition_result*100/ITR_PER_WINDOW
                                    ,SYSTEM_EXE.SSE*100/ITR_PER_WINDOW,SYSTEM_EXE.SST*100/ITR_PER_WINDOW)
            print(SYSTEM_AXE.CHARGING_RATE,start_window,EXE_partition_result,AXE_partition_result)


# Writing to CSV
if test:
    AXE_FILENAME = "AXE_test.csv"
    EXE_FILENAME = "EXE_test.csv"
else:
    AXE_FILENAME = "AXE.csv"
    EXE_FILENAME = "EXE.csv"
BOOKIE_AXE.write_to_csv(AXE_FILENAME)
BOOKIE_EXE.write_to_csv(EXE_FILENAME)

      