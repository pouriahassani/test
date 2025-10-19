// `timescale 1ns / 1ps
// //////////////////////////////////////////////////////////////////////////////////
// // Company: TU Wien
// // Engineer: Daniel Blattner
// // 
// // Create Date: 26.06.2023 09:35:05
// // Design Name: Decomposition, truncation and chunk-level leading-one quantization (DTCL)
// //              based multiplication approximation
// // Module Name: DTCL_AFPM
// // Project Name: AFPM
// // Target Devices: -
// // Tool Versions: -
// // Description: -
// // 
// // Dependencies: -
// // Revision:
// // Revision 0.01 - File Created
// // Revision 1.1 28.06.2023 - File Created
// // Revision 1.2 12.07.2023 - Fixed bug with chunks being summed up
// // Revision 1.3 21.07.2023 - Fixed wrong placement of multiplication result in significant
// // Additional Comments: The algorithm for the approximate floating point multiplier is based on the paper by Vishesh et al. 
// //                      https://ieeexplore.ieee.org/document/10129296
// //
// //////////////////////////////////////////////////////////////////////////////////

// // import defines::*;

// `timescale 1ns / 1ps
// //////////////////////////////////////////////////////////////////////////////////
// // Company: TU Wien
// // Engineer: Daniel Blattner
// // 
// // Create Date: 12.05.2023 08:56:30
// // Design Name: -
// // Module Name: Defines for constants and structs
// // Project Name: AFPM
// // Target Devices: - 
// // Tool Versions: -
// // Description: -
// // 
// // Dependencies: -
// // 
// // Revision:
// // Revision 0.01 - File Created
// // Additional Comments:
// // 
// //////////////////////////////////////////////////////////////////////////////////

// `ifndef __DEFINES_SV
// `define __DEFINES_SV



//     //
//     // Floating point types
//     //
    
//     parameter FLOAT32_EXP_WIDTH = 8;
//     parameter FLOAT32_SIG_WIDTH = 23;
    
//     // IEEE 754 Binary 32 encoding
//     typedef struct packed {
//         logic sign;
//         logic[FLOAT32_EXP_WIDTH - 1:0] exponent;
//         logic[FLOAT32_SIG_WIDTH - 1:0] significand;
//     } float32_t;


// `endif


// module A_FPM_D3aa41(x,y,z);

// input [31:0] x,y;
// output [31:0] z;

// wire [22:0] Tz;
// wire ctrl;
// wire [7:0] Ez;

// Significand_D3aa41 sig(x[22:0], y[22:0], Tz, ctrl);
// Exponent           exp(x[30:23], y[30:23], ctrl, Ez);

// assign z[22:0]  = Tz;
// assign z[30:23] = Ez;

// xor(z[31], x[31], y[31]);

// endmodule



// module Significand_D3aa41(Tx,Ty,Tz,ctrl);
// input [22:0] Tx,Ty;
// output [22:0] Tz;
// output ctrl;

// wire [47:0] result1;
// wire [22:0] result2;

// A_IM24r8_3aa41  m1({1'b1,Tx}, {1'b1,Ty}, result1);
// MUX21_23       mux1(result1[46:24], result1[45:23], result1[47], result2);

// assign Tz = result2;

// assign ctrl = result1[47];

// endmodule



// module A_IM24r8_3aa41(c,d,result);

// 	input  [23:0]  c;
// 	input  [23:0]  d;
// 	output [47:0] result;
	
// 	wire [15:0] result1;
// 	wire [15:0] result2;
// 	wire [15:0] result3;
// 	wire [15:0] result4;
// 	wire [15:0] result5;
// 	wire [15:0] result6;
// 	wire [15:0] result7;
// 	wire [15:0] result8;
// 	wire [15:0] result9;
	
// 	wire [8:0] RCO1;
// 	wire [8:0] RCO2;
// 	wire [8:0] RCO3;
// 	wire [8:0] RCO4;
// 	wire [8:0] RCO5;
// 	wire [8:0] RCO6;
// 	wire [8:0] RCO7;
// 	wire [8:0] RCO8;
// 	wire [8:0] RCO9;
// 	wire [8:0] RCO10;
// 	wire [8:0] RCO11;
// 	wire [8:0] RCO12;
// 	wire [8:0] RCO13;
// 	wire [8:0] RCO14; 
	
// 	wire S,C;
	 
// 	CDM8_aa m1(c[7:0]   , d[7:0]   , result1);
// 	CDM8_aa m2(c[15:8]  , d[7:0]   , result2);
// 	CDM8_aa m3(c[7:0]   , d[15:8]  , result3);
// 	CDM8_41 m4(c[23:16] , d[7:0]   , result4);
// 	E_IM8   m5(c[15:8]  , d[15:8]  , result5);
// 	E_IM8   m6(c[7:0]   , d[23:16] , result6);
// 	E_IM8   m7(c[23:16] , d[15:8]  , result7);
// 	E_IM8   m8(c[15:8]  , d[23:16] , result8);
// 	E_IM8   m9(c[23:16] , d[23:16] , result9);
	
// 	//The second 8 bits of the final result
// 	CLA8_co c1(result2[7:0] , result3[7:0]  , RCO1 );
// 	CLA8_co c2(RCO1[7:0]    , result1[15:8] , RCO2 );
	
// 	//The third 8 bits of the final result
// 	CLA8_cio c3(result2[15:8] , result3[15:8] , RCO1[8] , RCO3 );
// 	CLA8_cio c4(RCO3[7:0]     , result4[7:0]  , RCO2[8] , RCO4 );
	
// 	CLA8_co c5(RCO4[7:0] , result5[7:0] , RCO5);
// 	CLA8_co c6(RCO5[7:0] , result6[7:0] , RCO6);
	
// 	//The fourth 8 bits of the final result
// 	CLA8_cio c7(result4[15:8] , result5[15:8] , RCO3[8] , RCO7 );
// 	CLA8_cio c8(RCO7[7:0]     , result6[15:8] , RCO4[8] , RCO8);
	
// 	CLA8_cio  c9(RCO8[7:0] , result7[7:0] , RCO5[8] , RCO9);
// 	CLA8_cio c10(RCO9[7:0] , result8[7:0] , RCO6[8] , RCO10);
	
// 	//The fifth 8 bits of the final result
// 	CLA8_cio c11(result7[15:8] , result8[15:8] , RCO7[8] , RCO11);
// 	CLA8_cio c12(RCO11[7:0]    , result9[7:0]  , RCO8[8] , RCO12);
	
// 	CLA8_cio c13(RCO12[7:0] , {7'b0000000,RCO9[8]} , RCO10[8] , RCO13);
	
