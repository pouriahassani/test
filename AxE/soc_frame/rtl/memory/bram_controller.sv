`timescale 1ns / 1ps

/* ****************************************************************************
  BRAM Controller with AXI4-Lite Interface and Simulation Debug Access
  
  This module provides:
  1. AXI4-Lite slave interface for standard memory access
  2. BRAM interface with proper timing and handshaking  
  3. Simulation debug interface with ready/valid handshaking
  4. Proper arbitration between AXI and simulation access to prevent conflicts
  
  Key Features:
  - Supports byte-addressable writes with write strobes
  - Read-modify-write for partial word updates
  - Proper AXI4-Lite protocol compliance
  - Simulation memory access with ready/valid handshaking
  - Priority-based arbitration with explicit BRAM ownership tracking
  - Robust request handling prevents lost operations
  
  Timing Behavior:
  - BRAM operations complete in 1 cycle when bram_done asserts
  - sim_mem_ready pulses high for 1 cycle when simulation operation completes
  - All sequential logic uses non-blocking assignments (<=)
  
  Simulation Interface Requirements:
  - Testbench must hold sim_mem_*_en asserted until sim_mem_ready pulses
  - Controller latches requests on clock edges (one-cycle acceptance)
  - If AXI and simulation request simultaneously, AXI has priority but
    simulation request is preserved and serviced after AXI completes
  
  This Source Code Form is subject to the terms of the
  Open Hardware Description License, v. 1.0. If a copy
  of the OHDL was not distributed with this file, You
  can obtain one at http://juliusbaxter.net/ohdl/ohdl.txt

  Copyright (C) 2025 Pouria Hasani <pouria.hasani@uni-heidelberg.de>
***************************************************************************** */

module bram_controller
#()
(
    // =========================================================================
    // CLOCK AND RESET
    // =========================================================================
     input clk                    // System clock
    ,input res_n                  // Active-low reset

    // =========================================================================
    // AXI4-LITE SLAVE INTERFACE
    // =========================================================================
    ,if_axi_light.slave  s_axi    // AXI4-Lite slave interface for memory access

    // =========================================================================
    // BRAM INTERFACE
    // =========================================================================
    ,output reg [31:0] bram_addr  // BRAM address (word-aligned)
    ,output reg [31:0] bram_wdata // BRAM write data
    ,input      [31:0] bram_rdata // BRAM read data
    ,output reg        bram_read  // BRAM read enable (1 cycle pulse)
    ,output reg        bram_write // BRAM write enable (1 cycle pulse)
    ,input             bram_done  // BRAM operation complete (1 cycle pulse)

    // =========================================================================
    // SIMULATION DEBUG INTERFACE (Handshaking)
    // =========================================================================
    // This interface allows the simulator to access memory with proper timing
    // Ready signal pulses high for 1 cycle when complete
    // Testbench MUST hold *_en signals until ready pulses
    `ifndef SYNTHESIS
    ,input  wire [31:0] sim_mem_addr       // Simulation memory address
    ,input  wire        sim_mem_read_en    // Simulation read enable (hold until ready)
    ,output reg  [31:0] sim_mem_read_data  // Simulation read data (valid with ready)
    ,output reg         sim_mem_ready      // Simulation ready (1-cycle pulse)
    ,input  wire [31:0] sim_mem_write_data // Simulation write data
    ,input  wire        sim_mem_write_en   // Simulation write enable (hold until ready)
    `endif
);

// =========================================================================
// BRAM OWNERSHIP TRACKING
// =========================================================================
// Tracks which interface (AXI or SIM) initiated the current BRAM operation
// This prevents completion events from being misattributed
localparam [1:0] OWNER_NONE = 2'b00;
localparam [1:0] OWNER_AXI  = 2'b01;
localparam [1:0] OWNER_SIM  = 2'b10;

reg [1:0] bram_owner;  // Tracks current BRAM operation owner

// =========================================================================
// ARBITRATION STATE MACHINE
// =========================================================================
// Manages access between AXI and simulation interfaces
// AXI has priority, but simulation requests are preserved
typedef enum logic [1:0] { 
    ARB_IDLE       = 2'b00,  // No active requests
    ARB_AXI_ACTIVE = 2'b01,  // AXI operation in progress
    ARB_SIM_ACTIVE = 2'b10   // Simulation operation in progress
} arb_state_t;

arb_state_t arb_state;

// =========================================================================
// AXI4-LITE STATE MACHINE
// =========================================================================
// State machine for AXI4-Lite protocol compliance
typedef enum logic [2:0] { 
    IDLE       = 3'b000,  // Waiting for AXI requests
    WRITE_READ = 3'b001,  // Read existing data for read-modify-write
    WRITE_STRB = 3'b010,  // Apply write strobes to modify specific bytes
    WRITE      = 3'b011,  // Write modified data back to BRAM
    WRITE_RESP = 3'b100,  // Send write response to AXI master
    READ       = 3'b101,  // Read data from BRAM
    READ_RESP  = 3'b110   // Send read response to AXI master
} axi_state_t;

axi_state_t state;

// =========================================================================
// AXI4-LITE PROTOCOL REGISTERS
// =========================================================================
// Latched AXI signals for proper protocol timing
reg [`AXI_ADDR_WIDTH-1:0] latched_awaddr;  // Latched write address
reg [2:0] latched_awprot;                  // Latched write protection
reg [`AXI_DATA_WIDTH-1:0] latched_wdata;   // Latched write data
reg [`AXI_WSTRB_WIDTH-1:0] latched_wstrb;  // Latched write strobes
reg [`AXI_ADDR_WIDTH-1:0] latched_araddr;  // Latched read address
reg [2:0] latched_arprot;                  // Latched read protection
reg [`AXI_ADDR_WIDTH-1:0] index;           // Internal processing index
reg [1:0] status;                          // AXI response status

