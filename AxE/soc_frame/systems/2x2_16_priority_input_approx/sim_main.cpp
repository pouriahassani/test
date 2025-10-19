// DESCRIPTION: Verilator: Verilog example module - Improved version
//
// This file ONLY is placed into the Public Domain, for any use,
// without warranty, 2017 by Wilson Snyder.
//======================================================================

#include <time.h>
#include <signal.h>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>

// Include common routines
#include <verilated.h>

// Include model header, generated from Verilating "top.v"
#include "Vtop.h"

#include <verilated_vcd_c.h>

// Include generated memory layout
#include "axe_memory_layout.h"

// Current simulation time (64-bit unsigned)
vluint64_t main_time = 0;
VerilatedVcdC* tfp = NULL;
Vtop* top = NULL;

// Called by $time in Verilog
double sc_time_stamp() {
    return main_time;
}

char buffer[1000];
int buffer_index = 1000;
int leds_status = 0;
int triggers = 0;

// File I/O simulation support
struct HostFileInfo {
    std::fstream file;
    std::string filename;
    int mode;
    bool is_open;
    
    HostFileInfo() : mode(0), is_open(false) {}
};

std::unordered_map<int, HostFileInfo> host_files;

// File operations
#define FILE_OPEN_OP    1
#define FILE_READ_OP    2
#define FILE_WRITE_OP   3
#define FILE_CLOSE_OP   4
#define FILE_SIZE_OP    5

// =============================================================================
// CLOCK HELPER FUNCTIONS - Best Practice Implementation
// =============================================================================

// Execute a single clock edge (rising or falling)
void clock_edge(bool rising) {
    top->clk = rising ? 1 : 0;
    top->eval();
    if (tfp) tfp->dump(main_time);
    main_time++;
}

// Execute a full clock cycle (rising edge -> falling edge)
void clock_cycle() {
    clock_edge(true);   // Rising edge
    clock_edge(false);  // Falling edge
}

// Execute multiple clock cycles
void clock_cycles(int n) {
    for (int i = 0; i < n; i++) {
        clock_cycle();
    }
}

// Wait for a condition with timeout (in clock cycles)
template<typename ConditionFunc>
bool wait_for(ConditionFunc condition, int timeout_cycles = 1000) {
    int cycles = 0;
    while (!condition() && cycles < timeout_cycles) {
        clock_cycle();
        cycles++;
    }
    return cycles < timeout_cycles; // Return true if condition met, false if timeout
}

// =============================================================================
// MEMORY ACCESS FUNCTIONS
// =============================================================================

// Helper function to read a single 32-bit word from memory with proper handshaking
uint32_t read_word_from_memory(uint32_t addr) {
    // Setup read request on falling edge of clock
    top->sim_mem_addr = addr;
    top->sim_mem_read_en = 1;
    top->eval();
    if (tfp) tfp->dump(main_time);
    
    // Wait for ready signal using handshaking
    bool success = wait_for([]() { return top->sim_mem_ready; });
    
    if (!success) {
        VL_PRINTF("WARNING: Memory read timeout at address 0x%08x\n", addr);
    }
    
    // Capture result when ready
    uint32_t result = top->sim_mem_read_data;
    
    // Deassert read enable
    top->sim_mem_read_en = 0;
    top->eval();
    if (tfp) tfp->dump(main_time);
    
    // Complete the handshake with one more cycle
    clock_cycle();
    
    return result;
}

// Helper function to write a single 32-bit word to memory with proper handshaking
void write_word_to_memory(uint32_t addr, uint32_t data) {
    // Setup write request
    top->sim_mem_addr = addr;
    top->sim_mem_write_data = data;
    top->sim_mem_write_en = 1;
    top->eval();
    if (tfp) tfp->dump(main_time);
    
    // Wait for ready signal
    bool success = wait_for([]() { return top->sim_mem_ready; });
    
    if (!success) {
        VL_PRINTF("WARNING: Memory write timeout at address 0x%08x\n", addr);
    }
    
    // Deassert write enable
    top->sim_mem_write_en = 0;
    top->eval();
    if (tfp) tfp->dump(main_time);
    
    // Complete the handshake
    clock_cycle();
}

