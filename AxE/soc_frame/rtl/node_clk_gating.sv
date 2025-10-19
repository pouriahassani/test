
/* ****************************************************************************
  This Source Code Form is subject to the terms of the
  Open Hardware Description License, v. 1.0. If a copy
  of the OHDL was not distributed with this file, You
  can obtain one at http://juliusbaxter.net/ohdl/ohdl.txt
  
  Copyright (C) 2019 Stefan Huemer <stefan@huemer.tech>
  
***************************************************************************** */
// PCPI_COUNT is now controlled via command line -DPCPI_COUNT
module node #(
     parameter ID = 0
    
    ,parameter SEND_TO = 0
    ,parameter BIG = 0
)
(
     input clk
    ,input res_n
    
    ,output trap
    
    // File I/O signals for simulation
    ,output wire        file_instr_valid
    ,output wire [31:0] file_instruction
    ,output wire [31:0] file_reg_a0
    ,output wire [31:0] file_reg_a1
    ,output wire [31:0] file_reg_a2
    ,output wire [31:0] axi_offset_out
    ,output wire [31:0] current_pc_for_sim
    ,output wire [31:0] mem_instr_for_sim
    ,output wire debug_file_detect_sim
    ,input wire         sim_file_op_complete
    ,output req_ack // Acknowledge for request completion

    
    ,if_connect.bridge    noc
);
    
    if_axi_light #(.AXI_WSTRB_WIDTH(`AXI_WSTRB_WIDTH)) if_axi_light_cpu_to_detector();
    if_axi_light #() if_axi_light_detector_to_file_io();
    if_axi_light #() if_axi_light_file_io_to_offset();
    
    if_axi_light #() if_axi_light_offset_to_mux();
    if_axi_light #() if_axi_light_self_awareness_to_mux();
    
    if_axi_light #() if_axi_light_mux_to_slave_bridge();
    
    wire w_activate;
    wire [ `AXI_ADDR_WIDTH-1:0 ] w_axi_offset;
    
    wire w_fin;
    
    //~ wire w_clk = clk && w_activate;
    
    wire w_clk_gated;
    wire w_res_n_gated;
    assign axi_offset_out = w_axi_offset;
    // -------------------------------------------------------------------------
    // C L K _ G A T E R
    // -------------------------------------------------------------------------
    
    clk_gater #() clk_gater_inst
    (
         .clk( clk )
        ,.res_n( w_activate )
        
        ,.clk_gated( w_clk_gated )
        ,.res_n_gated( w_res_n_gated )
    );
    
    // -------------------------------------------------------------------------
    // P I C O
    // -------------------------------------------------------------------------
    
    picorv32_if_wrapper
    #(
         .NODE_ID (ID),
         .ENABLE_MUL ( BIG )
        ,.ENABLE_DIV ( BIG )
    )
    picorv32_if_wrapper_inst
    (
         .clk( w_clk_gated )
        ,.res_n( w_res_n_gated )
        
        ,.trap( trap )
        ,.current_pc_for_sim(current_pc_for_sim)
        ,.mem_instr_for_sim (mem_instr_for_sim)
        ,.m_axi( if_axi_light_cpu_to_detector.master )
        `ifdef PCPI_COUNT
        ,.intmul_count (intmul_count )
        ,.intdiv_count (intdiv_count )
        ,.fpadd_count  (fpadd_count  )
        ,.fpsub_count  (fpsub_count  )
        ,.intmulx_count(intmulx_count)
        ,.fpmul_count  (fpmul_count  )
        ,.fpdiv_count  (fpdiv_count  )
        ,.fpmulx_count (fpmulx_count )
        `endif
    );
    
    // -------------------------------------------------------------------------
    // A X I _ D E T E C T O R
    // -------------------------------------------------------------------------
    
    axi_detector
    #(
         .ADDR_DETECT ( 32'h 00FF_FFFC )
        
        ,.DETECT_READ( 0 )
        ,.DETECT_WRITE( 1 )
        
        ,.GREATER_THAN( 0 )
        
        ,.SIGNAL_PULSE( 1 )
        ,.FORWARD( 0 )
    )
    axi_detector_inst
    (
         .clk( w_clk_gated )
        ,.res_n( w_res_n_gated )
        
        ,.s_axi( if_axi_light_cpu_to_detector.slave )
        ,.m_axi( if_axi_light_detector_to_file_io.master )
        
        ,.sig( w_fin )
        ,.data(  )
    );
    
    // -------------------------------------------------------------------------
    // F I L E _ I O _ D E T E C T O R
    // -------------------------------------------------------------------------
    
    // File I/O detector signals
    wire        w_file_instr_valid;
    wire [31:0] w_file_instruction;
    wire [31:0] w_file_reg_a0;
    wire [31:0] w_file_reg_a1;
    wire [31:0] w_file_reg_a2;
    
    file_io_detector
    #(
     //     .DETECT_ADDR_BASE( 32'h 00FF_FF00 )
    )
    file_io_detector_inst
    (
         .clk( w_clk_gated )
        ,.res_n( w_res_n_gated )
        
        ,.axi_offset( w_axi_offset )
        
        ,.file_instr_valid( w_file_instr_valid )
        ,.file_instruction( w_file_instruction )
        ,.file_reg_a0( w_file_reg_a0 )
        ,.file_reg_a1( w_file_reg_a1 )
        ,.file_reg_a2( w_file_reg_a2 )
        ,.debug_file_detect_sim(debug_file_detect_sim)
        ,.sim_file_op_complete( sim_file_op_complete )
        ,.req_ack( req_ack ) // Acknowledge for request completion
        ,.s_axi( if_axi_light_detector_to_file_io.slave )
        ,.m_axi( if_axi_light_file_io_to_offset.master )
    );
    
    // -------------------------------------------------------------------------
    // A X I _ O F F S E T
    // -------------------------------------------------------------------------
    
    axi_offset
    #(
         .OFFSET( 0 )
        ,.USE_PARAMETER( 0 )
    )
    axi_offset_inst
    (
         .s_axi( if_axi_light_file_io_to_offset.slave )
        ,.m_axi( if_axi_light_offset_to_mux.master )
        
        ,.offset( w_axi_offset )
    );
    
    // -------------------------------------------------------------------------
    // S E L F _ A W A R E N E S S
    // -------------------------------------------------------------------------
    
    self_awareness
    #(
         .ID( ID )
    )
    self_awareness_inst
    (
         .clk( clk )
        ,.res_n( res_n )
        
        ,.activate( w_activate )
        ,.axi_offset( w_axi_offset )
        
        ,.fin( w_fin )
        
        ,.m_axi( if_axi_light_self_awareness_to_mux.master )
        `ifdef PCPI_COUNT
        ,.intmul_count (intmul_count )
        ,.intdiv_count (intdiv_count )
        ,.fpadd_count  (fpadd_count  )
        ,.fpsub_count  (fpsub_count  )
        ,.intmulx_count(intmulx_count)
        ,.fpmul_count  (fpmul_count  )
        ,.fpdiv_count  (fpdiv_count  )
        ,.fpmulx_count (fpmulx_count )
        `endif
    );
    
    // -------------------------------------------------------------------------
    // A X I _ M U X
    // -------------------------------------------------------------------------
    
    axi_mux #() axi_mux_inst
    (
         .selector( w_activate )
        
        ,.s_axi_0( if_axi_light_self_awareness_to_mux.slave )
        ,.s_axi_1( if_axi_light_offset_to_mux.slave )
        
        ,.m_axi_0( if_axi_light_mux_to_slave_bridge.master )
    );
    
    // -------------------------------------------------------------------------
    // S L A V E _ B R I D G E
    // -------------------------------------------------------------------------
    
    bridge_slave
    #(
         .ID( ID )
        
        ,.SEND_TO( SEND_TO )
    )
    bridge_slave_inst
    (
         .clk( clk )
        ,.res_n( res_n )
        
        ,.s_axi( if_axi_light_mux_to_slave_bridge.slave )
        ,.noc( noc )
    );
    
    // Connect internal file I/O signals to module outputs
    assign file_instr_valid = w_file_instr_valid;
    assign file_instruction = w_file_instruction;
    assign file_reg_a0 = w_file_reg_a0;
    assign file_reg_a1 = w_file_reg_a1;
    assign file_reg_a2 = w_file_reg_a2;

endmodule