// 	//The sixth 8 bits of the final result
// 	full_adder f1(RCO11[8] , RCO12[8] , RCO13[8] , S , C);
	
// 	CLA8_co c14(result9[15:8] , {6'b000000 , {C,S}} , RCO14);
	
// 	assign result[7:0]   = result1[7:0];
// 	assign result[15:8]  = RCO2[7:0];
// 	assign result[23:16] = RCO6[7:0];
// 	assign result[31:24] = RCO10[7:0];
// 	assign result[39:32] = RCO13[7:0];
// 	assign result[47:40] = RCO14[7:0];
	
// endmodule



// module CDM8_aa(c,d,resultX);

// 	input  [7:0] c;
// 	input  [7:0] d;
// 	output [15:0] resultX;
	
// 	wire [11:0] rA; 
// 	wire [11:0] rB;
	
// 	CDGroupX10 gA(c,d[3:0],rA);
// 	CDGroupX10 gB(c,d[7:4],rB);
	
// 	assign resultX[3:0] = rA[3:0];
	
// 	CLA cla0({4'b0000,rA[11:4]},rB[11:0],resultX[15:4]);

// endmodule



// module CDGroupX10(c,d,resultX);

// 	input  [7:0]  c;
// 	input  [3:0]  d;
// 	output [11:0] resultX;
	
// 	wire w0  [7:0];
// 	wire w11 [7:0];
// 	wire w12 [7:0];
// 	wire w13 [7:0];
// 	wire w14 [7:0];
// 	wire w21 [7:0];
// 	wire w22 [7:0];
// 	wire w23 [7:0];
// 	wire w24 [7:0];
// 	wire w31 [7:0];
// 	wire w32 [7:0];
// 	wire w33 [7:0];
// 	wire w34 [7:0];
	
// 	//row0
// 	and(w0[0],c[0],d[0]);
// 	and(w0[1],c[1],d[0]);
// 	and(w0[2],c[2],d[0]);
// 	and(w0[3],c[3],d[0]);
// 	and(w0[4],c[4],d[0]);
// 	and(w0[5],c[5],d[0]);
// 	and(w0[6],c[6],d[0]);
// 	and(w0[7],c[7],d[0]);
	
// 	assign resultX[0] = w0[0];
	
	
// 	CDPPU CD10(c[0],d[1]  ,w0[1],w13[0],w11[0],resultX[1]);
// 	CDPPU CD11(c[1],w11[0],w0[2],w13[1],w11[1],w14[1]);
// 	CDPPU CD12(c[2],w11[1],w0[3],w13[2],w11[2],w14[2]);
// 	CDPPU CD13(c[3],w11[2],w0[4],w13[3],w11[3],w14[3]);
// 	CDPPU CD14(c[4],w11[3],w0[5],w13[4],w11[4],w14[4]);
// 	CDPPU CD15(c[5],w11[4],w0[6],w13[5],w11[5],w14[5]);
// 	CDPPU CD16(c[6],w11[5],w0[7],w13[6],w11[6],w14[6]);
// 	CDPPU CD17(c[7],w11[6],1'b0 ,w13[7],w11[7],w14[7]);

	
	
// 	CDPPU CD20(w13[0],d[2]  ,w14[1],w23[0],w21[0],resultX[2]);
// 	CDPPU CD21(w13[1],w21[0],w14[2],w23[1],w21[1],w24[1]);
// 	CDPPU CD22(w13[2],w21[1],w14[3],w23[2],w21[2],w24[2]);
// 	CDPPU CD23(w13[3],w21[2],w14[4],w23[3],w21[3],w24[3]);
// 	CDPPU CD24(w13[4],w21[3],w14[5],w23[4],w21[4],w24[4]);
// 	CDPPU CD25(w13[5],w21[4],w14[6],w23[5],w21[5],w24[5]);
// 	CDPPU CD26(w13[6],w21[5],w14[7],w23[6],w21[6],w24[6]);
// 	CDPPU CD27(w13[7],w21[6],1'b0  ,w23[7],w21[7],w24[7]);
	

	
// 	CDPPU CD30(w23[0],d[3]  ,w24[1],w33[0],w31[0],resultX[3]);
// 	CDPPU CD31(w23[1],w31[0],w24[2],w33[1],w31[1],resultX[4]);
// 	CDPPU CD32(w23[2],w31[1],w24[3],w33[2],w31[2],resultX[5]);
// 	CDPPU CD33(w23[3],w31[2],w24[4],w33[3],w31[3],resultX[6]);
// 	CDPPU CD34(w23[4],w31[3],w24[5],w33[4],w31[4],resultX[7]);
// 	CDPPU CD35(w23[5],w31[4],w24[6],w33[5],w31[5],resultX[8]);
// 	CDPPU CD36(w23[6],w31[5],w24[7],w33[6],w31[6],resultX[9]);
// 	CDPPU CD37(w23[7],w31[6],1'b0  ,w33[7],w31[7],resultX[10]);

// 	assign resultX[11] = 1'b0;
	
// endmodule



// module CDPPU(ai,bi,Sin,ao,bo,Sout);

// 	input  ai,bi,Sin;
// 	output ao,bo,Sout;
	
// 	wire m;
	
// 	assign ao = ai;
// 	assign bo = bi;
// 	and(m,ai,bi);
// 	xor(Sout,Sin,m);
	
// endmodule


// module ppu(Ci,Di,Cin,Sin,Co,Do,Cout,Sout);

// 	input Ci,Di,Sin,Cin;
// 	output Co,Do,Cout,Sout;
	
// 	wire m;
	
// 	assign Do = Di;
// 	assign Co = Ci;
// 	and(m,Ci,Di);
// 	full_adder f0(m,Sin,Cin,Sout,Cout);
	
// endmodule


// module full_adder(a,b,Cin,sum,Cout);

// 	input a,b,Cin;
// 	output sum,Cout;
	
// 	wire w1,w2,w3;
	
// 	xor(w1,a,b);
// 	xor(sum,w1,Cin);
// 	and(w2,a,b);
// 	and(w3,w1,Cin);
// 	or(Cout,w3,w2);
	
// endmodule


// module CLA(a,b,result);

// 	input  [11:0] a ;
// 	input  [11:0] b ;
// 	output [11:0] result ;
	
// 	wire [11:0] p;
// 	wire [11:0] g;
// 	wire [11:1] c;
	
// 	xor(p[0],a[0],b[0]);
// 	and(g[0],a[0],b[0]);
	
// 	xor(p[1],a[1],b[1]);
// 	and(g[1],a[1],b[1]);
	
// 	xor(p[2],a[2],b[2]);
// 	and(g[2],a[2],b[2]);
	
