/* ****************************************************************************
  This Source Code Form is subject to the terms of the
  Open Hardware Description License, v. 1.0. If a copy
  of the OHDL was not distributed with this file, You
  can obtain one at http://juliusbaxter.net/ohdl/ohdl.txt
  
  Copyright (C) 2025 AxE Project
  
***************************************************************************** */

/**
 * @file file_io_detector.sv
 * @brief File I/O instruction detector for AxE SoC
 * 
 * This module detects custom file I/O instructions by monitoring AXI write
 * transactions to specific addresses. When a file instruction is detected,
 * it extracts the operation type and register values for simulation handling.
 */

`include "axe_memory_layout.vh"

module file_io_detector
#(
     parameter DETECT_ADDR_BASE = `FILE_TRIGGERS_BASE   // Base address from config
)
(
     input clk
    ,input res_n
    
    // AXI offset input for address translation
    ,input [ `AXI_ADDR_WIDTH-1:0 ] axi_offset
    
    // File instruction detection outputs
    ,output reg        file_instr_valid
    ,output reg [31:0] file_instruction
    ,output reg [31:0] file_reg_a0
    ,output reg [31:0] file_reg_a1  
    ,output reg [31:0] file_reg_a2
    ,output wire req_ack // Acknowledge for request completion
    ,output wire debug_file_detect_sim
    // Simulation completion input
    ,input wire        sim_file_op_complete
    
    // AXI interface
    ,if_axi_light.slave  s_axi
    ,if_axi_light.master m_axi
);
reg [31:0] file_instruction_type;
// File operation instruction opcodes
localparam FILE_OPEN_INSTR  = 32'h0EA5F00B;
localparam FILE_READ_INSTR  = 32'h0EA5F10B;
localparam FILE_WRITE_INSTR = 32'h0EA5F20B;
localparam FILE_CLOSE_INSTR = 32'h0EA5F30B;
localparam FILE_SIZE_INSTR  = 32'h0EA5F40B;

// Detection addresses from generated configuration
localparam FILE_OPEN_ADDR   = `FILE_OPEN_TRIGGER;
localparam FILE_READ_ADDR   = `FILE_READ_TRIGGER;
localparam FILE_WRITE_ADDR  = `FILE_WRITE_TRIGGER;
localparam FILE_CLOSE_ADDR  = `FILE_CLOSE_TRIGGER;
localparam FILE_SIZE_ADDR   = `FILE_SIZE_TRIGGER;

// State machine
enum {
    IDLE,
    DETECT_FILE_OP,
    WAIT_SIM_COMPLETE,
    FORWARD_TRANSACTION,
    WAIT_AXI_READY
} state, next_state;

// Latched transaction data
reg [31:0] latched_awaddr;
reg [31:0] latched_wdata;
reg        detected_file_op;
assign debug_file_detect_sim = detected_file_op;
// File operation detection logic
always_comb begin
    detected_file_op = 0;
    // file_instruction_type = 32'h0;
    if (s_axi.awvalid && s_axi.wvalid) begin
        case (s_axi.awaddr)
            FILE_OPEN_ADDR: begin
                detected_file_op = 1;
                file_instruction_type = 1;
            end
            FILE_READ_ADDR: begin
                detected_file_op = 1;
                file_instruction_type = 2;  // FILE_READ_OP = 3
            end
            FILE_WRITE_ADDR: begin
                detected_file_op = 1;
                file_instruction_type = 3;  // FILE_WRITE_OP = 4
            end
            FILE_CLOSE_ADDR: begin
                detected_file_op = 1;
                file_instruction_type = 4;  // FILE_CLOSE_OP = 2
            end
            FILE_SIZE_ADDR: begin
                detected_file_op = 1;
                file_instruction_type = 5;
            end
            default: begin
                detected_file_op = 0;
                file_instruction_type = 32'h0;
            end
        endcase
    end
end

// State machine
always_ff @(posedge clk) begin
    if (!res_n) begin
        state <= IDLE;
        file_instr_valid <= 0;
        file_reg_a0 <= 32'h0;
        file_reg_a1 <= 32'h0;
        file_reg_a2 <= 32'h0;
        latched_awaddr <= 32'h0;
        latched_wdata <= 32'h0;

    end else begin
        state <= next_state;
        // $display("Current state: %s detected_file_op=%b", state.name(),  detected_file_op);
        case (state)
            IDLE: begin
                file_instr_valid <= 0;
                if (detected_file_op) begin
                    // Latch the transaction
                    latched_awaddr <= s_axi.awaddr;
                    latched_wdata <= s_axi.wdata;
                    
                    // The wdata contains the address of the file_params structure
                    // Apply AXI offset for physical memory access
                    file_reg_a0 <= s_axi.wdata + axi_offset;  // Parameter structure address with offset
                    file_reg_a1 <= s_axi.awaddr;              // Operation trigger address
                    file_reg_a2 <= 32'h0;                     // Reserved for future use
                    file_instruction <= file_instruction_type;
                    file_instr_valid <= 1;
                end
                // $display("\ns_axi.awvalid %x && s_axi.wvalid %x s_axi.wdata %x s_axi.awaddr %x",s_axi.awvalid, s_axi.wvalid, s_axi.wdata, s_axi.awaddr);
            end
            
            DETECT_FILE_OP: begin
                // Hold the detection signal for one cycle
            end
            
            WAIT_SIM_COMPLETE: begin
                // Keep detection signal active until simulation completes
            end
            
            FORWARD_TRANSACTION: begin
                file_instr_valid <= 0;
                // Start AXI response phase
            end
            
            WAIT_AXI_READY: begin
                file_instr_valid <= 0;
                // Hold until AXI master accepts response
            end
        endcase
    end
end

// Next state logic
always_comb begin
    next_state = state;
    
    case (state)
        IDLE: begin
            if (detected_file_op) begin
                next_state = WAIT_SIM_COMPLETE;
            end
        end
        
        DETECT_FILE_OP: begin
            next_state = WAIT_SIM_COMPLETE;
            // $display("DETECT_FILE_OP: s_axi.bready=%b", s_axi.bready);
        end
        
        WAIT_SIM_COMPLETE: begin
            if (sim_file_op_complete) begin
                next_state = FORWARD_TRANSACTION;
            end
            // $display("WAIT_SIM_COMPLETE: s_axi.bready=%b", s_axi.bready);
        end
        
        FORWARD_TRANSACTION: begin
            // $display("FORWARD_TRANSACTION: s_axi.bready=%b", s_axi.bready);
            if (s_axi.bready) begin
                // $display("FORWARD_TRANSACTION: s_axi.bready=%b", s_axi.bready);
                next_state = WAIT_AXI_READY;
                req_ack = 1; // Acknowledge the request completion
            end

        end
        
        WAIT_AXI_READY: begin
            next_state = IDLE;
            req_ack = 0; // Acknowledge the request completion
            // $display("WAIT_AXI_READY: s_axi.bready=%b", s_axi.bready);
        end
    endcase
end

// AXI passthrough (for non-file operations)
always_comb begin
    // Default passthrough
    m_axi.awvalid = s_axi.awvalid;
    s_axi.awready = m_axi.awready;
    m_axi.awaddr  = s_axi.awaddr;
    m_axi.awprot  = s_axi.awprot;
    
    m_axi.wvalid  = s_axi.wvalid;
    s_axi.wready  = m_axi.wready;
    m_axi.wdata   = s_axi.wdata;
    m_axi.wstrb   = s_axi.wstrb;
    
    s_axi.bvalid  = m_axi.bvalid;
    m_axi.bready  = s_axi.bready;
    s_axi.bresp   = m_axi.bresp;
    
    m_axi.arvalid = s_axi.arvalid;
    s_axi.arready = m_axi.arready;
    m_axi.araddr  = s_axi.araddr;
    m_axi.arprot  = s_axi.arprot;
    
    s_axi.rvalid  = m_axi.rvalid;
    m_axi.rready  = s_axi.rready;
    s_axi.rdata   = m_axi.rdata;
    s_axi.rresp   = m_axi.rresp;
    
    // Handle file operation transactions
    if (detected_file_op || state == WAIT_SIM_COMPLETE || state == FORWARD_TRANSACTION || state == WAIT_AXI_READY) begin
        // Block transaction from reaching memory
        m_axi.awvalid = 0;
        m_axi.wvalid = 0;
        s_axi.awready = 0;
        s_axi.wready = 0;

        m_axi.arvalid = 1'b0; // don't send to memory
        s_axi.arready = 1'b0; // don't accept from master
        s_axi.rvalid  = 1'b0; // no read data yet
        s_axi.rdata   = '0;
        s_axi.rresp   = 2'b00;
        
        // Send response when simulation completes and hold until master ready
        if (state == FORWARD_TRANSACTION) begin
            s_axi.awready = 1; // Indicate address ready
            s_axi.wready = 1;  // Indicate write data ready
            s_axi.bvalid = 1;     // Hold response until bready
            s_axi.bresp = 2'b00;  // OKAY response
        end else begin
            s_axi.bvalid = 0;     // Hold response until complete
        end
    end
end

endmodule