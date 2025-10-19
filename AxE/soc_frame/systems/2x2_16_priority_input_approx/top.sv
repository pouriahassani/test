
/* ****************************************************************************
  This Source Code Form is subject to the terms of the
  Open Hardware Description License, v. 1.0. If a copy
  of the OHDL was not distributed with this file, You
  can obtain one at http://juliusbaxter.net/ohdl/ohdl.txt
  
  Copyright (C) 2019 Stefan Huemer <stefan@huemer.tech>
  
***************************************************************************** */

// exact: 56088
// approx: 55632

`include "defines.vh"
`include "../../rtl/defines_paths.vh"

`include "defines_arch.vh"
`include "defines_nodes.vh"

`include "defines_axi.vh"
`include "defines_noc.vh"
`include "defines_mem.vh"
`include "defines_clk.vh"

`include "defines_ascii.vh"
`include "defines_debugger.vh"

`ifdef AXE_ROOT_DEFINE
    `include "interfaces/if_axi_light.sv"
    `include "interfaces/if_connect.sv"
    
    `include "res_n_syn/res_n_syn.sv"
    
    `include "PiXo/picorv32_extended.v"
    
    `include "PiXo/picorv32_if_wrapper.sv"
    
    `include "memory/bram_controller.sv"
    `include "memory/bram.sv"
    
    `include "axi_detector/axi_detector.sv"
    
    `include "buffer/ring_buffer.sv"
    `include "debugger/debugger.sv"
    `include "file_io_detector/file_io_detector.sv"
    `include "axi_offset/axi_offset.sv"
    
    `include "axi_arbiter/axi_arbiter.sv"
    
    `include "axi_mux/axi_mux.sv"
`else
    `include "../../rtl/interfaces/if_axi_light.sv"
    `include "../../rtl/interfaces/if_connect.sv"
    `include "../../rtl/file_io_detector/file_io_detector.sv"
    `include "../../rtl/res_n_syn/res_n_syn.sv"
    
    `include "../../rtl/PiXo/picorv32_extended.v"
    
    `include "../../rtl/PiXo/picorv32_if_wrapper.sv"
    
    `include "../../rtl/memory/bram_controller.sv"
    `include "../../rtl/memory/bram.sv"
    
    `include "../../rtl/axi_detector/axi_detector.sv"
    
    `include "../../rtl/buffer/ring_buffer.sv"
    `include "../../rtl/debugger/debugger.sv"
    
    `include "../../rtl/axi_offset/axi_offset.sv"
    
    `include "../../rtl/axi_arbiter/axi_arbiter.sv"
    
    `include "../../rtl/axi_mux/axi_mux.sv"
`endif
`ifdef AXE_ROOT_DEFINE
    `include "axi_demux/axi_demux.sv"
    
    `include "control/control.sv"
    
    `include "self_awareness/self_awareness.sv"
    
    `include "bridge/bridge_slave_none_missing.sv"
    `include "bridge/bridge_slave_missing.sv"
    `include "bridge/bridge_slave.sv"
    
    `include "bridge/flit_buffer_none_missing.sv"
    `include "bridge/flit_buffer_missing.sv"
    `include "bridge/flit_buffer.sv"
    
    `include "bridge/bridge_master.sv"
    
    `include "noc/if_wrapper_noc_2x2_16.sv"
`else
    `include "../../rtl/axi_demux/axi_demux.sv"
    
    `include "../../rtl/control/control.sv"
    
    `include "../../rtl/self_awareness/self_awareness.sv"
    
    `include "../../rtl/bridge/bridge_slave_none_missing.sv"
    `include "../../rtl/bridge/bridge_slave_missing.sv"
    `include "../../rtl/bridge/bridge_slave.sv"
    
    `include "../../rtl/bridge/flit_buffer_none_missing.sv"
    `include "../../rtl/bridge/flit_buffer_missing.sv"
    `include "../../rtl/bridge/flit_buffer.sv"
    
    `include "../../rtl/bridge/bridge_master.sv"
    
    `include "../../rtl/noc/if_wrapper_noc_2x2_16.sv"
`endif

// TODO -> add to doc
// throughout the source code the defines are used like in the following
// case to avoid the use of `ifndef as the "n" is easy to miss.