// 	xor(p[3],a[3],b[3]);
// 	and(g[3],a[3],b[3]);
	
// 	xor(p[4],a[4],b[4]);
// 	and(g[4],a[4],b[4]);
	
// 	xor(p[5],a[5],b[5]);
// 	and(g[5],a[5],b[5]);
	
// 	xor(p[6],a[6],b[6]);
// 	and(g[6],a[6],b[6]);
	
// 	xor(p[7],a[7],b[7]);
// 	and(g[7],a[7],b[7]);
	
// 	xor(p[8],a[8],b[8]);
// 	and(g[8],a[8],b[8]);
	
// 	xor(p[9],a[9],b[9]);
// 	and(g[9],a[9],b[9]);
	
// 	xor(p[10],a[10],b[10]);
// 	and(g[10],a[10],b[10]);
	
// 	xor(p[11],a[11],b[11]);
// 	and(g[11],a[11],b[11]);
	
// 	assign c[1]  = g[0] ;
// 	assign c[2]  = g[1]  || (p[1]  && g[0]) ;
// 	assign c[3]  = g[2]  || (p[2]  && g[1])  || (p[1] && p[2]  && g[0]);
// 	assign c[4]  = g[3]  || (p[3]  && g[2])  || (p[2] && p[3]  && g[1]) || (p[1] && p[2] && p[3]  && g[0]);
// 	assign c[5]  = g[4]  || (p[4]  && g[3])  || (p[3] && p[4]  && g[2]) || (p[2] && p[3] && p[4]  && g[1]) || (p[1] && p[2] && p[3] && p[4]  && g[0]);
// 	assign c[6]  = g[5]  || (p[5]  && g[4])  || (p[4] && p[5]  && g[3]) || (p[3] && p[4] && p[5]  && g[2]) || (p[2] && p[3] && p[4] && p[5]  && g[1]) || (p[1] && p[2] && p[3] && p[4] && p[5]  && g[0]);
// 	assign c[7]  = g[6]  || (p[6]  && g[5])  || (p[5] && p[6]  && g[4]) || (p[4] && p[5] && p[6]  && g[3]) || (p[3] && p[4] && p[5] && p[6]  && g[2]) || (p[2] && p[3] && p[4] && p[5] && p[6]  && g[1]) || (p[1] && p[2] && p[3] && p[4] && p[5] && p[6]  && g[0]);
// 	assign c[8]  = g[7]  || (p[7]  && g[6])  || (p[6] && p[7]  && g[5]) || (p[5] && p[6] && p[7]  && g[4]) || (p[4] && p[5] && p[6] && p[7]  && g[3]) || (p[3] && p[4] && p[5] && p[6] && p[7]  && g[2]) || (p[2] && p[3] && p[4] && p[5] && p[6] && p[7]  && g[1]) || (p[1] && p[2] && p[3] && p[4] && p[5] && p[6] && p[7]  && g[0]);	
// 	assign c[9]  = g[8]  || (p[8]  && g[7])  || (p[7] && p[8]  && g[6]) || (p[6] && p[7] && p[8]  && g[5]) || (p[5] && p[6] && p[7] && p[8]  && g[4]) || (p[4] && p[5] && p[6] && p[7] && p[8]  && g[3]) || (p[3] && p[4] && p[5] && p[6] && p[7] && p[8]  && g[2]) || (p[2] && p[3] && p[4] && p[5] && p[6] && p[7] && p[8]  && g[1]) || (p[1] && p[2] && p[3] && p[4] && p[5] && p[6] && p[7] && p[8]  && g[0]);
// 	assign c[10] = g[9]  || (p[9]  && g[8])  || (p[8] && p[9]  && g[7]) || (p[7] && p[8] && p[9]  && g[6]) || (p[6] && p[7] && p[8] && p[9]  && g[5]) || (p[5] && p[6] && p[7] && p[8] && p[9]  && g[4]) || (p[4] && p[5] && p[6] && p[7] && p[8] && p[9]  && g[3]) || (p[3] && p[4] && p[5] && p[6] && p[7] && p[8] && p[9]  && g[2]) || (p[2] && p[3] && p[4] && p[5] && p[6] && p[7] && p[8] && p[9]  && g[1]) || (p[1] && p[2] && p[3] && p[4] && p[5] && p[6] && p[7] && p[8] && p[9]  && g[0]);	
// 	assign c[11] = g[10] || (p[10] && g[9])  || (p[9] && p[10] && g[8]) || (p[8] && p[9] && p[10] && g[7]) || (p[7] && p[8] && p[9] && p[10] && g[6]) || (p[6] && p[7] && p[8] && p[9] && p[10] && g[5]) || (p[5] && p[6] && p[7] && p[8] && p[9] && p[10] && g[4]) || (p[4] && p[5] && p[6] && p[7] && p[8] && p[9] && p[10] && g[3]) || (p[3] && p[4] && p[5] && p[6] && p[7] && p[8] && p[9] && p[10] && g[2]) || (p[2] && p[3] && p[4] && p[5] && p[6] && p[7] && p[8] && p[9] && p[10] && g[1]) || (p[1] && p[2] && p[3] && p[4] && p[5] && p[6] && p[7] && p[8] && p[9] && p[10] && g[0]);	

// 	assign result[0] = p[0];
// 	xor(result[1],p[1],c[1]);
// 	xor(result[2],p[2],c[2]);
// 	xor(result[3],p[3],c[3]);
// 	xor(result[4],p[4],c[4]);
// 	xor(result[5],p[5],c[5]);
// 	xor(result[6],p[6],c[6]);
// 	xor(result[7],p[7],c[7]);
// 	xor(result[8],p[8],c[8]);
// 	xor(result[9],p[9],c[9]);
// 	xor(result[10],p[10],c[10]);
// 	xor(result[11],p[11],c[11]);
		
// endmodule

// module CDM8_41(c,d,resultX);

// 	input  [7:0] c;
// 	input  [7:0] d;
// 	output [15:0] resultX;
	
// 	wire [11:0] rA; 
// 	wire [11:0] rB;
	
// 	CDGroupX4 gA(c,d[3:0],rA);
// 	Group     gB(c,d[7:4],rB);
	
// 	assign resultX[3:0] = rA[3:0];
	
// 	CLA cla0({4'b0000,rA[11:4]},rB[11:0],resultX[15:4]);

// endmodule

// module CDGroupX4(c,d,resultX);

// 	input  [7:0]  c;
// 	input  [3:0]  d;
// 	output [11:0] resultX;
	
