
/* ****************************************************************************
  This Source Code Form is subject to the terms of the
  Open Hardware Description License, v. 1.0. If a copy
  of the OHDL was not distributed with this file, You
  can obtain one at http://juliusbaxter.net/ohdl/ohdl.txt
  
  Copyright (C) 2019 Stefan Huemer <stefan@huemer.tech>
  
***************************************************************************** */
`define DEBUG_SELF_AWARENESS
// PCPI_COUNT is now controlled via command line -DPCPI_COUNT
module self_awareness
#(
     parameter ID = 0
)
(
     input clk
    ,input res_n
    
    //~ ,(* mark_debug = "true" *) output reg activate
    //~ ,(* mark_debug = "true" *) output reg [ `AXI_ADDR_WIDTH-1:0 ] axi_offset
    ,output reg activate
    ,output reg [ `AXI_ADDR_WIDTH-1:0 ] axi_offset
    
    //~ ,(* mark_debug = "true" *) input fin
    ,input fin
    
    ,if_axi_light.master  m_axi
    `ifdef PCPI_COUNT
    ,input [63:0] intmul_count
    ,input [63:0] intdiv_count
    ,input [63:0] fpadd_count
    ,input [63:0] fpsub_count
    ,input [63:0] intmulx_count
    ,input [63:0] fpmul_count
    ,input [63:0] fpdiv_count
    ,input [63:0] fpmulx_count
    `endif
);

//~ (* mark_debug = "true" *) enum
enum
{
     READ
    ,READ_WAIT
    ,EVAL
    ,FIN_WAIT
    ,WRITE
    ,WRITE_WAIT
}state;

parameter INDEX_CONTROL = `AXI_ADDR_WIDTH-1;

// the range which holds the node id. this starts at 2, as the 2 least
// significant bits are not used (byte addressing)

// TODO - could be done with node_processing_with like in the control module

parameter PICO_MSB = 6;
parameter PICO_LSB = 2;

parameter INDEX_PROG = 7;

// set in reset

//~ (* mark_debug = "true" *) reg[ `AXI_ADDR_WIDTH-1:0 ] addr_id;
reg[ `AXI_ADDR_WIDTH-1:0 ] addr_id;

// req
reg[ `AXI_ADDR_WIDTH*2-1:0 ] busy_counter;
reg[ `AXI_ADDR_WIDTH-1:0 ] latched_awaddr;
reg[                 2:0 ] latched_awprot;

reg[ `AXI_DATA_WIDTH-1:0 ] latched_wdata;
reg[`AXI_WSTRB_WIDTH-1:0 ] latched_wstrb;

reg[ `AXI_ADDR_WIDTH-1:0 ] latched_araddr;
reg[                 2:0 ] latched_arprot;

// resp

reg[                 1:0 ] latched_bresp;

reg[                 1:0 ] latched_rresp;
reg[ `AXI_DATA_WIDTH-1:0 ] latched_rdata;

reg done;

always @ ( posedge clk )
begin : self_awareness_proc
    
    m_axi.m_default();
    
    if ( ! res_n )
    begin
        
        state = READ;
        
        activate = 1'b0;
        
        addr_id = 0;
        addr_id[ INDEX_CONTROL     ] = 1'b1;
        addr_id[ INDEX_PROG        ] = 1'b1;
        addr_id[ PICO_MSB:PICO_LSB ] = ID;
        busy_counter <= 0;
        done = 0;
        
        // axi stuff
        
        // req
        
        latched_awaddr = 0;
        latched_awprot = 0;
        
        latched_wdata = 0;
        latched_wstrb = 0;
        
        latched_araddr = 0;
        latched_arprot = 0;
        
        // resp
        
        latched_bresp = 0;
        
        latched_rresp = 0;
        latched_rdata = 0;
        
    end
    else
    begin
        
        case(state)
        
        // ---------------------------------------------------------------------
        // READ
        // ---------------------------------------------------------------------
        
        // polling the control to find out if there is a program for the CPU to
        // execute
        
        READ :
        begin
            
            m_axi.read_req( addr_id, latched_arprot, done );
            if ( done == 1'b1 ) state = READ_WAIT;
            
        end
        
        // ---------------------------------------------------------------------
        // READ_WAIT
        // ---------------------------------------------------------------------
        
        READ_WAIT :
        begin
            
            m_axi.read_resp_wait( latched_rdata, latched_rresp, done );
            if ( done == 1'b1 ) state = EVAL;
            
        end
        
        // ---------------------------------------------------------------------
        // EVAL
        // ---------------------------------------------------------------------
        
        // once the read response has arrived we check if a task has been
        // assigned to the node.
        // this is the case if the rdata holds anything but 0.
        
        EVAL :
        begin
            
            if ( latched_rdata == 0 ) state = READ;
            else
            begin                
                `ifdef DEBUG_SELF_AWARENESS
                    $display( "\nNode %d starting cycle %0d\n",ID, busy_counter);   
                    $display( "SELF_AWARENESS: got program at addr: %h", latched_rdata );                                      
                `endif


                
                // the read data represents the address where the task is
                // located. this address will be added to all the read and
                // write requests by the CPU as an offset.
                
                activate = 1'b1;
                axi_offset = latched_rdata;
                
                state = FIN_WAIT;
                
            end
            
        end
        
        // ---------------------------------------------------------------------
        // FIN_WAIT
        // ---------------------------------------------------------------------
        
        FIN_WAIT :
        begin
            
            if ( fin == 1'b1 )
            begin
                `ifdef DEBUG_SELF_AWARENESS                        
                    $display( "SELF_AWARENESS: FIN" );   
                    $display( "\nNumber of busy cycles of node %d: %0d\n",ID, $unsigned(busy_counter));                        
                `endif
                `ifdef PCPI_COUNT
                    $display( "PCPI counts: intmul %0d, intdiv %0d, fpadd %0d, fpsub %0d, intmulx %0d, fpmul %0d, fpdiv %0d, fpmulx %0d", 
                        intmul_count, intdiv_count, fpadd_count, fpsub_count,
                        intmulx_count, fpmul_count, fpdiv_count, fpmulx_count );
                `endif
                
                activate = 1'b0;
                axi_offset = 0;
                
                state = WRITE;
                
            end
            else busy_counter <= busy_counter + 1;
        end
        
        // ---------------------------------------------------------------------
        // WRITE
        // ---------------------------------------------------------------------
        
        WRITE :
        begin
            
            m_axi.write_req( addr_id, latched_awprot, 0, latched_wstrb, done );
            if ( done == 1'b1 ) state = WRITE_WAIT;
            
        end
        
        // ---------------------------------------------------------------------
        // WRITE_WAIT
        // ---------------------------------------------------------------------
        
        WRITE_WAIT :
        begin
            
            m_axi.write_resp_wait( latched_bresp, done );
            if ( done == 1'b1 ) state = READ;
            
        end
        
        // ---------------------------------------------------------------------
        // DEFAULT
        // ---------------------------------------------------------------------
        
        default : state = READ;
        
        endcase
    end

end

endmodule