`ifdef AXE_ROOT_DEFINE
    `include  "noc/noc_connect_2x2_16/mkInputQueue.v"
    `include  "noc/noc_connect_2x2_16/mkIQRouterCoreSimple.v"
    `include  "noc/noc_connect_2x2_16/mkNetworkSimple.v"
    `include  "noc/noc_connect_2x2_16/mkOutPortFIFO.v"
    `include  "noc/noc_connect_2x2_16/mkRouterInputArbitersRoundRobin.v"
    `include  "noc/noc_connect_2x2_16/mkRouterOutputArbitersRoundRobin.v"
    `include  "noc/noc_connect_2x2_16/mkSepRouterAllocator.v"
    `include  "noc/noc_connect_2x2_16/module_gen_grant_carry.v"
    `include  "noc/noc_connect_2x2_16/module_outport_encoder.v"
    `include  "noc/noc_connect_2x2_16/RegFile_1port.v"
    `include  "noc/noc_connect_2x2_16/RegFileLoadSyn.v"
    
    `include "clk_gater/clk_gater.sv"
    
    // the following are modules that do not contain any logic.
    // they are only used to bundle other modules together.
    
    //~ `include "node.sv"
    `include "node_clk_gating.sv"
    
    //~ `include "controller_noc.sv"
    `include "controller_axi.sv"
    
    //~ `include `RTL_ROOT"/memory_controller.sv"
    `include "memory_controller_priority_input.sv"
`else
    `include "../../rtl/noc/noc_connect_2x2_16/mkInputQueue.v"
    `include "../../rtl/noc/noc_connect_2x2_16/mkIQRouterCoreSimple.v"
    `include "../../rtl/noc/noc_connect_2x2_16/mkNetworkSimple.v"
    `include "../../rtl/noc/noc_connect_2x2_16/mkOutPortFIFO.v"
    `include "../../rtl/noc/noc_connect_2x2_16/mkRouterInputArbitersRoundRobin.v"
    `include "../../rtl/noc/noc_connect_2x2_16/mkRouterOutputArbitersRoundRobin.v"
    `include "../../rtl/noc/noc_connect_2x2_16/mkSepRouterAllocator.v"
    `include "../../rtl/noc/noc_connect_2x2_16/module_gen_grant_carry.v"
    `include "../../rtl/noc/noc_connect_2x2_16/module_outport_encoder.v"
    `include "../../rtl/noc/noc_connect_2x2_16/RegFile_1port.v"
    `include "../../rtl/noc/noc_connect_2x2_16/RegFileLoadSyn.v"
    
    `include "../../rtl/clk_gater/clk_gater.sv"
    
    // the following are modules that do not contain any logic.
    // they are only used to bundle other modules together.
    
    //~ `include "../../rtl/node.sv"
    `include "../../rtl/node_clk_gating.sv"
    
    //~ `include "../../rtl/controller_noc.sv"
    `include "../../rtl/controller_axi.sv"
    
    //~ `include "../../rtl/memory_controller.sv"
    `include "../../rtl/memory_controller_priority_input.sv"
`endif

`ifdef SYNTHESIS
    `ifdef AXE_ROOT_DEFINE
        `include "uart/uart.sv"
        
        `include "uart/uart_clk.sv"
        `include "uart/uart_tx.sv"
    `else
        `include "../../rtl/uart/uart.sv"
        
        `include "../../rtl/uart/uart_clk.sv"
        `include "../../rtl/uart/uart_tx.sv"
    `endif