// 	wire w0  [7:0];
// 	wire w11 [7:0];
// 	wire w12 [7:0];
// 	wire w13 [7:0];
// 	wire w14 [7:0];
// 	wire w21 [7:0];
// 	wire w22 [7:0];
// 	wire w23 [7:0];
// 	wire w24 [7:0];
// 	wire w31 [7:0];
// 	wire w32 [7:0];
// 	wire w33 [7:0];
// 	wire w34 [7:0];
	
// 	//row0
// 	and(w0[0],c[0],d[0]);
// 	and(w0[1],c[1],d[0]);
// 	and(w0[2],c[2],d[0]);
// 	and(w0[3],c[3],d[0]);
// 	and(w0[4],c[4],d[0]);
// 	and(w0[5],c[5],d[0]);
// 	and(w0[6],c[6],d[0]);
// 	and(w0[7],c[7],d[0]);
	
// 	assign resultX[0] = w0[0];
	
	
// 	CDPPU CD10(c[0],d[1]  ,w0[1],w13[0],w11[0],resultX[1]);
// 	CDPPU CD11(c[1],w11[0],w0[2],w13[1],w11[1],w14[1]);
// 	CDPPU CD12(c[2],w11[1],w0[3],w13[2],w11[2],w14[2]);
	
// 	CDPPU CD20(w13[0],d[2]  ,w14[1],w23[0],w21[0],resultX[2]);
// 	CDPPU CD21(w13[1],w21[0],w14[2],w23[1],w21[1],w24[1]);
	
// 	PPUF pf(c[3],w11[2],w13[2],w21[1],w0[4],w13[3],w11[3],w23[2],w21[2],w22[2],w24[2]);
	
// 	CDPPU CD30(w23[0],d[3],w24[1],w33[0],w31[0],resultX[3]);
// 	PPUH  ph31(w23[1],w31[0],w24[2],w33[1],w31[1],w32[1],resultX[4]);
	
// 	PPUH  ph14(c[4],w11[3],w0[5],w13[4],w11[4],w12[4],w14[4]);
	
// 	ppu   p15(c[5],w11[4],w12[4],w0[6],w13[5],w11[5],w12[5],w14[5]);
// 	ppu   p16(c[6],w11[5],w12[5],w0[7],w13[6],w11[6],w12[6],w14[6]);
// 	ppu   p17(c[7],w11[6],w12[6],1'b0 ,w13[7],w11[7],w12[7],w14[7]);
	
// 	ppu p23(w13[3],w21[2],w22[2],w14[4],w23[3],w21[3],w22[3],w24[3]);
// 	ppu p24(w13[4],w21[3],w22[3],w14[5],w23[4],w21[4],w22[4],w24[4]);
// 	ppu p25(w13[5],w21[4],w22[4],w14[6],w23[5],w21[5],w22[5],w24[5]);
// 	ppu p26(w13[6],w21[5],w22[5],w14[7],w23[6],w21[6],w22[6],w24[6]);
// 	ppu p27(w13[7],w21[6],w22[6],w12[7],w23[7],w21[7],w22[7],w24[7]);
	
// 	ppu p32(w23[2],w31[1],w32[1],w24[3],w33[2],w31[2],w32[2],w34[2]);
// 	ppu p33(w23[3],w31[2],w32[2],w24[4],w33[3],w31[3],w32[3],w34[3]);
// 	ppu p34(w23[4],w31[3],w32[3],w24[5],w33[4],w31[4],w32[4],w34[4]);
// 	ppu p35(w23[5],w31[4],w32[4],w24[6],w33[5],w31[5],w32[5],w34[5]);
// 	ppu p36(w23[6],w31[5],w32[5],w24[7],w33[6],w31[6],w32[6],w34[6]);
// 	ppu p37(w23[7],w31[6],w32[6],w22[7],w33[7],w31[7],w32[7],w34[7]);
	
// 	assign resultX[5]  = w34[2];
// 	assign resultX[6]  = w34[3];
// 	assign resultX[7]  = w34[4];
// 	assign resultX[8]  = w34[5];
// 	assign resultX[9]  = w34[6];
// 	assign resultX[10] = w34[7];
// 	assign resultX[11] = w32[7];
	
// endmodule

// module PPUF(ai,bi,aj,bj,Sin,ao,bo,ajo,bjo,Cout,Sout);

// 	input  ai,bi,aj,bj,Sin;
// 	output ao,bo,ajo,bjo,Cout,Sout;
	
// 	wire m1,m2;
	
// 	assign ao = ai;
// 	assign bo = bi;
// 	assign ajo = aj;
// 	assign bjo = bj;
// 	and(m1,ai,bi);
// 	and(m2,aj,bj);
// 	full_adder h0(Sin,m1,m2,Sout,Cout);
	
// endmodule

// module PPUH(ai,bi,Sin,ao,bo,Cout,Sout);

// 	input  ai,bi,Sin;
// 	output ao,bo,Cout,Sout;
	
// 	wire m;
	
// 	assign ao = ai;
// 	assign bo = bi;
// 	and(m,ai,bi);
// 	half_adder h0(Sin,m,Sout,Cout);
	
// endmodule

// module half_adder(a,b,sum,Cout);

// 	input  a,b;
// 	output sum,Cout;
	
// 	xor(sum,a,b);
// 	and(Cout,a,b);


// endmodule


// module E_IM8(c,d,result);

// input [7:0] c;
// input [7:0] d;
// output [15:0] result;

// wire [11:0] rA; 
// wire [11:0] rB;
	
// Group gA(c,d[3:0],rA);
// Group gB(c,d[7:4],rB);
	
// assign result[3:0] = rA[3:0];
	
// CLA cla0({4'b0000,rA[11:4]},rB[11:0],result[15:4]);

// endmodule


// module Group(c,d,result);

// 	input  [7:0]  c;
// 	input  [3:0]  d;
// 	output [11:0] result;
	
// 	wire w0 [7:0];
// 	wire w11 [7:0];
// 	wire w12 [7:0];
// 	wire w13 [7:0];
// 	wire w14 [7:0];
// 	wire w21 [7:0];
// 	wire w22 [7:0];
// 	wire w23 [7:0];
// 	wire w24 [7:0];
// 	wire w31 [7:0];
// 	wire w32 [7:0];
// 	wire w33 [7:0];
// 	wire w34 [7:0];
	
// 	//row0
// 	and(w0[0],c[0],d[0]);
// 	and(w0[1],c[1],d[0]);
// 	and(w0[2],c[2],d[0]);
// 	and(w0[3],c[3],d[0]);
// 	and(w0[4],c[4],d[0]);
// 	and(w0[5],c[5],d[0]);
// 	and(w0[6],c[6],d[0]);
// 	and(w0[7],c[7],d[0]);
	
