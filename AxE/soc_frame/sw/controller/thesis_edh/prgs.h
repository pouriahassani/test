/* This file has been automatically generated */

#include "../../../systems/2x2_16_priority_input_approx/generated/axe_memory_layout.h"

#define NUM_PRGS ( 1 )

void init_prgs( prg_t *prgs )
{
	prgs[0].name = "mul";
	prgs[0].addr[ARCH_RV32IM] = 0x1000000; // Node 0 memory space
	prgs[0].c[ARCH_RV32IM] = 0;
	prgs[0].d[ARCH_RV32IM] = 0;
	prgs[0].t[ARCH_RV32IM] = 0;
	prgs[0].e[ARCH_RV32IM] = 0;
	prgs[0].c_clk_cnt[ARCH_RV32IM] = 0;
	prgs[0].t_clk_cnt[ARCH_RV32IM] = 0;
	prgs[0].d_multiplyer = 0b0000000111000000;
	prgs[0].s          = 5;
	prgs[0].s_cnt_down = 5;
	prgs[0].assigned_to = 0;
	prgs[0].next_release_clk_cnt = 0;
	prgs[0].next_release_overflows = 0;
	prgs[0].next_deadline_clk_cnt = 0;
	prgs[0].next_deadline_overflows = 0;

}
