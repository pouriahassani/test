/**
 * AxE Path Definitions for RTL (Industry Standard)
 * 
 * Simple, reliable path definitions using -I flags.
 * No complex macro concatenations - follows major ASIC team practices.
 * 
 * Usage: Build system provides -I flags for path resolution
 *   make compile  # Uses -I flags automatically
 */

`ifndef DEFINES_PATHS_VH
`define DEFINES_PATHS_VH

// ============================================================================
// Memory File Paths (Simple Relative Paths)
// ============================================================================

// Main program memory - resolved via -I$(AXE_ROOT) flag
`define MEMORY_HEX_FILE "test.hex"

// ============================================================================
// NoC Routing Table Paths (Simple Relative Paths)
// ============================================================================

// 2x2 mesh routing tables - resolved via -I$(TOOLS_ROOT)/Routing_Table flag
`define ROUTING_TABLE_0 "mesh_4RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_2RTsPerRow_2RTsPerCol_routing_0.hex"
`define ROUTING_TABLE_1 "mesh_4RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_2RTsPerRow_2RTsPerCol_routing_1.hex"
`define ROUTING_TABLE_2 "mesh_4RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_2RTsPerRow_2RTsPerCol_routing_2.hex"
`define ROUTING_TABLE_3 "mesh_4RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_2RTsPerRow_2RTsPerCol_routing_3.hex"

// 5x4 mesh routing tables (examples)
`define ROUTING_5X4_TABLE_0 "mesh_20RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_4RTsPerRow_5RTsPerCol_routing_0.hex"
`define ROUTING_5X4_TABLE_1 "mesh_20RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_4RTsPerRow_5RTsPerCol_routing_1.hex"

// ============================================================================
// Usage Examples
// ============================================================================

/*
// In your RTL modules:
$readmemh(`MEMORY_HEX_FILE, memory_array, 0);
$readmemh(`ROUTING_TABLE_0, routing_table_0, 0);

// Build system provides -I flags:
//   -I$(AXE_ROOT)                    # for test.hex
//   -I$(TOOLS_ROOT)/Routing_Table    # for routing tables
*/

`endif // DEFINES_PATHS_VH