// 	assign result[0] = w0[0];
	
// 	//ppu of row1
// 	ppu p10(c[0],d[1]  ,1'b0  ,w0[1],w13[0],w11[0],w12[0],w14[0]);
// 	ppu p11(c[1],w11[0],w12[0],w0[2],w13[1],w11[1],w12[1],w14[1]);
// 	ppu p12(c[2],w11[1],w12[1],w0[3],w13[2],w11[2],w12[2],w14[2]);
// 	ppu p13(c[3],w11[2],w12[2],w0[4],w13[3],w11[3],w12[3],w14[3]);
// 	ppu p14(c[4],w11[3],w12[3],w0[5],w13[4],w11[4],w12[4],w14[4]);
// 	ppu p15(c[5],w11[4],w12[4],w0[6],w13[5],w11[5],w12[5],w14[5]);
// 	ppu p16(c[6],w11[5],w12[5],w0[7],w13[6],w11[6],w12[6],w14[6]);
// 	ppu p17(c[7],w11[6],w12[6],1'b0 ,w13[7],w11[7],w12[7],w14[7]);
	
// 	assign result[1] = w14[0];
	
// 	//ppu of row2
// 	ppu p20(w13[0],d[2]  ,1'b0  ,w14[1],w23[0],w21[0],w22[0],w24[0]);
// 	ppu p21(w13[1],w21[0],w22[0],w14[2],w23[1],w21[1],w22[1],w24[1]);	
// 	ppu p22(w13[2],w21[1],w22[1],w14[3],w23[2],w21[2],w22[2],w24[2]);
// 	ppu p23(w13[3],w21[2],w22[2],w14[4],w23[3],w21[3],w22[3],w24[3]);
// 	ppu p24(w13[4],w21[3],w22[3],w14[5],w23[4],w21[4],w22[4],w24[4]);
// 	ppu p25(w13[5],w21[4],w22[4],w14[6],w23[5],w21[5],w22[5],w24[5]);
// 	ppu p26(w13[6],w21[5],w22[5],w14[7],w23[6],w21[6],w22[6],w24[6]);
// 	ppu p27(w13[7],w21[6],w22[6],w12[7],w23[7],w21[7],w22[7],w24[7]);
	
// 	assign result[2] = w24[0];
	
// 	//ppu of row3
// 	ppu p30(w23[0],d[3]  ,1'b0     ,w24[1],w33[0],w31[0],w32[0],w34[0]);
// 	ppu p31(w23[1],w31[0],w32[0],w24[2],w33[1],w31[1],w32[1],w34[1]);
// 	ppu p32(w23[2],w31[1],w32[1],w24[3],w33[2],w31[2],w32[2],w34[2]);
// 	ppu p33(w23[3],w31[2],w32[2],w24[4],w33[3],w31[3],w32[3],w34[3]);
// 	ppu p34(w23[4],w31[3],w32[3],w24[5],w33[4],w31[4],w32[4],w34[4]);
// 	ppu p35(w23[5],w31[4],w32[4],w24[6],w33[5],w31[5],w32[5],w34[5]);
// 	ppu p36(w23[6],w31[5],w32[5],w24[7],w33[6],w31[6],w32[6],w34[6]);
// 	ppu p37(w23[7],w31[6],w32[6],w22[7],w33[7],w31[7],w32[7],w34[7]);
	
// 	assign result[3]  = w34[0];
// 	assign result[4]  = w34[1];
// 	assign result[5]  = w34[2];
// 	assign result[6]  = w34[3];
// 	assign result[7]  = w34[4];
// 	assign result[8]  = w34[5];
// 	assign result[9]  = w34[6];
// 	assign result[10] = w34[7];
// 	assign result[11] = w32[7];
	

// endmodule


// module CLA8_co(a,b,result);

// 	input  [7:0] a ;
// 	input  [7:0] b ;
// 	output [8:0] result ;
	
// 	wire [7:0] p;
// 	wire [7:0] g;
// 	wire [8:1] c;
	
// 	xor(p[0],a[0],b[0]);
// 	and(g[0],a[0],b[0]);
	
// 	xor(p[1],a[1],b[1]);
// 	and(g[1],a[1],b[1]);
	
// 	xor(p[2],a[2],b[2]);
// 	and(g[2],a[2],b[2]);
	
// 	xor(p[3],a[3],b[3]);
// 	and(g[3],a[3],b[3]);
	
// 	xor(p[4],a[4],b[4]);
// 	and(g[4],a[4],b[4]);
	
// 	xor(p[5],a[5],b[5]);
// 	and(g[5],a[5],b[5]);
	
// 	xor(p[6],a[6],b[6]);
// 	and(g[6],a[6],b[6]);
	
// 	xor(p[7],a[7],b[7]);
// 	and(g[7],a[7],b[7]);
	
	
	
// 	assign c[1]  = g[0] ;
// 	assign c[2]  = g[1]  || (p[1]  && g[0]) ;
// 	assign c[3]  = g[2]  || (p[2]  && (g[1]  || (p[1]  && g[0])));
// 	assign c[4]  = g[3]  || (p[3]  && (g[2]  || (p[2]  && (g[1]  || (p[1]  && g[0])))));
// 	assign c[5]  = g[4]  || (p[4]  && (g[3]  || (p[3]  && (g[2]  || (p[2]  && (g[1]  || (p[1]  && g[0])))))));
// 	assign c[6]  = g[5]  || (p[5]  && (g[4]  || (p[4]  && (g[3]  || (p[3]  && (g[2]  || (p[2]  && (g[1]  || (p[1]  && g[0])))))))));
// 	assign c[7]  = g[6]  || (p[6]  && (g[5]  || (p[5]  && (g[4]  || (p[4]  && (g[3]  || (p[3]  && (g[2]  || (p[2]  && (g[1]  || (p[1]  && g[0])))))))))));
// 	assign c[8]  = g[7]  || (p[7]  && (g[6]  || (p[6]  && (g[5]  || (p[5]  && (g[4]  || (p[4]  && (g[3]  || (p[3]  && (g[2]  || (p[2]  && (g[1]  || (p[1]  && g[0])))))))))))));
	

// 	assign result[0] = p[0];
// 	xor(result[1],p[1],c[1]);
// 	xor(result[2],p[2],c[2]);
// 	xor(result[3],p[3],c[3]);
// 	xor(result[4],p[4],c[4]);
// 	xor(result[5],p[5],c[5]);
// 	xor(result[6],p[6],c[6]);
// 	xor(result[7],p[7],c[7]);
// 	assign result[8] = c[8];


// endmodule



// module CLA8_cio(a,b,cin,result);

