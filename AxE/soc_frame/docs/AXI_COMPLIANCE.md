# AXI Protocol Compliance in AxE SoC

## Overview

The AxE SoC uses AXI4-Lite protocol for all internal communication between processing cores, memory controllers, and peripheral devices. This document outlines AXI compliance requirements and current implementation status.

## AXI4-Lite Protocol Requirements

### Write Transaction Phases

AXI4-Lite write transactions consist of three independent phases:

1. **Write Address Phase**: `awvalid`/`awready` handshake
2. **Write Data Phase**: `wvalid`/`wready` handshake  
3. **Write Response Phase**: `bvalid`/`bready` handshake

### Key Protocol Rules

#### 1. Transaction Independence
- Address and write data phases can complete in any order
- Both phases must complete before write response is generated
- Master can pipeline multiple transactions

#### 2. Handshake Requirements
- Transaction occurs when both `valid` and `ready` are HIGH
- Once `valid` is asserted, it must remain HIGH until handshake
- `ready` can be asserted before, during, or after `valid`

#### 3. Transaction Commitment
- Once a handshake occurs, the transaction is committed
- Slave must process all committed transactions
- Slave cannot reject committed transaction phases

## Current Implementation Status

## System Architecture

### AXI Interconnect Block Diagram

```
┌─────────────┐    ┌──────────────┐    ┌───────────────┐    ┌──────────────┐
│ PicoRV32    │    │ AXI Detector │    │ File I/O      │    │ Memory       │
│ Core        │────│              │────│ Detector      │────│ Controller   │
│             │    │              │    │               │    │              │
└─────────────┘    └──────────────┘    └───────────────┘    └──────────────┘
      │                     │                   │                    │
      │ AXI4-Lite          │ AXI4-Lite        │ AXI4-Lite         │
      │ Write Req          │ Passthrough      │ Transaction       │
      │                    │ + Detection      │ Blocking          │
      │                    │                  │                   │
      ▼                    ▼                  ▼                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    AXI Transaction Flow                             │
│                                                                     │
│  Normal Operation:   awvalid/awready → wvalid/wready → bvalid/bready │
│  File Operation:     DETECT → BLOCK → SIMULATE → RESPOND → UNBLOCK  │
└─────────────────────────────────────────────────────────────────────┘
```

### Compliant Modules

#### Memory Controller (`memory_controller_priority_input.sv`)
- **Write transactions**: Proper address/data phase handling
- **Response timing**: Correct `bvalid`/`bready` handshaking  
- **Ready signals**: Stable throughout transaction lifecycle

#### AXI Detector (`axi_detector.sv`) - **Recently Fixed**
- **Issue**: Missing `bready`/`rready` connections for internal responses
- **Fix Applied**: Added proper ready signal forwarding:
  ```verilog
  // For write responses generated internally
  if (resp_from == RESP_FROM_THIS) begin
      s_axi.bvalid = r_bvalid;
      m_axi.bready = s_axi.bready;  // ✅ Fixed missing connection
      s_axi.bresp = RESP_OKAY;
  end
  ```

### Non-Compliant Modules

#### File I/O Detector (`file_io_detector.sv`) - Active Issue

**Problem**: Ready signal timing violation during file operations

**Violation Details:**
```verilog
// Current problematic implementation
if (detected_file_op || state == WAIT_SIM_COMPLETE || ...) begin
    s_axi.awready = 0;  // ❌ May reject committed address phase
    s_axi.wready = 0;   // ❌ May reject committed write data phase
    
    // Later in response phase
    s_axi.awready = 1;  // ❌ Incorrect timing for ready signals
    s_axi.wready = 1;   
end
```

**AXI Violation**: If address handshake completes (`awvalid & awready`), the subsequent write data phase (`wvalid & wready`) must also be accepted for the same transaction.

**Impact on System:**
- PicoRV32 cores may timeout waiting for write completion
- File operations may hang indefinitely  
- AXI protocol checkers will flag violations
- Unpredictable behavior with different master timing

**Root Cause Analysis:**
1. File operation detected during address phase
2. Detector immediately blocks all transactions
3. Write data phase of same transaction gets rejected
4. Master waits indefinitely for write completion

### Recommended Fixes

#### File I/O Detector Compliance Fix

**Approach**: Implement transaction phase tracking

```verilog
// Track transaction phases separately
reg address_phase_pending;
reg write_data_phase_pending;
reg transaction_committed;

// Address phase handling
always_ff @(posedge clk) begin
    if (s_axi.awvalid && s_axi.awready) begin
        address_phase_pending <= 1;
        if (detected_file_op)
            transaction_committed <= 1;
    end
    
    if (s_axi.wvalid && s_axi.wready && address_phase_pending) begin
        write_data_phase_pending <= 1;
    end
    
    if (s_axi.bvalid && s_axi.bready) begin
        address_phase_pending <= 0;
        write_data_phase_pending <= 0;
        transaction_committed <= 0;
    end
end

// Ready signal management
always_comb begin
    // Always accept committed transactions
    if (transaction_committed) begin
        s_axi.awready = 1;  // Must accept if address already committed
        s_axi.wready = 1;   // Must accept corresponding write data
    end else if (detected_file_op) begin
        s_axi.awready = 0;  // Block NEW transactions only
        s_axi.wready = 0;
    end else begin
        s_axi.awready = m_axi.awready;  // Normal passthrough
        s_axi.wready = m_axi.wready;
    end
end
```

## Testing and Verification

### AXI Compliance Checkers

Recommended tools for verification:
1. **Xilinx AXI Protocol Checker**: Hardware IP for runtime verification
2. **ARM AMBA AXI Protocol Checker**: Software-based verification
3. **SystemVerilog Assertions**: Custom protocol checking

### Test Scenarios

**High Priority Tests:**
1. **Interleaved Address/Data**: Address first, then data with delay
2. **Pipelined Transactions**: Multiple outstanding writes
3. **Back-to-back File Operations**: Stress test ready signal timing
4. **Mixed File/Memory Operations**: Ensure normal transactions unaffected

**Test Implementation:**
```systemverilog
// Example test for interleaved timing
initial begin
    // Send address
    axi.awvalid <= 1;
    axi.awaddr <= FILE_OPEN_TRIGGER;
    wait(axi.awready);
    axi.awvalid <= 0;
    
    // Delay before sending data  
    #10;
    
    // Send write data
    axi.wvalid <= 1;
    axi.wdata <= param_addr;
    wait(axi.wready);  // Should not hang here
    axi.wvalid <= 0;
    
    // Wait for response
    wait(axi.bvalid);
    axi.bready <= 1;
    #1;
    axi.bready <= 0;
end
```

## Migration Path

### Phase 1: Critical Fixes (Current)
1. ✅ Fix AXI detector ready signal forwarding
2. 🔄 Fix file I/O detector transaction tracking
3. 🔄 Add basic protocol assertions

### Phase 2: Verification (Next)
1. Implement comprehensive AXI test suite
2. Add protocol checkers to simulation
3. Stress test with various timing scenarios

### Phase 3: Optimization (Future)  
1. Optimize for lower latency
2. Add support for AXI4 (burst transactions)
3. Implement quality-of-service features

## References

- [AMBA AXI4-Lite Protocol Specification](https://documentation-service.arm.com/static/60d5b2f2bda80175cf70b5f6)
- [Xilinx AXI Reference Guide](https://docs.xilinx.com/v/u/en-US/ug1037-vivado-axi-reference-guide)
- AxE SoC File I/O Implementation: `docs/FILE_IO_IMPLEMENTATION.md`