// Helper function to read string from memory
std::string read_string_from_memory(uint32_t addr) {
    std::string result;
    for (int i = 0; i < 256; i++) { // Increased safety limit
        uint32_t word_addr = addr + (i & ~3);
        uint32_t word = read_word_from_memory(word_addr);
        char c = (char)((word >> ((i & 3) * 8)) & 0xFF);
        if (c == '\0') break;
        result += c;
    }
    return result;
}

// Helper function to write data to memory
void write_data_to_memory(uint32_t addr, const void* data, size_t size) {
    const uint8_t* bytes = (const uint8_t*)data;
    for (size_t i = 0; i < size; i += 4) {
        uint32_t word = 0;
        for (int j = 0; j < 4 && (i + j) < size; j++) {
            word |= (uint32_t(bytes[i + j]) << (j * 8));
        }
        write_word_to_memory(addr + i, word);
    }
}

// =============================================================================
// FILE I/O OPERATION HANDLERS
// =============================================================================

void handle_file_operation(int node_id, uint32_t operation, uint32_t param0, 
                          uint32_t param1, uint32_t param2, uint32_t axi_offset) {
    
   
    switch (operation) {
        case FILE_OPEN_OP: {
            uint32_t filename_ptr = read_word_from_memory(param0 + 4);
            int mode = read_word_from_memory(param0 + 16);
            int handle = read_word_from_memory(param0);
            uint32_t filename_ptr_with_offset = filename_ptr + axi_offset;
            
            std::string filename = read_string_from_memory(filename_ptr_with_offset);
            std::ios_base::openmode ios_mode = std::ios_base::binary;
            if (mode & 0x01) ios_mode |= std::ios_base::in;
            if (mode & 0x02) ios_mode |= std::ios_base::out;
            if (mode & 0x04) ios_mode |= std::ios_base::app;
            
            host_files[handle].filename = filename;
            host_files[handle].mode = mode;
            host_files[handle].file.open(filename, ios_mode);
            host_files[handle].is_open = host_files[handle].file.is_open();
            
            write_word_to_memory(param0 + 20, host_files[handle].is_open ? handle : -1);
            break;
            VL_PRINTF("****Opened file '%s' with handle %d (mode %d)\n", filename.c_str(), handle, mode);
        }
        
        case FILE_READ_OP: {
            int fd = read_word_from_memory(param0);
            uint32_t buffer_ptr = read_word_from_memory(param0 + 8);
            size_t size = read_word_from_memory(param0 + 12);
            uint32_t axi_offset_calc = (node_id + 1) * 0x01000000;
            uint32_t buffer_ptr_with_offset = buffer_ptr + axi_offset_calc;
            
            if (host_files.count(fd) && host_files[fd].is_open) {
                std::vector<char> buffer(size);
                host_files[fd].file.read(buffer.data(), size);
                int bytes_read = host_files[fd].file.gcount();
                write_data_to_memory(buffer_ptr_with_offset, buffer.data(), bytes_read);
                write_word_to_memory(param0 + 20, bytes_read);
            } else {
                write_word_to_memory(param0 + 20, -1);
            }
            break;
        }
        
        case FILE_WRITE_OP: {
            int fd = read_word_from_memory(param0);
            uint32_t buffer_ptr = read_word_from_memory(param0 + 8);
            size_t size = read_word_from_memory(param0 + 12);
            uint32_t axi_offset_calc = (node_id + 1) * 0x01000000;
            uint32_t buffer_ptr_with_offset = buffer_ptr + axi_offset_calc;
            
            if (host_files.count(fd) && host_files[fd].is_open) {
                std::vector<char> buffer(size);
                for (size_t i = 0; i < size; i += 4) {
                    uint32_t word = read_word_from_memory(buffer_ptr_with_offset + i);
                    for (int j = 0; j < 4 && (i + j) < size; j++) {
                        buffer[i + j] = (char)((word >> (j * 8)) & 0xFF);
                    }
                }
                host_files[fd].file.write(buffer.data(), size);
                host_files[fd].file.flush();
                write_word_to_memory(param0 + 20, size);
            } else {
                write_word_to_memory(param0 + 20, -1);
            }
            break;
        }
        
        case FILE_CLOSE_OP: {
            int fd = read_word_from_memory(param0);
            if (host_files.count(fd) && host_files[fd].is_open) {
                host_files[fd].file.close();
                host_files[fd].is_open = false;
                write_word_to_memory(param0 + 20, 0);
            } else {
                write_word_to_memory(param0 + 20, -1);
            }
            break;
        }
        
        case FILE_SIZE_OP: {
            uint32_t filename_ptr = read_word_from_memory(param0 + 4);
            uint32_t axi_offset_calc = (node_id + 1) * 0x01000000;
            uint32_t filename_ptr_with_offset = filename_ptr + axi_offset_calc;
            std::string filename = read_string_from_memory(filename_ptr_with_offset);
            
            std::ifstream file(filename, std::ifstream::ate | std::ifstream::binary);
            int file_size = -1;
            if (file.is_open()) {
                file_size = static_cast<int>(file.tellg());
            }
            file.close();
            write_word_to_memory(param0 + 20, file_size);
            break;
        }
    }
    
    // Signal completion
    if (node_id == 0) {
        top->sim_file_op_complete_0 = 1;

    } else if (node_id == 1) {
        top->sim_file_op_complete_1 = 1;
    }
    top->eval();
    if (tfp) tfp->dump(main_time);
    
    // Hold the completion signal for a few cycles to ensure it's sampled
    clock_cycles(2);
    
    // Wait for acknowledge
    if (node_id == 0) {
        wait_for([]() { return top->req_ack_0; });
    } else if (node_id == 1) {
        wait_for([]() { return top->req_ack_1; });
    }
    
    // Clear completion signals
    top->sim_file_op_complete_0 = 0;
    top->sim_file_op_complete_1 = 0;
    top->eval();
    if (tfp) tfp->dump(main_time);
    
}