// =========================================================================
// DATA PROCESSING REGISTERS
// =========================================================================
reg [`AXI_DATA_WIDTH-1:0] wdata_temp;      // Temporary write data for RMW
reg [`AXI_DATA_WIDTH-1:0] rdata_temp;      // Temporary read data
reg done;                                  // AXI operation completion flag

// =========================================================================
// SIMULATION INTERFACE REGISTERS
// =========================================================================
// These track pending simulation requests
`ifndef SYNTHESIS
reg sim_mem_read_pending;                 // Read operation pending
reg sim_mem_write_pending;                // Write operation pending  
reg [31:0] sim_mem_addr_latched;          // Latched simulation address
reg [31:0] sim_mem_write_data_latched;    // Latched simulation write data
`endif

// =========================================================================
// AXI TRANSACTION TRACKING
// =========================================================================
// Track if we're actively processing an AXI transaction
reg axi_transaction_active;

// =========================================================================
// ARBITRATION LOGIC
// =========================================================================
// AXI has priority, but only if no simulation request is already pending
// This prevents AXI from preempting a latched simulation request
`ifndef SYNTHESIS
wire sim_access_request = (sim_mem_read_en || sim_mem_write_en || 
                           sim_mem_read_pending || sim_mem_write_pending) && 
                          (arb_state == ARB_IDLE);
`else
wire sim_access_request = 1'b0;
`endif

// AXI can only take control if no simulation request is pending
wire axi_access_request = ((s_axi.awvalid && s_axi.wvalid) || s_axi.arvalid) && 
                         (arb_state == ARB_IDLE) &&
                         `ifndef SYNTHESIS
                         (!sim_mem_read_pending && !sim_mem_write_pending);
                         `else
                         1'b1;
                         `endif