`endif

module top
(
     input clk
    ,(* mark_debug = "true" *) input res_n
    
    // debugging
    
    `ifdef SYNTHESIS
        
        ,(* mark_debug = "true" *) output tx_out
        
    `else
        
        ,output [ `ASCII_WIDTH-1:0 ] buffer_out_data
        ,output buffer_out_valid
        ,input buffer_recv_busy
        
    `endif
    
    ,(* mark_debug = "true" *) output trap
    ,output trap_nodes
    
    ,output [ 7:0 ] leds_status
    ,output [ 7:0 ] triggers

    // File I/O signals for simulation
    ,output wire        file_instr_valid_0
    ,output wire [31:0] file_instruction_0
    ,output wire [31:0] file_reg_a0_0
    ,output wire [31:0] file_reg_a1_0
    ,output wire [31:0] file_reg_a2_0
    ,output wire [31:0] axi_offset_0
    
    ,output wire        file_instr_valid_1
    ,output wire [31:0] file_instruction_1
    ,output wire [31:0] file_reg_a0_1
    ,output wire [31:0] file_reg_a1_1
    ,output wire [31:0] file_reg_a2_1
    ,output wire [31:0] axi_offset_1
    ,output wire [31:0]current_pc_for_sim
    ,output wire [31:0]mem_instr_for_sim 
    ,output wire debug_file_detect_sim0
    ,output wire debug_file_detect_sim1
    // Memory debug interface for simulation
    `ifndef SYNTHESIS
    ,input  wire [31:0] sim_mem_addr
    ,input  wire        sim_mem_read_en
    ,output wire [31:0] sim_mem_read_data
    ,output wire        sim_mem_ready
    ,input  wire [31:0] sim_mem_write_data
    ,input  wire        sim_mem_write_en
    ,input  wire        sim_file_op_complete_0
    ,output wire req_ack_0 // Acknowledge for request completion
    ,output wire req_ack_1 // Acknowledge for request completion
    ,input  wire        sim_file_op_complete_1
    `endif
);
    
    assign trap_nodes = trap_0  ||
                        trap_1;
    
    // -------------------------------------------------------------------------
    // PARAMETERS
    // -------------------------------------------------------------------------
    
    //---------------------
    // SYSTEM ITSELF
    //---------------------
    
    // the NoC id to which the memory controller is connected.
    
    parameter NOC_MEM_ADDR = 2'b10;
    //~ parameter NOC_MEM_ADDR = 4'b0010;
    
    // -------------------------------------------------------------------------
    // WIRES
    // -------------------------------------------------------------------------
    
    // all the debugging signals are outputted from the nodes and
    // combined into a parallel signal and fed into the debugger relay.
    
    // ring buffer
    
    `ifdef SYNTHESIS
        
        wire [ `ASCII_WIDTH-1:0 ] buffer_out_data;
        wire buffer_out_valid;
        wire buffer_recv_busy;
        
    `endif
    
    wire w_res_n_syn;
    
    wire [ `ASCII_WIDTH-1:0 ] w_ascii_c_0;
    wire                      w_ascii_s_0;
    
    wire trap_0;
    wire trap_1;
    
    // -------------------------------------------------------------------------
    // INTERFACES
    // -------------------------------------------------------------------------
    
    // NoC interfaces
    
    if_connect #() if_connect_node_empty();
    
    if_connect #() if_connect_node_0();
    if_connect #() if_connect_node_1();
    
    if_connect #() if_connect_memory();
    
    if_axi_light #() if_axi_light_controller();
    
    // -------------------------------------------------------------------------
    // R E S _ N _ S Y N
    // -------------------------------------------------------------------------
    
    res_n_syn #() res_n_syn_inst
    (
         .clk( clk )
        ,.res_n( res_n )
        
        ,.res_n_syn( w_res_n_syn )
    );
    
    // -------------------------------------------------------------------------
    // O U T P U T
    // -------------------------------------------------------------------------
    
    `ifdef SYNTHESIS
        
        uart
        #(
             .BAUD( 921600 )
        )
        uart_inst
        (
             .clk( clk )
            ,.res_n( w_res_n_syn )
            
            ,.wr( buffer_out_valid )
            ,.data( buffer_out_data )
            
            ,.tx( tx_out )
            ,.busy( buffer_recv_busy )
        );
        
    `endif
    
    ring_buffer
    #(
        
         .DATA_WIDTH( 7 )
        ,.BUFFER_DEPTH( 150 )
        
        ,.ALLOW_OVERWRITE_ON_FULL( 0 )
    )
    ring_buffer_inst
    (
         .clk( clk )
        ,.res_n( w_res_n_syn )
        
        ,.data_in( w_ascii_c_0 )
        ,.data_in_valid( w_ascii_s_0 )
        
        ,.data_out( buffer_out_data )
        ,.data_out_valid( buffer_out_valid )
        
        ,.full(  )
        ,.recv_busy( buffer_recv_busy )
        
    );
    
    // -------------------------------------------------------------------------
    // C O N T R O L L E R
    // -------------------------------------------------------------------------
    
    controller
    #(
         .ID( 9 )
        
        ,.SEND_TO( NOC_MEM_ADDR )
    )
    controller_inst
    (
         .clk( clk )
        ,.res_n( w_res_n_syn )
        
        ,.trap( trap )
        
        ,.if_axi_controller_master( if_axi_light_controller.master )
        //~ ,.noc( if_connect_node_controller.bridge )
        
        ,.debugger_sig( w_ascii_s_0 )
        ,.debugger_ascii( w_ascii_c_0 )
    );
    
    // -------------------------------------------------------------------------
    // N O D E s
    // -------------------------------------------------------------------------
    
    node #( .ID(  0),.SEND_TO( NOC_MEM_ADDR ),.BIG(  `N0_ARCH ) ) node_0  ( 
        .clk( clk ),
        .res_n( w_res_n_syn ),
        .trap( trap_0 ),
        .file_instr_valid( file_instr_valid_0 ),
        .file_instruction( file_instruction_0 ),
        .file_reg_a0( file_reg_a0_0 ),
        .file_reg_a1( file_reg_a1_0 ),
        .axi_offset_out( axi_offset_0 ),
        .file_reg_a2( file_reg_a2_0 ),
        .current_pc_for_sim(current_pc_for_sim),
        .mem_instr_for_sim(mem_instr_for_sim),
        .debug_file_detect_sim(debug_file_detect_sim0),
        `ifndef SYNTHESIS
        .sim_file_op_complete( sim_file_op_complete_0 ),
        .req_ack( req_ack_0), // Acknowledge for request completion
        `endif
        .noc( if_connect_node_0.bridge )
    );
    
    node #( .ID( 1),.SEND_TO( NOC_MEM_ADDR ),.BIG(  `N1_ARCH ) ) node_1  ( 
        .clk( clk ),
        .res_n( w_res_n_syn ),
        .trap( trap_1 ),
        .file_instr_valid( file_instr_valid_1 ),
        .file_instruction( file_instruction_1 ),
        .file_reg_a0( file_reg_a0_1 ),
        .file_reg_a1( file_reg_a1_1 ),
        .file_reg_a2( file_reg_a2_1 ),
        .axi_offset_out( axi_offset_1 ),
        .debug_file_detect_sim(debug_file_detect_sim1),
        `ifndef SYNTHESIS
        .sim_file_op_complete( sim_file_op_complete_1 ),
        .req_ack( req_ack_1), // Acknowledge for request completion
        `endif
        .noc( if_connect_node_1.bridge )
    );
    //~ node #( .ID(  2 ),.SEND_TO( NOC_MEM_ADDR ),.BIG(  `N2_ARCH ) ) node_2  ( .clk( clk ),.res_n( w_res_n_syn ),.trap( trap_2  ),.noc( if_connect_node_2.bridge  ) );
    //~ node #( .ID(  3 ),.SEND_TO( NOC_MEM_ADDR ),.BIG(  `N3_ARCH ) ) node_3  ( .clk( clk ),.res_n( w_res_n_syn ),.trap( trap_3  ),.noc( if_connect_node_3.bridge  ) );
    //~ node #( .ID(  4 ),.SEND_TO( NOC_MEM_ADDR ),.BIG(  `N4_ARCH ) ) node_4  ( .clk( clk ),.res_n( w_res_n_syn ),.trap( trap_4  ),.noc( if_connect_node_4.bridge  ) );
    //~ node #( .ID(  5 ),.SEND_TO( NOC_MEM_ADDR ),.BIG(  `N5_ARCH ) ) node_5  ( .clk( clk ),.res_n( w_res_n_syn ),.trap( trap_5  ),.noc( if_connect_node_5.bridge  ) );
    //~ node #( .ID(  6 ),.SEND_TO( NOC_MEM_ADDR ),.BIG(  `N6_ARCH ) ) node_6  ( .clk( clk ),.res_n( w_res_n_syn ),.trap( trap_6  ),.noc( if_connect_node_6.bridge  ) );
    //~ node #( .ID(  7 ),.SEND_TO( NOC_MEM_ADDR ),.BIG(  `N7_ARCH ) ) node_7  ( .clk( clk ),.res_n( w_res_n_syn ),.trap( trap_7  ),.noc( if_connect_node_7.bridge  ) );
    //~ node #( .ID(  8 ),.SEND_TO( NOC_MEM_ADDR ),.BIG(  `N8_ARCH ) ) node_8  ( .clk( clk ),.res_n( w_res_n_syn ),.trap( trap_8  ),.noc( if_connect_node_8.bridge  ) );
    //~ node #( .ID(  9 ),.SEND_TO( NOC_MEM_ADDR ),.BIG(  `N9_ARCH ) ) node_9  ( .clk( clk ),.res_n( w_res_n_syn ),.trap( trap_9  ),.noc( if_connect_node_9.bridge  ) );
    //~ node #( .ID( 10 ),.SEND_TO( NOC_MEM_ADDR ),.BIG( `N10_ARCH ) ) node_10 ( .clk( clk ),.res_n( w_res_n_syn ),.trap( trap_10 ),.noc( if_connect_node_10.bridge ) );
    //~ node #( .ID( 11 ),.SEND_TO( NOC_MEM_ADDR ),.BIG( `N11_ARCH ) ) node_11 ( .clk( clk ),.res_n( w_res_n_syn ),.trap( trap_11 ),.noc( if_connect_node_11.bridge ) );
    //~ node #( .ID( 12 ),.SEND_TO( NOC_MEM_ADDR ),.BIG( `N12_ARCH ) ) node_12 ( .clk( clk ),.res_n( w_res_n_syn ),.trap( trap_12 ),.noc( if_connect_node_12.bridge ) );
    //~ node #( .ID( 13 ),.SEND_TO( NOC_MEM_ADDR ),.BIG( `N13_ARCH ) ) node_13 ( .clk( clk ),.res_n( w_res_n_syn ),.trap( trap_13 ),.noc( if_connect_node_13.bridge ) );
    //~ node #( .ID( 14 ),.SEND_TO( NOC_MEM_ADDR ),.BIG( `N14_ARCH ) ) node_14 ( .clk( clk ),.res_n( w_res_n_syn ),.trap( trap_14 ),.noc( if_connect_node_14.bridge ) );
    //~ node #( .ID( 15 ),.SEND_TO( NOC_MEM_ADDR ),.BIG( `N15_ARCH ) ) node_15 ( .clk( clk ),.res_n( w_res_n_syn ),.trap( trap_15 ),.noc( if_connect_node_15.bridge ) );
    //~ node #( .ID( 16 ),.SEND_TO( NOC_MEM_ADDR ),.BIG( `N16_ARCH ) ) node_16 ( .clk( clk ),.res_n( res_n ),.noc( if_connect_node_16.bridge ) );
    //~ node #( .ID( 17 ),.SEND_TO( NOC_MEM_ADDR ),.BIG( `N17_ARCH ) ) node_17 ( .clk( clk ),.res_n( res_n ),.noc( if_connect_node_17.bridge ) );
    //~ node #( .ID( 18 ),.SEND_TO( NOC_MEM_ADDR ),.BIG( `N18_ARCH ) ) node_18 ( .clk( clk ),.res_n( res_n ),.noc( if_connect_node_18.bridge ) );
    //~ node #( .ID( 19 ),.SEND_TO( NOC_MEM_ADDR ),.BIG( `N19_ARCH ) ) node_19 ( .clk( clk ),.res_n( res_n ),.noc( if_connect_node_19.bridge ) );
    //~ node #( .ID( 20 ),.SEND_TO( NOC_MEM_ADDR ),.BIG( `N20_ARCH ) ) node_20 ( .clk( clk ),.res_n( res_n ),.noc( if_connect_node_20.bridge ) );
    //~ node #( .ID( 21 ),.SEND_TO( NOC_MEM_ADDR ),.BIG( `N21_ARCH ) ) node_21 ( .clk( clk ),.res_n( res_n ),.noc( if_connect_node_21.bridge ) );
    //~ node #( .ID( 22 ),.SEND_TO( NOC_MEM_ADDR ),.BIG( `N22_ARCH ) ) node_22 ( .clk( clk ),.res_n( res_n ),.noc( if_connect_node_22.bridge ) );
    //~ node #( .ID( 23 ),.SEND_TO( NOC_MEM_ADDR ),.BIG( `N23_ARCH ) ) node_23 ( .clk( clk ),.res_n( res_n ),.noc( if_connect_node_23.bridge ) );
    
    // -------------------------------------------------------------------------
    // M E M O R Y _ C O N T R O L L E R
    // -------------------------------------------------------------------------
    
    memory_controller #() memory_controller_inst
    (
         .clk( clk )
        ,.res_n( w_res_n_syn )
        
        ,.if_axi_priority_input_slave( if_axi_light_controller.slave )
        
        ,.noc( if_connect_memory.bridge )
        
        ,.leds_status( leds_status )
        ,.triggers( triggers )
        
        `ifndef SYNTHESIS
        ,.sim_mem_addr      ( sim_mem_addr      )
        ,.sim_mem_read_en   ( sim_mem_read_en   )
        ,.sim_mem_read_data ( sim_mem_read_data )
        ,.sim_mem_ready     ( sim_mem_ready     )
        ,.sim_mem_write_data( sim_mem_write_data)
        ,.sim_mem_write_en  ( sim_mem_write_en  )
        `endif
    );
    
    // -------------------------------------------------------------------------
    // N O C
    // -------------------------------------------------------------------------
    
    if_wrapper_noc_2x2_16 #() if_wrapper_noc_2x2_16_inst
    (
         .clk( clk )
        ,.res_n( w_res_n_syn )
        
        ,.noc_0 ( if_connect_node_0.noc     )
        ,.noc_1 ( if_connect_node_1.noc     )
        
        ,.noc_2 ( if_connect_memory.noc     )
        
        ,.noc_3 ( if_connect_node_empty.noc )
    );
    
endmodule