// 	input cin ;
// 	input  [7:0] a ;
// 	input  [7:0] b ;
// 	output [8:0] result ;
	
// 	wire [7:0] p;
// 	wire [7:0] g;
// 	wire [8:1] c;
	
// 	xor(p[0],a[0],b[0]);
// 	and(g[0],a[0],b[0]);
	
// 	xor(p[1],a[1],b[1]);
// 	and(g[1],a[1],b[1]);
	
// 	xor(p[2],a[2],b[2]);
// 	and(g[2],a[2],b[2]);
	
// 	xor(p[3],a[3],b[3]);
// 	and(g[3],a[3],b[3]);
	
// 	xor(p[4],a[4],b[4]);
// 	and(g[4],a[4],b[4]);
	
// 	xor(p[5],a[5],b[5]);
// 	and(g[5],a[5],b[5]);
	
// 	xor(p[6],a[6],b[6]);
// 	and(g[6],a[6],b[6]);
	
// 	xor(p[7],a[7],b[7]);
// 	and(g[7],a[7],b[7]);
	
	
	
// 	assign c[1]  = g[0]  || (p[0]  && cin) ;
// 	assign c[2]  = g[1]  || (p[1]  && (g[0]  || (p[0] && cin))) ;
// 	assign c[3]  = g[2]  || (p[2]  && (g[1]  || (p[1]  && (g[0]  || (p[0] && cin)))));
// 	assign c[4]  = g[3]  || (p[3]  && (g[2]  || (p[2]  && (g[1]  || (p[1]  && (g[0]  || (p[0] && cin)))))));
// 	assign c[5]  = g[4]  || (p[4]  && (g[3]  || (p[3]  && (g[2]  || (p[2]  && (g[1]  || (p[1]  && (g[0]  || (p[0] && cin)))))))));
// 	assign c[6]  = g[5]  || (p[5]  && (g[4]  || (p[4]  && (g[3]  || (p[3]  && (g[2]  || (p[2]  && (g[1]  || (p[1]  && (g[0]  || (p[0] && cin)))))))))));
// 	assign c[7]  = g[6]  || (p[6]  && (g[5]  || (p[5]  && (g[4]  || (p[4]  && (g[3]  || (p[3]  && (g[2]  || (p[2]  && (g[1]  || (p[1]  && (g[0]  || (p[0] && cin)))))))))))));
// 	assign c[8]  = g[7]  || (p[7]  && (g[6]  || (p[6]  && (g[5]  || (p[5]  && (g[4]  || (p[4]  && (g[3]  || (p[3]  && (g[2]  || (p[2]  && (g[1]  || (p[1]  && (g[0]  || (p[0] && cin)))))))))))))));
	

// 	xor(result[0],p[0],cin);
// 	xor(result[1],p[1],c[1]);
// 	xor(result[2],p[2],c[2]);
// 	xor(result[3],p[3],c[3]);
// 	xor(result[4],p[4],c[4]);
// 	xor(result[5],p[5],c[5]);
// 	xor(result[6],p[6],c[6]);
// 	xor(result[7],p[7],c[7]);
// 	assign result[8] = c[8];


// endmodule



// module MUX21_23(a, b, s, out);

// input [22:0] a, b;
// input s;
// output [22:0] out;

// assign out = s ? a : b ;

// endmodule


// module Exponent(Ex, Ey, s, Ez);

// input [7:0] Ex, Ey;
// input s;
// output [7:0] Ez;

// wire [8:0] result1,result2,result3;

// RCA8 rca1(Ex, Ey, 1'b0, result1);
// RCA8 rca2(result1[7:0], 8'b10000001, 1'b0, result2);
// RCA8 rca3(result1[7:0], 8'b10000010, 1'b0, result3);

// MUX21_8 mux(result3[7:0], result2[7:0], s, Ez);

// endmodule



// module RCA8(a,b,cin,result);

// input [7:0] a,b;
// input cin;
// output [8:0] result;

// wire [7:0] sum;
// wire [8:1] cout;

// full_adder f0(a[0], b[0], cin    , sum[0], cout[1]);
// full_adder f1(a[1], b[1], cout[1], sum[1], cout[2]);
// full_adder f2(a[2], b[2], cout[2], sum[2], cout[3]);
// full_adder f3(a[3], b[3], cout[3], sum[3], cout[4]);
// full_adder f4(a[4], b[4], cout[4], sum[4], cout[5]);
// full_adder f5(a[5], b[5], cout[5], sum[5], cout[6]);
// full_adder f6(a[6], b[6], cout[6], sum[6], cout[7]);
// full_adder f7(a[7], b[7], cout[7], sum[7], cout[8]);

// assign result[7:0] = sum;
// assign result[8] = cout[8];


// endmodule


// module MUX21_8(a, b, s, out);

// input [7:0] a, b;
// input s;
// output [7:0] out;

// assign out = s ? a : b ;

// endmodule


// module DTCL_AFPM(
//     input float32_t   fp_multiplier,
//     input float32_t   fp_multiplicand,
//     output float32_t  fp_product);
    
//     // Number of exact bits
//     parameter E = 10;
//     // Number of approximate bits
//     parameter A = 6;
//     // Size of a chunk 
//     parameter K = 2;
//     // Partision of martissa
//     ////////////////////////////////////////////////////
//     //|  E   |      A      |             T           |//
//     ////////////////////////////////////////////////////
    
//     // DO NOT CHANGE THESE PARAMETER!!
//     // Number of truncated bits
//     parameter T = FLOAT32_SIG_WIDTH+1-E-A;
//     // Number of chunks
//     parameter chunk_num = A/K;
    
//     parameter RESULT_WIDTH = 2*(A+E);
    
//     initial begin
//             // $display("Current Configuration: Exact Bits: %0d Approximate Bits: %0d Chunk Size: %0d\n",E,A,K);
//             assert (A%K == 0) else $display("The number of approximate bits (A) should be devisible by the size of the chunk(s) (K)\n");
//     end
    
//     logic multiplier_is_nan;
//     logic multiplicand_is_nan;
//     logic multiplier_is_inf;
//     logic multiplicand_is_inf;
//     logic multiplier_is_zero;
//     logic multiplicand_is_zero;
//     logic multiplier_hidden_bit;
//     logic multiplicand_hidden_bit;
//     logic mul_is_nan;
    