// =========================================================================
// MAIN CONTROLLER SEQUENTIAL LOGIC
// =========================================================================
always @(posedge clk) begin : proc_bram_controller
    
    // =====================================================================
    // RESET STATE - Initialize all registers
    // =====================================================================
    if (!res_n) begin
        // Arbitration and ownership
        arb_state <= ARB_IDLE;
        bram_owner <= OWNER_NONE;
        axi_transaction_active <= 1'b0;
        
        // AXI state machine
        state <= IDLE;
        index <= 0;
        status <= 2'b00;
        
        // Data processing registers
        wdata_temp <= 0;
        rdata_temp <= 0;
        
        // BRAM interface
        bram_addr <= 0;
        bram_wdata <= 0;
        bram_read <= 0;
        bram_write <= 0;
        
        // Simulation interface
        `ifndef SYNTHESIS
        sim_mem_ready <= 1'b0;
        sim_mem_read_data <= 32'h0;
        sim_mem_read_pending <= 1'b0;
        sim_mem_write_pending <= 1'b0;
        sim_mem_addr_latched <= 32'h0;
        sim_mem_write_data_latched <= 32'h0;
        `endif
        
    end else begin
    
    // =====================================================================
    // DEFAULT ASSIGNMENTS (every cycle)
    // =====================================================================
    bram_read <= 1'b0;          // Default: no BRAM read
    bram_write <= 1'b0;         // Default: no BRAM write
    
    // Simulation ready defaults to 0 every cycle
    `ifndef SYNTHESIS
    sim_mem_ready <= 1'b0;
    `endif
    
    // Set AXI interface defaults
    s_axi.s_default();
    
    // =====================================================================
    // SIMULATION REQUEST LATCHING (Non-synthesis only)
    // =====================================================================
    // Latch simulation requests early to prevent loss
    // This happens regardless of arbitration state
    `ifndef SYNTHESIS
    if (!sim_mem_read_pending && sim_mem_read_en) begin
        sim_mem_read_pending <= 1'b1;
        sim_mem_addr_latched <= sim_mem_addr;
    end
    if (!sim_mem_write_pending && sim_mem_write_en) begin
        sim_mem_write_pending <= 1'b1;
        sim_mem_addr_latched <= sim_mem_addr;
        sim_mem_write_data_latched <= sim_mem_write_data;
    end
    `endif
    
    // =====================================================================
    // BRAM COMPLETION HANDLING (for both AXI and SIM)
    // =====================================================================
    // When BRAM completes, check who owns it and handle accordingly
    if (bram_done) begin
        case (bram_owner)
            OWNER_SIM: begin
                `ifndef SYNTHESIS
                // Simulation completion: pulse ready and provide data
                sim_mem_ready <= 1'b1;
                sim_mem_read_data <= bram_rdata;  // Capture read data
                
                // Clear pending flags
                if (sim_mem_read_pending) sim_mem_read_pending <= 1'b0;
                if (sim_mem_write_pending) sim_mem_write_pending <= 1'b0;
                `endif
                
                // Clear ownership
                bram_owner <= OWNER_NONE;
            end
            
            OWNER_AXI: begin
                // AXI completion is handled in the AXI state machine
                // Just clear ownership here
                bram_owner <= OWNER_NONE;
            end
            
            default: begin
                // Should not happen - clear ownership anyway
                bram_owner <= OWNER_NONE;
            end
        endcase
    end
    
    // =====================================================================
    // ARBITRATION STATE MACHINE
    // =====================================================================
    case (arb_state)
        ARB_IDLE: begin
            // Priority: AXI first (but only if no sim pending), then simulation
            if (axi_access_request) begin
                arb_state <= ARB_AXI_ACTIVE;
                axi_transaction_active <= 1'b1;  // Mark transaction as active
            end else if (sim_access_request) begin
                arb_state <= ARB_SIM_ACTIVE;
            end
        end
        
        ARB_AXI_ACTIVE: begin
            // Return to idle only when transaction completes
            // Transaction is complete when we return to IDLE state
            // after having processed a request
            if (state == IDLE && !axi_transaction_active) begin
                arb_state <= ARB_IDLE;
            end
        end
        
        ARB_SIM_ACTIVE: begin
            // Handle simulation memory access
            `ifndef SYNTHESIS
            if (sim_mem_read_pending || sim_mem_write_pending) begin
                // Only start BRAM operation if no owner yet
                if (bram_owner == OWNER_NONE) begin
                    bram_addr <= sim_mem_addr_latched;
                    bram_owner <= OWNER_SIM;
                    
                    if (sim_mem_read_pending) begin
                        bram_read <= 1'b1;
                    end else if (sim_mem_write_pending) begin
                        bram_write <= 1'b1;
                        bram_wdata <= sim_mem_write_data_latched;
                    end
                end
                // Stay in this state until bram_done clears pending flags
            end else begin
                // No pending operations, return to idle
                arb_state <= ARB_IDLE;
            end
            `else
            arb_state <= ARB_IDLE;
            `endif
        end
        
        default: arb_state <= ARB_IDLE;
    endcase

    // =====================================================================
    // AXI4-LITE STATE MACHINE (only when AXI is active)
    // =====================================================================
    if (arb_state == ARB_AXI_ACTIVE) begin
        case (state)
            // =============================================================
            // IDLE - Wait for AXI requests
            // =============================================================
            IDLE: begin
                status <= `RESP_OKAY;
                
                // Handle AXI write requests (address + data channels)
                s_axi.write_req_wait(latched_awaddr, latched_awprot, latched_wdata, latched_wstrb, done);
                if (done) state <= WRITE_READ;
                
                // Handle AXI read requests (address channel)
                s_axi.read_req_wait(latched_araddr, latched_arprot, done);
                if (done) state <= READ;
            end

            // =============================================================
            // WRITE_READ - Read existing data for read-modify-write
            // =============================================================
            WRITE_READ: begin
                if (bram_owner == OWNER_NONE) begin
                    bram_read <= 1'b1;
                    bram_addr <= latched_awaddr;
                    bram_owner <= OWNER_AXI;
                end
                
                if (bram_done && bram_owner == OWNER_AXI) begin
                    wdata_temp <= bram_rdata;
                    state <= WRITE_STRB;
                end
            end

            // =============================================================
            // WRITE_STRB - Apply write strobes to modify specific bytes
            // =============================================================
            WRITE_STRB: begin
                if (latched_wstrb[0]) wdata_temp[7:0] <= latched_wdata[7:0];
                if (latched_wstrb[1]) wdata_temp[15:8] <= latched_wdata[15:8];
                if (latched_wstrb[2]) wdata_temp[23:16] <= latched_wdata[23:16];
                if (latched_wstrb[3]) wdata_temp[31:24] <= latched_wdata[31:24];
                state <= WRITE;
            end

            // =============================================================
            // WRITE - Write the modified data back to BRAM
            // =============================================================
            WRITE: begin
                if (bram_owner == OWNER_NONE) begin
                    bram_write <= 1'b1;
                    bram_addr <= latched_awaddr;
                    bram_wdata <= wdata_temp;
                    bram_owner <= OWNER_AXI;
                end
                
                if (bram_done && bram_owner == OWNER_AXI) begin
                    state <= WRITE_RESP;
                end
            end

            // =============================================================
            // WRITE_RESP - Send write response back to AXI master
            // =============================================================
            WRITE_RESP: begin
                s_axi.write_resp(status, done);
                if (done) begin
                    state <= IDLE;
                    axi_transaction_active <= 1'b0;  // Transaction complete
                end
            end

            // =============================================================
            // READ - Read data from BRAM
            // =============================================================
            READ: begin
                if (bram_owner == OWNER_NONE) begin
                    bram_read <= 1'b1;
                    bram_addr <= latched_araddr;
                    bram_owner <= OWNER_AXI;
                end
                
                if (bram_done && bram_owner == OWNER_AXI) begin
                    rdata_temp <= bram_rdata;
                    state <= READ_RESP;
                end
            end

            // =============================================================
            // READ_RESP - Send read response back to AXI master
            // =============================================================
            READ_RESP: begin
                s_axi.read_resp(rdata_temp, status, done);
                if (done) begin
                    state <= IDLE;
                    axi_transaction_active <= 1'b0;  // Transaction complete
                end
            end

            // =============================================================
            // DEFAULT - Safety fallback
            // =============================================================
            default: state <= IDLE;
        endcase
    end

    end
end

endmodule