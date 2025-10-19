import csv
class Bookie:
    
    def __init__( self ):
        
        self.record = {}
        
    
    def record_entry( self, start_window, charging_rate,result,SSE,SST ):
        
        self.record[(charging_rate, start_window)] = {"result": result, "SSE": SSE, "SST": SST}

    def write_to_csv(self, filename="output.csv"):
            """Writes the dictionary records to a CSV file."""
            with open(filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                # Write header
                writer.writerow(["Charging Rate", "Start Window", "Result", "SSE", "SST"])

                # Write rows
                for (charging_rate, start_window), values in self.record.items():
                    writer.writerow([charging_rate, start_window, values["result"], values["SSE"], values["SST"]])