// =============================================================================
// SIGNAL HANDLERS
// =============================================================================

void ctrl_c_handler(int dummy) {
    for (int i = 0; i < buffer_index; i++) {
        VL_PRINTF("%c", buffer[i]);
    }
    exit(0);
}

// =============================================================================
// MAIN SIMULATION LOOP
// =============================================================================

int main(int argc, char** argv, char** env) {
    signal(SIGINT, ctrl_c_handler);
    
    if (0 && argc && argv && env) {}
    Verilated::commandArgs(argc, argv);

    // Construct the Verilated model
    top = new Vtop;
    
    // Initialize inputs to known state
    top->clk = 0;
    top->res_n = 0;
    top->sim_mem_addr = 0;
    top->sim_mem_read_en = 0;
    top->sim_mem_write_en = 0;
    top->sim_mem_write_data = 0;
    top->sim_file_op_complete_0 = 0;
    top->sim_file_op_complete_1 = 0;
    
    // Initial evaluation
    top->eval();
    
    // Setup waveform tracing
    const char* flag = Verilated::commandArgsPlusMatch("trace");
    // if (flag && 0 == strcmp(flag, "+trace")) {
    //     Verilated::traceEverOn(true);
    //     VL_PRINTF("Enabling waves into logs/vlt_dump.vcd...\n");
    //     tfp = new VerilatedVcdC;
    //     top->trace(tfp, 99);
    //     Verilated::mkdir("logs");
    //     tfp->open("logs/vlt_dump.vcd");
    // }
    
    VL_PRINTF("\n");
    VL_PRINTF("--------------------\n");
    VL_PRINTF("starting 2x2_16\n");
    VL_PRINTF("--------------------\n");
    VL_PRINTF("\n");
    
    // Reset sequence - hold reset for 10 cycles
    clock_cycles(10);
    top->res_n = 1;
    top->eval();
    if (tfp) tfp->dump(main_time);
    
    // Main simulation loop
    while (!Verilated::gotFinish()) {
        // Execute one clock cycle
        clock_edge(true);  // Rising edge
        
        // Sample outputs on rising edge (after eval)
        if (top->trap) {
            VL_PRINTF("trap\n");
        }
        
        if (top->trap_nodes) {
            VL_PRINTF("trap nodes\n");
        }
        
        // UART output handling
        if (top->buffer_out_valid) {
            if (top->buffer_out_data == 0x04) {
                for (int i = 0; i < buffer_index; i++) {
                    VL_PRINTF("%c", buffer[i]);
                }
                VL_PRINTF("kill me\n");
                break;
            }
            
            int i = 0;
            while (i < buffer_index && buffer[i] != '\0') {
                VL_PRINTF("%c", buffer[i]);
                i++;
            }
            for (i = 0; i < buffer_index; i++) {
                buffer[i] = '\0';
            }
            VL_PRINTF("%c", top->buffer_out_data);
        }
        
        // LED status display
        if (leds_status != top->leds_status) {
            leds_status = top->leds_status;
            VL_PRINTF("+---+---+---+---+---+---+---+---+\n");
            VL_PRINTF("|");
            for (int j = 7; j >= 0; j--) {
                VL_PRINTF(" %i |", ((leds_status >> j) & 1));
            }
            VL_PRINTF("\n");
            VL_PRINTF("+---+---+---+---+---+---+---+---+\n");
        }
        
        // Triggers display
        if (triggers != top->triggers) {
            triggers = top->triggers;
            VL_PRINTF("/---/---/---/---/---/---/---/---/\n");
            VL_PRINTF("|");
            for (int j = 7; j >= 0; j--) {
                VL_PRINTF(" %i |", ((triggers >> j) & 1));
            }
            VL_PRINTF("\n");
            VL_PRINTF("/---/---/---/---/---/---/---/---/\n");
        }
        
        // File I/O operations - Check and handle immediately
        if (top->file_instr_valid_0) {
            // VL_PRINTF("[TB] Detected file operation for node 0: instruction=%d\n", top->file_instruction_0);
            handle_file_operation(0, top->file_instruction_0, 
                                top->file_reg_a0_0, top->file_reg_a1_0, 
                                top->file_reg_a2_0, top->axi_offset_0);
            // VL_PRINTF("[TB] File operation complete for node 0\n");
        }
        
        if (top->file_instr_valid_1) {
            // VL_PRINTF("[TB] Detected file operation for node 1: instruction=%d\n", top->file_instruction_1);
            handle_file_operation(1, top->file_instruction_1,
                                top->file_reg_a0_1, top->file_reg_a1_1, 
                                top->file_reg_a2_1, top->axi_offset_1);
            // VL_PRINTF("[TB] File operation complete for node 1\n");
        }
        
        // Complete the current clock cycle with falling edge
        clock_edge(false);
        
        // Timeout check
        if (main_time >= 1000000000000) {
            VL_PRINTF("\n");
            VL_PRINTF("--------------------\n");
            VL_PRINTF("done\n");
            VL_PRINTF("--------------------\n");
            VL_PRINTF("\n");
            VL_PRINTF("time max reached\n");
            break;
        }
    }
    
    // Final model cleanup
    top->final();
    
    // Close trace file
    if (tfp) {
        tfp->close();
        delete tfp;
        tfp = NULL;
    }
    
    // Destroy model
    delete top;
    
    exit(0);
}