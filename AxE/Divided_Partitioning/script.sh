#!/bin/bash

# Initial value for Start_Charge
START_CHARGE=0.0

# Loop 50 times
for i in {1..50}
do
    # Run Python script with Start_Charge and send to background
    python3 partitioning.py "$START_CHARGE" &

    # Increment Start_Charge by 1.0
    START_CHARGE=$(echo "$START_CHARGE + 2.0" | bc)
done

# Wait for all background jobs to finish
wait

echo "All processes completed."