//     assign multiplier_is_nan = fp_multiplier.exponent == 8'hff && fp_multiplier.significand != 0;
//     assign multiplicand_is_nan = fp_multiplicand.exponent == 8'hff && fp_multiplicand.significand != 0;
//     assign multiplier_is_inf = fp_multiplier.exponent == 8'hff && fp_multiplier.significand == 0;
//     assign multiplicand_is_inf = fp_multiplicand.exponent == 8'hff && fp_multiplicand.significand == 0;
//     assign multiplier_is_zero = fp_multiplier.exponent == 0 && fp_multiplier.significand == 0;
//     assign multiplicand_is_zero = fp_multiplicand.exponent == 0 && fp_multiplicand.significand == 0;
//     assign multiplier_hidden_bit = fp_multiplier.exponent != 0;         // 0 -> Subnormal number
//     assign multiplicand_hidden_bit = fp_multiplicand.exponent != 0;
//     // Result is NaN if one number is NaN or a 0.0*inf multiplication occur
//     assign mul_is_nan = multiplier_is_nan || multiplicand_is_nan || 
//                         (multiplier_is_zero && multiplicand_is_inf) || 
//                         (multiplicand_is_zero && multiplier_is_inf);
    
//     logic[FLOAT32_SIG_WIDTH:0] multiplier_full_significand;
//     logic[FLOAT32_SIG_WIDTH:0] multiplicand_full_significand;
    
//     assign multiplier_full_significand = {multiplier_hidden_bit,fp_multiplier.significand};
//     assign multiplicand_full_significand = {multiplicand_hidden_bit,fp_multiplicand.significand};
    
//     // Return the position of the first '1' from the MSB    
//     // If no one was deteced the return LSB is 0 else 1
//     function logic[$clog2(K):0] lob (input logic[K-1:0] chunk);
//         for (int idx = K-1; idx >= 0; idx--) begin
//             if(chunk[idx] == 1) begin
//                 return {idx,1'b1};
//             end
//         end
//         return 0;
//     endfunction;
    
//     logic[E-1:0] multiplier_exact;
//     logic[E-1:0] multiplicand_exact;
//     logic[A-1:0] multiplier_approximate;
//     logic[A-1:0] multiplicand_approximate;
//     // Part of the significant, which is multiplied using an exact method
//     assign multiplier_exact = multiplier_full_significand[FLOAT32_SIG_WIDTH:FLOAT32_SIG_WIDTH-E+1];
//     assign multiplicand_exact = multiplicand_full_significand[FLOAT32_SIG_WIDTH:FLOAT32_SIG_WIDTH-E+1];
//     // Part of the signigicant, which is multiplied using the approximate method
//     // The LSB of the A-region is rounded with the MSB of the T-region
//     assign multiplier_approximate = {multiplier_full_significand[FLOAT32_SIG_WIDTH-E:FLOAT32_SIG_WIDTH-E-A+2],
//             multiplier_full_significand[FLOAT32_SIG_WIDTH-E-A+1] | multiplier_full_significand[FLOAT32_SIG_WIDTH-E-A]};
//     assign multiplicand_approximate = {multiplicand_full_significand[FLOAT32_SIG_WIDTH-E:FLOAT32_SIG_WIDTH-E-A+2],
//             multiplicand_full_significand[FLOAT32_SIG_WIDTH-E-A+1] | multiplicand_full_significand[FLOAT32_SIG_WIDTH-E-A]};
    
//     logic[K-1:0] multiplier_chunks[chunk_num-1:0];
//     logic[K-1:0] multiplicand_chunks[chunk_num-1:0];
//     // Slice the approximate part into chunks
//     always_comb begin
//         for(int idx = 0; idx < chunk_num; idx++) begin
//             multiplier_chunks[idx] = multiplier_approximate[K*idx +: K];
//             multiplicand_chunks[idx] = multiplicand_approximate[K*idx +: K];
//         end
//     end
    
//     logic[$clog2(K)-1:0] multiplier_chunks_quantized[chunk_num-1:0];
//     logic[chunk_num-1:0] multiplier_chunks_nzero;
//     logic[$clog2(K)-1:0] multiplicand_chunks_quantized[chunk_num-1:0];
//     logic[chunk_num-1:0] multiplicand_chunks_nzero;
//     // Get position of first '1' from each chunk
//     always_comb begin
//         for(int idx = 0; idx < chunk_num; idx++) begin
//             {multiplier_chunks_quantized[idx],multiplier_chunks_nzero[idx]} = lob(multiplier_chunks[idx]);
//             {multiplicand_chunks_quantized[idx],multiplicand_chunks_nzero[idx]} = lob(multiplicand_chunks[idx]);
//         end
//     end
    
//     logic[A-1:0] const_1 = 1;
//     logic[A-1:0] multiplier_approximate_quantized[chunk_num-1:0];
//     int quantized_offset[chunk_num-1:0];
//     always_comb begin
//         if (multiplier_chunks_nzero[0]) begin
//             multiplier_approximate_quantized[0] = const_1 << multiplier_chunks_quantized[0];
//         end else begin
//             multiplier_approximate_quantized[0] = {A{1'b0}};
//         end
//         for(int idx = 1; idx < chunk_num; idx++) begin
//             quantized_offset[idx] = {{32-$clog2(K){1'b0}},multiplier_chunks_quantized[idx]} + idx*K;
//             if (multiplier_chunks_nzero[idx]) begin
//                 multiplier_approximate_quantized[idx] = (const_1 << quantized_offset[idx])
//                                                         + multiplier_approximate_quantized[idx-1];
//             end else begin
//                 multiplier_approximate_quantized[idx] = multiplier_approximate_quantized[idx-1];
//             end
//         end
//     end
    
//     // Calculate the partial product
//     // The E-region uses a accurate multiplier
//     // The combined region uses a shit and add method 
//     logic[(2*E)-1:0] prod_exact;
//     logic[(A+E)-1:0] prod_exact_approximate1[chunk_num-1:0];
//     logic[(A+E)-1:0] prod_exact_approximate2[chunk_num-1:0];
//     logic[(2*A)-1:0] prod_approximated[chunk_num-1:0];
//     int base_offset[chunk_num-1:0];
//     int multiplicand_offset[chunk_num-1:0];
//     int multiplier_offset[chunk_num-1:0];
//     always_comb begin
//         prod_exact = multiplier_exact*multiplicand_exact;
//         // Reduce the chunk-array
//         // Final result is in the last position (index chunk_num-1)
//         if (multiplicand_chunks_nzero[0]) begin
//             prod_exact_approximate1[0] = {{A{1'b0}},multiplier_exact} << multiplicand_chunks_quantized[0];
//             prod_approximated[0] = {{A{1'b0}},multiplier_approximate_quantized[chunk_num-1]} << multiplicand_chunks_quantized[0];
//         end else begin
//             prod_exact_approximate1[0] = {A+E{1'b0}};
//             prod_approximated[0] = {2*A{1'b0}};
//         end
//         if (multiplier_chunks_nzero[0]) begin
//             prod_exact_approximate2[0] = {{A{1'b0}},multiplicand_exact} << multiplier_chunks_quantized[0];
//         end else begin
//             prod_exact_approximate2[0] = {A+E{1'b0}};
//         end

//         for(int idx = 1; idx < chunk_num; idx++) begin
//             // Thanks verilator ( ?? ???)
//             base_offset[idx] = idx*K;
//             multiplicand_offset[idx] = {{32-$clog2(K){1'b0}},multiplicand_chunks_quantized[idx]} + base_offset[idx];
//             multiplier_offset[idx] = {{32-$clog2(K){1'b0}},multiplier_chunks_quantized[idx]} + base_offset[idx];
//             if (multiplicand_chunks_nzero[idx]) begin
//                 prod_exact_approximate1[idx] = ({{A{1'b0}},multiplier_exact} << (multiplicand_offset[idx][A+E-1:0])) + 
//                                                 prod_exact_approximate1[idx-1];
//                 prod_approximated[idx] = ({{A{1'b0}},multiplier_approximate_quantized[chunk_num-1]} << (multiplicand_offset[idx][(2*A)-1:0])) + 
//                                         prod_approximated[idx-1];                                
//             end else begin
//                 prod_exact_approximate1[idx] = prod_exact_approximate1[idx-1];
//                 prod_approximated[idx] = prod_approximated[idx-1];
//             end
//             if (multiplier_chunks_nzero[idx]) begin
//                 prod_exact_approximate2[idx] = ({{A{1'b0}},multiplicand_exact} << (multiplier_offset[idx][A+E-1:0])) +
//                                                 prod_exact_approximate2[idx-1];
//             end else begin
//                 prod_exact_approximate2[idx] = prod_exact_approximate2[idx-1];
//             end
//         end
//     end
    
//     /*always_comb begin
//         prod_exact = multiplier_exact*multiplicand_exact;
//         // Reduce the chunk-array
//         // Final result is in the last position (index chunk_num-1)
//         if (multiplicand_chunks_nzero[0]) begin
//             prod_exact_approximate1[0] = multiplier_exact << multiplicand_chunks_quantized[0];
//             prod_approximated[0] = multiplier_approximate << multiplicand_chunks_quantized[0];
//         end else begin
//             prod_exact_approximate1[0] = {A+E{1'b0}};
//             prod_approximated[0] = {2*A{1'b0}};
//         end
//         if (multiplier_chunks_nzero[0]) begin
//             prod_exact_approximate2[0] = multiplicand_exact << multiplier_chunks_quantized[0];
//         end else begin
//             prod_exact_approximate2[0] = {A+E{1'b0}};
//         end
//         for(int idx = 1; idx < chunk_num; idx++) begin
//             if (multiplicand_chunks_nzero[idx]) begin
//                 prod_exact_approximate1[idx] = multiplier_exact << (multiplicand_chunks_quantized[idx] + idx*K) + 
//                                                 prod_exact_approximate1[idx-1];
//                 prod_approximated[idx] = multiplier_approximate << (multiplicand_chunks_quantized[idx] + idx*K) + 
//                                         prod_approximated[idx-1];                                
//             end else begin
//                 prod_exact_approximate1[idx] = prod_exact_approximate1[idx-1];
//                 prod_approximated[idx] = prod_approximated[idx-1];
//             end
//             if (multiplier_chunks_nzero[idx]) begin
//                 prod_exact_approximate2[idx] = multiplicand_exact << (multiplier_chunks_quantized[idx] + idx*K) +
//                                                 prod_exact_approximate2[idx-1];
//             end else begin
//                 prod_exact_approximate2[idx] = prod_exact_approximate2[idx-1];
//             end
//         end
//     end*/
    
//     logic[RESULT_WIDTH-1:0] mul_product;
//     logic mul_exponent_cin;
//     logic[FLOAT32_EXP_WIDTH-1:0] mul_exponent;
//     logic mul_exponent_underflow;
//     logic mul_exponent_carry;

//     always_comb begin
    
//         // Calculate the combined product of the martissa
//         mul_product = (prod_exact << 2*A) + 
//                     ((prod_exact_approximate1[chunk_num-1] + prod_exact_approximate2[chunk_num-1]) << A) + 
//                     (prod_approximated[chunk_num-1]);
//         // Normalize matrissa
//         if (mul_product[RESULT_WIDTH-1] == 1'b1) begin
//             mul_exponent_cin = 1'b1;
//         end else begin
//             mul_exponent_cin = 1'b0;
//         end
//         // Calculation of the exponent
//         {mul_exponent_underflow, mul_exponent_carry, mul_exponent}
//                 = {2'd0, fp_multiplier.exponent} + {2'd0, fp_multiplicand.exponent} - 10'd127 + mul_exponent_cin; 
        
//         // Result handeling
//         if (mul_is_nan) begin
//             // Internal NaN encoding
//             fp_product.sign = 1'b0;
//             fp_product.exponent = 8'hff;
//             fp_product.significand = 23'h7FFFFF;
//         end else begin
//             // Sign bit
//             fp_product.sign = fp_multiplier.sign ^ fp_multiplicand.sign;
//             if (mul_exponent_underflow || multiplier_is_zero || multiplicand_is_zero) begin
//                 // Result is zero
//                 fp_product.exponent = 8'h0;
//                 fp_product.significand = 23'h0;
//             end else begin
//                 if (mul_exponent_carry) begin
//                     // Result is inf
//                     fp_product.exponent = 8'hff;
//                     fp_product.significand = 23'h0;
//                 end else begin
//                     // Result of approximation
//                     fp_product.exponent = mul_exponent;
//                     // Normalize matrissa
//                     // Result of multiplication can be bigger or smaller than the significant
//                     // Therefore both cases must be handeled
//                     if (mul_product[2*(A+E)-1]) begin
//                         if (2*(A+E)-1 >= FLOAT32_SIG_WIDTH) begin
//                             fp_product.significand = mul_product[2*(A+E)-2:2*(A+E)-2-(FLOAT32_SIG_WIDTH-1)]; 
//                         end else begin
//                             fp_product.significand = {mul_product[2*(A+E)-2:0],'0}; 
//                         end
//                     end else begin
//                         if (2*(A+E)-2 >= FLOAT32_SIG_WIDTH) begin
//                             fp_product.significand = mul_product[2*(A+E)-3:2*(A+E)-3-(FLOAT32_SIG_WIDTH-1)];
//                         end else begin
//                             fp_product.significand = {mul_product[2*(A+E)-3:0],'0};
//                         end
//                     end
//                 end
//             end
//         end
//     end

// endmodule
