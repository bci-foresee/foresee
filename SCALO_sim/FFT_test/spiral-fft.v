/* verilator lint_off MULTITOP */

//   Input/output stream: 4 complex words per cycle
//   Throughput: one transform every 256 cycles
//   Latency: 777 cycles

//   Resources required:
//     48 multipliers (32 x 32 bit)
//     104 adders (32 x 32 bit)
//     4 RAMs (32 words, 64 bits per word)
//     12 RAMs (512 words, 64 bits per word)
//     4 RAMs (8 words, 64 bits per word)
//     4 RAMs (128 words, 64 bits per word)
//     6 ROMs (256 words, 32 bits per word)
//     6 ROMs (64 words, 32 bits per word)
//     6 ROMs (16 words, 32 bits per word)

// Generated on Mon Jun 17 17:11:20 UTC 2024

// Latency: 777 clock cycles
// Throughput: 1 transform every 256 cycles

// We use an interleaved complex data format.  X0 represents the
// real portion of the first input, and X1 represents the imaginary
// portion.  The X variables are system inputs and the Y variables
// are system outputs.

// The design uses a system of flag signals to indicate the
// beginning of the input and output data streams.  The 'next'
// input (asserted high), is used to instruct the system that the
// input stream will begin on the following cycle.

// This system has a 'gap' of 256 cycles.  This means that
// 256 cycles must elapse between the beginning of the input
// vectors.

// The output signal 'next_out' (also asserted high) indicates
// that the output vector will begin streaming out of the system
 // on the following cycle.

// The system has a latency of 777 cycles.  This means that
// the 'next_out' will be asserted 777 cycles after the user
// asserts 'next'.

// The simple testbench below will demonstrate the timing for loading
// and unloading data vectors.
// The system reset signal is asserted high.

// Please note: when simulating floating point code, you must include
// Xilinx's DSP slice simulation module.


// Latency: 777
// Gap: 256
// module_name_is:dft_top


// The 1024 complex data points enter the system over 256 cycles
// Wait until next_out goes high, then wait one clock cycle and begin receiving data

module dft_top(clk, reset, next, next_out,
   X0, Y0,
   X1, Y1,
   X2, Y2,
   X3, Y3,
   X4, Y4,
   X5, Y5,
   X6, Y6,
   X7, Y7);

   output next_out;
   input clk, reset, next;

   input [31:0] X0,
      X1,
      X2,
      X3,
      X4,
      X5,
      X6,
      X7;

   output [31:0] Y0,
      Y1,
      Y2,
      Y3,
      Y4,
      Y5,
      Y6,
      Y7;

   wire [31:0] t0_0;
   wire [31:0] t0_1;
   wire [31:0] t0_2;
   wire [31:0] t0_3;
   wire [31:0] t0_4;
   wire [31:0] t0_5;
   wire [31:0] t0_6;
   wire [31:0] t0_7;
   wire next_0;
   wire [31:0] t1_0;
   wire [31:0] t1_1;
   wire [31:0] t1_2;
   wire [31:0] t1_3;
   wire [31:0] t1_4;
   wire [31:0] t1_5;
   wire [31:0] t1_6;
   wire [31:0] t1_7;
   wire next_1;
   wire [31:0] t2_0;
   wire [31:0] t2_1;
   wire [31:0] t2_2;
   wire [31:0] t2_3;
   wire [31:0] t2_4;
   wire [31:0] t2_5;
   wire [31:0] t2_6;
   wire [31:0] t2_7;
   wire next_2;
   wire [31:0] t3_0;
   wire [31:0] t3_1;
   wire [31:0] t3_2;
   wire [31:0] t3_3;
   wire [31:0] t3_4;
   wire [31:0] t3_5;
   wire [31:0] t3_6;
   wire [31:0] t3_7;
   wire next_3;
   wire [31:0] t4_0;
   wire [31:0] t4_1;
   wire [31:0] t4_2;
   wire [31:0] t4_3;
   wire [31:0] t4_4;
   wire [31:0] t4_5;
   wire [31:0] t4_6;
   wire [31:0] t4_7;
   wire next_4;
   wire [31:0] t5_0;
   wire [31:0] t5_1;
   wire [31:0] t5_2;
   wire [31:0] t5_3;
   wire [31:0] t5_4;
   wire [31:0] t5_5;
   wire [31:0] t5_6;
   wire [31:0] t5_7;
   wire next_5;
   wire [31:0] t6_0;
   wire [31:0] t6_1;
   wire [31:0] t6_2;
   wire [31:0] t6_3;
   wire [31:0] t6_4;
   wire [31:0] t6_5;
   wire [31:0] t6_6;
   wire [31:0] t6_7;
   wire next_6;
   wire [31:0] t7_0;
   wire [31:0] t7_1;
   wire [31:0] t7_2;
   wire [31:0] t7_3;
   wire [31:0] t7_4;
   wire [31:0] t7_5;
   wire [31:0] t7_6;
   wire [31:0] t7_7;
   wire next_7;
   wire [31:0] t8_0;
   wire [31:0] t8_1;
   wire [31:0] t8_2;
   wire [31:0] t8_3;
   wire [31:0] t8_4;
   wire [31:0] t8_5;
   wire [31:0] t8_6;
   wire [31:0] t8_7;
   wire next_8;
   wire [31:0] t9_0;
   wire [31:0] t9_1;
   wire [31:0] t9_2;
   wire [31:0] t9_3;
   wire [31:0] t9_4;
   wire [31:0] t9_5;
   wire [31:0] t9_6;
   wire [31:0] t9_7;
   wire next_9;
   wire [31:0] t10_0;
   wire [31:0] t10_1;
   wire [31:0] t10_2;
   wire [31:0] t10_3;
   wire [31:0] t10_4;
   wire [31:0] t10_5;
   wire [31:0] t10_6;
   wire [31:0] t10_7;
   wire next_10;
   wire [31:0] t11_0;
   wire [31:0] t11_1;
   wire [31:0] t11_2;
   wire [31:0] t11_3;
   wire [31:0] t11_4;
   wire [31:0] t11_5;
   wire [31:0] t11_6;
   wire [31:0] t11_7;
   wire next_11;
   wire [31:0] t12_0;
   wire [31:0] t12_1;
   wire [31:0] t12_2;
   wire [31:0] t12_3;
   wire [31:0] t12_4;
   wire [31:0] t12_5;
   wire [31:0] t12_6;
   wire [31:0] t12_7;
   wire next_12;
   wire [31:0] t13_0;
   wire [31:0] t13_1;
   wire [31:0] t13_2;
   wire [31:0] t13_3;
   wire [31:0] t13_4;
   wire [31:0] t13_5;
   wire [31:0] t13_6;
   wire [31:0] t13_7;
   wire next_13;
   wire [31:0] t14_0;
   wire [31:0] t14_1;
   wire [31:0] t14_2;
   wire [31:0] t14_3;
   wire [31:0] t14_4;
   wire [31:0] t14_5;
   wire [31:0] t14_6;
   wire [31:0] t14_7;
   wire next_14;
   wire [31:0] t15_0;
   wire [31:0] t15_1;
   wire [31:0] t15_2;
   wire [31:0] t15_3;
   wire [31:0] t15_4;
   wire [31:0] t15_5;
   wire [31:0] t15_6;
   wire [31:0] t15_7;
   wire next_15;
   assign t0_0 = X0;
   assign Y0 = t15_0;
   assign t0_1 = X1;
   assign Y1 = t15_1;
   assign t0_2 = X2;
   assign Y2 = t15_2;
   assign t0_3 = X3;
   assign Y3 = t15_3;
   assign t0_4 = X4;
   assign Y4 = t15_4;
   assign t0_5 = X5;
   assign Y5 = t15_5;
   assign t0_6 = X6;
   assign Y6 = t15_6;
   assign t0_7 = X7;
   assign Y7 = t15_7;
   assign next_0 = next;
   assign next_out = next_15;

// latency=242, gap=256
   rc79108 stage0(.clk(clk), .reset(reset), .next(next_0), .next_out(next_1),
    .X0(t0_0), .Y0(t1_0),
    .X1(t0_1), .Y1(t1_1),
    .X2(t0_2), .Y2(t1_2),
    .X3(t0_3), .Y3(t1_3),
    .X4(t0_4), .Y4(t1_4),
    .X5(t0_5), .Y5(t1_5),
    .X6(t0_6), .Y6(t1_6),
    .X7(t0_7), .Y7(t1_7));


// latency=3, gap=256
   codeBlock79110 stage1(.clk(clk), .reset(reset), .next_in(next_1), .next_out(next_2),
       .X0_in(t1_0), .Y0(t2_0),
       .X1_in(t1_1), .Y1(t2_1),
       .X2_in(t1_2), .Y2(t2_2),
       .X3_in(t1_3), .Y3(t2_3),
       .X4_in(t1_4), .Y4(t2_4),
       .X5_in(t1_5), .Y5(t2_5),
       .X6_in(t1_6), .Y6(t2_6),
       .X7_in(t1_7), .Y7(t2_7));


// latency=8, gap=256
   rc79323 stage2(.clk(clk), .reset(reset), .next(next_2), .next_out(next_3),
    .X0(t2_0), .Y0(t3_0),
    .X1(t2_1), .Y1(t3_1),
    .X2(t2_2), .Y2(t3_2),
    .X3(t2_3), .Y3(t3_3),
    .X4(t2_4), .Y4(t3_4),
    .X5(t2_5), .Y5(t3_5),
    .X6(t2_6), .Y6(t3_6),
    .X7(t2_7), .Y7(t3_7));


// latency=12, gap=256
   DirSum_79696 stage3(.next(next_3), .clk(clk), .reset(reset), .next_out(next_4),
       .X0(t3_0), .Y0(t4_0),
       .X1(t3_1), .Y1(t4_1),
       .X2(t3_2), .Y2(t4_2),
       .X3(t3_3), .Y3(t4_3),
       .X4(t3_4), .Y4(t4_4),
       .X5(t3_5), .Y5(t4_5),
       .X6(t3_6), .Y6(t4_6),
       .X7(t3_7), .Y7(t4_7));


// latency=3, gap=256
   codeBlock79699 stage4(.clk(clk), .reset(reset), .next_in(next_4), .next_out(next_5),
       .X0_in(t4_0), .Y0(t5_0),
       .X1_in(t4_1), .Y1(t5_1),
       .X2_in(t4_2), .Y2(t5_2),
       .X3_in(t4_3), .Y3(t5_3),
       .X4_in(t4_4), .Y4(t5_4),
       .X5_in(t4_5), .Y5(t5_5),
       .X6_in(t4_6), .Y6(t5_6),
       .X7_in(t4_7), .Y7(t5_7));


// latency=17, gap=256
   rc79912 stage5(.clk(clk), .reset(reset), .next(next_5), .next_out(next_6),
    .X0(t5_0), .Y0(t6_0),
    .X1(t5_1), .Y1(t6_1),
    .X2(t5_2), .Y2(t6_2),
    .X3(t5_3), .Y3(t6_3),
    .X4(t5_4), .Y4(t6_4),
    .X5(t5_5), .Y5(t6_5),
    .X6(t5_6), .Y6(t6_6),
    .X7(t5_7), .Y7(t6_7));


// latency=12, gap=256
   DirSum_80381 stage6(.next(next_6), .clk(clk), .reset(reset), .next_out(next_7),
       .X0(t6_0), .Y0(t7_0),
       .X1(t6_1), .Y1(t7_1),
       .X2(t6_2), .Y2(t7_2),
       .X3(t6_3), .Y3(t7_3),
       .X4(t6_4), .Y4(t7_4),
       .X5(t6_5), .Y5(t7_5),
       .X6(t6_6), .Y6(t7_6),
       .X7(t6_7), .Y7(t7_7));


// latency=3, gap=256
   codeBlock80384 stage7(.clk(clk), .reset(reset), .next_in(next_7), .next_out(next_8),
       .X0_in(t7_0), .Y0(t8_0),
       .X1_in(t7_1), .Y1(t8_1),
       .X2_in(t7_2), .Y2(t8_2),
       .X3_in(t7_3), .Y3(t8_3),
       .X4_in(t7_4), .Y4(t8_4),
       .X5_in(t7_5), .Y5(t8_5),
       .X6_in(t7_6), .Y6(t8_6),
       .X7_in(t7_7), .Y7(t8_7));


// latency=53, gap=256
   rc80597 stage8(.clk(clk), .reset(reset), .next(next_8), .next_out(next_9),
    .X0(t8_0), .Y0(t9_0),
    .X1(t8_1), .Y1(t9_1),
    .X2(t8_2), .Y2(t9_2),
    .X3(t8_3), .Y3(t9_3),
    .X4(t8_4), .Y4(t9_4),
    .X5(t8_5), .Y5(t9_5),
    .X6(t8_6), .Y6(t9_6),
    .X7(t8_7), .Y7(t9_7));


// latency=12, gap=256
   DirSum_81450 stage9(.next(next_9), .clk(clk), .reset(reset), .next_out(next_10),
       .X0(t9_0), .Y0(t10_0),
       .X1(t9_1), .Y1(t10_1),
       .X2(t9_2), .Y2(t10_2),
       .X3(t9_3), .Y3(t10_3),
       .X4(t9_4), .Y4(t10_4),
       .X5(t9_5), .Y5(t10_5),
       .X6(t9_6), .Y6(t10_6),
       .X7(t9_7), .Y7(t10_7));


// latency=3, gap=256
   codeBlock81453 stage10(.clk(clk), .reset(reset), .next_in(next_10), .next_out(next_11),
       .X0_in(t10_0), .Y0(t11_0),
       .X1_in(t10_1), .Y1(t11_1),
       .X2_in(t10_2), .Y2(t11_2),
       .X3_in(t10_3), .Y3(t11_3),
       .X4_in(t10_4), .Y4(t11_4),
       .X5_in(t10_5), .Y5(t11_5),
       .X6_in(t10_6), .Y6(t11_6),
       .X7_in(t10_7), .Y7(t11_7));


// latency=197, gap=256
   rc81666 stage11(.clk(clk), .reset(reset), .next(next_11), .next_out(next_12),
    .X0(t11_0), .Y0(t12_0),
    .X1(t11_1), .Y1(t12_1),
    .X2(t11_2), .Y2(t12_2),
    .X3(t11_3), .Y3(t12_3),
    .X4(t11_4), .Y4(t12_4),
    .X5(t11_5), .Y5(t12_5),
    .X6(t11_6), .Y6(t12_6),
    .X7(t11_7), .Y7(t12_7));


// latency=12, gap=256
   DirSum_84054 stage12(.next(next_12), .clk(clk), .reset(reset), .next_out(next_13),
       .X0(t12_0), .Y0(t13_0),
       .X1(t12_1), .Y1(t13_1),
       .X2(t12_2), .Y2(t13_2),
       .X3(t12_3), .Y3(t13_3),
       .X4(t12_4), .Y4(t13_4),
       .X5(t12_5), .Y5(t13_5),
       .X6(t12_6), .Y6(t13_6),
       .X7(t12_7), .Y7(t13_7));


// latency=3, gap=256
   codeBlock84057 stage13(.clk(clk), .reset(reset), .next_in(next_13), .next_out(next_14),
       .X0_in(t13_0), .Y0(t14_0),
       .X1_in(t13_1), .Y1(t14_1),
       .X2_in(t13_2), .Y2(t14_2),
       .X3_in(t13_3), .Y3(t14_3),
       .X4_in(t13_4), .Y4(t14_4),
       .X5_in(t13_5), .Y5(t14_5),
       .X6_in(t13_6), .Y6(t14_6),
       .X7_in(t13_7), .Y7(t14_7));


// latency=197, gap=256
   rc84270 stage14(.clk(clk), .reset(reset), .next(next_14), .next_out(next_15),
    .X0(t14_0), .Y0(t15_0),
    .X1(t14_1), .Y1(t15_1),
    .X2(t14_2), .Y2(t15_2),
    .X3(t14_3), .Y3(t15_3),
    .X4(t14_4), .Y4(t15_4),
    .X5(t14_5), .Y5(t15_5),
    .X6(t14_6), .Y6(t15_6),
    .X7(t14_7), .Y7(t15_7));


endmodule

// Latency: 242
// Gap: 256
module rc79108(clk, reset, next, next_out,
   X0, Y0,
   X1, Y1,
   X2, Y2,
   X3, Y3,
   X4, Y4,
   X5, Y5,
   X6, Y6,
   X7, Y7);

   output next_out;
   input clk, reset, next;

   input [31:0] X0,
      X1,
      X2,
      X3,
      X4,
      X5,
      X6,
      X7;

   output [31:0] Y0,
      Y1,
      Y2,
      Y3,
      Y4,
      Y5,
      Y6,
      Y7;

   wire [63:0] t0;
   wire [63:0] s0;
   assign t0 = {X0, X1};
   wire [63:0] t1;
   wire [63:0] s1;
   assign t1 = {X2, X3};
   wire [63:0] t2;
   wire [63:0] s2;
   assign t2 = {X4, X5};
   wire [63:0] t3;
   wire [63:0] s3;
   assign t3 = {X6, X7};
   assign Y0 = s0[63:32];
   assign Y1 = s0[31:0];
   assign Y2 = s1[63:32];
   assign Y3 = s1[31:0];
   assign Y4 = s2[63:32];
   assign Y5 = s2[31:0];
   assign Y6 = s3[63:32];
   assign Y7 = s3[31:0];

   perm79106 instPerm85673(.x0(t0), .y0(s0),
    .x1(t1), .y1(s1),
    .x2(t2), .y2(s2),
    .x3(t3), .y3(s3),
   .clk(clk), .next(next), .next_out(next_out), .reset(reset)
);



endmodule

// Latency: 242
// Gap: 256
module perm79106(clk, next, reset, next_out,
   x0, y0,
   x1, y1,
   x2, y2,
   x3, y3);
   parameter numBanks = 4;
   parameter logBanks = 2;
   parameter depth = 256;
   parameter logDepth = 8;
   parameter width = 64;

   input [width-1:0]  x0;
   output [width-1:0]  y0;
   wire [width-1:0]  ybuff0;
   input [width-1:0]  x1;
   output [width-1:0]  y1;
   wire [width-1:0]  ybuff1;
   input [width-1:0]  x2;
   output [width-1:0]  y2;
   wire [width-1:0]  ybuff2;
   input [width-1:0]  x3;
   output [width-1:0]  y3;
   wire [width-1:0]  ybuff3;
   input 	      clk, next, reset;
   output 	     next_out;

   wire    	     next0;

   reg              inFlip0, outFlip0;
   reg              inActive, outActive;

   wire [logBanks-1:0] inBank0, outBank0;
   wire [logDepth-1:0] inAddr0, outAddr0;
   wire [logBanks-1:0] outBank_a0;
   wire [logDepth-1:0] outAddr_a0;
   wire [logDepth+logBanks-1:0] addr0, addr0b, addr0c;
   wire [logBanks-1:0] inBank1, outBank1;
   wire [logDepth-1:0] inAddr1, outAddr1;
   wire [logBanks-1:0] outBank_a1;
   wire [logDepth-1:0] outAddr_a1;
   wire [logDepth+logBanks-1:0] addr1, addr1b, addr1c;
   wire [logBanks-1:0] inBank2, outBank2;
   wire [logDepth-1:0] inAddr2, outAddr2;
   wire [logBanks-1:0] outBank_a2;
   wire [logDepth-1:0] outAddr_a2;
   wire [logDepth+logBanks-1:0] addr2, addr2b, addr2c;
   wire [logBanks-1:0] inBank3, outBank3;
   wire [logDepth-1:0] inAddr3, outAddr3;
   wire [logBanks-1:0] outBank_a3;
   wire [logDepth-1:0] outAddr_a3;
   wire [logDepth+logBanks-1:0] addr3, addr3b, addr3c;


   reg [logDepth-1:0]  inCount, outCount, outCount_d, outCount_dd, outCount_for_rd_addr, outCount_for_rd_data;  

   assign    addr0 = {inCount, 2'd0};
   assign    addr0b = {outCount, 2'd0};
   assign    addr0c = {outCount_for_rd_addr, 2'd0};
   assign    addr1 = {inCount, 2'd1};
   assign    addr1b = {outCount, 2'd1};
   assign    addr1c = {outCount_for_rd_addr, 2'd1};
   assign    addr2 = {inCount, 2'd2};
   assign    addr2b = {outCount, 2'd2};
   assign    addr2c = {outCount_for_rd_addr, 2'd2};
   assign    addr3 = {inCount, 2'd3};
   assign    addr3b = {outCount, 2'd3};
   assign    addr3c = {outCount_for_rd_addr, 2'd3};
    wire [width+logDepth-1:0] w_0_0, w_0_1, w_0_2, w_0_3, w_1_0, w_1_1, w_1_2, w_1_3, w_2_0, w_2_1, w_2_2, w_2_3;

    reg [width-1:0] z_0_0;
    reg [width-1:0] z_0_1;
    reg [width-1:0] z_0_2;
    reg [width-1:0] z_0_3;
    wire [width-1:0] z_1_0, z_1_1, z_1_2, z_1_3, z_2_0, z_2_1, z_2_2, z_2_3;

    wire [logDepth-1:0] u_0_0, u_0_1, u_0_2, u_0_3, u_1_0, u_1_1, u_1_2, u_1_3, u_2_0, u_2_1, u_2_2, u_2_3;

    reg inFlip1, outFlip1;
    always @(posedge clk) begin
        inFlip1 <= inFlip0;
        outFlip1 <= outFlip0;
    end

   assign inBank0[0] = addr0[8] ^ addr0[0];
   assign inBank0[1] = addr0[9] ^ addr0[1];
   assign inAddr0[0] = addr0[6];
   assign inAddr0[1] = addr0[7];
   assign inAddr0[2] = addr0[4];
   assign inAddr0[3] = addr0[5];
   assign inAddr0[4] = addr0[2];
   assign inAddr0[5] = addr0[3];
   assign inAddr0[6] = addr0[0];
   assign inAddr0[7] = addr0[1];
   assign outBank0[0] = addr0b[8] ^ addr0b[0];
   assign outBank0[1] = addr0b[9] ^ addr0b[1];
   assign outAddr0[0] = addr0b[2];
   assign outAddr0[1] = addr0b[3];
   assign outAddr0[2] = addr0b[4];
   assign outAddr0[3] = addr0b[5];
   assign outAddr0[4] = addr0b[6];
   assign outAddr0[5] = addr0b[7];
   assign outAddr0[6] = addr0b[8];
   assign outAddr0[7] = addr0b[9];
   assign outBank_a0[0] = addr0c[8] ^ addr0c[0];
   assign outBank_a0[1] = addr0c[9] ^ addr0c[1];
   assign outAddr_a0[0] = addr0c[2];
   assign outAddr_a0[1] = addr0c[3];
   assign outAddr_a0[2] = addr0c[4];
   assign outAddr_a0[3] = addr0c[5];
   assign outAddr_a0[4] = addr0c[6];
   assign outAddr_a0[5] = addr0c[7];
   assign outAddr_a0[6] = addr0c[8];
   assign outAddr_a0[7] = addr0c[9];

   assign inBank1[0] = addr1[8] ^ addr1[0];
   assign inBank1[1] = addr1[9] ^ addr1[1];
   assign inAddr1[0] = addr1[6];
   assign inAddr1[1] = addr1[7];
   assign inAddr1[2] = addr1[4];
   assign inAddr1[3] = addr1[5];
   assign inAddr1[4] = addr1[2];
   assign inAddr1[5] = addr1[3];
   assign inAddr1[6] = addr1[0];
   assign inAddr1[7] = addr1[1];
   assign outBank1[0] = addr1b[8] ^ addr1b[0];
   assign outBank1[1] = addr1b[9] ^ addr1b[1];
   assign outAddr1[0] = addr1b[2];
   assign outAddr1[1] = addr1b[3];
   assign outAddr1[2] = addr1b[4];
   assign outAddr1[3] = addr1b[5];
   assign outAddr1[4] = addr1b[6];
   assign outAddr1[5] = addr1b[7];
   assign outAddr1[6] = addr1b[8];
   assign outAddr1[7] = addr1b[9];
   assign outBank_a1[0] = addr1c[8] ^ addr1c[0];
   assign outBank_a1[1] = addr1c[9] ^ addr1c[1];
   assign outAddr_a1[0] = addr1c[2];
   assign outAddr_a1[1] = addr1c[3];
   assign outAddr_a1[2] = addr1c[4];
   assign outAddr_a1[3] = addr1c[5];
   assign outAddr_a1[4] = addr1c[6];
   assign outAddr_a1[5] = addr1c[7];
   assign outAddr_a1[6] = addr1c[8];
   assign outAddr_a1[7] = addr1c[9];

   assign inBank2[0] = addr2[8] ^ addr2[0];
   assign inBank2[1] = addr2[9] ^ addr2[1];
   assign inAddr2[0] = addr2[6];
   assign inAddr2[1] = addr2[7];
   assign inAddr2[2] = addr2[4];
   assign inAddr2[3] = addr2[5];
   assign inAddr2[4] = addr2[2];
   assign inAddr2[5] = addr2[3];
   assign inAddr2[6] = addr2[0];
   assign inAddr2[7] = addr2[1];
   assign outBank2[0] = addr2b[8] ^ addr2b[0];
   assign outBank2[1] = addr2b[9] ^ addr2b[1];
   assign outAddr2[0] = addr2b[2];
   assign outAddr2[1] = addr2b[3];
   assign outAddr2[2] = addr2b[4];
   assign outAddr2[3] = addr2b[5];
   assign outAddr2[4] = addr2b[6];
   assign outAddr2[5] = addr2b[7];
   assign outAddr2[6] = addr2b[8];
   assign outAddr2[7] = addr2b[9];
   assign outBank_a2[0] = addr2c[8] ^ addr2c[0];
   assign outBank_a2[1] = addr2c[9] ^ addr2c[1];
   assign outAddr_a2[0] = addr2c[2];
   assign outAddr_a2[1] = addr2c[3];
   assign outAddr_a2[2] = addr2c[4];
   assign outAddr_a2[3] = addr2c[5];
   assign outAddr_a2[4] = addr2c[6];
   assign outAddr_a2[5] = addr2c[7];
   assign outAddr_a2[6] = addr2c[8];
   assign outAddr_a2[7] = addr2c[9];

   assign inBank3[0] = addr3[8] ^ addr3[0];
   assign inBank3[1] = addr3[9] ^ addr3[1];
   assign inAddr3[0] = addr3[6];
   assign inAddr3[1] = addr3[7];
   assign inAddr3[2] = addr3[4];
   assign inAddr3[3] = addr3[5];
   assign inAddr3[4] = addr3[2];
   assign inAddr3[5] = addr3[3];
   assign inAddr3[6] = addr3[0];
   assign inAddr3[7] = addr3[1];
   assign outBank3[0] = addr3b[8] ^ addr3b[0];
   assign outBank3[1] = addr3b[9] ^ addr3b[1];
   assign outAddr3[0] = addr3b[2];
   assign outAddr3[1] = addr3b[3];
   assign outAddr3[2] = addr3b[4];
   assign outAddr3[3] = addr3b[5];
   assign outAddr3[4] = addr3b[6];
   assign outAddr3[5] = addr3b[7];
   assign outAddr3[6] = addr3b[8];
   assign outAddr3[7] = addr3b[9];
   assign outBank_a3[0] = addr3c[8] ^ addr3c[0];
   assign outBank_a3[1] = addr3c[9] ^ addr3c[1];
   assign outAddr_a3[0] = addr3c[2];
   assign outAddr_a3[1] = addr3c[3];
   assign outAddr_a3[2] = addr3c[4];
   assign outAddr_a3[3] = addr3c[5];
   assign outAddr_a3[4] = addr3c[6];
   assign outAddr_a3[5] = addr3c[7];
   assign outAddr_a3[6] = addr3c[8];
   assign outAddr_a3[7] = addr3c[9];

   nextReg #(238, 8) nextReg_85678(.X(next), .Y(next0), .reset(reset), .clk(clk));


   shiftRegFIFO #(4, 1) shiftFIFO_85681(.X(next0), .Y(next_out), .clk(clk));


   memArray1024_79106 #(numBanks, logBanks, depth, logDepth, width)
     memSys(.inFlip(inFlip1), .outFlip(outFlip1), .next(next), .reset(reset),
        .x0(w_2_0[width+logDepth-1:logDepth]), .y0(ybuff0),
        .inAddr0(w_2_0[logDepth-1:0]),
        .outAddr0(u_2_0), 
        .x1(w_2_1[width+logDepth-1:logDepth]), .y1(ybuff1),
        .inAddr1(w_2_1[logDepth-1:0]),
        .outAddr1(u_2_1), 
        .x2(w_2_2[width+logDepth-1:logDepth]), .y2(ybuff2),
        .inAddr2(w_2_2[logDepth-1:0]),
        .outAddr2(u_2_2), 
        .x3(w_2_3[width+logDepth-1:logDepth]), .y3(ybuff3),
        .inAddr3(w_2_3[logDepth-1:0]),
        .outAddr3(u_2_3), 
        .clk(clk));

   always @(posedge clk) begin
      if (reset == 1) begin
      z_0_0 <= 0;
      z_0_1 <= 0;
      z_0_2 <= 0;
      z_0_3 <= 0;
         inFlip0 <= 0; outFlip0 <= 1; outCount <= 0; inCount <= 0;
        outCount_for_rd_addr <= 0;
        outCount_for_rd_data <= 0;
      end
      else begin
          outCount_d <= outCount;
          outCount_dd <= outCount_d;
         if (inCount == 237)
            outCount_for_rd_addr <= 0;
         else
            outCount_for_rd_addr <= outCount_for_rd_addr+1;
         if (inCount == 240)
            outCount_for_rd_data <= 0;
         else
            outCount_for_rd_data <= outCount_for_rd_data+1;
      z_0_0 <= ybuff0;
      z_0_1 <= ybuff1;
      z_0_2 <= ybuff2;
      z_0_3 <= ybuff3;
         if (inCount == 237) begin
            outFlip0 <= ~outFlip0;
            outCount <= 0;
         end
         else
            outCount <= outCount+1;
         if (inCount == 255) begin
            inFlip0 <= ~inFlip0;
         end
         if (next == 1) begin
            if (inCount >= 237)
               inFlip0 <= ~inFlip0;
            inCount <= 0;
         end
         else
            inCount <= inCount + 1;
      end
   end
    assign w_0_0 = {x0, inAddr0};
    assign w_0_1 = {x1, inAddr1};
    assign w_0_2 = {x2, inAddr2};
    assign w_0_3 = {x3, inAddr3};
    assign y0 = z_2_0;
    assign y1 = z_2_1;
    assign y2 = z_2_2;
    assign y3 = z_2_3;
    assign u_0_0 = outAddr_a0;
    assign u_0_1 = outAddr_a1;
    assign u_0_2 = outAddr_a2;
    assign u_0_3 = outAddr_a3;
    wire wr_ctrl_st_0;
    assign wr_ctrl_st_0 = inCount[7];

    switch #(logDepth+width) in_sw_0_0(.x0(w_0_0), .x1(w_0_2), .y0(w_1_0), .y1(w_1_2), .ctrl(wr_ctrl_st_0));
    switch #(logDepth+width) in_sw_0_1(.x0(w_0_1), .x1(w_0_3), .y0(w_1_1), .y1(w_1_3), .ctrl(wr_ctrl_st_0));
    reg [width+logDepth-1:0] w_1_0_pipe;
    reg [width+logDepth-1:0] w_1_1_pipe;
    reg [width+logDepth-1:0] w_1_2_pipe;
    reg [width+logDepth-1:0] w_1_3_pipe;

    always @(posedge clk) begin
        w_1_0_pipe <= w_1_0;
        w_1_1_pipe <= w_1_1;
        w_1_2_pipe <= w_1_2;
        w_1_3_pipe <= w_1_3;
    end

    wire wr_ctrl_st_1;
    reg wr_ctrl_st_1_1;
    always @(posedge clk) begin
        wr_ctrl_st_1_1 <= inCount[6];
    end
    assign wr_ctrl_st_1 = wr_ctrl_st_1_1;

    switch #(logDepth+width) in_sw_1_0(.x0(w_1_0_pipe), .x1(w_1_1_pipe), .y0(w_2_0), .y1(w_2_1), .ctrl(wr_ctrl_st_1));
    switch #(logDepth+width) in_sw_1_1(.x0(w_1_2_pipe), .x1(w_1_3_pipe), .y0(w_2_2), .y1(w_2_3), .ctrl(wr_ctrl_st_1));
    wire rdd_ctrl_st_0;
    assign rdd_ctrl_st_0 = outCount_for_rd_data[7];

    switch #(width) out_sw_0_0(.x0(z_0_0), .x1(z_0_2), .y0(z_1_0), .y1(z_1_2), .ctrl(rdd_ctrl_st_0));
    switch #(width) out_sw_0_1(.x0(z_0_1), .x1(z_0_3), .y0(z_1_1), .y1(z_1_3), .ctrl(rdd_ctrl_st_0));
    reg [width-1:0] z_1_0_pipe;
    reg [width-1:0] z_1_1_pipe;
    reg [width-1:0] z_1_2_pipe;
    reg [width-1:0] z_1_3_pipe;

    always @(posedge clk) begin
        z_1_0_pipe <= z_1_0;
        z_1_1_pipe <= z_1_1;
        z_1_2_pipe <= z_1_2;
        z_1_3_pipe <= z_1_3;
    end

    wire rdd_ctrl_st_1;
    reg rdd_ctrl_st_1_1;
    always @(posedge clk) begin
        rdd_ctrl_st_1_1 <= outCount_for_rd_data[6];

    end
    assign rdd_ctrl_st_1 = rdd_ctrl_st_1_1;

    switch #(width) out_sw_1_0(.x0(z_1_0_pipe), .x1(z_1_1_pipe), .y0(z_2_0), .y1(z_2_1), .ctrl(rdd_ctrl_st_1));
    switch #(width) out_sw_1_1(.x0(z_1_2_pipe), .x1(z_1_3_pipe), .y0(z_2_2), .y1(z_2_3), .ctrl(rdd_ctrl_st_1));
    wire rda_ctrl_st_0;
    assign rda_ctrl_st_0 = outCount_for_rd_addr[7];

    switch #(logDepth) rdaddr_sw_0_0(.x0(u_0_0), .x1(u_0_2), .y0(u_1_0), .y1(u_1_2), .ctrl(rda_ctrl_st_0));
    switch #(logDepth) rdaddr_sw_0_1(.x0(u_0_1), .x1(u_0_3), .y0(u_1_1), .y1(u_1_3), .ctrl(rda_ctrl_st_0));
    reg [logDepth-1:0] u_1_0_pipe;
    reg [logDepth-1:0] u_1_1_pipe;
    reg [logDepth-1:0] u_1_2_pipe;
    reg [logDepth-1:0] u_1_3_pipe;

    always @(posedge clk) begin
        u_1_0_pipe <= u_1_0;
        u_1_1_pipe <= u_1_1;
        u_1_2_pipe <= u_1_2;
        u_1_3_pipe <= u_1_3;
    end

    wire rda_ctrl_st_1;
    reg rda_ctrl_st_1_1;
    always @(posedge clk) begin
        rda_ctrl_st_1_1 <= outCount_for_rd_addr[6];

    end
    assign rda_ctrl_st_1 = rda_ctrl_st_1_1;

    switch #(logDepth) rdaddr_sw_1_0(.x0(u_1_0_pipe), .x1(u_1_1_pipe), .y0(u_2_0), .y1(u_2_1), .ctrl(rda_ctrl_st_1));
    switch #(logDepth) rdaddr_sw_1_1(.x0(u_1_2_pipe), .x1(u_1_3_pipe), .y0(u_2_2), .y1(u_2_3), .ctrl(rda_ctrl_st_1));
endmodule

module memArray1024_79106(next, reset,
                x0, y0,
                inAddr0,
                outAddr0,
                x1, y1,
                inAddr1,
                outAddr1,
                x2, y2,
                inAddr2,
                outAddr2,
                x3, y3,
                inAddr3,
                outAddr3,
                clk, inFlip, outFlip);

   parameter numBanks = 4;
   parameter logBanks = 2;
   parameter depth = 256;
   parameter logDepth = 8;
   parameter width = 64;
         
   input     clk, next, reset;
   input    inFlip, outFlip;
   wire    next0;
   
   input [width-1:0]   x0;
   output [width-1:0]  y0;
   input [logDepth-1:0] inAddr0, outAddr0;
   input [width-1:0]   x1;
   output [width-1:0]  y1;
   input [logDepth-1:0] inAddr1, outAddr1;
   input [width-1:0]   x2;
   output [width-1:0]  y2;
   input [logDepth-1:0] inAddr2, outAddr2;
   input [width-1:0]   x3;
   output [width-1:0]  y3;
   input [logDepth-1:0] inAddr3, outAddr3;
   nextReg #(256, 8) nextReg_85686(.X(next), .Y(next0), .reset(reset), .clk(clk));


   memMod #(depth*2, width, logDepth+1) 
     memMod0(.in(x0), .out(y0), .inAddr({inFlip, inAddr0}),
	   .outAddr({outFlip, outAddr0}), .writeSel(1'b1), .clk(clk));   
   memMod #(depth*2, width, logDepth+1) 
     memMod1(.in(x1), .out(y1), .inAddr({inFlip, inAddr1}),
	   .outAddr({outFlip, outAddr1}), .writeSel(1'b1), .clk(clk));   
   memMod #(depth*2, width, logDepth+1) 
     memMod2(.in(x2), .out(y2), .inAddr({inFlip, inAddr2}),
	   .outAddr({outFlip, outAddr2}), .writeSel(1'b1), .clk(clk));   
   memMod #(depth*2, width, logDepth+1) 
     memMod3(.in(x3), .out(y3), .inAddr({inFlip, inAddr3}),
	   .outAddr({outFlip, outAddr3}), .writeSel(1'b1), .clk(clk));   
endmodule

module nextReg(X, Y, reset, clk);
   parameter depth=2, logDepth=1;

   output Y;
   input X;
   input              clk, reset;
   reg [logDepth:0] count;
   reg                active;

   assign Y = (count == depth) ? 1 : 0;

   always @ (posedge clk) begin
      if (reset == 1) begin
         count <= 0;
         active <= 0;
      end
      else if (X == 1) begin
         active <= 1;
         count <= 1;
      end
      else if (count == depth) begin
         count <= 0;
         active <= 0;
      end
      else if (active)
         count <= count+1;
   end
endmodule


module memMod(in, out, inAddr, outAddr, writeSel, clk);
   
   parameter depth=1024, width=16, logDepth=10;
   
   input [width-1:0]    in;
   input [logDepth-1:0] inAddr, outAddr;
   input 	        writeSel, clk;
   output [width-1:0] 	out;
   reg [width-1:0] 	out;
   
   // synthesis attribute ram_style of mem is block

   reg [width-1:0] 	mem[depth-1:0]; 
   
   always @(posedge clk) begin
      out <= mem[outAddr];
      
      if (writeSel)
        mem[inAddr] <= in;
   end
endmodule 



module memMod_dist(in, out, inAddr, outAddr, writeSel, clk);
   
   parameter depth=1024, width=16, logDepth=10;
   
   input [width-1:0]    in;
   input [logDepth-1:0] inAddr, outAddr;
   input 	        writeSel, clk;
   output [width-1:0] 	out;
   reg [width-1:0] 	out;
   
   // synthesis attribute ram_style of mem is distributed

   reg [width-1:0] 	mem[depth-1:0]; 
   
   always @(posedge clk) begin
      out <= mem[outAddr];
      
      if (writeSel)
        mem[inAddr] <= in;
   end
endmodule 

module switch(ctrl, x0, x1, y0, y1);
    parameter width = 16;
    input [width-1:0] x0, x1;
    output [width-1:0] y0, y1;
    input ctrl;
    assign y0 = (ctrl == 0) ? x0 : x1;
    assign y1 = (ctrl == 0) ? x1 : x0;
endmodule

module shiftRegFIFO(X, Y, clk);
   parameter depth=1, width=1;

   output [width-1:0] Y;
   input  [width-1:0] X;
   input              clk;

   reg [width-1:0]    mem [depth-1:0];
   integer            index;

   assign Y = mem[depth-1];

   always @ (posedge clk) begin
      for(index=1;index<depth;index=index+1) begin
         mem[index] <= mem[index-1];
      end
      mem[0]<=X;
   end
endmodule

// Latency: 3
// Gap: 1
module codeBlock79110(clk, reset, next_in, next_out,
   X0_in, Y0,
   X1_in, Y1,
   X2_in, Y2,
   X3_in, Y3,
   X4_in, Y4,
   X5_in, Y5,
   X6_in, Y6,
   X7_in, Y7);

   output next_out;
   input clk, reset, next_in;

   reg next;

   input [31:0] X0_in,
      X1_in,
      X2_in,
      X3_in,
      X4_in,
      X5_in,
      X6_in,
      X7_in;

   reg   [31:0] X0,
      X1,
      X2,
      X3,
      X4,
      X5,
      X6,
      X7;

   output [31:0] Y0,
      Y1,
      Y2,
      Y3,
      Y4,
      Y5,
      Y6,
      Y7;

   shiftRegFIFO #(2, 1) shiftFIFO_85693(.X(next), .Y(next_out), .clk(clk));


   wire signed [31:0] a498;
   wire signed [31:0] a499;
   wire signed [31:0] a500;
   wire signed [31:0] a501;
   wire signed [31:0] a506;
   wire signed [31:0] a507;
   wire signed [31:0] a508;
   wire signed [31:0] a509;
   wire signed [31:0] t626;
   wire signed [31:0] t627;
   wire signed [31:0] t628;
   wire signed [31:0] t629;
   wire signed [31:0] t630;
   wire signed [31:0] t631;
   wire signed [31:0] t632;
   wire signed [31:0] t633;
   wire signed [31:0] t634;
   wire signed [31:0] t635;
   wire signed [31:0] t636;
   wire signed [31:0] t637;
   wire signed [31:0] Y0;
   wire signed [31:0] Y1;
   wire signed [31:0] Y4;
   wire signed [31:0] Y5;
   wire signed [31:0] t638;
   wire signed [31:0] t639;
   wire signed [31:0] t640;
   wire signed [31:0] t641;
   wire signed [31:0] Y2;
   wire signed [31:0] Y3;
   wire signed [31:0] Y6;
   wire signed [31:0] Y7;


   assign a498 = X0;
   assign a499 = X4;
   assign a500 = X1;
   assign a501 = X5;
   assign a506 = X2;
   assign a507 = X6;
   assign a508 = X3;
   assign a509 = X7;
   assign Y0 = t634;
   assign Y1 = t635;
   assign Y4 = t636;
   assign Y5 = t637;
   assign Y2 = t638;
   assign Y3 = t639;
   assign Y6 = t640;
   assign Y7 = t641;

    addfxp #(32, 1) add79122(.a(a498), .b(a499), .clk(clk), .q(t626));    // 0
    addfxp #(32, 1) add79137(.a(a500), .b(a501), .clk(clk), .q(t627));    // 0
    subfxp #(32, 1) sub79152(.a(a498), .b(a499), .clk(clk), .q(t628));    // 0
    subfxp #(32, 1) sub79167(.a(a500), .b(a501), .clk(clk), .q(t629));    // 0
    addfxp #(32, 1) add79182(.a(a506), .b(a507), .clk(clk), .q(t630));    // 0
    addfxp #(32, 1) add79197(.a(a508), .b(a509), .clk(clk), .q(t631));    // 0
    subfxp #(32, 1) sub79212(.a(a506), .b(a507), .clk(clk), .q(t632));    // 0
    subfxp #(32, 1) sub79227(.a(a508), .b(a509), .clk(clk), .q(t633));    // 0
    addfxp #(32, 1) add79234(.a(t626), .b(t630), .clk(clk), .q(t634));    // 1
    addfxp #(32, 1) add79241(.a(t627), .b(t631), .clk(clk), .q(t635));    // 1
    subfxp #(32, 1) sub79248(.a(t626), .b(t630), .clk(clk), .q(t636));    // 1
    subfxp #(32, 1) sub79255(.a(t627), .b(t631), .clk(clk), .q(t637));    // 1
    addfxp #(32, 1) add79278(.a(t628), .b(t633), .clk(clk), .q(t638));    // 1
    subfxp #(32, 1) sub79285(.a(t629), .b(t632), .clk(clk), .q(t639));    // 1
    subfxp #(32, 1) sub79292(.a(t628), .b(t633), .clk(clk), .q(t640));    // 1
    addfxp #(32, 1) add79299(.a(t629), .b(t632), .clk(clk), .q(t641));    // 1


   always @(posedge clk) begin
      if (reset == 1) begin
      end
      else begin
         X0 <= X0_in;
         X1 <= X1_in;
         X2 <= X2_in;
         X3 <= X3_in;
         X4 <= X4_in;
         X5 <= X5_in;
         X6 <= X6_in;
         X7 <= X7_in;
         next <= next_in;
      end
   end
endmodule

// Latency: 8
// Gap: 4
module rc79323(clk, reset, next, next_out,
   X0, Y0,
   X1, Y1,
   X2, Y2,
   X3, Y3,
   X4, Y4,
   X5, Y5,
   X6, Y6,
   X7, Y7);

   output next_out;
   input clk, reset, next;

   input [31:0] X0,
      X1,
      X2,
      X3,
      X4,
      X5,
      X6,
      X7;

   output [31:0] Y0,
      Y1,
      Y2,
      Y3,
      Y4,
      Y5,
      Y6,
      Y7;

   wire [63:0] t0;
   wire [63:0] s0;
   assign t0 = {X0, X1};
   wire [63:0] t1;
   wire [63:0] s1;
   assign t1 = {X2, X3};
   wire [63:0] t2;
   wire [63:0] s2;
   assign t2 = {X4, X5};
   wire [63:0] t3;
   wire [63:0] s3;
   assign t3 = {X6, X7};
   assign Y0 = s0[63:32];
   assign Y1 = s0[31:0];
   assign Y2 = s1[63:32];
   assign Y3 = s1[31:0];
   assign Y4 = s2[63:32];
   assign Y5 = s2[31:0];
   assign Y6 = s3[63:32];
   assign Y7 = s3[31:0];

   perm79321 instPerm85694(.x0(t0), .y0(s0),
    .x1(t1), .y1(s1),
    .x2(t2), .y2(s2),
    .x3(t3), .y3(s3),
   .clk(clk), .next(next), .next_out(next_out), .reset(reset)
);



endmodule

// Latency: 8
// Gap: 4
module perm79321(clk, next, reset, next_out,
   x0, y0,
   x1, y1,
   x2, y2,
   x3, y3);
   parameter numBanks = 4;
   parameter logBanks = 2;
   parameter depth = 4;
   parameter logDepth = 2;
   parameter width = 64;

   input [width-1:0]  x0;
   output [width-1:0]  y0;
   wire [width-1:0]  ybuff0;
   input [width-1:0]  x1;
   output [width-1:0]  y1;
   wire [width-1:0]  ybuff1;
   input [width-1:0]  x2;
   output [width-1:0]  y2;
   wire [width-1:0]  ybuff2;
   input [width-1:0]  x3;
   output [width-1:0]  y3;
   wire [width-1:0]  ybuff3;
   input 	      clk, next, reset;
   output 	     next_out;

   wire    	     next0;

   reg              inFlip0, outFlip0;
   reg              inActive, outActive;

   wire [logBanks-1:0] inBank0, outBank0;
   wire [logDepth-1:0] inAddr0, outAddr0;
   wire [logBanks-1:0] outBank_a0;
   wire [logDepth-1:0] outAddr_a0;
   wire [logDepth+logBanks-1:0] addr0, addr0b, addr0c;
   wire [logBanks-1:0] inBank1, outBank1;
   wire [logDepth-1:0] inAddr1, outAddr1;
   wire [logBanks-1:0] outBank_a1;
   wire [logDepth-1:0] outAddr_a1;
   wire [logDepth+logBanks-1:0] addr1, addr1b, addr1c;
   wire [logBanks-1:0] inBank2, outBank2;
   wire [logDepth-1:0] inAddr2, outAddr2;
   wire [logBanks-1:0] outBank_a2;
   wire [logDepth-1:0] outAddr_a2;
   wire [logDepth+logBanks-1:0] addr2, addr2b, addr2c;
   wire [logBanks-1:0] inBank3, outBank3;
   wire [logDepth-1:0] inAddr3, outAddr3;
   wire [logBanks-1:0] outBank_a3;
   wire [logDepth-1:0] outAddr_a3;
   wire [logDepth+logBanks-1:0] addr3, addr3b, addr3c;


   reg [logDepth-1:0]  inCount, outCount, outCount_d, outCount_dd, outCount_for_rd_addr, outCount_for_rd_data;  

   assign    addr0 = {inCount, 2'd0};
   assign    addr0b = {outCount, 2'd0};
   assign    addr0c = {outCount_for_rd_addr, 2'd0};
   assign    addr1 = {inCount, 2'd1};
   assign    addr1b = {outCount, 2'd1};
   assign    addr1c = {outCount_for_rd_addr, 2'd1};
   assign    addr2 = {inCount, 2'd2};
   assign    addr2b = {outCount, 2'd2};
   assign    addr2c = {outCount_for_rd_addr, 2'd2};
   assign    addr3 = {inCount, 2'd3};
   assign    addr3b = {outCount, 2'd3};
   assign    addr3c = {outCount_for_rd_addr, 2'd3};
    wire [width+logDepth-1:0] w_0_0, w_0_1, w_0_2, w_0_3, w_1_0, w_1_1, w_1_2, w_1_3, w_2_0, w_2_1, w_2_2, w_2_3;

    reg [width-1:0] z_0_0;
    reg [width-1:0] z_0_1;
    reg [width-1:0] z_0_2;
    reg [width-1:0] z_0_3;
    wire [width-1:0] z_1_0, z_1_1, z_1_2, z_1_3, z_2_0, z_2_1, z_2_2, z_2_3;

    wire [logDepth-1:0] u_0_0, u_0_1, u_0_2, u_0_3, u_1_0, u_1_1, u_1_2, u_1_3, u_2_0, u_2_1, u_2_2, u_2_3;

    reg inFlip1, outFlip1;
    always @(posedge clk) begin
        inFlip1 <= inFlip0;
        outFlip1 <= outFlip0;
    end

   assign inBank0[0] = addr0[2] ^ addr0[0];
   assign inBank0[1] = addr0[3] ^ addr0[1];
   assign inAddr0[0] = addr0[0];
   assign inAddr0[1] = addr0[1];
   assign outBank0[0] = addr0b[2] ^ addr0b[0];
   assign outBank0[1] = addr0b[3] ^ addr0b[1];
   assign outAddr0[0] = addr0b[2];
   assign outAddr0[1] = addr0b[3];
   assign outBank_a0[0] = addr0c[2] ^ addr0c[0];
   assign outBank_a0[1] = addr0c[3] ^ addr0c[1];
   assign outAddr_a0[0] = addr0c[2];
   assign outAddr_a0[1] = addr0c[3];

   assign inBank1[0] = addr1[2] ^ addr1[0];
   assign inBank1[1] = addr1[3] ^ addr1[1];
   assign inAddr1[0] = addr1[0];
   assign inAddr1[1] = addr1[1];
   assign outBank1[0] = addr1b[2] ^ addr1b[0];
   assign outBank1[1] = addr1b[3] ^ addr1b[1];
   assign outAddr1[0] = addr1b[2];
   assign outAddr1[1] = addr1b[3];
   assign outBank_a1[0] = addr1c[2] ^ addr1c[0];
   assign outBank_a1[1] = addr1c[3] ^ addr1c[1];
   assign outAddr_a1[0] = addr1c[2];
   assign outAddr_a1[1] = addr1c[3];

   assign inBank2[0] = addr2[2] ^ addr2[0];
   assign inBank2[1] = addr2[3] ^ addr2[1];
   assign inAddr2[0] = addr2[0];
   assign inAddr2[1] = addr2[1];
   assign outBank2[0] = addr2b[2] ^ addr2b[0];
   assign outBank2[1] = addr2b[3] ^ addr2b[1];
   assign outAddr2[0] = addr2b[2];
   assign outAddr2[1] = addr2b[3];
   assign outBank_a2[0] = addr2c[2] ^ addr2c[0];
   assign outBank_a2[1] = addr2c[3] ^ addr2c[1];
   assign outAddr_a2[0] = addr2c[2];
   assign outAddr_a2[1] = addr2c[3];

   assign inBank3[0] = addr3[2] ^ addr3[0];
   assign inBank3[1] = addr3[3] ^ addr3[1];
   assign inAddr3[0] = addr3[0];
   assign inAddr3[1] = addr3[1];
   assign outBank3[0] = addr3b[2] ^ addr3b[0];
   assign outBank3[1] = addr3b[3] ^ addr3b[1];
   assign outAddr3[0] = addr3b[2];
   assign outAddr3[1] = addr3b[3];
   assign outBank_a3[0] = addr3c[2] ^ addr3c[0];
   assign outBank_a3[1] = addr3c[3] ^ addr3c[1];
   assign outAddr_a3[0] = addr3c[2];
   assign outAddr_a3[1] = addr3c[3];

   shiftRegFIFO #(4, 1) shiftFIFO_85697(.X(next), .Y(next0), .clk(clk));


   shiftRegFIFO #(4, 1) shiftFIFO_85700(.X(next0), .Y(next_out), .clk(clk));


   memArray16_79321 #(numBanks, logBanks, depth, logDepth, width)
     memSys(.inFlip(inFlip1), .outFlip(outFlip1), .next(next), .reset(reset),
        .x0(w_2_0[width+logDepth-1:logDepth]), .y0(ybuff0),
        .inAddr0(w_2_0[logDepth-1:0]),
        .outAddr0(u_2_0), 
        .x1(w_2_1[width+logDepth-1:logDepth]), .y1(ybuff1),
        .inAddr1(w_2_1[logDepth-1:0]),
        .outAddr1(u_2_1), 
        .x2(w_2_2[width+logDepth-1:logDepth]), .y2(ybuff2),
        .inAddr2(w_2_2[logDepth-1:0]),
        .outAddr2(u_2_2), 
        .x3(w_2_3[width+logDepth-1:logDepth]), .y3(ybuff3),
        .inAddr3(w_2_3[logDepth-1:0]),
        .outAddr3(u_2_3), 
        .clk(clk));

    reg resetOutCountRd2_4;
    reg resetOutCountRd2_5;
    reg resetOutCountRd2_6;

    always @(posedge clk) begin
        if (reset == 1) begin
            resetOutCountRd2_4 <= 0;
            resetOutCountRd2_5 <= 0;
            resetOutCountRd2_6 <= 0;
        end
        else begin
            resetOutCountRd2_4 <= (inCount == 3) ? 1'b1 : 1'b0;
            resetOutCountRd2_5 <= resetOutCountRd2_4;
            resetOutCountRd2_6 <= resetOutCountRd2_5;
            if (resetOutCountRd2_6 == 1'b1)
                outCount_for_rd_data <= 0;
            else
                outCount_for_rd_data <= outCount_for_rd_data+1;
        end
    end
   always @(posedge clk) begin
      if (reset == 1) begin
      z_0_0 <= 0;
      z_0_1 <= 0;
      z_0_2 <= 0;
      z_0_3 <= 0;
         inFlip0 <= 0; outFlip0 <= 1; outCount <= 0; inCount <= 0;
        outCount_for_rd_addr <= 0;
      end
      else begin
          outCount_d <= outCount;
          outCount_dd <= outCount_d;
         if (inCount == 3)
            outCount_for_rd_addr <= 0;
         else
            outCount_for_rd_addr <= outCount_for_rd_addr+1;
      z_0_0 <= ybuff0;
      z_0_1 <= ybuff1;
      z_0_2 <= ybuff2;
      z_0_3 <= ybuff3;
         if (inCount == 3) begin
            outFlip0 <= ~outFlip0;
            outCount <= 0;
         end
         else
            outCount <= outCount+1;
         if (inCount == 3) begin
            inFlip0 <= ~inFlip0;
         end
         if (next == 1) begin
            if (inCount >= 3)
               inFlip0 <= ~inFlip0;
            inCount <= 0;
         end
         else
            inCount <= inCount + 1;
      end
   end
    assign w_0_0 = {x0, inAddr0};
    assign w_0_1 = {x1, inAddr1};
    assign w_0_2 = {x2, inAddr2};
    assign w_0_3 = {x3, inAddr3};
    assign y0 = z_2_0;
    assign y1 = z_2_1;
    assign y2 = z_2_2;
    assign y3 = z_2_3;
    assign u_0_0 = outAddr_a0;
    assign u_0_1 = outAddr_a1;
    assign u_0_2 = outAddr_a2;
    assign u_0_3 = outAddr_a3;
    wire wr_ctrl_st_0;
    assign wr_ctrl_st_0 = inCount[1];

    switch #(logDepth+width) in_sw_0_0(.x0(w_0_0), .x1(w_0_2), .y0(w_1_0), .y1(w_1_2), .ctrl(wr_ctrl_st_0));
    switch #(logDepth+width) in_sw_0_1(.x0(w_0_1), .x1(w_0_3), .y0(w_1_1), .y1(w_1_3), .ctrl(wr_ctrl_st_0));
    reg [width+logDepth-1:0] w_1_0_pipe;
    reg [width+logDepth-1:0] w_1_1_pipe;
    reg [width+logDepth-1:0] w_1_2_pipe;
    reg [width+logDepth-1:0] w_1_3_pipe;

    always @(posedge clk) begin
        w_1_0_pipe <= w_1_0;
        w_1_1_pipe <= w_1_1;
        w_1_2_pipe <= w_1_2;
        w_1_3_pipe <= w_1_3;
    end

    wire wr_ctrl_st_1;
    reg wr_ctrl_st_1_1;
    always @(posedge clk) begin
        wr_ctrl_st_1_1 <= inCount[0];
    end
    assign wr_ctrl_st_1 = wr_ctrl_st_1_1;

    switch #(logDepth+width) in_sw_1_0(.x0(w_1_0_pipe), .x1(w_1_1_pipe), .y0(w_2_0), .y1(w_2_1), .ctrl(wr_ctrl_st_1));
    switch #(logDepth+width) in_sw_1_1(.x0(w_1_2_pipe), .x1(w_1_3_pipe), .y0(w_2_2), .y1(w_2_3), .ctrl(wr_ctrl_st_1));
    wire rdd_ctrl_st_0;
    assign rdd_ctrl_st_0 = outCount_for_rd_data[1];

    switch #(width) out_sw_0_0(.x0(z_0_0), .x1(z_0_2), .y0(z_1_0), .y1(z_1_2), .ctrl(rdd_ctrl_st_0));
    switch #(width) out_sw_0_1(.x0(z_0_1), .x1(z_0_3), .y0(z_1_1), .y1(z_1_3), .ctrl(rdd_ctrl_st_0));
    reg [width-1:0] z_1_0_pipe;
    reg [width-1:0] z_1_1_pipe;
    reg [width-1:0] z_1_2_pipe;
    reg [width-1:0] z_1_3_pipe;

    always @(posedge clk) begin
        z_1_0_pipe <= z_1_0;
        z_1_1_pipe <= z_1_1;
        z_1_2_pipe <= z_1_2;
        z_1_3_pipe <= z_1_3;
    end

    wire rdd_ctrl_st_1;
    reg rdd_ctrl_st_1_1;
    always @(posedge clk) begin
        rdd_ctrl_st_1_1 <= outCount_for_rd_data[0];

    end
    assign rdd_ctrl_st_1 = rdd_ctrl_st_1_1;

    switch #(width) out_sw_1_0(.x0(z_1_0_pipe), .x1(z_1_1_pipe), .y0(z_2_0), .y1(z_2_1), .ctrl(rdd_ctrl_st_1));
    switch #(width) out_sw_1_1(.x0(z_1_2_pipe), .x1(z_1_3_pipe), .y0(z_2_2), .y1(z_2_3), .ctrl(rdd_ctrl_st_1));
    wire rda_ctrl_st_0;
    assign rda_ctrl_st_0 = outCount_for_rd_addr[1];

    switch #(logDepth) rdaddr_sw_0_0(.x0(u_0_0), .x1(u_0_2), .y0(u_1_0), .y1(u_1_2), .ctrl(rda_ctrl_st_0));
    switch #(logDepth) rdaddr_sw_0_1(.x0(u_0_1), .x1(u_0_3), .y0(u_1_1), .y1(u_1_3), .ctrl(rda_ctrl_st_0));
    reg [logDepth-1:0] u_1_0_pipe;
    reg [logDepth-1:0] u_1_1_pipe;
    reg [logDepth-1:0] u_1_2_pipe;
    reg [logDepth-1:0] u_1_3_pipe;

    always @(posedge clk) begin
        u_1_0_pipe <= u_1_0;
        u_1_1_pipe <= u_1_1;
        u_1_2_pipe <= u_1_2;
        u_1_3_pipe <= u_1_3;
    end

    wire rda_ctrl_st_1;
    reg rda_ctrl_st_1_1;
    always @(posedge clk) begin
        rda_ctrl_st_1_1 <= outCount_for_rd_addr[0];

    end
    assign rda_ctrl_st_1 = rda_ctrl_st_1_1;

    switch #(logDepth) rdaddr_sw_1_0(.x0(u_1_0_pipe), .x1(u_1_1_pipe), .y0(u_2_0), .y1(u_2_1), .ctrl(rda_ctrl_st_1));
    switch #(logDepth) rdaddr_sw_1_1(.x0(u_1_2_pipe), .x1(u_1_3_pipe), .y0(u_2_2), .y1(u_2_3), .ctrl(rda_ctrl_st_1));
endmodule

module memArray16_79321(next, reset,
                x0, y0,
                inAddr0,
                outAddr0,
                x1, y1,
                inAddr1,
                outAddr1,
                x2, y2,
                inAddr2,
                outAddr2,
                x3, y3,
                inAddr3,
                outAddr3,
                clk, inFlip, outFlip);

   parameter numBanks = 4;
   parameter logBanks = 2;
   parameter depth = 4;
   parameter logDepth = 2;
   parameter width = 64;
         
   input     clk, next, reset;
   input    inFlip, outFlip;
   wire    next0;
   
   input [width-1:0]   x0;
   output [width-1:0]  y0;
   input [logDepth-1:0] inAddr0, outAddr0;
   input [width-1:0]   x1;
   output [width-1:0]  y1;
   input [logDepth-1:0] inAddr1, outAddr1;
   input [width-1:0]   x2;
   output [width-1:0]  y2;
   input [logDepth-1:0] inAddr2, outAddr2;
   input [width-1:0]   x3;
   output [width-1:0]  y3;
   input [logDepth-1:0] inAddr3, outAddr3;
   shiftRegFIFO #(4, 1) shiftFIFO_85703(.X(next), .Y(next0), .clk(clk));


   memMod #(depth*2, width, logDepth+1) 
     memMod0(.in(x0), .out(y0), .inAddr({inFlip, inAddr0}),
	   .outAddr({outFlip, outAddr0}), .writeSel(1'b1), .clk(clk));   
   memMod #(depth*2, width, logDepth+1) 
     memMod1(.in(x1), .out(y1), .inAddr({inFlip, inAddr1}),
	   .outAddr({outFlip, outAddr1}), .writeSel(1'b1), .clk(clk));   
   memMod #(depth*2, width, logDepth+1) 
     memMod2(.in(x2), .out(y2), .inAddr({inFlip, inAddr2}),
	   .outAddr({outFlip, outAddr2}), .writeSel(1'b1), .clk(clk));   
   memMod #(depth*2, width, logDepth+1) 
     memMod3(.in(x3), .out(y3), .inAddr({inFlip, inAddr3}),
	   .outAddr({outFlip, outAddr3}), .writeSel(1'b1), .clk(clk));   
endmodule

// Latency: 12
// Gap: 4
module DirSum_79696(clk, reset, next, next_out,
      X0, Y0,
      X1, Y1,
      X2, Y2,
      X3, Y3,
      X4, Y4,
      X5, Y5,
      X6, Y6,
      X7, Y7);

   output next_out;
   input clk, reset, next;

   reg [1:0] i4;

   input [31:0] X0,
      X1,
      X2,
      X3,
      X4,
      X5,
      X6,
      X7;

   output [31:0] Y0,
      Y1,
      Y2,
      Y3,
      Y4,
      Y5,
      Y6,
      Y7;

   always @(posedge clk) begin
      if (reset == 1) begin
         i4 <= 0;
      end
      else begin
         if (next == 1)
            i4 <= 0;
         else if (i4 == 3)
            i4 <= 0;
         else
            i4 <= i4 + 1;
      end
   end

   codeBlock79326 codeBlockIsnt85704(.clk(clk), .reset(reset), .next_in(next), .next_out(next_out),
.i4_in(i4),
       .X0_in(X0), .Y0(Y0),
       .X1_in(X1), .Y1(Y1),
       .X2_in(X2), .Y2(Y2),
       .X3_in(X3), .Y3(Y3),
       .X4_in(X4), .Y4(Y4),
       .X5_in(X5), .Y5(Y5),
       .X6_in(X6), .Y6(Y6),
       .X7_in(X7), .Y7(Y7));

endmodule

module D40_79652(addr, out, clk);
   input clk;
   output [31:0] out;
   reg [31:0] out, out2, out3;
   input [1:0] addr;

   always @(posedge clk) begin
      out2 <= out3;
      out <= out2;
   case(addr)
      0: out3 <= 32'h0;
      1: out3 <= 32'hc4df2862;
      2: out3 <= 32'hd2bec333;
      3: out3 <= 32'h187de2a7;
      default: out3 <= 0;
   endcase
   end
// synthesis attribute rom_style of out3 is "block"
endmodule



module D39_79658(addr, out, clk);
   input clk;
   output [31:0] out;
   reg [31:0] out, out2, out3;
   input [1:0] addr;

   always @(posedge clk) begin
      out2 <= out3;
      out <= out2;
   case(addr)
      0: out3 <= 32'h0;
      1: out3 <= 32'hd2bec333;
      2: out3 <= 32'hc0000000;
      3: out3 <= 32'hd2bec333;
      default: out3 <= 0;
   endcase
   end
// synthesis attribute rom_style of out3 is "block"
endmodule



module D38_79664(addr, out, clk);
   input clk;
   output [31:0] out;
   reg [31:0] out, out2, out3;
   input [1:0] addr;

   always @(posedge clk) begin
      out2 <= out3;
      out <= out2;
   case(addr)
      0: out3 <= 32'h0;
      1: out3 <= 32'he7821d59;
      2: out3 <= 32'hd2bec333;
      3: out3 <= 32'hc4df2862;
      default: out3 <= 0;
   endcase
   end
// synthesis attribute rom_style of out3 is "block"
endmodule



module D36_79676(addr, out, clk);
   input clk;
   output [31:0] out;
   reg [31:0] out, out2, out3;
   input [1:0] addr;

   always @(posedge clk) begin
      out2 <= out3;
      out <= out2;
   case(addr)
      0: out3 <= 32'h40000000;
      1: out3 <= 32'h187de2a7;
      2: out3 <= 32'hd2bec333;
      3: out3 <= 32'hc4df2862;
      default: out3 <= 0;
   endcase
   end
// synthesis attribute rom_style of out3 is "block"
endmodule



module D35_79682(addr, out, clk);
   input clk;
   output [31:0] out;
   reg [31:0] out, out2, out3;
   input [1:0] addr;

   always @(posedge clk) begin
      out2 <= out3;
      out <= out2;
   case(addr)
      0: out3 <= 32'h40000000;
      1: out3 <= 32'h2d413ccd;
      2: out3 <= 32'h0;
      3: out3 <= 32'hd2bec333;
      default: out3 <= 0;
   endcase
   end
// synthesis attribute rom_style of out3 is "block"
endmodule



module D34_79688(addr, out, clk);
   input clk;
   output [31:0] out;
   reg [31:0] out, out2, out3;
   input [1:0] addr;

   always @(posedge clk) begin
      out2 <= out3;
      out <= out2;
   case(addr)
      0: out3 <= 32'h40000000;
      1: out3 <= 32'h3b20d79e;
      2: out3 <= 32'h2d413ccd;
      3: out3 <= 32'h187de2a7;
      default: out3 <= 0;
   endcase
   end
// synthesis attribute rom_style of out3 is "block"
endmodule



// Latency: 12
// Gap: 1
module codeBlock79326(clk, reset, next_in, next_out,
   i4_in,
   X0_in, Y0,
   X1_in, Y1,
   X2_in, Y2,
   X3_in, Y3,
   X4_in, Y4,
   X5_in, Y5,
   X6_in, Y6,
   X7_in, Y7);

   output next_out;
   input clk, reset, next_in;

   reg next;
   input [1:0] i4_in;
   reg [1:0] i4;

   input [31:0] X0_in,
      X1_in,
      X2_in,
      X3_in,
      X4_in,
      X5_in,
      X6_in,
      X7_in;

   reg   [31:0] X0,
      X1,
      X2,
      X3,
      X4,
      X5,
      X6,
      X7;

   output [31:0] Y0,
      Y1,
      Y2,
      Y3,
      Y4,
      Y5,
      Y6,
      Y7;

   shiftRegFIFO #(11, 1) shiftFIFO_85707(.X(next), .Y(next_out), .clk(clk));


   wire signed [31:0] a466;
   wire signed [31:0] a443;
   wire signed [31:0] a469;
   wire signed [31:0] a447;
   wire signed [31:0] a470;
   wire signed [31:0] a471;
   wire signed [31:0] a474;
   wire signed [31:0] a475;
   wire signed [31:0] a478;
   wire signed [31:0] a479;
   reg signed [31:0] tm152;
   reg signed [31:0] tm156;
   reg signed [31:0] tm168;
   reg signed [31:0] tm172;
   reg signed [31:0] tm184;
   reg signed [31:0] tm188;
   reg signed [31:0] tm200;
   reg signed [31:0] tm211;
   reg signed [31:0] tm153;
   reg signed [31:0] tm157;
   reg signed [31:0] tm169;
   reg signed [31:0] tm173;
   reg signed [31:0] tm185;
   reg signed [31:0] tm189;
   reg signed [31:0] tm201;
   reg signed [31:0] tm212;
   wire signed [31:0] tm2;
   wire signed [31:0] a448;
   wire signed [31:0] tm3;
   wire signed [31:0] a450;
   wire signed [31:0] tm4;
   wire signed [31:0] a454;
   wire signed [31:0] tm5;
   wire signed [31:0] a456;
   wire signed [31:0] tm6;
   wire signed [31:0] a460;
   wire signed [31:0] tm7;
   wire signed [31:0] a462;
   reg signed [31:0] tm154;
   reg signed [31:0] tm158;
   reg signed [31:0] tm170;
   reg signed [31:0] tm174;
   reg signed [31:0] tm186;
   reg signed [31:0] tm190;
   reg signed [31:0] tm202;
   reg signed [31:0] tm213;
   reg signed [31:0] tm36;
   reg signed [31:0] tm37;
   reg signed [31:0] tm40;
   reg signed [31:0] tm41;
   reg signed [31:0] tm44;
   reg signed [31:0] tm45;
   reg signed [31:0] tm155;
   reg signed [31:0] tm159;
   reg signed [31:0] tm171;
   reg signed [31:0] tm175;
   reg signed [31:0] tm187;
   reg signed [31:0] tm191;
   reg signed [31:0] tm203;
   reg signed [31:0] tm214;
   reg signed [31:0] tm204;
   reg signed [31:0] tm215;
   reg signed [31:0] tm205;
   reg signed [31:0] tm216;
   reg signed [31:0] tm206;
   reg signed [31:0] tm217;
   reg signed [31:0] tm207;
   reg signed [31:0] tm218;
   reg signed [31:0] tm208;
   reg signed [31:0] tm219;
   wire signed [31:0] a449;
   wire signed [31:0] a451;
   wire signed [31:0] a452;
   wire signed [31:0] a453;
   wire signed [31:0] a455;
   wire signed [31:0] a457;
   wire signed [31:0] a458;
   wire signed [31:0] a459;
   wire signed [31:0] a461;
   wire signed [31:0] a463;
   wire signed [31:0] a464;
   wire signed [31:0] a465;
   reg signed [31:0] tm209;
   reg signed [31:0] tm220;
   wire signed [31:0] Y0;
   wire signed [31:0] Y1;
   wire signed [31:0] Y2;
   wire signed [31:0] Y3;
   wire signed [31:0] Y4;
   wire signed [31:0] Y5;
   wire signed [31:0] Y6;
   wire signed [31:0] Y7;
   reg signed [31:0] tm210;
   reg signed [31:0] tm221;


   assign a466 = X0;
   assign a443 = a466;
   assign a469 = X1;
   assign a447 = a469;
   assign a470 = X2;
   assign a471 = X3;
   assign a474 = X4;
   assign a475 = X5;
   assign a478 = X6;
   assign a479 = X7;
   assign a448 = tm2;
   assign a450 = tm3;
   assign a454 = tm4;
   assign a456 = tm5;
   assign a460 = tm6;
   assign a462 = tm7;
   assign Y0 = tm210;
   assign Y1 = tm221;

   D40_79652 instD40inst0_79652(.addr(i4[1:0]), .out(tm7), .clk(clk));

   D39_79658 instD39inst0_79658(.addr(i4[1:0]), .out(tm5), .clk(clk));

   D38_79664 instD38inst0_79664(.addr(i4[1:0]), .out(tm3), .clk(clk));

   D36_79676 instD36inst0_79676(.addr(i4[1:0]), .out(tm6), .clk(clk));

   D35_79682 instD35inst0_79682(.addr(i4[1:0]), .out(tm4), .clk(clk));

   D34_79688 instD34inst0_79688(.addr(i4[1:0]), .out(tm2), .clk(clk));

    multfix #(32, 6) m79425(.a(tm36), .b(tm155), .clk(clk), .q_sc(a449), .q_unsc(), .rst(reset));
    multfix #(32, 6) m79447(.a(tm37), .b(tm159), .clk(clk), .q_sc(a451), .q_unsc(), .rst(reset));
    multfix #(32, 6) m79465(.a(tm37), .b(tm155), .clk(clk), .q_sc(a452), .q_unsc(), .rst(reset));
    multfix #(32, 6) m79476(.a(tm36), .b(tm159), .clk(clk), .q_sc(a453), .q_unsc(), .rst(reset));
    multfix #(32, 6) m79505(.a(tm40), .b(tm171), .clk(clk), .q_sc(a455), .q_unsc(), .rst(reset));
    multfix #(32, 6) m79527(.a(tm41), .b(tm175), .clk(clk), .q_sc(a457), .q_unsc(), .rst(reset));
    multfix #(32, 6) m79545(.a(tm41), .b(tm171), .clk(clk), .q_sc(a458), .q_unsc(), .rst(reset));
    multfix #(32, 6) m79556(.a(tm40), .b(tm175), .clk(clk), .q_sc(a459), .q_unsc(), .rst(reset));
    multfix #(32, 6) m79585(.a(tm44), .b(tm187), .clk(clk), .q_sc(a461), .q_unsc(), .rst(reset));
    multfix #(32, 6) m79607(.a(tm45), .b(tm191), .clk(clk), .q_sc(a463), .q_unsc(), .rst(reset));
    multfix #(32, 6) m79625(.a(tm45), .b(tm187), .clk(clk), .q_sc(a464), .q_unsc(), .rst(reset));
    multfix #(32, 6) m79636(.a(tm44), .b(tm191), .clk(clk), .q_sc(a465), .q_unsc(), .rst(reset));
    subfxp #(32, 1) sub79454(.a(a449), .b(a451), .clk(clk), .q(Y2));    // 10
    addfxp #(32, 1) add79483(.a(a452), .b(a453), .clk(clk), .q(Y3));    // 10
    subfxp #(32, 1) sub79534(.a(a455), .b(a457), .clk(clk), .q(Y4));    // 10
    addfxp #(32, 1) add79563(.a(a458), .b(a459), .clk(clk), .q(Y5));    // 10
    subfxp #(32, 1) sub79614(.a(a461), .b(a463), .clk(clk), .q(Y6));    // 10
    addfxp #(32, 1) add79643(.a(a464), .b(a465), .clk(clk), .q(Y7));    // 10


   always @(posedge clk) begin
      if (reset == 1) begin
         tm36 <= 0;
         tm155 <= 0;
         tm37 <= 0;
         tm159 <= 0;
         tm37 <= 0;
         tm155 <= 0;
         tm36 <= 0;
         tm159 <= 0;
         tm40 <= 0;
         tm171 <= 0;
         tm41 <= 0;
         tm175 <= 0;
         tm41 <= 0;
         tm171 <= 0;
         tm40 <= 0;
         tm175 <= 0;
         tm44 <= 0;
         tm187 <= 0;
         tm45 <= 0;
         tm191 <= 0;
         tm45 <= 0;
         tm187 <= 0;
         tm44 <= 0;
         tm191 <= 0;
      end
      else begin
         i4 <= i4_in;
         X0 <= X0_in;
         X1 <= X1_in;
         X2 <= X2_in;
         X3 <= X3_in;
         X4 <= X4_in;
         X5 <= X5_in;
         X6 <= X6_in;
         X7 <= X7_in;
         next <= next_in;
         tm152 <= a470;
         tm156 <= a471;
         tm168 <= a474;
         tm172 <= a475;
         tm184 <= a478;
         tm188 <= a479;
         tm200 <= a443;
         tm211 <= a447;
         tm153 <= tm152;
         tm157 <= tm156;
         tm169 <= tm168;
         tm173 <= tm172;
         tm185 <= tm184;
         tm189 <= tm188;
         tm201 <= tm200;
         tm212 <= tm211;
         tm154 <= tm153;
         tm158 <= tm157;
         tm170 <= tm169;
         tm174 <= tm173;
         tm186 <= tm185;
         tm190 <= tm189;
         tm202 <= tm201;
         tm213 <= tm212;
         tm36 <= a448;
         tm37 <= a450;
         tm40 <= a454;
         tm41 <= a456;
         tm44 <= a460;
         tm45 <= a462;
         tm155 <= tm154;
         tm159 <= tm158;
         tm171 <= tm170;
         tm175 <= tm174;
         tm187 <= tm186;
         tm191 <= tm190;
         tm203 <= tm202;
         tm214 <= tm213;
         tm204 <= tm203;
         tm215 <= tm214;
         tm205 <= tm204;
         tm216 <= tm215;
         tm206 <= tm205;
         tm217 <= tm216;
         tm207 <= tm206;
         tm218 <= tm217;
         tm208 <= tm207;
         tm219 <= tm218;
         tm209 <= tm208;
         tm220 <= tm219;
         tm210 <= tm209;
         tm221 <= tm220;
      end
   end
endmodule

// Latency: 3
// Gap: 1
module codeBlock79699(clk, reset, next_in, next_out,
   X0_in, Y0,
   X1_in, Y1,
   X2_in, Y2,
   X3_in, Y3,
   X4_in, Y4,
   X5_in, Y5,
   X6_in, Y6,
   X7_in, Y7);

   output next_out;
   input clk, reset, next_in;

   reg next;

   input [31:0] X0_in,
      X1_in,
      X2_in,
      X3_in,
      X4_in,
      X5_in,
      X6_in,
      X7_in;

   reg   [31:0] X0,
      X1,
      X2,
      X3,
      X4,
      X5,
      X6,
      X7;

   output [31:0] Y0,
      Y1,
      Y2,
      Y3,
      Y4,
      Y5,
      Y6,
      Y7;

   shiftRegFIFO #(2, 1) shiftFIFO_85710(.X(next), .Y(next_out), .clk(clk));


   wire signed [31:0] a377;
   wire signed [31:0] a378;
   wire signed [31:0] a379;
   wire signed [31:0] a380;
   wire signed [31:0] a385;
   wire signed [31:0] a387;
   wire signed [31:0] a388;
   wire signed [31:0] a389;
   wire signed [31:0] t498;
   wire signed [31:0] t499;
   wire signed [31:0] t500;
   wire signed [31:0] t501;
   wire signed [31:0] t502;
   wire signed [31:0] t503;
   wire signed [31:0] t504;
   wire signed [31:0] t505;
   wire signed [31:0] t506;
   wire signed [31:0] t507;
   wire signed [31:0] t508;
   wire signed [31:0] t509;
   wire signed [31:0] Y0;
   wire signed [31:0] Y1;
   wire signed [31:0] Y4;
   wire signed [31:0] Y5;
   wire signed [31:0] t510;
   wire signed [31:0] t511;
   wire signed [31:0] t512;
   wire signed [31:0] t513;
   wire signed [31:0] Y2;
   wire signed [31:0] Y3;
   wire signed [31:0] Y6;
   wire signed [31:0] Y7;


   assign a377 = X0;
   assign a378 = X4;
   assign a379 = X1;
   assign a380 = X5;
   assign a385 = X2;
   assign a387 = X6;
   assign a388 = X3;
   assign a389 = X7;
   assign Y0 = t506;
   assign Y1 = t507;
   assign Y4 = t508;
   assign Y5 = t509;
   assign Y2 = t510;
   assign Y3 = t511;
   assign Y6 = t512;
   assign Y7 = t513;

    addfxp #(32, 1) add79711(.a(a377), .b(a378), .clk(clk), .q(t498));    // 0
    addfxp #(32, 1) add79726(.a(a379), .b(a380), .clk(clk), .q(t499));    // 0
    subfxp #(32, 1) sub79741(.a(a377), .b(a378), .clk(clk), .q(t500));    // 0
    subfxp #(32, 1) sub79756(.a(a379), .b(a380), .clk(clk), .q(t501));    // 0
    addfxp #(32, 1) add79771(.a(a385), .b(a387), .clk(clk), .q(t502));    // 0
    addfxp #(32, 1) add79786(.a(a388), .b(a389), .clk(clk), .q(t503));    // 0
    subfxp #(32, 1) sub79801(.a(a385), .b(a387), .clk(clk), .q(t504));    // 0
    subfxp #(32, 1) sub79816(.a(a388), .b(a389), .clk(clk), .q(t505));    // 0
    addfxp #(32, 1) add79823(.a(t498), .b(t502), .clk(clk), .q(t506));    // 1
    addfxp #(32, 1) add79830(.a(t499), .b(t503), .clk(clk), .q(t507));    // 1
    subfxp #(32, 1) sub79837(.a(t498), .b(t502), .clk(clk), .q(t508));    // 1
    subfxp #(32, 1) sub79844(.a(t499), .b(t503), .clk(clk), .q(t509));    // 1
    addfxp #(32, 1) add79867(.a(t500), .b(t505), .clk(clk), .q(t510));    // 1
    subfxp #(32, 1) sub79874(.a(t501), .b(t504), .clk(clk), .q(t511));    // 1
    subfxp #(32, 1) sub79881(.a(t500), .b(t505), .clk(clk), .q(t512));    // 1
    addfxp #(32, 1) add79888(.a(t501), .b(t504), .clk(clk), .q(t513));    // 1


   always @(posedge clk) begin
      if (reset == 1) begin
      end
      else begin
         X0 <= X0_in;
         X1 <= X1_in;
         X2 <= X2_in;
         X3 <= X3_in;
         X4 <= X4_in;
         X5 <= X5_in;
         X6 <= X6_in;
         X7 <= X7_in;
         next <= next_in;
      end
   end
endmodule

// Latency: 17
// Gap: 16
module rc79912(clk, reset, next, next_out,
   X0, Y0,
   X1, Y1,
   X2, Y2,
   X3, Y3,
   X4, Y4,
   X5, Y5,
   X6, Y6,
   X7, Y7);

   output next_out;
   input clk, reset, next;

   input [31:0] X0,
      X1,
      X2,
      X3,
      X4,
      X5,
      X6,
      X7;

   output [31:0] Y0,
      Y1,
      Y2,
      Y3,
      Y4,
      Y5,
      Y6,
      Y7;

   wire [63:0] t0;
   wire [63:0] s0;
   assign t0 = {X0, X1};
   wire [63:0] t1;
   wire [63:0] s1;
   assign t1 = {X2, X3};
   wire [63:0] t2;
   wire [63:0] s2;
   assign t2 = {X4, X5};
   wire [63:0] t3;
   wire [63:0] s3;
   assign t3 = {X6, X7};
   assign Y0 = s0[63:32];
   assign Y1 = s0[31:0];
   assign Y2 = s1[63:32];
   assign Y3 = s1[31:0];
   assign Y4 = s2[63:32];
   assign Y5 = s2[31:0];
   assign Y6 = s3[63:32];
   assign Y7 = s3[31:0];

   perm79910 instPerm85711(.x0(t0), .y0(s0),
    .x1(t1), .y1(s1),
    .x2(t2), .y2(s2),
    .x3(t3), .y3(s3),
   .clk(clk), .next(next), .next_out(next_out), .reset(reset)
);



endmodule

// Latency: 17
// Gap: 16
module perm79910(clk, next, reset, next_out,
   x0, y0,
   x1, y1,
   x2, y2,
   x3, y3);
   parameter numBanks = 4;
   parameter logBanks = 2;
   parameter depth = 16;
   parameter logDepth = 4;
   parameter width = 64;

   input [width-1:0]  x0;
   output [width-1:0]  y0;
   wire [width-1:0]  ybuff0;
   input [width-1:0]  x1;
   output [width-1:0]  y1;
   wire [width-1:0]  ybuff1;
   input [width-1:0]  x2;
   output [width-1:0]  y2;
   wire [width-1:0]  ybuff2;
   input [width-1:0]  x3;
   output [width-1:0]  y3;
   wire [width-1:0]  ybuff3;
   input 	      clk, next, reset;
   output 	     next_out;

   wire    	     next0;

   reg              inFlip0, outFlip0;
   reg              inActive, outActive;

   wire [logBanks-1:0] inBank0, outBank0;
   wire [logDepth-1:0] inAddr0, outAddr0;
   wire [logBanks-1:0] outBank_a0;
   wire [logDepth-1:0] outAddr_a0;
   wire [logDepth+logBanks-1:0] addr0, addr0b, addr0c;
   wire [logBanks-1:0] inBank1, outBank1;
   wire [logDepth-1:0] inAddr1, outAddr1;
   wire [logBanks-1:0] outBank_a1;
   wire [logDepth-1:0] outAddr_a1;
   wire [logDepth+logBanks-1:0] addr1, addr1b, addr1c;
   wire [logBanks-1:0] inBank2, outBank2;
   wire [logDepth-1:0] inAddr2, outAddr2;
   wire [logBanks-1:0] outBank_a2;
   wire [logDepth-1:0] outAddr_a2;
   wire [logDepth+logBanks-1:0] addr2, addr2b, addr2c;
   wire [logBanks-1:0] inBank3, outBank3;
   wire [logDepth-1:0] inAddr3, outAddr3;
   wire [logBanks-1:0] outBank_a3;
   wire [logDepth-1:0] outAddr_a3;
   wire [logDepth+logBanks-1:0] addr3, addr3b, addr3c;


   reg [logDepth-1:0]  inCount, outCount, outCount_d, outCount_dd, outCount_for_rd_addr, outCount_for_rd_data;  

   assign    addr0 = {inCount, 2'd0};
   assign    addr0b = {outCount, 2'd0};
   assign    addr0c = {outCount_for_rd_addr, 2'd0};
   assign    addr1 = {inCount, 2'd1};
   assign    addr1b = {outCount, 2'd1};
   assign    addr1c = {outCount_for_rd_addr, 2'd1};
   assign    addr2 = {inCount, 2'd2};
   assign    addr2b = {outCount, 2'd2};
   assign    addr2c = {outCount_for_rd_addr, 2'd2};
   assign    addr3 = {inCount, 2'd3};
   assign    addr3b = {outCount, 2'd3};
   assign    addr3c = {outCount_for_rd_addr, 2'd3};
    wire [width+logDepth-1:0] w_0_0, w_0_1, w_0_2, w_0_3, w_1_0, w_1_1, w_1_2, w_1_3, w_2_0, w_2_1, w_2_2, w_2_3;

    reg [width-1:0] z_0_0;
    reg [width-1:0] z_0_1;
    reg [width-1:0] z_0_2;
    reg [width-1:0] z_0_3;
    wire [width-1:0] z_1_0, z_1_1, z_1_2, z_1_3, z_2_0, z_2_1, z_2_2, z_2_3;

    wire [logDepth-1:0] u_0_0, u_0_1, u_0_2, u_0_3, u_1_0, u_1_1, u_1_2, u_1_3, u_2_0, u_2_1, u_2_2, u_2_3;

    reg inFlip1, outFlip1;
    always @(posedge clk) begin
        inFlip1 <= inFlip0;
        outFlip1 <= outFlip0;
    end

   assign inBank0[0] = addr0[4] ^ addr0[0];
   assign inBank0[1] = addr0[5] ^ addr0[1];
   assign inAddr0[0] = addr0[2];
   assign inAddr0[1] = addr0[3];
   assign inAddr0[2] = addr0[0];
   assign inAddr0[3] = addr0[1];
   assign outBank0[0] = addr0b[4] ^ addr0b[0];
   assign outBank0[1] = addr0b[5] ^ addr0b[1];
   assign outAddr0[0] = addr0b[2];
   assign outAddr0[1] = addr0b[3];
   assign outAddr0[2] = addr0b[4];
   assign outAddr0[3] = addr0b[5];
   assign outBank_a0[0] = addr0c[4] ^ addr0c[0];
   assign outBank_a0[1] = addr0c[5] ^ addr0c[1];
   assign outAddr_a0[0] = addr0c[2];
   assign outAddr_a0[1] = addr0c[3];
   assign outAddr_a0[2] = addr0c[4];
   assign outAddr_a0[3] = addr0c[5];

   assign inBank1[0] = addr1[4] ^ addr1[0];
   assign inBank1[1] = addr1[5] ^ addr1[1];
   assign inAddr1[0] = addr1[2];
   assign inAddr1[1] = addr1[3];
   assign inAddr1[2] = addr1[0];
   assign inAddr1[3] = addr1[1];
   assign outBank1[0] = addr1b[4] ^ addr1b[0];
   assign outBank1[1] = addr1b[5] ^ addr1b[1];
   assign outAddr1[0] = addr1b[2];
   assign outAddr1[1] = addr1b[3];
   assign outAddr1[2] = addr1b[4];
   assign outAddr1[3] = addr1b[5];
   assign outBank_a1[0] = addr1c[4] ^ addr1c[0];
   assign outBank_a1[1] = addr1c[5] ^ addr1c[1];
   assign outAddr_a1[0] = addr1c[2];
   assign outAddr_a1[1] = addr1c[3];
   assign outAddr_a1[2] = addr1c[4];
   assign outAddr_a1[3] = addr1c[5];

   assign inBank2[0] = addr2[4] ^ addr2[0];
   assign inBank2[1] = addr2[5] ^ addr2[1];
   assign inAddr2[0] = addr2[2];
   assign inAddr2[1] = addr2[3];
   assign inAddr2[2] = addr2[0];
   assign inAddr2[3] = addr2[1];
   assign outBank2[0] = addr2b[4] ^ addr2b[0];
   assign outBank2[1] = addr2b[5] ^ addr2b[1];
   assign outAddr2[0] = addr2b[2];
   assign outAddr2[1] = addr2b[3];
   assign outAddr2[2] = addr2b[4];
   assign outAddr2[3] = addr2b[5];
   assign outBank_a2[0] = addr2c[4] ^ addr2c[0];
   assign outBank_a2[1] = addr2c[5] ^ addr2c[1];
   assign outAddr_a2[0] = addr2c[2];
   assign outAddr_a2[1] = addr2c[3];
   assign outAddr_a2[2] = addr2c[4];
   assign outAddr_a2[3] = addr2c[5];

   assign inBank3[0] = addr3[4] ^ addr3[0];
   assign inBank3[1] = addr3[5] ^ addr3[1];
   assign inAddr3[0] = addr3[2];
   assign inAddr3[1] = addr3[3];
   assign inAddr3[2] = addr3[0];
   assign inAddr3[3] = addr3[1];
   assign outBank3[0] = addr3b[4] ^ addr3b[0];
   assign outBank3[1] = addr3b[5] ^ addr3b[1];
   assign outAddr3[0] = addr3b[2];
   assign outAddr3[1] = addr3b[3];
   assign outAddr3[2] = addr3b[4];
   assign outAddr3[3] = addr3b[5];
   assign outBank_a3[0] = addr3c[4] ^ addr3c[0];
   assign outBank_a3[1] = addr3c[5] ^ addr3c[1];
   assign outAddr_a3[0] = addr3c[2];
   assign outAddr_a3[1] = addr3c[3];
   assign outAddr_a3[2] = addr3c[4];
   assign outAddr_a3[3] = addr3c[5];

   nextReg #(13, 4) nextReg_85716(.X(next), .Y(next0), .reset(reset), .clk(clk));


   shiftRegFIFO #(4, 1) shiftFIFO_85719(.X(next0), .Y(next_out), .clk(clk));


   memArray64_79910 #(numBanks, logBanks, depth, logDepth, width)
     memSys(.inFlip(inFlip1), .outFlip(outFlip1), .next(next), .reset(reset),
        .x0(w_2_0[width+logDepth-1:logDepth]), .y0(ybuff0),
        .inAddr0(w_2_0[logDepth-1:0]),
        .outAddr0(u_2_0), 
        .x1(w_2_1[width+logDepth-1:logDepth]), .y1(ybuff1),
        .inAddr1(w_2_1[logDepth-1:0]),
        .outAddr1(u_2_1), 
        .x2(w_2_2[width+logDepth-1:logDepth]), .y2(ybuff2),
        .inAddr2(w_2_2[logDepth-1:0]),
        .outAddr2(u_2_2), 
        .x3(w_2_3[width+logDepth-1:logDepth]), .y3(ybuff3),
        .inAddr3(w_2_3[logDepth-1:0]),
        .outAddr3(u_2_3), 
        .clk(clk));

   always @(posedge clk) begin
      if (reset == 1) begin
      z_0_0 <= 0;
      z_0_1 <= 0;
      z_0_2 <= 0;
      z_0_3 <= 0;
         inFlip0 <= 0; outFlip0 <= 1; outCount <= 0; inCount <= 0;
        outCount_for_rd_addr <= 0;
        outCount_for_rd_data <= 0;
      end
      else begin
          outCount_d <= outCount;
          outCount_dd <= outCount_d;
         if (inCount == 12)
            outCount_for_rd_addr <= 0;
         else
            outCount_for_rd_addr <= outCount_for_rd_addr+1;
         if (inCount == 15)
            outCount_for_rd_data <= 0;
         else
            outCount_for_rd_data <= outCount_for_rd_data+1;
      z_0_0 <= ybuff0;
      z_0_1 <= ybuff1;
      z_0_2 <= ybuff2;
      z_0_3 <= ybuff3;
         if (inCount == 12) begin
            outFlip0 <= ~outFlip0;
            outCount <= 0;
         end
         else
            outCount <= outCount+1;
         if (inCount == 15) begin
            inFlip0 <= ~inFlip0;
         end
         if (next == 1) begin
            if (inCount >= 12)
               inFlip0 <= ~inFlip0;
            inCount <= 0;
         end
         else
            inCount <= inCount + 1;
      end
   end
    assign w_0_0 = {x0, inAddr0};
    assign w_0_1 = {x1, inAddr1};
    assign w_0_2 = {x2, inAddr2};
    assign w_0_3 = {x3, inAddr3};
    assign y0 = z_2_0;
    assign y1 = z_2_1;
    assign y2 = z_2_2;
    assign y3 = z_2_3;
    assign u_0_0 = outAddr_a0;
    assign u_0_1 = outAddr_a1;
    assign u_0_2 = outAddr_a2;
    assign u_0_3 = outAddr_a3;
    wire wr_ctrl_st_0;
    assign wr_ctrl_st_0 = inCount[3];

    switch #(logDepth+width) in_sw_0_0(.x0(w_0_0), .x1(w_0_2), .y0(w_1_0), .y1(w_1_2), .ctrl(wr_ctrl_st_0));
    switch #(logDepth+width) in_sw_0_1(.x0(w_0_1), .x1(w_0_3), .y0(w_1_1), .y1(w_1_3), .ctrl(wr_ctrl_st_0));
    reg [width+logDepth-1:0] w_1_0_pipe;
    reg [width+logDepth-1:0] w_1_1_pipe;
    reg [width+logDepth-1:0] w_1_2_pipe;
    reg [width+logDepth-1:0] w_1_3_pipe;

    always @(posedge clk) begin
        w_1_0_pipe <= w_1_0;
        w_1_1_pipe <= w_1_1;
        w_1_2_pipe <= w_1_2;
        w_1_3_pipe <= w_1_3;
    end

    wire wr_ctrl_st_1;
    reg wr_ctrl_st_1_1;
    always @(posedge clk) begin
        wr_ctrl_st_1_1 <= inCount[2];
    end
    assign wr_ctrl_st_1 = wr_ctrl_st_1_1;

    switch #(logDepth+width) in_sw_1_0(.x0(w_1_0_pipe), .x1(w_1_1_pipe), .y0(w_2_0), .y1(w_2_1), .ctrl(wr_ctrl_st_1));
    switch #(logDepth+width) in_sw_1_1(.x0(w_1_2_pipe), .x1(w_1_3_pipe), .y0(w_2_2), .y1(w_2_3), .ctrl(wr_ctrl_st_1));
    wire rdd_ctrl_st_0;
    assign rdd_ctrl_st_0 = outCount_for_rd_data[3];

    switch #(width) out_sw_0_0(.x0(z_0_0), .x1(z_0_2), .y0(z_1_0), .y1(z_1_2), .ctrl(rdd_ctrl_st_0));
    switch #(width) out_sw_0_1(.x0(z_0_1), .x1(z_0_3), .y0(z_1_1), .y1(z_1_3), .ctrl(rdd_ctrl_st_0));
    reg [width-1:0] z_1_0_pipe;
    reg [width-1:0] z_1_1_pipe;
    reg [width-1:0] z_1_2_pipe;
    reg [width-1:0] z_1_3_pipe;

    always @(posedge clk) begin
        z_1_0_pipe <= z_1_0;
        z_1_1_pipe <= z_1_1;
        z_1_2_pipe <= z_1_2;
        z_1_3_pipe <= z_1_3;
    end

    wire rdd_ctrl_st_1;
    reg rdd_ctrl_st_1_1;
    always @(posedge clk) begin
        rdd_ctrl_st_1_1 <= outCount_for_rd_data[2];

    end
    assign rdd_ctrl_st_1 = rdd_ctrl_st_1_1;

    switch #(width) out_sw_1_0(.x0(z_1_0_pipe), .x1(z_1_1_pipe), .y0(z_2_0), .y1(z_2_1), .ctrl(rdd_ctrl_st_1));
    switch #(width) out_sw_1_1(.x0(z_1_2_pipe), .x1(z_1_3_pipe), .y0(z_2_2), .y1(z_2_3), .ctrl(rdd_ctrl_st_1));
    wire rda_ctrl_st_0;
    assign rda_ctrl_st_0 = outCount_for_rd_addr[3];

    switch #(logDepth) rdaddr_sw_0_0(.x0(u_0_0), .x1(u_0_2), .y0(u_1_0), .y1(u_1_2), .ctrl(rda_ctrl_st_0));
    switch #(logDepth) rdaddr_sw_0_1(.x0(u_0_1), .x1(u_0_3), .y0(u_1_1), .y1(u_1_3), .ctrl(rda_ctrl_st_0));
    reg [logDepth-1:0] u_1_0_pipe;
    reg [logDepth-1:0] u_1_1_pipe;
    reg [logDepth-1:0] u_1_2_pipe;
    reg [logDepth-1:0] u_1_3_pipe;

    always @(posedge clk) begin
        u_1_0_pipe <= u_1_0;
        u_1_1_pipe <= u_1_1;
        u_1_2_pipe <= u_1_2;
        u_1_3_pipe <= u_1_3;
    end

    wire rda_ctrl_st_1;
    reg rda_ctrl_st_1_1;
    always @(posedge clk) begin
        rda_ctrl_st_1_1 <= outCount_for_rd_addr[2];

    end
    assign rda_ctrl_st_1 = rda_ctrl_st_1_1;

    switch #(logDepth) rdaddr_sw_1_0(.x0(u_1_0_pipe), .x1(u_1_1_pipe), .y0(u_2_0), .y1(u_2_1), .ctrl(rda_ctrl_st_1));
    switch #(logDepth) rdaddr_sw_1_1(.x0(u_1_2_pipe), .x1(u_1_3_pipe), .y0(u_2_2), .y1(u_2_3), .ctrl(rda_ctrl_st_1));
endmodule

module memArray64_79910(next, reset,
                x0, y0,
                inAddr0,
                outAddr0,
                x1, y1,
                inAddr1,
                outAddr1,
                x2, y2,
                inAddr2,
                outAddr2,
                x3, y3,
                inAddr3,
                outAddr3,
                clk, inFlip, outFlip);

   parameter numBanks = 4;
   parameter logBanks = 2;
   parameter depth = 16;
   parameter logDepth = 4;
   parameter width = 64;
         
   input     clk, next, reset;
   input    inFlip, outFlip;
   wire    next0;
   
   input [width-1:0]   x0;
   output [width-1:0]  y0;
   input [logDepth-1:0] inAddr0, outAddr0;
   input [width-1:0]   x1;
   output [width-1:0]  y1;
   input [logDepth-1:0] inAddr1, outAddr1;
   input [width-1:0]   x2;
   output [width-1:0]  y2;
   input [logDepth-1:0] inAddr2, outAddr2;
   input [width-1:0]   x3;
   output [width-1:0]  y3;
   input [logDepth-1:0] inAddr3, outAddr3;
   nextReg #(16, 4) nextReg_85724(.X(next), .Y(next0), .reset(reset), .clk(clk));


   memMod #(depth*2, width, logDepth+1) 
     memMod0(.in(x0), .out(y0), .inAddr({inFlip, inAddr0}),
	   .outAddr({outFlip, outAddr0}), .writeSel(1'b1), .clk(clk));   
   memMod #(depth*2, width, logDepth+1) 
     memMod1(.in(x1), .out(y1), .inAddr({inFlip, inAddr1}),
	   .outAddr({outFlip, outAddr1}), .writeSel(1'b1), .clk(clk));   
   memMod #(depth*2, width, logDepth+1) 
     memMod2(.in(x2), .out(y2), .inAddr({inFlip, inAddr2}),
	   .outAddr({outFlip, outAddr2}), .writeSel(1'b1), .clk(clk));   
   memMod #(depth*2, width, logDepth+1) 
     memMod3(.in(x3), .out(y3), .inAddr({inFlip, inAddr3}),
	   .outAddr({outFlip, outAddr3}), .writeSel(1'b1), .clk(clk));   
endmodule

// Latency: 12
// Gap: 16
module DirSum_80381(clk, reset, next, next_out,
      X0, Y0,
      X1, Y1,
      X2, Y2,
      X3, Y3,
      X4, Y4,
      X5, Y5,
      X6, Y6,
      X7, Y7);

   output next_out;
   input clk, reset, next;

   reg [3:0] i3;

   input [31:0] X0,
      X1,
      X2,
      X3,
      X4,
      X5,
      X6,
      X7;

   output [31:0] Y0,
      Y1,
      Y2,
      Y3,
      Y4,
      Y5,
      Y6,
      Y7;

   always @(posedge clk) begin
      if (reset == 1) begin
         i3 <= 0;
      end
      else begin
         if (next == 1)
            i3 <= 0;
         else if (i3 == 15)
            i3 <= 0;
         else
            i3 <= i3 + 1;
      end
   end

   codeBlock79915 codeBlockIsnt85729(.clk(clk), .reset(reset), .next_in(next), .next_out(next_out),
.i3_in(i3),
       .X0_in(X0), .Y0(Y0),
       .X1_in(X1), .Y1(Y1),
       .X2_in(X2), .Y2(Y2),
       .X3_in(X3), .Y3(Y3),
       .X4_in(X4), .Y4(Y4),
       .X5_in(X5), .Y5(Y5),
       .X6_in(X6), .Y6(Y6),
       .X7_in(X7), .Y7(Y7));

endmodule

module D30_80253(addr, out, clk);
   input clk;
   output [31:0] out;
   reg [31:0] out, out2, out3;
   input [3:0] addr;

   always @(posedge clk) begin
      out2 <= out3;
      out <= out2;
   case(addr)
      0: out3 <= 32'h0;
      1: out3 <= 32'hed6bf9d1;
      2: out3 <= 32'hdc71898d;
      3: out3 <= 32'hce86ff2a;
      4: out3 <= 32'hc4df2862;
      5: out3 <= 32'hc04ee4b8;
      6: out3 <= 32'hc13ad060;
      7: out3 <= 32'hc78e9a1d;
      8: out3 <= 32'hd2bec333;
      9: out3 <= 32'he1d4a2c8;
      10: out3 <= 32'hf383a3e2;
      11: out3 <= 32'h645e9af;
      12: out3 <= 32'h187de2a7;
      13: out3 <= 32'h2899e64a;
      14: out3 <= 32'h3536cc52;
      15: out3 <= 32'h3d3e82ae;
      default: out3 <= 0;
   endcase
   end
// synthesis attribute rom_style of out3 is "block"
endmodule



module D29_80271(addr, out, clk);
   input clk;
   output [31:0] out;
   reg [31:0] out, out2, out3;
   input [3:0] addr;

   always @(posedge clk) begin
      out2 <= out3;
      out <= out2;
   case(addr)
      0: out3 <= 32'h0;
      1: out3 <= 32'hf383a3e2;
      2: out3 <= 32'he7821d59;
      3: out3 <= 32'hdc71898d;
      4: out3 <= 32'hd2bec333;
      5: out3 <= 32'hcac933ae;
      6: out3 <= 32'hc4df2862;
      7: out3 <= 32'hc13ad060;
      8: out3 <= 32'hc0000000;
      9: out3 <= 32'hc13ad060;
      10: out3 <= 32'hc4df2862;
      11: out3 <= 32'hcac933ae;
      12: out3 <= 32'hd2bec333;
      13: out3 <= 32'hdc71898d;
      14: out3 <= 32'he7821d59;
      15: out3 <= 32'hf383a3e2;
      default: out3 <= 0;
   endcase
   end
// synthesis attribute rom_style of out3 is "block"
endmodule



module D28_80289(addr, out, clk);
   input clk;
   output [31:0] out;
   reg [31:0] out, out2, out3;
   input [3:0] addr;

   always @(posedge clk) begin
      out2 <= out3;
      out <= out2;
   case(addr)
      0: out3 <= 32'h0;
      1: out3 <= 32'hf9ba1651;
      2: out3 <= 32'hf383a3e2;
      3: out3 <= 32'hed6bf9d1;
      4: out3 <= 32'he7821d59;
      5: out3 <= 32'he1d4a2c8;
      6: out3 <= 32'hdc71898d;
      7: out3 <= 32'hd76619b6;
      8: out3 <= 32'hd2bec333;
      9: out3 <= 32'hce86ff2a;
      10: out3 <= 32'hcac933ae;
      11: out3 <= 32'hc78e9a1d;
      12: out3 <= 32'hc4df2862;
      13: out3 <= 32'hc2c17d52;
      14: out3 <= 32'hc13ad060;
      15: out3 <= 32'hc04ee4b8;
      default: out3 <= 0;
   endcase
   end
// synthesis attribute rom_style of out3 is "block"
endmodule



module D26_80325(addr, out, clk);
   input clk;
   output [31:0] out;
   reg [31:0] out, out2, out3;
   input [3:0] addr;

   always @(posedge clk) begin
      out2 <= out3;
      out <= out2;
   case(addr)
      0: out3 <= 32'h40000000;
      1: out3 <= 32'h3d3e82ae;
      2: out3 <= 32'h3536cc52;
      3: out3 <= 32'h2899e64a;
      4: out3 <= 32'h187de2a7;
      5: out3 <= 32'h645e9af;
      6: out3 <= 32'hf383a3e2;
      7: out3 <= 32'he1d4a2c8;
      8: out3 <= 32'hd2bec333;
      9: out3 <= 32'hc78e9a1d;
      10: out3 <= 32'hc13ad060;
      11: out3 <= 32'hc04ee4b8;
      12: out3 <= 32'hc4df2862;
      13: out3 <= 32'hce86ff2a;
      14: out3 <= 32'hdc71898d;
      15: out3 <= 32'hed6bf9d1;
      default: out3 <= 0;
   endcase
   end
// synthesis attribute rom_style of out3 is "block"
endmodule



module D25_80343(addr, out, clk);
   input clk;
   output [31:0] out;
   reg [31:0] out, out2, out3;
   input [3:0] addr;

   always @(posedge clk) begin
      out2 <= out3;
      out <= out2;
   case(addr)
      0: out3 <= 32'h40000000;
      1: out3 <= 32'h3ec52fa0;
      2: out3 <= 32'h3b20d79e;
      3: out3 <= 32'h3536cc52;
      4: out3 <= 32'h2d413ccd;
      5: out3 <= 32'h238e7673;
      6: out3 <= 32'h187de2a7;
      7: out3 <= 32'hc7c5c1e;
      8: out3 <= 32'h0;
      9: out3 <= 32'hf383a3e2;
      10: out3 <= 32'he7821d59;
      11: out3 <= 32'hdc71898d;
      12: out3 <= 32'hd2bec333;
      13: out3 <= 32'hcac933ae;
      14: out3 <= 32'hc4df2862;
      15: out3 <= 32'hc13ad060;
      default: out3 <= 0;
   endcase
   end
// synthesis attribute rom_style of out3 is "block"
endmodule



module D24_80361(addr, out, clk);
   input clk;
   output [31:0] out;
   reg [31:0] out, out2, out3;
   input [3:0] addr;

   always @(posedge clk) begin
      out2 <= out3;
      out <= out2;
   case(addr)
      0: out3 <= 32'h40000000;
      1: out3 <= 32'h3fb11b48;
      2: out3 <= 32'h3ec52fa0;
      3: out3 <= 32'h3d3e82ae;
      4: out3 <= 32'h3b20d79e;
      5: out3 <= 32'h387165e3;
      6: out3 <= 32'h3536cc52;
      7: out3 <= 32'h317900d6;
      8: out3 <= 32'h2d413ccd;
      9: out3 <= 32'h2899e64a;
      10: out3 <= 32'h238e7673;
      11: out3 <= 32'h1e2b5d38;
      12: out3 <= 32'h187de2a7;
      13: out3 <= 32'h1294062f;
      14: out3 <= 32'hc7c5c1e;
      15: out3 <= 32'h645e9af;
      default: out3 <= 0;
   endcase
   end
// synthesis attribute rom_style of out3 is "block"
endmodule



// Latency: 12
// Gap: 1
module codeBlock79915(clk, reset, next_in, next_out,
   i3_in,
   X0_in, Y0,
   X1_in, Y1,
   X2_in, Y2,
   X3_in, Y3,
   X4_in, Y4,
   X5_in, Y5,
   X6_in, Y6,
   X7_in, Y7);

   output next_out;
   input clk, reset, next_in;

   reg next;
   input [3:0] i3_in;
   reg [3:0] i3;

   input [31:0] X0_in,
      X1_in,
      X2_in,
      X3_in,
      X4_in,
      X5_in,
      X6_in,
      X7_in;

   reg   [31:0] X0,
      X1,
      X2,
      X3,
      X4,
      X5,
      X6,
      X7;

   output [31:0] Y0,
      Y1,
      Y2,
      Y3,
      Y4,
      Y5,
      Y6,
      Y7;

   shiftRegFIFO #(11, 1) shiftFIFO_85732(.X(next), .Y(next_out), .clk(clk));


   wire signed [31:0] a345;
   wire signed [31:0] a322;
   wire signed [31:0] a348;
   wire signed [31:0] a326;
   wire signed [31:0] a349;
   wire signed [31:0] a350;
   wire signed [31:0] a353;
   wire signed [31:0] a354;
   wire signed [31:0] a357;
   wire signed [31:0] a358;
   reg signed [31:0] tm222;
   reg signed [31:0] tm226;
   reg signed [31:0] tm238;
   reg signed [31:0] tm242;
   reg signed [31:0] tm254;
   reg signed [31:0] tm258;
   reg signed [31:0] tm270;
   reg signed [31:0] tm281;
   reg signed [31:0] tm223;
   reg signed [31:0] tm227;
   reg signed [31:0] tm239;
   reg signed [31:0] tm243;
   reg signed [31:0] tm255;
   reg signed [31:0] tm259;
   reg signed [31:0] tm271;
   reg signed [31:0] tm282;
   wire signed [31:0] tm10;
   wire signed [31:0] a327;
   wire signed [31:0] tm11;
   wire signed [31:0] a329;
   wire signed [31:0] tm12;
   wire signed [31:0] a333;
   wire signed [31:0] tm13;
   wire signed [31:0] a335;
   wire signed [31:0] tm14;
   wire signed [31:0] a339;
   wire signed [31:0] tm15;
   wire signed [31:0] a341;
   reg signed [31:0] tm224;
   reg signed [31:0] tm228;
   reg signed [31:0] tm240;
   reg signed [31:0] tm244;
   reg signed [31:0] tm256;
   reg signed [31:0] tm260;
   reg signed [31:0] tm272;
   reg signed [31:0] tm283;
   reg signed [31:0] tm52;
   reg signed [31:0] tm53;
   reg signed [31:0] tm56;
   reg signed [31:0] tm57;
   reg signed [31:0] tm60;
   reg signed [31:0] tm61;
   reg signed [31:0] tm225;
   reg signed [31:0] tm229;
   reg signed [31:0] tm241;
   reg signed [31:0] tm245;
   reg signed [31:0] tm257;
   reg signed [31:0] tm261;
   reg signed [31:0] tm273;
   reg signed [31:0] tm284;
   reg signed [31:0] tm274;
   reg signed [31:0] tm285;
   reg signed [31:0] tm275;
   reg signed [31:0] tm286;
   reg signed [31:0] tm276;
   reg signed [31:0] tm287;
   reg signed [31:0] tm277;
   reg signed [31:0] tm288;
   reg signed [31:0] tm278;
   reg signed [31:0] tm289;
   wire signed [31:0] a328;
   wire signed [31:0] a330;
   wire signed [31:0] a331;
   wire signed [31:0] a332;
   wire signed [31:0] a334;
   wire signed [31:0] a336;
   wire signed [31:0] a337;
   wire signed [31:0] a338;
   wire signed [31:0] a340;
   wire signed [31:0] a342;
   wire signed [31:0] a343;
   wire signed [31:0] a344;
   reg signed [31:0] tm279;
   reg signed [31:0] tm290;
   wire signed [31:0] Y0;
   wire signed [31:0] Y1;
   wire signed [31:0] Y2;
   wire signed [31:0] Y3;
   wire signed [31:0] Y4;
   wire signed [31:0] Y5;
   wire signed [31:0] Y6;
   wire signed [31:0] Y7;
   reg signed [31:0] tm280;
   reg signed [31:0] tm291;


   assign a345 = X0;
   assign a322 = a345;
   assign a348 = X1;
   assign a326 = a348;
   assign a349 = X2;
   assign a350 = X3;
   assign a353 = X4;
   assign a354 = X5;
   assign a357 = X6;
   assign a358 = X7;
   assign a327 = tm10;
   assign a329 = tm11;
   assign a333 = tm12;
   assign a335 = tm13;
   assign a339 = tm14;
   assign a341 = tm15;
   assign Y0 = tm280;
   assign Y1 = tm291;

   D30_80253 instD30inst0_80253(.addr(i3[3:0]), .out(tm15), .clk(clk));

   D29_80271 instD29inst0_80271(.addr(i3[3:0]), .out(tm13), .clk(clk));

   D28_80289 instD28inst0_80289(.addr(i3[3:0]), .out(tm11), .clk(clk));

   D26_80325 instD26inst0_80325(.addr(i3[3:0]), .out(tm14), .clk(clk));

   D25_80343 instD25inst0_80343(.addr(i3[3:0]), .out(tm12), .clk(clk));

   D24_80361 instD24inst0_80361(.addr(i3[3:0]), .out(tm10), .clk(clk));

    multfix #(32, 6) m80014(.a(tm52), .b(tm225), .clk(clk), .q_sc(a328), .q_unsc(), .rst(reset));
    multfix #(32, 6) m80036(.a(tm53), .b(tm229), .clk(clk), .q_sc(a330), .q_unsc(), .rst(reset));
    multfix #(32, 6) m80054(.a(tm53), .b(tm225), .clk(clk), .q_sc(a331), .q_unsc(), .rst(reset));
    multfix #(32, 6) m80065(.a(tm52), .b(tm229), .clk(clk), .q_sc(a332), .q_unsc(), .rst(reset));
    multfix #(32, 6) m80094(.a(tm56), .b(tm241), .clk(clk), .q_sc(a334), .q_unsc(), .rst(reset));
    multfix #(32, 6) m80116(.a(tm57), .b(tm245), .clk(clk), .q_sc(a336), .q_unsc(), .rst(reset));
    multfix #(32, 6) m80134(.a(tm57), .b(tm241), .clk(clk), .q_sc(a337), .q_unsc(), .rst(reset));
    multfix #(32, 6) m80145(.a(tm56), .b(tm245), .clk(clk), .q_sc(a338), .q_unsc(), .rst(reset));
    multfix #(32, 6) m80174(.a(tm60), .b(tm257), .clk(clk), .q_sc(a340), .q_unsc(), .rst(reset));
    multfix #(32, 6) m80196(.a(tm61), .b(tm261), .clk(clk), .q_sc(a342), .q_unsc(), .rst(reset));
    multfix #(32, 6) m80214(.a(tm61), .b(tm257), .clk(clk), .q_sc(a343), .q_unsc(), .rst(reset));
    multfix #(32, 6) m80225(.a(tm60), .b(tm261), .clk(clk), .q_sc(a344), .q_unsc(), .rst(reset));
    subfxp #(32, 1) sub80043(.a(a328), .b(a330), .clk(clk), .q(Y2));    // 10
    addfxp #(32, 1) add80072(.a(a331), .b(a332), .clk(clk), .q(Y3));    // 10
    subfxp #(32, 1) sub80123(.a(a334), .b(a336), .clk(clk), .q(Y4));    // 10
    addfxp #(32, 1) add80152(.a(a337), .b(a338), .clk(clk), .q(Y5));    // 10
    subfxp #(32, 1) sub80203(.a(a340), .b(a342), .clk(clk), .q(Y6));    // 10
    addfxp #(32, 1) add80232(.a(a343), .b(a344), .clk(clk), .q(Y7));    // 10


   always @(posedge clk) begin
      if (reset == 1) begin
         tm52 <= 0;
         tm225 <= 0;
         tm53 <= 0;
         tm229 <= 0;
         tm53 <= 0;
         tm225 <= 0;
         tm52 <= 0;
         tm229 <= 0;
         tm56 <= 0;
         tm241 <= 0;
         tm57 <= 0;
         tm245 <= 0;
         tm57 <= 0;
         tm241 <= 0;
         tm56 <= 0;
         tm245 <= 0;
         tm60 <= 0;
         tm257 <= 0;
         tm61 <= 0;
         tm261 <= 0;
         tm61 <= 0;
         tm257 <= 0;
         tm60 <= 0;
         tm261 <= 0;
      end
      else begin
         i3 <= i3_in;
         X0 <= X0_in;
         X1 <= X1_in;
         X2 <= X2_in;
         X3 <= X3_in;
         X4 <= X4_in;
         X5 <= X5_in;
         X6 <= X6_in;
         X7 <= X7_in;
         next <= next_in;
         tm222 <= a349;
         tm226 <= a350;
         tm238 <= a353;
         tm242 <= a354;
         tm254 <= a357;
         tm258 <= a358;
         tm270 <= a322;
         tm281 <= a326;
         tm223 <= tm222;
         tm227 <= tm226;
         tm239 <= tm238;
         tm243 <= tm242;
         tm255 <= tm254;
         tm259 <= tm258;
         tm271 <= tm270;
         tm282 <= tm281;
         tm224 <= tm223;
         tm228 <= tm227;
         tm240 <= tm239;
         tm244 <= tm243;
         tm256 <= tm255;
         tm260 <= tm259;
         tm272 <= tm271;
         tm283 <= tm282;
         tm52 <= a327;
         tm53 <= a329;
         tm56 <= a333;
         tm57 <= a335;
         tm60 <= a339;
         tm61 <= a341;
         tm225 <= tm224;
         tm229 <= tm228;
         tm241 <= tm240;
         tm245 <= tm244;
         tm257 <= tm256;
         tm261 <= tm260;
         tm273 <= tm272;
         tm284 <= tm283;
         tm274 <= tm273;
         tm285 <= tm284;
         tm275 <= tm274;
         tm286 <= tm285;
         tm276 <= tm275;
         tm287 <= tm286;
         tm277 <= tm276;
         tm288 <= tm287;
         tm278 <= tm277;
         tm289 <= tm288;
         tm279 <= tm278;
         tm290 <= tm289;
         tm280 <= tm279;
         tm291 <= tm290;
      end
   end
endmodule

// Latency: 3
// Gap: 1
module codeBlock80384(clk, reset, next_in, next_out,
   X0_in, Y0,
   X1_in, Y1,
   X2_in, Y2,
   X3_in, Y3,
   X4_in, Y4,
   X5_in, Y5,
   X6_in, Y6,
   X7_in, Y7);

   output next_out;
   input clk, reset, next_in;

   reg next;

   input [31:0] X0_in,
      X1_in,
      X2_in,
      X3_in,
      X4_in,
      X5_in,
      X6_in,
      X7_in;

   reg   [31:0] X0,
      X1,
      X2,
      X3,
      X4,
      X5,
      X6,
      X7;

   output [31:0] Y0,
      Y1,
      Y2,
      Y3,
      Y4,
      Y5,
      Y6,
      Y7;

   shiftRegFIFO #(2, 1) shiftFIFO_85735(.X(next), .Y(next_out), .clk(clk));


   wire signed [31:0] a257;
   wire signed [31:0] a258;
   wire signed [31:0] a259;
   wire signed [31:0] a260;
   wire signed [31:0] a265;
   wire signed [31:0] a266;
   wire signed [31:0] a267;
   wire signed [31:0] a268;
   wire signed [31:0] t369;
   wire signed [31:0] t370;
   wire signed [31:0] t371;
   wire signed [31:0] t372;
   wire signed [31:0] t373;
   wire signed [31:0] t374;
   wire signed [31:0] t375;
   wire signed [31:0] t376;
   wire signed [31:0] t377;
   wire signed [31:0] t378;
   wire signed [31:0] t379;
   wire signed [31:0] t380;
   wire signed [31:0] Y0;
   wire signed [31:0] Y1;
   wire signed [31:0] Y4;
   wire signed [31:0] Y5;
   wire signed [31:0] t381;
   wire signed [31:0] t382;
   wire signed [31:0] t383;
   wire signed [31:0] t384;
   wire signed [31:0] Y2;
   wire signed [31:0] Y3;
   wire signed [31:0] Y6;
   wire signed [31:0] Y7;


   assign a257 = X0;
   assign a258 = X4;
   assign a259 = X1;
   assign a260 = X5;
   assign a265 = X2;
   assign a266 = X6;
   assign a267 = X3;
   assign a268 = X7;
   assign Y0 = t377;
   assign Y1 = t378;
   assign Y4 = t379;
   assign Y5 = t380;
   assign Y2 = t381;
   assign Y3 = t382;
   assign Y6 = t383;
   assign Y7 = t384;

    addfxp #(32, 1) add80396(.a(a257), .b(a258), .clk(clk), .q(t369));    // 0
    addfxp #(32, 1) add80411(.a(a259), .b(a260), .clk(clk), .q(t370));    // 0
    subfxp #(32, 1) sub80426(.a(a257), .b(a258), .clk(clk), .q(t371));    // 0
    subfxp #(32, 1) sub80441(.a(a259), .b(a260), .clk(clk), .q(t372));    // 0
    addfxp #(32, 1) add80456(.a(a265), .b(a266), .clk(clk), .q(t373));    // 0
    addfxp #(32, 1) add80471(.a(a267), .b(a268), .clk(clk), .q(t374));    // 0
    subfxp #(32, 1) sub80486(.a(a265), .b(a266), .clk(clk), .q(t375));    // 0
    subfxp #(32, 1) sub80501(.a(a267), .b(a268), .clk(clk), .q(t376));    // 0
    addfxp #(32, 1) add80508(.a(t369), .b(t373), .clk(clk), .q(t377));    // 1
    addfxp #(32, 1) add80515(.a(t370), .b(t374), .clk(clk), .q(t378));    // 1
    subfxp #(32, 1) sub80522(.a(t369), .b(t373), .clk(clk), .q(t379));    // 1
    subfxp #(32, 1) sub80529(.a(t370), .b(t374), .clk(clk), .q(t380));    // 1
    addfxp #(32, 1) add80552(.a(t371), .b(t376), .clk(clk), .q(t381));    // 1
    subfxp #(32, 1) sub80559(.a(t372), .b(t375), .clk(clk), .q(t382));    // 1
    subfxp #(32, 1) sub80566(.a(t371), .b(t376), .clk(clk), .q(t383));    // 1
    addfxp #(32, 1) add80573(.a(t372), .b(t375), .clk(clk), .q(t384));    // 1


   always @(posedge clk) begin
      if (reset == 1) begin
      end
      else begin
         X0 <= X0_in;
         X1 <= X1_in;
         X2 <= X2_in;
         X3 <= X3_in;
         X4 <= X4_in;
         X5 <= X5_in;
         X6 <= X6_in;
         X7 <= X7_in;
         next <= next_in;
      end
   end
endmodule

// Latency: 53
// Gap: 64
module rc80597(clk, reset, next, next_out,
   X0, Y0,
   X1, Y1,
   X2, Y2,
   X3, Y3,
   X4, Y4,
   X5, Y5,
   X6, Y6,
   X7, Y7);

   output next_out;
   input clk, reset, next;

   input [31:0] X0,
      X1,
      X2,
      X3,
      X4,
      X5,
      X6,
      X7;

   output [31:0] Y0,
      Y1,
      Y2,
      Y3,
      Y4,
      Y5,
      Y6,
      Y7;

   wire [63:0] t0;
   wire [63:0] s0;
   assign t0 = {X0, X1};
   wire [63:0] t1;
   wire [63:0] s1;
   assign t1 = {X2, X3};
   wire [63:0] t2;
   wire [63:0] s2;
   assign t2 = {X4, X5};
   wire [63:0] t3;
   wire [63:0] s3;
   assign t3 = {X6, X7};
   assign Y0 = s0[63:32];
   assign Y1 = s0[31:0];
   assign Y2 = s1[63:32];
   assign Y3 = s1[31:0];
   assign Y4 = s2[63:32];
   assign Y5 = s2[31:0];
   assign Y6 = s3[63:32];
   assign Y7 = s3[31:0];

   perm80595 instPerm85736(.x0(t0), .y0(s0),
    .x1(t1), .y1(s1),
    .x2(t2), .y2(s2),
    .x3(t3), .y3(s3),
   .clk(clk), .next(next), .next_out(next_out), .reset(reset)
);



endmodule

// Latency: 53
// Gap: 64
module perm80595(clk, next, reset, next_out,
   x0, y0,
   x1, y1,
   x2, y2,
   x3, y3);
   parameter numBanks = 4;
   parameter logBanks = 2;
   parameter depth = 64;
   parameter logDepth = 6;
   parameter width = 64;

   input [width-1:0]  x0;
   output [width-1:0]  y0;
   wire [width-1:0]  ybuff0;
   input [width-1:0]  x1;
   output [width-1:0]  y1;
   wire [width-1:0]  ybuff1;
   input [width-1:0]  x2;
   output [width-1:0]  y2;
   wire [width-1:0]  ybuff2;
   input [width-1:0]  x3;
   output [width-1:0]  y3;
   wire [width-1:0]  ybuff3;
   input 	      clk, next, reset;
   output 	     next_out;

   wire    	     next0;

   reg              inFlip0, outFlip0;
   reg              inActive, outActive;

   wire [logBanks-1:0] inBank0, outBank0;
   wire [logDepth-1:0] inAddr0, outAddr0;
   wire [logBanks-1:0] outBank_a0;
   wire [logDepth-1:0] outAddr_a0;
   wire [logDepth+logBanks-1:0] addr0, addr0b, addr0c;
   wire [logBanks-1:0] inBank1, outBank1;
   wire [logDepth-1:0] inAddr1, outAddr1;
   wire [logBanks-1:0] outBank_a1;
   wire [logDepth-1:0] outAddr_a1;
   wire [logDepth+logBanks-1:0] addr1, addr1b, addr1c;
   wire [logBanks-1:0] inBank2, outBank2;
   wire [logDepth-1:0] inAddr2, outAddr2;
   wire [logBanks-1:0] outBank_a2;
   wire [logDepth-1:0] outAddr_a2;
   wire [logDepth+logBanks-1:0] addr2, addr2b, addr2c;
   wire [logBanks-1:0] inBank3, outBank3;
   wire [logDepth-1:0] inAddr3, outAddr3;
   wire [logBanks-1:0] outBank_a3;
   wire [logDepth-1:0] outAddr_a3;
   wire [logDepth+logBanks-1:0] addr3, addr3b, addr3c;


   reg [logDepth-1:0]  inCount, outCount, outCount_d, outCount_dd, outCount_for_rd_addr, outCount_for_rd_data;  

   assign    addr0 = {inCount, 2'd0};
   assign    addr0b = {outCount, 2'd0};
   assign    addr0c = {outCount_for_rd_addr, 2'd0};
   assign    addr1 = {inCount, 2'd1};
   assign    addr1b = {outCount, 2'd1};
   assign    addr1c = {outCount_for_rd_addr, 2'd1};
   assign    addr2 = {inCount, 2'd2};
   assign    addr2b = {outCount, 2'd2};
   assign    addr2c = {outCount_for_rd_addr, 2'd2};
   assign    addr3 = {inCount, 2'd3};
   assign    addr3b = {outCount, 2'd3};
   assign    addr3c = {outCount_for_rd_addr, 2'd3};
    wire [width+logDepth-1:0] w_0_0, w_0_1, w_0_2, w_0_3, w_1_0, w_1_1, w_1_2, w_1_3, w_2_0, w_2_1, w_2_2, w_2_3;

    reg [width-1:0] z_0_0;
    reg [width-1:0] z_0_1;
    reg [width-1:0] z_0_2;
    reg [width-1:0] z_0_3;
    wire [width-1:0] z_1_0, z_1_1, z_1_2, z_1_3, z_2_0, z_2_1, z_2_2, z_2_3;

    wire [logDepth-1:0] u_0_0, u_0_1, u_0_2, u_0_3, u_1_0, u_1_1, u_1_2, u_1_3, u_2_0, u_2_1, u_2_2, u_2_3;

    reg inFlip1, outFlip1;
    always @(posedge clk) begin
        inFlip1 <= inFlip0;
        outFlip1 <= outFlip0;
    end

   assign inBank0[0] = addr0[6] ^ addr0[0];
   assign inBank0[1] = addr0[7] ^ addr0[1];
   assign inAddr0[0] = addr0[2];
   assign inAddr0[1] = addr0[3];
   assign inAddr0[2] = addr0[4];
   assign inAddr0[3] = addr0[5];
   assign inAddr0[4] = addr0[0];
   assign inAddr0[5] = addr0[1];
   assign outBank0[0] = addr0b[6] ^ addr0b[0];
   assign outBank0[1] = addr0b[7] ^ addr0b[1];
   assign outAddr0[0] = addr0b[2];
   assign outAddr0[1] = addr0b[3];
   assign outAddr0[2] = addr0b[4];
   assign outAddr0[3] = addr0b[5];
   assign outAddr0[4] = addr0b[6];
   assign outAddr0[5] = addr0b[7];
   assign outBank_a0[0] = addr0c[6] ^ addr0c[0];
   assign outBank_a0[1] = addr0c[7] ^ addr0c[1];
   assign outAddr_a0[0] = addr0c[2];
   assign outAddr_a0[1] = addr0c[3];
   assign outAddr_a0[2] = addr0c[4];
   assign outAddr_a0[3] = addr0c[5];
   assign outAddr_a0[4] = addr0c[6];
   assign outAddr_a0[5] = addr0c[7];

   assign inBank1[0] = addr1[6] ^ addr1[0];
   assign inBank1[1] = addr1[7] ^ addr1[1];
   assign inAddr1[0] = addr1[2];
   assign inAddr1[1] = addr1[3];
   assign inAddr1[2] = addr1[4];
   assign inAddr1[3] = addr1[5];
   assign inAddr1[4] = addr1[0];
   assign inAddr1[5] = addr1[1];
   assign outBank1[0] = addr1b[6] ^ addr1b[0];
   assign outBank1[1] = addr1b[7] ^ addr1b[1];
   assign outAddr1[0] = addr1b[2];
   assign outAddr1[1] = addr1b[3];
   assign outAddr1[2] = addr1b[4];
   assign outAddr1[3] = addr1b[5];
   assign outAddr1[4] = addr1b[6];
   assign outAddr1[5] = addr1b[7];
   assign outBank_a1[0] = addr1c[6] ^ addr1c[0];
   assign outBank_a1[1] = addr1c[7] ^ addr1c[1];
   assign outAddr_a1[0] = addr1c[2];
   assign outAddr_a1[1] = addr1c[3];
   assign outAddr_a1[2] = addr1c[4];
   assign outAddr_a1[3] = addr1c[5];
   assign outAddr_a1[4] = addr1c[6];
   assign outAddr_a1[5] = addr1c[7];

   assign inBank2[0] = addr2[6] ^ addr2[0];
   assign inBank2[1] = addr2[7] ^ addr2[1];
   assign inAddr2[0] = addr2[2];
   assign inAddr2[1] = addr2[3];
   assign inAddr2[2] = addr2[4];
   assign inAddr2[3] = addr2[5];
   assign inAddr2[4] = addr2[0];
   assign inAddr2[5] = addr2[1];
   assign outBank2[0] = addr2b[6] ^ addr2b[0];
   assign outBank2[1] = addr2b[7] ^ addr2b[1];
   assign outAddr2[0] = addr2b[2];
   assign outAddr2[1] = addr2b[3];
   assign outAddr2[2] = addr2b[4];
   assign outAddr2[3] = addr2b[5];
   assign outAddr2[4] = addr2b[6];
   assign outAddr2[5] = addr2b[7];
   assign outBank_a2[0] = addr2c[6] ^ addr2c[0];
   assign outBank_a2[1] = addr2c[7] ^ addr2c[1];
   assign outAddr_a2[0] = addr2c[2];
   assign outAddr_a2[1] = addr2c[3];
   assign outAddr_a2[2] = addr2c[4];
   assign outAddr_a2[3] = addr2c[5];
   assign outAddr_a2[4] = addr2c[6];
   assign outAddr_a2[5] = addr2c[7];

   assign inBank3[0] = addr3[6] ^ addr3[0];
   assign inBank3[1] = addr3[7] ^ addr3[1];
   assign inAddr3[0] = addr3[2];
   assign inAddr3[1] = addr3[3];
   assign inAddr3[2] = addr3[4];
   assign inAddr3[3] = addr3[5];
   assign inAddr3[4] = addr3[0];
   assign inAddr3[5] = addr3[1];
   assign outBank3[0] = addr3b[6] ^ addr3b[0];
   assign outBank3[1] = addr3b[7] ^ addr3b[1];
   assign outAddr3[0] = addr3b[2];
   assign outAddr3[1] = addr3b[3];
   assign outAddr3[2] = addr3b[4];
   assign outAddr3[3] = addr3b[5];
   assign outAddr3[4] = addr3b[6];
   assign outAddr3[5] = addr3b[7];
   assign outBank_a3[0] = addr3c[6] ^ addr3c[0];
   assign outBank_a3[1] = addr3c[7] ^ addr3c[1];
   assign outAddr_a3[0] = addr3c[2];
   assign outAddr_a3[1] = addr3c[3];
   assign outAddr_a3[2] = addr3c[4];
   assign outAddr_a3[3] = addr3c[5];
   assign outAddr_a3[4] = addr3c[6];
   assign outAddr_a3[5] = addr3c[7];

   nextReg #(49, 6) nextReg_85741(.X(next), .Y(next0), .reset(reset), .clk(clk));


   shiftRegFIFO #(4, 1) shiftFIFO_85744(.X(next0), .Y(next_out), .clk(clk));


   memArray256_80595 #(numBanks, logBanks, depth, logDepth, width)
     memSys(.inFlip(inFlip1), .outFlip(outFlip1), .next(next), .reset(reset),
        .x0(w_2_0[width+logDepth-1:logDepth]), .y0(ybuff0),
        .inAddr0(w_2_0[logDepth-1:0]),
        .outAddr0(u_2_0), 
        .x1(w_2_1[width+logDepth-1:logDepth]), .y1(ybuff1),
        .inAddr1(w_2_1[logDepth-1:0]),
        .outAddr1(u_2_1), 
        .x2(w_2_2[width+logDepth-1:logDepth]), .y2(ybuff2),
        .inAddr2(w_2_2[logDepth-1:0]),
        .outAddr2(u_2_2), 
        .x3(w_2_3[width+logDepth-1:logDepth]), .y3(ybuff3),
        .inAddr3(w_2_3[logDepth-1:0]),
        .outAddr3(u_2_3), 
        .clk(clk));

   always @(posedge clk) begin
      if (reset == 1) begin
      z_0_0 <= 0;
      z_0_1 <= 0;
      z_0_2 <= 0;
      z_0_3 <= 0;
         inFlip0 <= 0; outFlip0 <= 1; outCount <= 0; inCount <= 0;
        outCount_for_rd_addr <= 0;
        outCount_for_rd_data <= 0;
      end
      else begin
          outCount_d <= outCount;
          outCount_dd <= outCount_d;
         if (inCount == 48)
            outCount_for_rd_addr <= 0;
         else
            outCount_for_rd_addr <= outCount_for_rd_addr+1;
         if (inCount == 51)
            outCount_for_rd_data <= 0;
         else
            outCount_for_rd_data <= outCount_for_rd_data+1;
      z_0_0 <= ybuff0;
      z_0_1 <= ybuff1;
      z_0_2 <= ybuff2;
      z_0_3 <= ybuff3;
         if (inCount == 48) begin
            outFlip0 <= ~outFlip0;
            outCount <= 0;
         end
         else
            outCount <= outCount+1;
         if (inCount == 63) begin
            inFlip0 <= ~inFlip0;
         end
         if (next == 1) begin
            if (inCount >= 48)
               inFlip0 <= ~inFlip0;
            inCount <= 0;
         end
         else
            inCount <= inCount + 1;
      end
   end
    assign w_0_0 = {x0, inAddr0};
    assign w_0_1 = {x1, inAddr1};
    assign w_0_2 = {x2, inAddr2};
    assign w_0_3 = {x3, inAddr3};
    assign y0 = z_2_0;
    assign y1 = z_2_1;
    assign y2 = z_2_2;
    assign y3 = z_2_3;
    assign u_0_0 = outAddr_a0;
    assign u_0_1 = outAddr_a1;
    assign u_0_2 = outAddr_a2;
    assign u_0_3 = outAddr_a3;
    wire wr_ctrl_st_0;
    assign wr_ctrl_st_0 = inCount[5];

    switch #(logDepth+width) in_sw_0_0(.x0(w_0_0), .x1(w_0_2), .y0(w_1_0), .y1(w_1_2), .ctrl(wr_ctrl_st_0));
    switch #(logDepth+width) in_sw_0_1(.x0(w_0_1), .x1(w_0_3), .y0(w_1_1), .y1(w_1_3), .ctrl(wr_ctrl_st_0));
    reg [width+logDepth-1:0] w_1_0_pipe;
    reg [width+logDepth-1:0] w_1_1_pipe;
    reg [width+logDepth-1:0] w_1_2_pipe;
    reg [width+logDepth-1:0] w_1_3_pipe;

    always @(posedge clk) begin
        w_1_0_pipe <= w_1_0;
        w_1_1_pipe <= w_1_1;
        w_1_2_pipe <= w_1_2;
        w_1_3_pipe <= w_1_3;
    end

    wire wr_ctrl_st_1;
    reg wr_ctrl_st_1_1;
    always @(posedge clk) begin
        wr_ctrl_st_1_1 <= inCount[4];
    end
    assign wr_ctrl_st_1 = wr_ctrl_st_1_1;

    switch #(logDepth+width) in_sw_1_0(.x0(w_1_0_pipe), .x1(w_1_1_pipe), .y0(w_2_0), .y1(w_2_1), .ctrl(wr_ctrl_st_1));
    switch #(logDepth+width) in_sw_1_1(.x0(w_1_2_pipe), .x1(w_1_3_pipe), .y0(w_2_2), .y1(w_2_3), .ctrl(wr_ctrl_st_1));
    wire rdd_ctrl_st_0;
    assign rdd_ctrl_st_0 = outCount_for_rd_data[5];

    switch #(width) out_sw_0_0(.x0(z_0_0), .x1(z_0_2), .y0(z_1_0), .y1(z_1_2), .ctrl(rdd_ctrl_st_0));
    switch #(width) out_sw_0_1(.x0(z_0_1), .x1(z_0_3), .y0(z_1_1), .y1(z_1_3), .ctrl(rdd_ctrl_st_0));
    reg [width-1:0] z_1_0_pipe;
    reg [width-1:0] z_1_1_pipe;
    reg [width-1:0] z_1_2_pipe;
    reg [width-1:0] z_1_3_pipe;

    always @(posedge clk) begin
        z_1_0_pipe <= z_1_0;
        z_1_1_pipe <= z_1_1;
        z_1_2_pipe <= z_1_2;
        z_1_3_pipe <= z_1_3;
    end

    wire rdd_ctrl_st_1;
    reg rdd_ctrl_st_1_1;
    always @(posedge clk) begin
        rdd_ctrl_st_1_1 <= outCount_for_rd_data[4];

    end
    assign rdd_ctrl_st_1 = rdd_ctrl_st_1_1;

    switch #(width) out_sw_1_0(.x0(z_1_0_pipe), .x1(z_1_1_pipe), .y0(z_2_0), .y1(z_2_1), .ctrl(rdd_ctrl_st_1));
    switch #(width) out_sw_1_1(.x0(z_1_2_pipe), .x1(z_1_3_pipe), .y0(z_2_2), .y1(z_2_3), .ctrl(rdd_ctrl_st_1));
    wire rda_ctrl_st_0;
    assign rda_ctrl_st_0 = outCount_for_rd_addr[5];

    switch #(logDepth) rdaddr_sw_0_0(.x0(u_0_0), .x1(u_0_2), .y0(u_1_0), .y1(u_1_2), .ctrl(rda_ctrl_st_0));
    switch #(logDepth) rdaddr_sw_0_1(.x0(u_0_1), .x1(u_0_3), .y0(u_1_1), .y1(u_1_3), .ctrl(rda_ctrl_st_0));
    reg [logDepth-1:0] u_1_0_pipe;
    reg [logDepth-1:0] u_1_1_pipe;
    reg [logDepth-1:0] u_1_2_pipe;
    reg [logDepth-1:0] u_1_3_pipe;

    always @(posedge clk) begin
        u_1_0_pipe <= u_1_0;
        u_1_1_pipe <= u_1_1;
        u_1_2_pipe <= u_1_2;
        u_1_3_pipe <= u_1_3;
    end

    wire rda_ctrl_st_1;
    reg rda_ctrl_st_1_1;
    always @(posedge clk) begin
        rda_ctrl_st_1_1 <= outCount_for_rd_addr[4];

    end
    assign rda_ctrl_st_1 = rda_ctrl_st_1_1;

    switch #(logDepth) rdaddr_sw_1_0(.x0(u_1_0_pipe), .x1(u_1_1_pipe), .y0(u_2_0), .y1(u_2_1), .ctrl(rda_ctrl_st_1));
    switch #(logDepth) rdaddr_sw_1_1(.x0(u_1_2_pipe), .x1(u_1_3_pipe), .y0(u_2_2), .y1(u_2_3), .ctrl(rda_ctrl_st_1));
endmodule

module memArray256_80595(next, reset,
                x0, y0,
                inAddr0,
                outAddr0,
                x1, y1,
                inAddr1,
                outAddr1,
                x2, y2,
                inAddr2,
                outAddr2,
                x3, y3,
                inAddr3,
                outAddr3,
                clk, inFlip, outFlip);

   parameter numBanks = 4;
   parameter logBanks = 2;
   parameter depth = 64;
   parameter logDepth = 6;
   parameter width = 64;
         
   input     clk, next, reset;
   input    inFlip, outFlip;
   wire    next0;
   
   input [width-1:0]   x0;
   output [width-1:0]  y0;
   input [logDepth-1:0] inAddr0, outAddr0;
   input [width-1:0]   x1;
   output [width-1:0]  y1;
   input [logDepth-1:0] inAddr1, outAddr1;
   input [width-1:0]   x2;
   output [width-1:0]  y2;
   input [logDepth-1:0] inAddr2, outAddr2;
   input [width-1:0]   x3;
   output [width-1:0]  y3;
   input [logDepth-1:0] inAddr3, outAddr3;
   nextReg #(64, 6) nextReg_85749(.X(next), .Y(next0), .reset(reset), .clk(clk));


   memMod #(depth*2, width, logDepth+1) 
     memMod0(.in(x0), .out(y0), .inAddr({inFlip, inAddr0}),
	   .outAddr({outFlip, outAddr0}), .writeSel(1'b1), .clk(clk));   
   memMod #(depth*2, width, logDepth+1) 
     memMod1(.in(x1), .out(y1), .inAddr({inFlip, inAddr1}),
	   .outAddr({outFlip, outAddr1}), .writeSel(1'b1), .clk(clk));   
   memMod #(depth*2, width, logDepth+1) 
     memMod2(.in(x2), .out(y2), .inAddr({inFlip, inAddr2}),
	   .outAddr({outFlip, outAddr2}), .writeSel(1'b1), .clk(clk));   
   memMod #(depth*2, width, logDepth+1) 
     memMod3(.in(x3), .out(y3), .inAddr({inFlip, inAddr3}),
	   .outAddr({outFlip, outAddr3}), .writeSel(1'b1), .clk(clk));   
endmodule

// Latency: 12
// Gap: 64
module DirSum_81450(clk, reset, next, next_out,
      X0, Y0,
      X1, Y1,
      X2, Y2,
      X3, Y3,
      X4, Y4,
      X5, Y5,
      X6, Y6,
      X7, Y7);

   output next_out;
   input clk, reset, next;

   reg [5:0] i2;

   input [31:0] X0,
      X1,
      X2,
      X3,
      X4,
      X5,
      X6,
      X7;

   output [31:0] Y0,
      Y1,
      Y2,
      Y3,
      Y4,
      Y5,
      Y6,
      Y7;

   always @(posedge clk) begin
      if (reset == 1) begin
         i2 <= 0;
      end
      else begin
         if (next == 1)
            i2 <= 0;
         else if (i2 == 63)
            i2 <= 0;
         else
            i2 <= i2 + 1;
      end
   end

   codeBlock80600 codeBlockIsnt85754(.clk(clk), .reset(reset), .next_in(next), .next_out(next_out),
.i2_in(i2),
       .X0_in(X0), .Y0(Y0),
       .X1_in(X1), .Y1(Y1),
       .X2_in(X2), .Y2(Y2),
       .X3_in(X3), .Y3(Y3),
       .X4_in(X4), .Y4(Y4),
       .X5_in(X5), .Y5(Y5),
       .X6_in(X6), .Y6(Y6),
       .X7_in(X7), .Y7(Y7));

endmodule

module D20_80986(addr, out, clk);
   input clk;
   output [31:0] out;
   reg [31:0] out, out2, out3;
   input [5:0] addr;

   always @(posedge clk) begin
      out2 <= out3;
      out <= out2;
   case(addr)
      0: out3 <= 32'h0;
      1: out3 <= 32'hfb4ab7db;
      2: out3 <= 32'hf69bf7c9;
      3: out3 <= 32'hf1fa3ecb;
      4: out3 <= 32'hed6bf9d1;
      5: out3 <= 32'he8f77acf;
      6: out3 <= 32'he4a2eff6;
      7: out3 <= 32'he0745b24;
      8: out3 <= 32'hdc71898d;
      9: out3 <= 32'hd8a00bae;
      10: out3 <= 32'hd5052d97;
      11: out3 <= 32'hd1a5ef90;
      12: out3 <= 32'hce86ff2a;
      13: out3 <= 32'hcbacb0bf;
      14: out3 <= 32'hc91af976;
      15: out3 <= 32'hc6d569be;
      16: out3 <= 32'hc4df2862;
      17: out3 <= 32'hc33aee27;
      18: out3 <= 32'hc1eb0209;
      19: out3 <= 32'hc0f1360b;
      20: out3 <= 32'hc04ee4b8;
      21: out3 <= 32'hc004ef3f;
      22: out3 <= 32'hc013bc39;
      23: out3 <= 32'hc07b371e;
      24: out3 <= 32'hc13ad060;
      25: out3 <= 32'hc2517e31;
      26: out3 <= 32'hc3bdbdf6;
      27: out3 <= 32'hc57d965d;
      28: out3 <= 32'hc78e9a1d;
      29: out3 <= 32'hc9edeb50;
      30: out3 <= 32'hcc983f70;
      31: out3 <= 32'hcf89e3e8;
      32: out3 <= 32'hd2bec333;
      33: out3 <= 32'hd6326a88;
      34: out3 <= 32'hd9e01006;
      35: out3 <= 32'hddc29958;
      36: out3 <= 32'he1d4a2c8;
      37: out3 <= 32'he61086bc;
      38: out3 <= 32'hea70658a;
      39: out3 <= 32'heeee2d9d;
      40: out3 <= 32'hf383a3e2;
      41: out3 <= 32'hf82a6c6a;
      42: out3 <= 32'hfcdc1342;
      43: out3 <= 32'h192155f;
      44: out3 <= 32'h645e9af;
      45: out3 <= 32'haf10a22;
      46: out3 <= 32'hf8cfcbe;
      47: out3 <= 32'h14135c94;
      48: out3 <= 32'h187de2a7;
      49: out3 <= 32'h1cc66e99;
      50: out3 <= 32'h20e70f32;
      51: out3 <= 32'h24da0a9a;
      52: out3 <= 32'h2899e64a;
      53: out3 <= 32'h2c216eaa;
      54: out3 <= 32'h2f6bbe45;
      55: out3 <= 32'h32744493;
      56: out3 <= 32'h3536cc52;
      57: out3 <= 32'h37af8159;
      58: out3 <= 32'h39daf5e8;
      59: out3 <= 32'h3bb6276e;
      60: out3 <= 32'h3d3e82ae;
      61: out3 <= 32'h3e71e759;
      62: out3 <= 32'h3f4eaafe;
      63: out3 <= 32'h3fd39b5a;
      default: out3 <= 0;
   endcase
   end
// synthesis attribute rom_style of out3 is "block"
endmodule



module D19_81052(addr, out, clk);
   input clk;
   output [31:0] out;
   reg [31:0] out, out2, out3;
   input [5:0] addr;

   always @(posedge clk) begin
      out2 <= out3;
      out <= out2;
   case(addr)
      0: out3 <= 32'h0;
      1: out3 <= 32'hfcdc1342;
      2: out3 <= 32'hf9ba1651;
      3: out3 <= 32'hf69bf7c9;
      4: out3 <= 32'hf383a3e2;
      5: out3 <= 32'hf0730342;
      6: out3 <= 32'hed6bf9d1;
      7: out3 <= 32'hea70658a;
      8: out3 <= 32'he7821d59;
      9: out3 <= 32'he4a2eff6;
      10: out3 <= 32'he1d4a2c8;
      11: out3 <= 32'hdf18f0ce;
      12: out3 <= 32'hdc71898d;
      13: out3 <= 32'hd9e01006;
      14: out3 <= 32'hd76619b6;
      15: out3 <= 32'hd5052d97;
      16: out3 <= 32'hd2bec333;
      17: out3 <= 32'hd09441bb;
      18: out3 <= 32'hce86ff2a;
      19: out3 <= 32'hcc983f70;
      20: out3 <= 32'hcac933ae;
      21: out3 <= 32'hc91af976;
      22: out3 <= 32'hc78e9a1d;
      23: out3 <= 32'hc6250a18;
      24: out3 <= 32'hc4df2862;
      25: out3 <= 32'hc3bdbdf6;
      26: out3 <= 32'hc2c17d52;
      27: out3 <= 32'hc1eb0209;
      28: out3 <= 32'hc13ad060;
      29: out3 <= 32'hc0b15502;
      30: out3 <= 32'hc04ee4b8;
      31: out3 <= 32'hc013bc39;
      32: out3 <= 32'hc0000000;
      33: out3 <= 32'hc013bc39;
      34: out3 <= 32'hc04ee4b8;
      35: out3 <= 32'hc0b15502;
      36: out3 <= 32'hc13ad060;
      37: out3 <= 32'hc1eb0209;
      38: out3 <= 32'hc2c17d52;
      39: out3 <= 32'hc3bdbdf6;
      40: out3 <= 32'hc4df2862;
      41: out3 <= 32'hc6250a18;
      42: out3 <= 32'hc78e9a1d;
      43: out3 <= 32'hc91af976;
      44: out3 <= 32'hcac933ae;
      45: out3 <= 32'hcc983f70;
      46: out3 <= 32'hce86ff2a;
      47: out3 <= 32'hd09441bb;
      48: out3 <= 32'hd2bec333;
      49: out3 <= 32'hd5052d97;
      50: out3 <= 32'hd76619b6;
      51: out3 <= 32'hd9e01006;
      52: out3 <= 32'hdc71898d;
      53: out3 <= 32'hdf18f0ce;
      54: out3 <= 32'he1d4a2c8;
      55: out3 <= 32'he4a2eff6;
      56: out3 <= 32'he7821d59;
      57: out3 <= 32'hea70658a;
      58: out3 <= 32'hed6bf9d1;
      59: out3 <= 32'hf0730342;
      60: out3 <= 32'hf383a3e2;
      61: out3 <= 32'hf69bf7c9;
      62: out3 <= 32'hf9ba1651;
      63: out3 <= 32'hfcdc1342;
      default: out3 <= 0;
   endcase
   end
// synthesis attribute rom_style of out3 is "block"
endmodule



module D18_81184(addr, out, clk);
   input clk;
   output [31:0] out;
   reg [31:0] out, out2, out3;
   input [5:0] addr;

   always @(posedge clk) begin
      out2 <= out3;
      out <= out2;
   case(addr)
      0: out3 <= 32'h0;
      1: out3 <= 32'hfe6deaa1;
      2: out3 <= 32'hfcdc1342;
      3: out3 <= 32'hfb4ab7db;
      4: out3 <= 32'hf9ba1651;
      5: out3 <= 32'hf82a6c6a;
      6: out3 <= 32'hf69bf7c9;
      7: out3 <= 32'hf50ef5de;
      8: out3 <= 32'hf383a3e2;
      9: out3 <= 32'hf1fa3ecb;
      10: out3 <= 32'hf0730342;
      11: out3 <= 32'heeee2d9d;
      12: out3 <= 32'hed6bf9d1;
      13: out3 <= 32'hebeca36c;
      14: out3 <= 32'hea70658a;
      15: out3 <= 32'he8f77acf;
      16: out3 <= 32'he7821d59;
      17: out3 <= 32'he61086bc;
      18: out3 <= 32'he4a2eff6;
      19: out3 <= 32'he3399167;
      20: out3 <= 32'he1d4a2c8;
      21: out3 <= 32'he0745b24;
      22: out3 <= 32'hdf18f0ce;
      23: out3 <= 32'hddc29958;
      24: out3 <= 32'hdc71898d;
      25: out3 <= 32'hdb25f566;
      26: out3 <= 32'hd9e01006;
      27: out3 <= 32'hd8a00bae;
      28: out3 <= 32'hd76619b6;
      29: out3 <= 32'hd6326a88;
      30: out3 <= 32'hd5052d97;
      31: out3 <= 32'hd3de9156;
      32: out3 <= 32'hd2bec333;
      33: out3 <= 32'hd1a5ef90;
      34: out3 <= 32'hd09441bb;
      35: out3 <= 32'hcf89e3e8;
      36: out3 <= 32'hce86ff2a;
      37: out3 <= 32'hcd8bbb6d;
      38: out3 <= 32'hcc983f70;
      39: out3 <= 32'hcbacb0bf;
      40: out3 <= 32'hcac933ae;
      41: out3 <= 32'hc9edeb50;
      42: out3 <= 32'hc91af976;
      43: out3 <= 32'hc8507ea7;
      44: out3 <= 32'hc78e9a1d;
      45: out3 <= 32'hc6d569be;
      46: out3 <= 32'hc6250a18;
      47: out3 <= 32'hc57d965d;
      48: out3 <= 32'hc4df2862;
      49: out3 <= 32'hc449d892;
      50: out3 <= 32'hc3bdbdf6;
      51: out3 <= 32'hc33aee27;
      52: out3 <= 32'hc2c17d52;
      53: out3 <= 32'hc2517e31;
      54: out3 <= 32'hc1eb0209;
      55: out3 <= 32'hc18e18a7;
      56: out3 <= 32'hc13ad060;
      57: out3 <= 32'hc0f1360b;
      58: out3 <= 32'hc0b15502;
      59: out3 <= 32'hc07b371e;
      60: out3 <= 32'hc04ee4b8;
      61: out3 <= 32'hc02c64a6;
      62: out3 <= 32'hc013bc39;
      63: out3 <= 32'hc004ef3f;
      default: out3 <= 0;
   endcase
   end
// synthesis attribute rom_style of out3 is "block"
endmodule



module D14_81250(addr, out, clk);
   input clk;
   output [31:0] out;
   reg [31:0] out, out2, out3;
   input [5:0] addr;

   always @(posedge clk) begin
      out2 <= out3;
      out <= out2;
   case(addr)
      0: out3 <= 32'h40000000;
      1: out3 <= 32'h3ffb10c1;
      2: out3 <= 32'h3fec43c7;
      3: out3 <= 32'h3fd39b5a;
      4: out3 <= 32'h3fb11b48;
      5: out3 <= 32'h3f84c8e2;
      6: out3 <= 32'h3f4eaafe;
      7: out3 <= 32'h3f0ec9f5;
      8: out3 <= 32'h3ec52fa0;
      9: out3 <= 32'h3e71e759;
      10: out3 <= 32'h3e14fdf7;
      11: out3 <= 32'h3dae81cf;
      12: out3 <= 32'h3d3e82ae;
      13: out3 <= 32'h3cc511d9;
      14: out3 <= 32'h3c42420a;
      15: out3 <= 32'h3bb6276e;
      16: out3 <= 32'h3b20d79e;
      17: out3 <= 32'h3a8269a3;
      18: out3 <= 32'h39daf5e8;
      19: out3 <= 32'h392a9642;
      20: out3 <= 32'h387165e3;
      21: out3 <= 32'h37af8159;
      22: out3 <= 32'h36e5068a;
      23: out3 <= 32'h361214b0;
      24: out3 <= 32'h3536cc52;
      25: out3 <= 32'h34534f41;
      26: out3 <= 32'h3367c090;
      27: out3 <= 32'h32744493;
      28: out3 <= 32'h317900d6;
      29: out3 <= 32'h30761c18;
      30: out3 <= 32'h2f6bbe45;
      31: out3 <= 32'h2e5a1070;
      32: out3 <= 32'h2d413ccd;
      33: out3 <= 32'h2c216eaa;
      34: out3 <= 32'h2afad269;
      35: out3 <= 32'h29cd9578;
      36: out3 <= 32'h2899e64a;
      37: out3 <= 32'h275ff452;
      38: out3 <= 32'h261feffa;
      39: out3 <= 32'h24da0a9a;
      40: out3 <= 32'h238e7673;
      41: out3 <= 32'h223d66a8;
      42: out3 <= 32'h20e70f32;
      43: out3 <= 32'h1f8ba4dc;
      44: out3 <= 32'h1e2b5d38;
      45: out3 <= 32'h1cc66e99;
      46: out3 <= 32'h1b5d100a;
      47: out3 <= 32'h19ef7944;
      48: out3 <= 32'h187de2a7;
      49: out3 <= 32'h17088531;
      50: out3 <= 32'h158f9a76;
      51: out3 <= 32'h14135c94;
      52: out3 <= 32'h1294062f;
      53: out3 <= 32'h1111d263;
      54: out3 <= 32'hf8cfcbe;
      55: out3 <= 32'he05c135;
      56: out3 <= 32'hc7c5c1e;
      57: out3 <= 32'haf10a22;
      58: out3 <= 32'h9640837;
      59: out3 <= 32'h7d59396;
      60: out3 <= 32'h645e9af;
      61: out3 <= 32'h4b54825;
      62: out3 <= 32'h323ecbe;
      63: out3 <= 32'h192155f;
      default: out3 <= 0;
   endcase
   end
// synthesis attribute rom_style of out3 is "block"
endmodule



module D15_81382(addr, out, clk);
   input clk;
   output [31:0] out;
   reg [31:0] out, out2, out3;
   input [5:0] addr;

   always @(posedge clk) begin
      out2 <= out3;
      out <= out2;
   case(addr)
      0: out3 <= 32'h40000000;
      1: out3 <= 32'h3fec43c7;
      2: out3 <= 32'h3fb11b48;
      3: out3 <= 32'h3f4eaafe;
      4: out3 <= 32'h3ec52fa0;
      5: out3 <= 32'h3e14fdf7;
      6: out3 <= 32'h3d3e82ae;
      7: out3 <= 32'h3c42420a;
      8: out3 <= 32'h3b20d79e;
      9: out3 <= 32'h39daf5e8;
      10: out3 <= 32'h387165e3;
      11: out3 <= 32'h36e5068a;
      12: out3 <= 32'h3536cc52;
      13: out3 <= 32'h3367c090;
      14: out3 <= 32'h317900d6;
      15: out3 <= 32'h2f6bbe45;
      16: out3 <= 32'h2d413ccd;
      17: out3 <= 32'h2afad269;
      18: out3 <= 32'h2899e64a;
      19: out3 <= 32'h261feffa;
      20: out3 <= 32'h238e7673;
      21: out3 <= 32'h20e70f32;
      22: out3 <= 32'h1e2b5d38;
      23: out3 <= 32'h1b5d100a;
      24: out3 <= 32'h187de2a7;
      25: out3 <= 32'h158f9a76;
      26: out3 <= 32'h1294062f;
      27: out3 <= 32'hf8cfcbe;
      28: out3 <= 32'hc7c5c1e;
      29: out3 <= 32'h9640837;
      30: out3 <= 32'h645e9af;
      31: out3 <= 32'h323ecbe;
      32: out3 <= 32'h0;
      33: out3 <= 32'hfcdc1342;
      34: out3 <= 32'hf9ba1651;
      35: out3 <= 32'hf69bf7c9;
      36: out3 <= 32'hf383a3e2;
      37: out3 <= 32'hf0730342;
      38: out3 <= 32'hed6bf9d1;
      39: out3 <= 32'hea70658a;
      40: out3 <= 32'he7821d59;
      41: out3 <= 32'he4a2eff6;
      42: out3 <= 32'he1d4a2c8;
      43: out3 <= 32'hdf18f0ce;
      44: out3 <= 32'hdc71898d;
      45: out3 <= 32'hd9e01006;
      46: out3 <= 32'hd76619b6;
      47: out3 <= 32'hd5052d97;
      48: out3 <= 32'hd2bec333;
      49: out3 <= 32'hd09441bb;
      50: out3 <= 32'hce86ff2a;
      51: out3 <= 32'hcc983f70;
      52: out3 <= 32'hcac933ae;
      53: out3 <= 32'hc91af976;
      54: out3 <= 32'hc78e9a1d;
      55: out3 <= 32'hc6250a18;
      56: out3 <= 32'hc4df2862;
      57: out3 <= 32'hc3bdbdf6;
      58: out3 <= 32'hc2c17d52;
      59: out3 <= 32'hc1eb0209;
      60: out3 <= 32'hc13ad060;
      61: out3 <= 32'hc0b15502;
      62: out3 <= 32'hc04ee4b8;
      63: out3 <= 32'hc013bc39;
      default: out3 <= 0;
   endcase
   end
// synthesis attribute rom_style of out3 is "block"
endmodule



module D16_81448(addr, out, clk);
   input clk;
   output [31:0] out;
   reg [31:0] out, out2, out3;
   input [5:0] addr;

   always @(posedge clk) begin
      out2 <= out3;
      out <= out2;
   case(addr)
      0: out3 <= 32'h40000000;
      1: out3 <= 32'h3fd39b5a;
      2: out3 <= 32'h3f4eaafe;
      3: out3 <= 32'h3e71e759;
      4: out3 <= 32'h3d3e82ae;
      5: out3 <= 32'h3bb6276e;
      6: out3 <= 32'h39daf5e8;
      7: out3 <= 32'h37af8159;
      8: out3 <= 32'h3536cc52;
      9: out3 <= 32'h32744493;
      10: out3 <= 32'h2f6bbe45;
      11: out3 <= 32'h2c216eaa;
      12: out3 <= 32'h2899e64a;
      13: out3 <= 32'h24da0a9a;
      14: out3 <= 32'h20e70f32;
      15: out3 <= 32'h1cc66e99;
      16: out3 <= 32'h187de2a7;
      17: out3 <= 32'h14135c94;
      18: out3 <= 32'hf8cfcbe;
      19: out3 <= 32'haf10a22;
      20: out3 <= 32'h645e9af;
      21: out3 <= 32'h192155f;
      22: out3 <= 32'hfcdc1342;
      23: out3 <= 32'hf82a6c6a;
      24: out3 <= 32'hf383a3e2;
      25: out3 <= 32'heeee2d9d;
      26: out3 <= 32'hea70658a;
      27: out3 <= 32'he61086bc;
      28: out3 <= 32'he1d4a2c8;
      29: out3 <= 32'hddc29958;
      30: out3 <= 32'hd9e01006;
      31: out3 <= 32'hd6326a88;
      32: out3 <= 32'hd2bec333;
      33: out3 <= 32'hcf89e3e8;
      34: out3 <= 32'hcc983f70;
      35: out3 <= 32'hc9edeb50;
      36: out3 <= 32'hc78e9a1d;
      37: out3 <= 32'hc57d965d;
      38: out3 <= 32'hc3bdbdf6;
      39: out3 <= 32'hc2517e31;
      40: out3 <= 32'hc13ad060;
      41: out3 <= 32'hc07b371e;
      42: out3 <= 32'hc013bc39;
      43: out3 <= 32'hc004ef3f;
      44: out3 <= 32'hc04ee4b8;
      45: out3 <= 32'hc0f1360b;
      46: out3 <= 32'hc1eb0209;
      47: out3 <= 32'hc33aee27;
      48: out3 <= 32'hc4df2862;
      49: out3 <= 32'hc6d569be;
      50: out3 <= 32'hc91af976;
      51: out3 <= 32'hcbacb0bf;
      52: out3 <= 32'hce86ff2a;
      53: out3 <= 32'hd1a5ef90;
      54: out3 <= 32'hd5052d97;
      55: out3 <= 32'hd8a00bae;
      56: out3 <= 32'hdc71898d;
      57: out3 <= 32'he0745b24;
      58: out3 <= 32'he4a2eff6;
      59: out3 <= 32'he8f77acf;
      60: out3 <= 32'hed6bf9d1;
      61: out3 <= 32'hf1fa3ecb;
      62: out3 <= 32'hf69bf7c9;
      63: out3 <= 32'hfb4ab7db;
      default: out3 <= 0;
   endcase
   end
// synthesis attribute rom_style of out3 is "block"
endmodule



// Latency: 12
// Gap: 1
module codeBlock80600(clk, reset, next_in, next_out,
   i2_in,
   X0_in, Y0,
   X1_in, Y1,
   X2_in, Y2,
   X3_in, Y3,
   X4_in, Y4,
   X5_in, Y5,
   X6_in, Y6,
   X7_in, Y7);

   output next_out;
   input clk, reset, next_in;

   reg next;
   input [5:0] i2_in;
   reg [5:0] i2;

   input [31:0] X0_in,
      X1_in,
      X2_in,
      X3_in,
      X4_in,
      X5_in,
      X6_in,
      X7_in;

   reg   [31:0] X0,
      X1,
      X2,
      X3,
      X4,
      X5,
      X6,
      X7;

   output [31:0] Y0,
      Y1,
      Y2,
      Y3,
      Y4,
      Y5,
      Y6,
      Y7;

   shiftRegFIFO #(11, 1) shiftFIFO_85757(.X(next), .Y(next_out), .clk(clk));


   wire signed [31:0] a225;
   wire signed [31:0] a202;
   wire signed [31:0] a228;
   wire signed [31:0] a206;
   wire signed [31:0] a229;
   wire signed [31:0] a230;
   wire signed [31:0] a233;
   wire signed [31:0] a234;
   wire signed [31:0] a237;
   wire signed [31:0] a238;
   reg signed [31:0] tm292;
   reg signed [31:0] tm296;
   reg signed [31:0] tm308;
   reg signed [31:0] tm312;
   reg signed [31:0] tm324;
   reg signed [31:0] tm328;
   reg signed [31:0] tm340;
   reg signed [31:0] tm351;
   reg signed [31:0] tm293;
   reg signed [31:0] tm297;
   reg signed [31:0] tm309;
   reg signed [31:0] tm313;
   reg signed [31:0] tm325;
   reg signed [31:0] tm329;
   reg signed [31:0] tm341;
   reg signed [31:0] tm352;
   wire signed [31:0] tm18;
   wire signed [31:0] a207;
   wire signed [31:0] tm19;
   wire signed [31:0] a209;
   wire signed [31:0] tm20;
   wire signed [31:0] a213;
   wire signed [31:0] tm21;
   wire signed [31:0] a215;
   wire signed [31:0] tm22;
   wire signed [31:0] a219;
   wire signed [31:0] tm23;
   wire signed [31:0] a221;
   reg signed [31:0] tm294;
   reg signed [31:0] tm298;
   reg signed [31:0] tm310;
   reg signed [31:0] tm314;
   reg signed [31:0] tm326;
   reg signed [31:0] tm330;
   reg signed [31:0] tm342;
   reg signed [31:0] tm353;
   reg signed [31:0] tm68;
   reg signed [31:0] tm69;
   reg signed [31:0] tm72;
   reg signed [31:0] tm73;
   reg signed [31:0] tm76;
   reg signed [31:0] tm77;
   reg signed [31:0] tm295;
   reg signed [31:0] tm299;
   reg signed [31:0] tm311;
   reg signed [31:0] tm315;
   reg signed [31:0] tm327;
   reg signed [31:0] tm331;
   reg signed [31:0] tm343;
   reg signed [31:0] tm354;
   reg signed [31:0] tm344;
   reg signed [31:0] tm355;
   reg signed [31:0] tm345;
   reg signed [31:0] tm356;
   reg signed [31:0] tm346;
   reg signed [31:0] tm357;
   reg signed [31:0] tm347;
   reg signed [31:0] tm358;
   reg signed [31:0] tm348;
   reg signed [31:0] tm359;
   wire signed [31:0] a208;
   wire signed [31:0] a210;
   wire signed [31:0] a211;
   wire signed [31:0] a212;
   wire signed [31:0] a214;
   wire signed [31:0] a216;
   wire signed [31:0] a217;
   wire signed [31:0] a218;
   wire signed [31:0] a220;
   wire signed [31:0] a222;
   wire signed [31:0] a223;
   wire signed [31:0] a224;
   reg signed [31:0] tm349;
   reg signed [31:0] tm360;
   wire signed [31:0] Y0;
   wire signed [31:0] Y1;
   wire signed [31:0] Y2;
   wire signed [31:0] Y3;
   wire signed [31:0] Y4;
   wire signed [31:0] Y5;
   wire signed [31:0] Y6;
   wire signed [31:0] Y7;
   reg signed [31:0] tm350;
   reg signed [31:0] tm361;


   assign a225 = X0;
   assign a202 = a225;
   assign a228 = X1;
   assign a206 = a228;
   assign a229 = X2;
   assign a230 = X3;
   assign a233 = X4;
   assign a234 = X5;
   assign a237 = X6;
   assign a238 = X7;
   assign a207 = tm18;
   assign a209 = tm19;
   assign a213 = tm20;
   assign a215 = tm21;
   assign a219 = tm22;
   assign a221 = tm23;
   assign Y0 = tm350;
   assign Y1 = tm361;

   D20_80986 instD20inst0_80986(.addr(i2[5:0]), .out(tm23), .clk(clk));

   D19_81052 instD19inst0_81052(.addr(i2[5:0]), .out(tm21), .clk(clk));

   D18_81184 instD18inst0_81184(.addr(i2[5:0]), .out(tm19), .clk(clk));

   D14_81250 instD14inst0_81250(.addr(i2[5:0]), .out(tm18), .clk(clk));

   D15_81382 instD15inst0_81382(.addr(i2[5:0]), .out(tm20), .clk(clk));

   D16_81448 instD16inst0_81448(.addr(i2[5:0]), .out(tm22), .clk(clk));

    multfix #(32, 6) m80699(.a(tm68), .b(tm295), .clk(clk), .q_sc(a208), .q_unsc(), .rst(reset));
    multfix #(32, 6) m80721(.a(tm69), .b(tm299), .clk(clk), .q_sc(a210), .q_unsc(), .rst(reset));
    multfix #(32, 6) m80739(.a(tm69), .b(tm295), .clk(clk), .q_sc(a211), .q_unsc(), .rst(reset));
    multfix #(32, 6) m80750(.a(tm68), .b(tm299), .clk(clk), .q_sc(a212), .q_unsc(), .rst(reset));
    multfix #(32, 6) m80779(.a(tm72), .b(tm311), .clk(clk), .q_sc(a214), .q_unsc(), .rst(reset));
    multfix #(32, 6) m80801(.a(tm73), .b(tm315), .clk(clk), .q_sc(a216), .q_unsc(), .rst(reset));
    multfix #(32, 6) m80819(.a(tm73), .b(tm311), .clk(clk), .q_sc(a217), .q_unsc(), .rst(reset));
    multfix #(32, 6) m80830(.a(tm72), .b(tm315), .clk(clk), .q_sc(a218), .q_unsc(), .rst(reset));
    multfix #(32, 6) m80859(.a(tm76), .b(tm327), .clk(clk), .q_sc(a220), .q_unsc(), .rst(reset));
    multfix #(32, 6) m80881(.a(tm77), .b(tm331), .clk(clk), .q_sc(a222), .q_unsc(), .rst(reset));
    multfix #(32, 6) m80899(.a(tm77), .b(tm327), .clk(clk), .q_sc(a223), .q_unsc(), .rst(reset));
    multfix #(32, 6) m80910(.a(tm76), .b(tm331), .clk(clk), .q_sc(a224), .q_unsc(), .rst(reset));
    subfxp #(32, 1) sub80728(.a(a208), .b(a210), .clk(clk), .q(Y2));    // 10
    addfxp #(32, 1) add80757(.a(a211), .b(a212), .clk(clk), .q(Y3));    // 10
    subfxp #(32, 1) sub80808(.a(a214), .b(a216), .clk(clk), .q(Y4));    // 10
    addfxp #(32, 1) add80837(.a(a217), .b(a218), .clk(clk), .q(Y5));    // 10
    subfxp #(32, 1) sub80888(.a(a220), .b(a222), .clk(clk), .q(Y6));    // 10
    addfxp #(32, 1) add80917(.a(a223), .b(a224), .clk(clk), .q(Y7));    // 10


   always @(posedge clk) begin
      if (reset == 1) begin
         tm68 <= 0;
         tm295 <= 0;
         tm69 <= 0;
         tm299 <= 0;
         tm69 <= 0;
         tm295 <= 0;
         tm68 <= 0;
         tm299 <= 0;
         tm72 <= 0;
         tm311 <= 0;
         tm73 <= 0;
         tm315 <= 0;
         tm73 <= 0;
         tm311 <= 0;
         tm72 <= 0;
         tm315 <= 0;
         tm76 <= 0;
         tm327 <= 0;
         tm77 <= 0;
         tm331 <= 0;
         tm77 <= 0;
         tm327 <= 0;
         tm76 <= 0;
         tm331 <= 0;
      end
      else begin
         i2 <= i2_in;
         X0 <= X0_in;
         X1 <= X1_in;
         X2 <= X2_in;
         X3 <= X3_in;
         X4 <= X4_in;
         X5 <= X5_in;
         X6 <= X6_in;
         X7 <= X7_in;
         next <= next_in;
         tm292 <= a229;
         tm296 <= a230;
         tm308 <= a233;
         tm312 <= a234;
         tm324 <= a237;
         tm328 <= a238;
         tm340 <= a202;
         tm351 <= a206;
         tm293 <= tm292;
         tm297 <= tm296;
         tm309 <= tm308;
         tm313 <= tm312;
         tm325 <= tm324;
         tm329 <= tm328;
         tm341 <= tm340;
         tm352 <= tm351;
         tm294 <= tm293;
         tm298 <= tm297;
         tm310 <= tm309;
         tm314 <= tm313;
         tm326 <= tm325;
         tm330 <= tm329;
         tm342 <= tm341;
         tm353 <= tm352;
         tm68 <= a207;
         tm69 <= a209;
         tm72 <= a213;
         tm73 <= a215;
         tm76 <= a219;
         tm77 <= a221;
         tm295 <= tm294;
         tm299 <= tm298;
         tm311 <= tm310;
         tm315 <= tm314;
         tm327 <= tm326;
         tm331 <= tm330;
         tm343 <= tm342;
         tm354 <= tm353;
         tm344 <= tm343;
         tm355 <= tm354;
         tm345 <= tm344;
         tm356 <= tm355;
         tm346 <= tm345;
         tm357 <= tm356;
         tm347 <= tm346;
         tm358 <= tm357;
         tm348 <= tm347;
         tm359 <= tm358;
         tm349 <= tm348;
         tm360 <= tm359;
         tm350 <= tm349;
         tm361 <= tm360;
      end
   end
endmodule

// Latency: 3
// Gap: 1
module codeBlock81453(clk, reset, next_in, next_out,
   X0_in, Y0,
   X1_in, Y1,
   X2_in, Y2,
   X3_in, Y3,
   X4_in, Y4,
   X5_in, Y5,
   X6_in, Y6,
   X7_in, Y7);

   output next_out;
   input clk, reset, next_in;

   reg next;

   input [31:0] X0_in,
      X1_in,
      X2_in,
      X3_in,
      X4_in,
      X5_in,
      X6_in,
      X7_in;

   reg   [31:0] X0,
      X1,
      X2,
      X3,
      X4,
      X5,
      X6,
      X7;

   output [31:0] Y0,
      Y1,
      Y2,
      Y3,
      Y4,
      Y5,
      Y6,
      Y7;

   shiftRegFIFO #(2, 1) shiftFIFO_85760(.X(next), .Y(next_out), .clk(clk));


   wire signed [31:0] a137;
   wire signed [31:0] a138;
   wire signed [31:0] a139;
   wire signed [31:0] a140;
   wire signed [31:0] a145;
   wire signed [31:0] a146;
   wire signed [31:0] a147;
   wire signed [31:0] a148;
   wire signed [31:0] t241;
   wire signed [31:0] t242;
   wire signed [31:0] t243;
   wire signed [31:0] t244;
   wire signed [31:0] t245;
   wire signed [31:0] t246;
   wire signed [31:0] t247;
   wire signed [31:0] t248;
   wire signed [31:0] t249;
   wire signed [31:0] t250;
   wire signed [31:0] t251;
   wire signed [31:0] t252;
   wire signed [31:0] Y0;
   wire signed [31:0] Y1;
   wire signed [31:0] Y4;
   wire signed [31:0] Y5;
   wire signed [31:0] t253;
   wire signed [31:0] t254;
   wire signed [31:0] t255;
   wire signed [31:0] t256;
   wire signed [31:0] Y2;
   wire signed [31:0] Y3;
   wire signed [31:0] Y6;
   wire signed [31:0] Y7;


   assign a137 = X0;
   assign a138 = X4;
   assign a139 = X1;
   assign a140 = X5;
   assign a145 = X2;
   assign a146 = X6;
   assign a147 = X3;
   assign a148 = X7;
   assign Y0 = t249;
   assign Y1 = t250;
   assign Y4 = t251;
   assign Y5 = t252;
   assign Y2 = t253;
   assign Y3 = t254;
   assign Y6 = t255;
   assign Y7 = t256;

    addfxp #(32, 1) add81465(.a(a137), .b(a138), .clk(clk), .q(t241));    // 0
    addfxp #(32, 1) add81480(.a(a139), .b(a140), .clk(clk), .q(t242));    // 0
    subfxp #(32, 1) sub81495(.a(a137), .b(a138), .clk(clk), .q(t243));    // 0
    subfxp #(32, 1) sub81510(.a(a139), .b(a140), .clk(clk), .q(t244));    // 0
    addfxp #(32, 1) add81525(.a(a145), .b(a146), .clk(clk), .q(t245));    // 0
    addfxp #(32, 1) add81540(.a(a147), .b(a148), .clk(clk), .q(t246));    // 0
    subfxp #(32, 1) sub81555(.a(a145), .b(a146), .clk(clk), .q(t247));    // 0
    subfxp #(32, 1) sub81570(.a(a147), .b(a148), .clk(clk), .q(t248));    // 0
    addfxp #(32, 1) add81577(.a(t241), .b(t245), .clk(clk), .q(t249));    // 1
    addfxp #(32, 1) add81584(.a(t242), .b(t246), .clk(clk), .q(t250));    // 1
    subfxp #(32, 1) sub81591(.a(t241), .b(t245), .clk(clk), .q(t251));    // 1
    subfxp #(32, 1) sub81598(.a(t242), .b(t246), .clk(clk), .q(t252));    // 1
    addfxp #(32, 1) add81621(.a(t243), .b(t248), .clk(clk), .q(t253));    // 1
    subfxp #(32, 1) sub81628(.a(t244), .b(t247), .clk(clk), .q(t254));    // 1
    subfxp #(32, 1) sub81635(.a(t243), .b(t248), .clk(clk), .q(t255));    // 1
    addfxp #(32, 1) add81642(.a(t244), .b(t247), .clk(clk), .q(t256));    // 1


   always @(posedge clk) begin
      if (reset == 1) begin
      end
      else begin
         X0 <= X0_in;
         X1 <= X1_in;
         X2 <= X2_in;
         X3 <= X3_in;
         X4 <= X4_in;
         X5 <= X5_in;
         X6 <= X6_in;
         X7 <= X7_in;
         next <= next_in;
      end
   end
endmodule

// Latency: 197
// Gap: 256
module rc81666(clk, reset, next, next_out,
   X0, Y0,
   X1, Y1,
   X2, Y2,
   X3, Y3,
   X4, Y4,
   X5, Y5,
   X6, Y6,
   X7, Y7);

   output next_out;
   input clk, reset, next;

   input [31:0] X0,
      X1,
      X2,
      X3,
      X4,
      X5,
      X6,
      X7;

   output [31:0] Y0,
      Y1,
      Y2,
      Y3,
      Y4,
      Y5,
      Y6,
      Y7;

   wire [63:0] t0;
   wire [63:0] s0;
   assign t0 = {X0, X1};
   wire [63:0] t1;
   wire [63:0] s1;
   assign t1 = {X2, X3};
   wire [63:0] t2;
   wire [63:0] s2;
   assign t2 = {X4, X5};
   wire [63:0] t3;
   wire [63:0] s3;
   assign t3 = {X6, X7};
   assign Y0 = s0[63:32];
   assign Y1 = s0[31:0];
   assign Y2 = s1[63:32];
   assign Y3 = s1[31:0];
   assign Y4 = s2[63:32];
   assign Y5 = s2[31:0];
   assign Y6 = s3[63:32];
   assign Y7 = s3[31:0];

   perm81664 instPerm85761(.x0(t0), .y0(s0),
    .x1(t1), .y1(s1),
    .x2(t2), .y2(s2),
    .x3(t3), .y3(s3),
   .clk(clk), .next(next), .next_out(next_out), .reset(reset)
);



endmodule

// Latency: 197
// Gap: 256
module perm81664(clk, next, reset, next_out,
   x0, y0,
   x1, y1,
   x2, y2,
   x3, y3);
   parameter numBanks = 4;
   parameter logBanks = 2;
   parameter depth = 256;
   parameter logDepth = 8;
   parameter width = 64;

   input [width-1:0]  x0;
   output [width-1:0]  y0;
   wire [width-1:0]  ybuff0;
   input [width-1:0]  x1;
   output [width-1:0]  y1;
   wire [width-1:0]  ybuff1;
   input [width-1:0]  x2;
   output [width-1:0]  y2;
   wire [width-1:0]  ybuff2;
   input [width-1:0]  x3;
   output [width-1:0]  y3;
   wire [width-1:0]  ybuff3;
   input 	      clk, next, reset;
   output 	     next_out;

   wire    	     next0;

   reg              inFlip0, outFlip0;
   reg              inActive, outActive;

   wire [logBanks-1:0] inBank0, outBank0;
   wire [logDepth-1:0] inAddr0, outAddr0;
   wire [logBanks-1:0] outBank_a0;
   wire [logDepth-1:0] outAddr_a0;
   wire [logDepth+logBanks-1:0] addr0, addr0b, addr0c;
   wire [logBanks-1:0] inBank1, outBank1;
   wire [logDepth-1:0] inAddr1, outAddr1;
   wire [logBanks-1:0] outBank_a1;
   wire [logDepth-1:0] outAddr_a1;
   wire [logDepth+logBanks-1:0] addr1, addr1b, addr1c;
   wire [logBanks-1:0] inBank2, outBank2;
   wire [logDepth-1:0] inAddr2, outAddr2;
   wire [logBanks-1:0] outBank_a2;
   wire [logDepth-1:0] outAddr_a2;
   wire [logDepth+logBanks-1:0] addr2, addr2b, addr2c;
   wire [logBanks-1:0] inBank3, outBank3;
   wire [logDepth-1:0] inAddr3, outAddr3;
   wire [logBanks-1:0] outBank_a3;
   wire [logDepth-1:0] outAddr_a3;
   wire [logDepth+logBanks-1:0] addr3, addr3b, addr3c;


   reg [logDepth-1:0]  inCount, outCount, outCount_d, outCount_dd, outCount_for_rd_addr, outCount_for_rd_data;  

   assign    addr0 = {inCount, 2'd0};
   assign    addr0b = {outCount, 2'd0};
   assign    addr0c = {outCount_for_rd_addr, 2'd0};
   assign    addr1 = {inCount, 2'd1};
   assign    addr1b = {outCount, 2'd1};
   assign    addr1c = {outCount_for_rd_addr, 2'd1};
   assign    addr2 = {inCount, 2'd2};
   assign    addr2b = {outCount, 2'd2};
   assign    addr2c = {outCount_for_rd_addr, 2'd2};
   assign    addr3 = {inCount, 2'd3};
   assign    addr3b = {outCount, 2'd3};
   assign    addr3c = {outCount_for_rd_addr, 2'd3};
    wire [width+logDepth-1:0] w_0_0, w_0_1, w_0_2, w_0_3, w_1_0, w_1_1, w_1_2, w_1_3, w_2_0, w_2_1, w_2_2, w_2_3;

    reg [width-1:0] z_0_0;
    reg [width-1:0] z_0_1;
    reg [width-1:0] z_0_2;
    reg [width-1:0] z_0_3;
    wire [width-1:0] z_1_0, z_1_1, z_1_2, z_1_3, z_2_0, z_2_1, z_2_2, z_2_3;

    wire [logDepth-1:0] u_0_0, u_0_1, u_0_2, u_0_3, u_1_0, u_1_1, u_1_2, u_1_3, u_2_0, u_2_1, u_2_2, u_2_3;

    reg inFlip1, outFlip1;
    always @(posedge clk) begin
        inFlip1 <= inFlip0;
        outFlip1 <= outFlip0;
    end

   assign inBank0[0] = addr0[8] ^ addr0[0];
   assign inBank0[1] = addr0[9] ^ addr0[1];
   assign inAddr0[0] = addr0[2];
   assign inAddr0[1] = addr0[3];
   assign inAddr0[2] = addr0[4];
   assign inAddr0[3] = addr0[5];
   assign inAddr0[4] = addr0[6];
   assign inAddr0[5] = addr0[7];
   assign inAddr0[6] = addr0[0];
   assign inAddr0[7] = addr0[1];
   assign outBank0[0] = addr0b[8] ^ addr0b[0];
   assign outBank0[1] = addr0b[9] ^ addr0b[1];
   assign outAddr0[0] = addr0b[2];
   assign outAddr0[1] = addr0b[3];
   assign outAddr0[2] = addr0b[4];
   assign outAddr0[3] = addr0b[5];
   assign outAddr0[4] = addr0b[6];
   assign outAddr0[5] = addr0b[7];
   assign outAddr0[6] = addr0b[8];
   assign outAddr0[7] = addr0b[9];
   assign outBank_a0[0] = addr0c[8] ^ addr0c[0];
   assign outBank_a0[1] = addr0c[9] ^ addr0c[1];
   assign outAddr_a0[0] = addr0c[2];
   assign outAddr_a0[1] = addr0c[3];
   assign outAddr_a0[2] = addr0c[4];
   assign outAddr_a0[3] = addr0c[5];
   assign outAddr_a0[4] = addr0c[6];
   assign outAddr_a0[5] = addr0c[7];
   assign outAddr_a0[6] = addr0c[8];
   assign outAddr_a0[7] = addr0c[9];

   assign inBank1[0] = addr1[8] ^ addr1[0];
   assign inBank1[1] = addr1[9] ^ addr1[1];
   assign inAddr1[0] = addr1[2];
   assign inAddr1[1] = addr1[3];
   assign inAddr1[2] = addr1[4];
   assign inAddr1[3] = addr1[5];
   assign inAddr1[4] = addr1[6];
   assign inAddr1[5] = addr1[7];
   assign inAddr1[6] = addr1[0];
   assign inAddr1[7] = addr1[1];
   assign outBank1[0] = addr1b[8] ^ addr1b[0];
   assign outBank1[1] = addr1b[9] ^ addr1b[1];
   assign outAddr1[0] = addr1b[2];
   assign outAddr1[1] = addr1b[3];
   assign outAddr1[2] = addr1b[4];
   assign outAddr1[3] = addr1b[5];
   assign outAddr1[4] = addr1b[6];
   assign outAddr1[5] = addr1b[7];
   assign outAddr1[6] = addr1b[8];
   assign outAddr1[7] = addr1b[9];
   assign outBank_a1[0] = addr1c[8] ^ addr1c[0];
   assign outBank_a1[1] = addr1c[9] ^ addr1c[1];
   assign outAddr_a1[0] = addr1c[2];
   assign outAddr_a1[1] = addr1c[3];
   assign outAddr_a1[2] = addr1c[4];
   assign outAddr_a1[3] = addr1c[5];
   assign outAddr_a1[4] = addr1c[6];
   assign outAddr_a1[5] = addr1c[7];
   assign outAddr_a1[6] = addr1c[8];
   assign outAddr_a1[7] = addr1c[9];

   assign inBank2[0] = addr2[8] ^ addr2[0];
   assign inBank2[1] = addr2[9] ^ addr2[1];
   assign inAddr2[0] = addr2[2];
   assign inAddr2[1] = addr2[3];
   assign inAddr2[2] = addr2[4];
   assign inAddr2[3] = addr2[5];
   assign inAddr2[4] = addr2[6];
   assign inAddr2[5] = addr2[7];
   assign inAddr2[6] = addr2[0];
   assign inAddr2[7] = addr2[1];
   assign outBank2[0] = addr2b[8] ^ addr2b[0];
   assign outBank2[1] = addr2b[9] ^ addr2b[1];
   assign outAddr2[0] = addr2b[2];
   assign outAddr2[1] = addr2b[3];
   assign outAddr2[2] = addr2b[4];
   assign outAddr2[3] = addr2b[5];
   assign outAddr2[4] = addr2b[6];
   assign outAddr2[5] = addr2b[7];
   assign outAddr2[6] = addr2b[8];
   assign outAddr2[7] = addr2b[9];
   assign outBank_a2[0] = addr2c[8] ^ addr2c[0];
   assign outBank_a2[1] = addr2c[9] ^ addr2c[1];
   assign outAddr_a2[0] = addr2c[2];
   assign outAddr_a2[1] = addr2c[3];
   assign outAddr_a2[2] = addr2c[4];
   assign outAddr_a2[3] = addr2c[5];
   assign outAddr_a2[4] = addr2c[6];
   assign outAddr_a2[5] = addr2c[7];
   assign outAddr_a2[6] = addr2c[8];
   assign outAddr_a2[7] = addr2c[9];

   assign inBank3[0] = addr3[8] ^ addr3[0];
   assign inBank3[1] = addr3[9] ^ addr3[1];
   assign inAddr3[0] = addr3[2];
   assign inAddr3[1] = addr3[3];
   assign inAddr3[2] = addr3[4];
   assign inAddr3[3] = addr3[5];
   assign inAddr3[4] = addr3[6];
   assign inAddr3[5] = addr3[7];
   assign inAddr3[6] = addr3[0];
   assign inAddr3[7] = addr3[1];
   assign outBank3[0] = addr3b[8] ^ addr3b[0];
   assign outBank3[1] = addr3b[9] ^ addr3b[1];
   assign outAddr3[0] = addr3b[2];
   assign outAddr3[1] = addr3b[3];
   assign outAddr3[2] = addr3b[4];
   assign outAddr3[3] = addr3b[5];
   assign outAddr3[4] = addr3b[6];
   assign outAddr3[5] = addr3b[7];
   assign outAddr3[6] = addr3b[8];
   assign outAddr3[7] = addr3b[9];
   assign outBank_a3[0] = addr3c[8] ^ addr3c[0];
   assign outBank_a3[1] = addr3c[9] ^ addr3c[1];
   assign outAddr_a3[0] = addr3c[2];
   assign outAddr_a3[1] = addr3c[3];
   assign outAddr_a3[2] = addr3c[4];
   assign outAddr_a3[3] = addr3c[5];
   assign outAddr_a3[4] = addr3c[6];
   assign outAddr_a3[5] = addr3c[7];
   assign outAddr_a3[6] = addr3c[8];
   assign outAddr_a3[7] = addr3c[9];

   nextReg #(193, 8) nextReg_85766(.X(next), .Y(next0), .reset(reset), .clk(clk));


   shiftRegFIFO #(4, 1) shiftFIFO_85769(.X(next0), .Y(next_out), .clk(clk));


   memArray1024_81664 #(numBanks, logBanks, depth, logDepth, width)
     memSys(.inFlip(inFlip1), .outFlip(outFlip1), .next(next), .reset(reset),
        .x0(w_2_0[width+logDepth-1:logDepth]), .y0(ybuff0),
        .inAddr0(w_2_0[logDepth-1:0]),
        .outAddr0(u_2_0), 
        .x1(w_2_1[width+logDepth-1:logDepth]), .y1(ybuff1),
        .inAddr1(w_2_1[logDepth-1:0]),
        .outAddr1(u_2_1), 
        .x2(w_2_2[width+logDepth-1:logDepth]), .y2(ybuff2),
        .inAddr2(w_2_2[logDepth-1:0]),
        .outAddr2(u_2_2), 
        .x3(w_2_3[width+logDepth-1:logDepth]), .y3(ybuff3),
        .inAddr3(w_2_3[logDepth-1:0]),
        .outAddr3(u_2_3), 
        .clk(clk));

   always @(posedge clk) begin
      if (reset == 1) begin
      z_0_0 <= 0;
      z_0_1 <= 0;
      z_0_2 <= 0;
      z_0_3 <= 0;
         inFlip0 <= 0; outFlip0 <= 1; outCount <= 0; inCount <= 0;
        outCount_for_rd_addr <= 0;
        outCount_for_rd_data <= 0;
      end
      else begin
          outCount_d <= outCount;
          outCount_dd <= outCount_d;
         if (inCount == 192)
            outCount_for_rd_addr <= 0;
         else
            outCount_for_rd_addr <= outCount_for_rd_addr+1;
         if (inCount == 195)
            outCount_for_rd_data <= 0;
         else
            outCount_for_rd_data <= outCount_for_rd_data+1;
      z_0_0 <= ybuff0;
      z_0_1 <= ybuff1;
      z_0_2 <= ybuff2;
      z_0_3 <= ybuff3;
         if (inCount == 192) begin
            outFlip0 <= ~outFlip0;
            outCount <= 0;
         end
         else
            outCount <= outCount+1;
         if (inCount == 255) begin
            inFlip0 <= ~inFlip0;
         end
         if (next == 1) begin
            if (inCount >= 192)
               inFlip0 <= ~inFlip0;
            inCount <= 0;
         end
         else
            inCount <= inCount + 1;
      end
   end
    assign w_0_0 = {x0, inAddr0};
    assign w_0_1 = {x1, inAddr1};
    assign w_0_2 = {x2, inAddr2};
    assign w_0_3 = {x3, inAddr3};
    assign y0 = z_2_0;
    assign y1 = z_2_1;
    assign y2 = z_2_2;
    assign y3 = z_2_3;
    assign u_0_0 = outAddr_a0;
    assign u_0_1 = outAddr_a1;
    assign u_0_2 = outAddr_a2;
    assign u_0_3 = outAddr_a3;
    wire wr_ctrl_st_0;
    assign wr_ctrl_st_0 = inCount[7];

    switch #(logDepth+width) in_sw_0_0(.x0(w_0_0), .x1(w_0_2), .y0(w_1_0), .y1(w_1_2), .ctrl(wr_ctrl_st_0));
    switch #(logDepth+width) in_sw_0_1(.x0(w_0_1), .x1(w_0_3), .y0(w_1_1), .y1(w_1_3), .ctrl(wr_ctrl_st_0));
    reg [width+logDepth-1:0] w_1_0_pipe;
    reg [width+logDepth-1:0] w_1_1_pipe;
    reg [width+logDepth-1:0] w_1_2_pipe;
    reg [width+logDepth-1:0] w_1_3_pipe;

    always @(posedge clk) begin
        w_1_0_pipe <= w_1_0;
        w_1_1_pipe <= w_1_1;
        w_1_2_pipe <= w_1_2;
        w_1_3_pipe <= w_1_3;
    end

    wire wr_ctrl_st_1;
    reg wr_ctrl_st_1_1;
    always @(posedge clk) begin
        wr_ctrl_st_1_1 <= inCount[6];
    end
    assign wr_ctrl_st_1 = wr_ctrl_st_1_1;

    switch #(logDepth+width) in_sw_1_0(.x0(w_1_0_pipe), .x1(w_1_1_pipe), .y0(w_2_0), .y1(w_2_1), .ctrl(wr_ctrl_st_1));
    switch #(logDepth+width) in_sw_1_1(.x0(w_1_2_pipe), .x1(w_1_3_pipe), .y0(w_2_2), .y1(w_2_3), .ctrl(wr_ctrl_st_1));
    wire rdd_ctrl_st_0;
    assign rdd_ctrl_st_0 = outCount_for_rd_data[7];

    switch #(width) out_sw_0_0(.x0(z_0_0), .x1(z_0_2), .y0(z_1_0), .y1(z_1_2), .ctrl(rdd_ctrl_st_0));
    switch #(width) out_sw_0_1(.x0(z_0_1), .x1(z_0_3), .y0(z_1_1), .y1(z_1_3), .ctrl(rdd_ctrl_st_0));
    reg [width-1:0] z_1_0_pipe;
    reg [width-1:0] z_1_1_pipe;
    reg [width-1:0] z_1_2_pipe;
    reg [width-1:0] z_1_3_pipe;

    always @(posedge clk) begin
        z_1_0_pipe <= z_1_0;
        z_1_1_pipe <= z_1_1;
        z_1_2_pipe <= z_1_2;
        z_1_3_pipe <= z_1_3;
    end

    wire rdd_ctrl_st_1;
    reg rdd_ctrl_st_1_1;
    always @(posedge clk) begin
        rdd_ctrl_st_1_1 <= outCount_for_rd_data[6];

    end
    assign rdd_ctrl_st_1 = rdd_ctrl_st_1_1;

    switch #(width) out_sw_1_0(.x0(z_1_0_pipe), .x1(z_1_1_pipe), .y0(z_2_0), .y1(z_2_1), .ctrl(rdd_ctrl_st_1));
    switch #(width) out_sw_1_1(.x0(z_1_2_pipe), .x1(z_1_3_pipe), .y0(z_2_2), .y1(z_2_3), .ctrl(rdd_ctrl_st_1));
    wire rda_ctrl_st_0;
    assign rda_ctrl_st_0 = outCount_for_rd_addr[7];

    switch #(logDepth) rdaddr_sw_0_0(.x0(u_0_0), .x1(u_0_2), .y0(u_1_0), .y1(u_1_2), .ctrl(rda_ctrl_st_0));
    switch #(logDepth) rdaddr_sw_0_1(.x0(u_0_1), .x1(u_0_3), .y0(u_1_1), .y1(u_1_3), .ctrl(rda_ctrl_st_0));
    reg [logDepth-1:0] u_1_0_pipe;
    reg [logDepth-1:0] u_1_1_pipe;
    reg [logDepth-1:0] u_1_2_pipe;
    reg [logDepth-1:0] u_1_3_pipe;

    always @(posedge clk) begin
        u_1_0_pipe <= u_1_0;
        u_1_1_pipe <= u_1_1;
        u_1_2_pipe <= u_1_2;
        u_1_3_pipe <= u_1_3;
    end

    wire rda_ctrl_st_1;
    reg rda_ctrl_st_1_1;
    always @(posedge clk) begin
        rda_ctrl_st_1_1 <= outCount_for_rd_addr[6];

    end
    assign rda_ctrl_st_1 = rda_ctrl_st_1_1;

    switch #(logDepth) rdaddr_sw_1_0(.x0(u_1_0_pipe), .x1(u_1_1_pipe), .y0(u_2_0), .y1(u_2_1), .ctrl(rda_ctrl_st_1));
    switch #(logDepth) rdaddr_sw_1_1(.x0(u_1_2_pipe), .x1(u_1_3_pipe), .y0(u_2_2), .y1(u_2_3), .ctrl(rda_ctrl_st_1));
endmodule

module memArray1024_81664(next, reset,
                x0, y0,
                inAddr0,
                outAddr0,
                x1, y1,
                inAddr1,
                outAddr1,
                x2, y2,
                inAddr2,
                outAddr2,
                x3, y3,
                inAddr3,
                outAddr3,
                clk, inFlip, outFlip);

   parameter numBanks = 4;
   parameter logBanks = 2;
   parameter depth = 256;
   parameter logDepth = 8;
   parameter width = 64;
         
   input     clk, next, reset;
   input    inFlip, outFlip;
   wire    next0;
   
   input [width-1:0]   x0;
   output [width-1:0]  y0;
   input [logDepth-1:0] inAddr0, outAddr0;
   input [width-1:0]   x1;
   output [width-1:0]  y1;
   input [logDepth-1:0] inAddr1, outAddr1;
   input [width-1:0]   x2;
   output [width-1:0]  y2;
   input [logDepth-1:0] inAddr2, outAddr2;
   input [width-1:0]   x3;
   output [width-1:0]  y3;
   input [logDepth-1:0] inAddr3, outAddr3;
   nextReg #(256, 8) nextReg_85774(.X(next), .Y(next0), .reset(reset), .clk(clk));


   memMod #(depth*2, width, logDepth+1) 
     memMod0(.in(x0), .out(y0), .inAddr({inFlip, inAddr0}),
	   .outAddr({outFlip, outAddr0}), .writeSel(1'b1), .clk(clk));   
   memMod #(depth*2, width, logDepth+1) 
     memMod1(.in(x1), .out(y1), .inAddr({inFlip, inAddr1}),
	   .outAddr({outFlip, outAddr1}), .writeSel(1'b1), .clk(clk));   
   memMod #(depth*2, width, logDepth+1) 
     memMod2(.in(x2), .out(y2), .inAddr({inFlip, inAddr2}),
	   .outAddr({outFlip, outAddr2}), .writeSel(1'b1), .clk(clk));   
   memMod #(depth*2, width, logDepth+1) 
     memMod3(.in(x3), .out(y3), .inAddr({inFlip, inAddr3}),
	   .outAddr({outFlip, outAddr3}), .writeSel(1'b1), .clk(clk));   
endmodule

// Latency: 12
// Gap: 256
module DirSum_84054(clk, reset, next, next_out,
      X0, Y0,
      X1, Y1,
      X2, Y2,
      X3, Y3,
      X4, Y4,
      X5, Y5,
      X6, Y6,
      X7, Y7);

   output next_out;
   input clk, reset, next;

   reg [7:0] i1;

   input [31:0] X0,
      X1,
      X2,
      X3,
      X4,
      X5,
      X6,
      X7;

   output [31:0] Y0,
      Y1,
      Y2,
      Y3,
      Y4,
      Y5,
      Y6,
      Y7;

   always @(posedge clk) begin
      if (reset == 1) begin
         i1 <= 0;
      end
      else begin
         if (next == 1)
            i1 <= 0;
         else if (i1 == 255)
            i1 <= 0;
         else
            i1 <= i1 + 1;
      end
   end

   codeBlock81668 codeBlockIsnt85779(.clk(clk), .reset(reset), .next_in(next), .next_out(next_out),
.i1_in(i1),
       .X0_in(X0), .Y0(Y0),
       .X1_in(X1), .Y1(Y1),
       .X2_in(X2), .Y2(Y2),
       .X3_in(X3), .Y3(Y3),
       .X4_in(X4), .Y4(Y4),
       .X5_in(X5), .Y5(Y5),
       .X6_in(X6), .Y6(Y6),
       .X7_in(X7), .Y7(Y7));

endmodule

module D4_82246(addr, out, clk);
   input clk;
   output [31:0] out;
   reg [31:0] out, out2, out3;
   input [7:0] addr;

   always @(posedge clk) begin
      out2 <= out3;
      out <= out2;
   case(addr)
      0: out3 <= 32'h40000000;
      1: out3 <= 32'h3fffb10b;
      2: out3 <= 32'h3ffec42d;
      3: out3 <= 32'h3ffd3969;
      4: out3 <= 32'h3ffb10c1;
      5: out3 <= 32'h3ff84a3c;
      6: out3 <= 32'h3ff4e5e0;
      7: out3 <= 32'h3ff0e3b6;
      8: out3 <= 32'h3fec43c7;
      9: out3 <= 32'h3fe7061f;
      10: out3 <= 32'h3fe12acb;
      11: out3 <= 32'h3fdab1d9;
      12: out3 <= 32'h3fd39b5a;
      13: out3 <= 32'h3fcbe75e;
      14: out3 <= 32'h3fc395f9;
      15: out3 <= 32'h3fbaa740;
      16: out3 <= 32'h3fb11b48;
      17: out3 <= 32'h3fa6f228;
      18: out3 <= 32'h3f9c2bfb;
      19: out3 <= 32'h3f90c8da;
      20: out3 <= 32'h3f84c8e2;
      21: out3 <= 32'h3f782c30;
      22: out3 <= 32'h3f6af2e3;
      23: out3 <= 32'h3f5d1d1d;
      24: out3 <= 32'h3f4eaafe;
      25: out3 <= 32'h3f3f9cab;
      26: out3 <= 32'h3f2ff24a;
      27: out3 <= 32'h3f1fabff;
      28: out3 <= 32'h3f0ec9f5;
      29: out3 <= 32'h3efd4c54;
      30: out3 <= 32'h3eeb3347;
      31: out3 <= 32'h3ed87efc;
      32: out3 <= 32'h3ec52fa0;
      33: out3 <= 32'h3eb14563;
      34: out3 <= 32'h3e9cc076;
      35: out3 <= 32'h3e87a10c;
      36: out3 <= 32'h3e71e759;
      37: out3 <= 32'h3e5b9392;
      38: out3 <= 32'h3e44a5ef;
      39: out3 <= 32'h3e2d1ea8;
      40: out3 <= 32'h3e14fdf7;
      41: out3 <= 32'h3dfc4418;
      42: out3 <= 32'h3de2f148;
      43: out3 <= 32'h3dc905c5;
      44: out3 <= 32'h3dae81cf;
      45: out3 <= 32'h3d9365a8;
      46: out3 <= 32'h3d77b192;
      47: out3 <= 32'h3d5b65d2;
      48: out3 <= 32'h3d3e82ae;
      49: out3 <= 32'h3d21086c;
      50: out3 <= 32'h3d02f757;
      51: out3 <= 32'h3ce44fb7;
      52: out3 <= 32'h3cc511d9;
      53: out3 <= 32'h3ca53e09;
      54: out3 <= 32'h3c84d496;
      55: out3 <= 32'h3c63d5d1;
      56: out3 <= 32'h3c42420a;
      57: out3 <= 32'h3c201994;
      58: out3 <= 32'h3bfd5cc4;
      59: out3 <= 32'h3bda0bf0;
      60: out3 <= 32'h3bb6276e;
      61: out3 <= 32'h3b91af97;
      62: out3 <= 32'h3b6ca4c4;
      63: out3 <= 32'h3b470753;
      64: out3 <= 32'h3b20d79e;
      65: out3 <= 32'h3afa1605;
      66: out3 <= 32'h3ad2c2e8;
      67: out3 <= 32'h3aaadea6;
      68: out3 <= 32'h3a8269a3;
      69: out3 <= 32'h3a596442;
      70: out3 <= 32'h3a2fcee8;
      71: out3 <= 32'h3a05a9fd;
      72: out3 <= 32'h39daf5e8;
      73: out3 <= 32'h39afb313;
      74: out3 <= 32'h3983e1e8;
      75: out3 <= 32'h395782d3;
      76: out3 <= 32'h392a9642;
      77: out3 <= 32'h38fd1ca4;
      78: out3 <= 32'h38cf1669;
      79: out3 <= 32'h38a08402;
      80: out3 <= 32'h387165e3;
      81: out3 <= 32'h3841bc7f;
      82: out3 <= 32'h3811884d;
      83: out3 <= 32'h37e0c9c3;
      84: out3 <= 32'h37af8159;
      85: out3 <= 32'h377daf89;
      86: out3 <= 32'h374b54ce;
      87: out3 <= 32'h371871a5;
      88: out3 <= 32'h36e5068a;
      89: out3 <= 32'h36b113fd;
      90: out3 <= 32'h367c9a7e;
      91: out3 <= 32'h36479a8e;
      92: out3 <= 32'h361214b0;
      93: out3 <= 32'h35dc0968;
      94: out3 <= 32'h35a5793c;
      95: out3 <= 32'h356e64b2;
      96: out3 <= 32'h3536cc52;
      97: out3 <= 32'h34feb0a5;
      98: out3 <= 32'h34c61236;
      99: out3 <= 32'h348cf190;
      100: out3 <= 32'h34534f41;
      101: out3 <= 32'h34192bd5;
      102: out3 <= 32'h33de87de;
      103: out3 <= 32'h33a363ec;
      104: out3 <= 32'h3367c090;
      105: out3 <= 32'h332b9e5e;
      106: out3 <= 32'h32eefdea;
      107: out3 <= 32'h32b1dfc9;
      108: out3 <= 32'h32744493;
      109: out3 <= 32'h32362ce0;
      110: out3 <= 32'h31f79948;
      111: out3 <= 32'h31b88a66;
      112: out3 <= 32'h317900d6;
      113: out3 <= 32'h3138fd35;
      114: out3 <= 32'h30f8801f;
      115: out3 <= 32'h30b78a36;
      116: out3 <= 32'h30761c18;
      117: out3 <= 32'h30343667;
      118: out3 <= 32'h2ff1d9c7;
      119: out3 <= 32'h2faf06da;
      120: out3 <= 32'h2f6bbe45;
      121: out3 <= 32'h2f2800af;
      122: out3 <= 32'h2ee3cebe;
      123: out3 <= 32'h2e9f291b;
      124: out3 <= 32'h2e5a1070;
      125: out3 <= 32'h2e148566;
      126: out3 <= 32'h2dce88aa;
      127: out3 <= 32'h2d881ae8;
      128: out3 <= 32'h2d413ccd;
      129: out3 <= 32'h2cf9ef09;
      130: out3 <= 32'h2cb2324c;
      131: out3 <= 32'h2c6a0746;
      132: out3 <= 32'h2c216eaa;
      133: out3 <= 32'h2bd8692b;
      134: out3 <= 32'h2b8ef77d;
      135: out3 <= 32'h2b451a55;
      136: out3 <= 32'h2afad269;
      137: out3 <= 32'h2ab02071;
      138: out3 <= 32'h2a650525;
      139: out3 <= 32'h2a19813f;
      140: out3 <= 32'h29cd9578;
      141: out3 <= 32'h2981428c;
      142: out3 <= 32'h29348937;
      143: out3 <= 32'h28e76a37;
      144: out3 <= 32'h2899e64a;
      145: out3 <= 32'h284bfe2f;
      146: out3 <= 32'h27fdb2a7;
      147: out3 <= 32'h27af0472;
      148: out3 <= 32'h275ff452;
      149: out3 <= 32'h2710830c;
      150: out3 <= 32'h26c0b162;
      151: out3 <= 32'h2670801a;
      152: out3 <= 32'h261feffa;
      153: out3 <= 32'h25cf01c8;
      154: out3 <= 32'h257db64c;
      155: out3 <= 32'h252c0e4f;
      156: out3 <= 32'h24da0a9a;
      157: out3 <= 32'h2487abf7;
      158: out3 <= 32'h2434f332;
      159: out3 <= 32'h23e1e117;
      160: out3 <= 32'h238e7673;
      161: out3 <= 32'h233ab414;
      162: out3 <= 32'h22e69ac8;
      163: out3 <= 32'h22922b5e;
      164: out3 <= 32'h223d66a8;
      165: out3 <= 32'h21e84d76;
      166: out3 <= 32'h2192e09b;
      167: out3 <= 32'h213d20e8;
      168: out3 <= 32'h20e70f32;
      169: out3 <= 32'h2090ac4d;
      170: out3 <= 32'h2039f90f;
      171: out3 <= 32'h1fe2f64c;
      172: out3 <= 32'h1f8ba4dc;
      173: out3 <= 32'h1f340596;
      174: out3 <= 32'h1edc1953;
      175: out3 <= 32'h1e83e0eb;
      176: out3 <= 32'h1e2b5d38;
      177: out3 <= 32'h1dd28f15;
      178: out3 <= 32'h1d79775c;
      179: out3 <= 32'h1d2016e9;
      180: out3 <= 32'h1cc66e99;
      181: out3 <= 32'h1c6c7f4a;
      182: out3 <= 32'h1c1249d8;
      183: out3 <= 32'h1bb7cf23;
      184: out3 <= 32'h1b5d100a;
      185: out3 <= 32'h1b020d6c;
      186: out3 <= 32'h1aa6c82b;
      187: out3 <= 32'h1a4b4128;
      188: out3 <= 32'h19ef7944;
      189: out3 <= 32'h19937161;
      190: out3 <= 32'h19372a64;
      191: out3 <= 32'h18daa52f;
      192: out3 <= 32'h187de2a7;
      193: out3 <= 32'h1820e3b0;
      194: out3 <= 32'h17c3a931;
      195: out3 <= 32'h1766340f;
      196: out3 <= 32'h17088531;
      197: out3 <= 32'h16aa9d7e;
      198: out3 <= 32'h164c7ddd;
      199: out3 <= 32'h15ee2738;
      200: out3 <= 32'h158f9a76;
      201: out3 <= 32'h1530d881;
      202: out3 <= 32'h14d1e242;
      203: out3 <= 32'h1472b8a5;
      204: out3 <= 32'h14135c94;
      205: out3 <= 32'h13b3cefa;
      206: out3 <= 32'h135410c3;
      207: out3 <= 32'h12f422db;
      208: out3 <= 32'h1294062f;
      209: out3 <= 32'h1233bbac;
      210: out3 <= 32'h11d3443f;
      211: out3 <= 32'h1172a0d7;
      212: out3 <= 32'h1111d263;
      213: out3 <= 32'h10b0d9d0;
      214: out3 <= 32'h104fb80e;
      215: out3 <= 32'hfee6e0d;
      216: out3 <= 32'hf8cfcbe;
      217: out3 <= 32'hf2b650f;
      218: out3 <= 32'hec9a7f3;
      219: out3 <= 32'he67c65a;
      220: out3 <= 32'he05c135;
      221: out3 <= 32'hda39978;
      222: out3 <= 32'hd415013;
      223: out3 <= 32'hcdee5f9;
      224: out3 <= 32'hc7c5c1e;
      225: out3 <= 32'hc19b374;
      226: out3 <= 32'hbb6ecef;
      227: out3 <= 32'hb540982;
      228: out3 <= 32'haf10a22;
      229: out3 <= 32'ha8defc3;
      230: out3 <= 32'ha2abb59;
      231: out3 <= 32'h9c76dd8;
      232: out3 <= 32'h9640837;
      233: out3 <= 32'h9008b6a;
      234: out3 <= 32'h89cf867;
      235: out3 <= 32'h8395024;
      236: out3 <= 32'h7d59396;
      237: out3 <= 32'h771c3b3;
      238: out3 <= 32'h70de172;
      239: out3 <= 32'h6a9edc9;
      240: out3 <= 32'h645e9af;
      241: out3 <= 32'h5e1d61b;
      242: out3 <= 32'h57db403;
      243: out3 <= 32'h519845e;
      244: out3 <= 32'h4b54825;
      245: out3 <= 32'h451004d;
      246: out3 <= 32'h3ecadcf;
      247: out3 <= 32'h38851a2;
      248: out3 <= 32'h323ecbe;
      249: out3 <= 32'h2bf801a;
      250: out3 <= 32'h25b0caf;
      251: out3 <= 32'h1f69373;
      252: out3 <= 32'h192155f;
      253: out3 <= 32'h12d936c;
      254: out3 <= 32'hc90e90;
      255: out3 <= 32'h6487c4;
      default: out3 <= 0;
   endcase
   end
// synthesis attribute rom_style of out3 is "block"
endmodule



module D9_82504(addr, out, clk);
   input clk;
   output [31:0] out;
   reg [31:0] out, out2, out3;
   input [7:0] addr;

   always @(posedge clk) begin
      out2 <= out3;
      out <= out2;
   case(addr)
      0: out3 <= 32'h0;
      1: out3 <= 32'hff36f170;
      2: out3 <= 32'hfe6deaa1;
      3: out3 <= 32'hfda4f351;
      4: out3 <= 32'hfcdc1342;
      5: out3 <= 32'hfc135231;
      6: out3 <= 32'hfb4ab7db;
      7: out3 <= 32'hfa824bfd;
      8: out3 <= 32'hf9ba1651;
      9: out3 <= 32'hf8f21e8e;
      10: out3 <= 32'hf82a6c6a;
      11: out3 <= 32'hf7630799;
      12: out3 <= 32'hf69bf7c9;
      13: out3 <= 32'hf5d544a7;
      14: out3 <= 32'hf50ef5de;
      15: out3 <= 32'hf4491311;
      16: out3 <= 32'hf383a3e2;
      17: out3 <= 32'hf2beafed;
      18: out3 <= 32'hf1fa3ecb;
      19: out3 <= 32'hf136580d;
      20: out3 <= 32'hf0730342;
      21: out3 <= 32'hefb047f2;
      22: out3 <= 32'heeee2d9d;
      23: out3 <= 32'hee2cbbc1;
      24: out3 <= 32'hed6bf9d1;
      25: out3 <= 32'hecabef3d;
      26: out3 <= 32'hebeca36c;
      27: out3 <= 32'heb2e1dbe;
      28: out3 <= 32'hea70658a;
      29: out3 <= 32'he9b38223;
      30: out3 <= 32'he8f77acf;
      31: out3 <= 32'he83c56cf;
      32: out3 <= 32'he7821d59;
      33: out3 <= 32'he6c8d59c;
      34: out3 <= 32'he61086bc;
      35: out3 <= 32'he55937d5;
      36: out3 <= 32'he4a2eff6;
      37: out3 <= 32'he3edb628;
      38: out3 <= 32'he3399167;
      39: out3 <= 32'he28688a4;
      40: out3 <= 32'he1d4a2c8;
      41: out3 <= 32'he123e6ad;
      42: out3 <= 32'he0745b24;
      43: out3 <= 32'hdfc606f1;
      44: out3 <= 32'hdf18f0ce;
      45: out3 <= 32'hde6d1f65;
      46: out3 <= 32'hddc29958;
      47: out3 <= 32'hdd196538;
      48: out3 <= 32'hdc71898d;
      49: out3 <= 32'hdbcb0cce;
      50: out3 <= 32'hdb25f566;
      51: out3 <= 32'hda8249b4;
      52: out3 <= 32'hd9e01006;
      53: out3 <= 32'hd93f4e9e;
      54: out3 <= 32'hd8a00bae;
      55: out3 <= 32'hd8024d59;
      56: out3 <= 32'hd76619b6;
      57: out3 <= 32'hd6cb76c9;
      58: out3 <= 32'hd6326a88;
      59: out3 <= 32'hd59afadb;
      60: out3 <= 32'hd5052d97;
      61: out3 <= 32'hd4710883;
      62: out3 <= 32'hd3de9156;
      63: out3 <= 32'hd34dcdb4;
      64: out3 <= 32'hd2bec333;
      65: out3 <= 32'hd2317756;
      66: out3 <= 32'hd1a5ef90;
      67: out3 <= 32'hd11c3142;
      68: out3 <= 32'hd09441bb;
      69: out3 <= 32'hd00e2639;
      70: out3 <= 32'hcf89e3e8;
      71: out3 <= 32'hcf077fe1;
      72: out3 <= 32'hce86ff2a;
      73: out3 <= 32'hce0866b8;
      74: out3 <= 32'hcd8bbb6d;
      75: out3 <= 32'hcd110216;
      76: out3 <= 32'hcc983f70;
      77: out3 <= 32'hcc217822;
      78: out3 <= 32'hcbacb0bf;
      79: out3 <= 32'hcb39edca;
      80: out3 <= 32'hcac933ae;
      81: out3 <= 32'hca5a86c4;
      82: out3 <= 32'hc9edeb50;
      83: out3 <= 32'hc9836582;
      84: out3 <= 32'hc91af976;
      85: out3 <= 32'hc8b4ab32;
      86: out3 <= 32'hc8507ea7;
      87: out3 <= 32'hc7ee77b3;
      88: out3 <= 32'hc78e9a1d;
      89: out3 <= 32'hc730e997;
      90: out3 <= 32'hc6d569be;
      91: out3 <= 32'hc67c1e18;
      92: out3 <= 32'hc6250a18;
      93: out3 <= 32'hc5d03118;
      94: out3 <= 32'hc57d965d;
      95: out3 <= 32'hc52d3d18;
      96: out3 <= 32'hc4df2862;
      97: out3 <= 32'hc4935b3c;
      98: out3 <= 32'hc449d892;
      99: out3 <= 32'hc402a33c;
      100: out3 <= 32'hc3bdbdf6;
      101: out3 <= 32'hc37b2b6a;
      102: out3 <= 32'hc33aee27;
      103: out3 <= 32'hc2fd08a9;
      104: out3 <= 32'hc2c17d52;
      105: out3 <= 32'hc2884e6e;
      106: out3 <= 32'hc2517e31;
      107: out3 <= 32'hc21d0eb8;
      108: out3 <= 32'hc1eb0209;
      109: out3 <= 32'hc1bb5a11;
      110: out3 <= 32'hc18e18a7;
      111: out3 <= 32'hc1633f8a;
      112: out3 <= 32'hc13ad060;
      113: out3 <= 32'hc114ccb9;
      114: out3 <= 32'hc0f1360b;
      115: out3 <= 32'hc0d00db6;
      116: out3 <= 32'hc0b15502;
      117: out3 <= 32'hc0950d1d;
      118: out3 <= 32'hc07b371e;
      119: out3 <= 32'hc063d405;
      120: out3 <= 32'hc04ee4b8;
      121: out3 <= 32'hc03c6a07;
      122: out3 <= 32'hc02c64a6;
      123: out3 <= 32'hc01ed535;
      124: out3 <= 32'hc013bc39;
      125: out3 <= 32'hc00b1a20;
      126: out3 <= 32'hc004ef3f;
      127: out3 <= 32'hc0013bd3;
      128: out3 <= 32'hc0000000;
      129: out3 <= 32'hc0013bd3;
      130: out3 <= 32'hc004ef3f;
      131: out3 <= 32'hc00b1a20;
      132: out3 <= 32'hc013bc39;
      133: out3 <= 32'hc01ed535;
      134: out3 <= 32'hc02c64a6;
      135: out3 <= 32'hc03c6a07;
      136: out3 <= 32'hc04ee4b8;
      137: out3 <= 32'hc063d405;
      138: out3 <= 32'hc07b371e;
      139: out3 <= 32'hc0950d1d;
      140: out3 <= 32'hc0b15502;
      141: out3 <= 32'hc0d00db6;
      142: out3 <= 32'hc0f1360b;
      143: out3 <= 32'hc114ccb9;
      144: out3 <= 32'hc13ad060;
      145: out3 <= 32'hc1633f8a;
      146: out3 <= 32'hc18e18a7;
      147: out3 <= 32'hc1bb5a11;
      148: out3 <= 32'hc1eb0209;
      149: out3 <= 32'hc21d0eb8;
      150: out3 <= 32'hc2517e31;
      151: out3 <= 32'hc2884e6e;
      152: out3 <= 32'hc2c17d52;
      153: out3 <= 32'hc2fd08a9;
      154: out3 <= 32'hc33aee27;
      155: out3 <= 32'hc37b2b6a;
      156: out3 <= 32'hc3bdbdf6;
      157: out3 <= 32'hc402a33c;
      158: out3 <= 32'hc449d892;
      159: out3 <= 32'hc4935b3c;
      160: out3 <= 32'hc4df2862;
      161: out3 <= 32'hc52d3d18;
      162: out3 <= 32'hc57d965d;
      163: out3 <= 32'hc5d03118;
      164: out3 <= 32'hc6250a18;
      165: out3 <= 32'hc67c1e18;
      166: out3 <= 32'hc6d569be;
      167: out3 <= 32'hc730e997;
      168: out3 <= 32'hc78e9a1d;
      169: out3 <= 32'hc7ee77b3;
      170: out3 <= 32'hc8507ea7;
      171: out3 <= 32'hc8b4ab32;
      172: out3 <= 32'hc91af976;
      173: out3 <= 32'hc9836582;
      174: out3 <= 32'hc9edeb50;
      175: out3 <= 32'hca5a86c4;
      176: out3 <= 32'hcac933ae;
      177: out3 <= 32'hcb39edca;
      178: out3 <= 32'hcbacb0bf;
      179: out3 <= 32'hcc217822;
      180: out3 <= 32'hcc983f70;
      181: out3 <= 32'hcd110216;
      182: out3 <= 32'hcd8bbb6d;
      183: out3 <= 32'hce0866b8;
      184: out3 <= 32'hce86ff2a;
      185: out3 <= 32'hcf077fe1;
      186: out3 <= 32'hcf89e3e8;
      187: out3 <= 32'hd00e2639;
      188: out3 <= 32'hd09441bb;
      189: out3 <= 32'hd11c3142;
      190: out3 <= 32'hd1a5ef90;
      191: out3 <= 32'hd2317756;
      192: out3 <= 32'hd2bec333;
      193: out3 <= 32'hd34dcdb4;
      194: out3 <= 32'hd3de9156;
      195: out3 <= 32'hd4710883;
      196: out3 <= 32'hd5052d97;
      197: out3 <= 32'hd59afadb;
      198: out3 <= 32'hd6326a88;
      199: out3 <= 32'hd6cb76c9;
      200: out3 <= 32'hd76619b6;
      201: out3 <= 32'hd8024d59;
      202: out3 <= 32'hd8a00bae;
      203: out3 <= 32'hd93f4e9e;
      204: out3 <= 32'hd9e01006;
      205: out3 <= 32'hda8249b4;
      206: out3 <= 32'hdb25f566;
      207: out3 <= 32'hdbcb0cce;
      208: out3 <= 32'hdc71898d;
      209: out3 <= 32'hdd196538;
      210: out3 <= 32'hddc29958;
      211: out3 <= 32'hde6d1f65;
      212: out3 <= 32'hdf18f0ce;
      213: out3 <= 32'hdfc606f1;
      214: out3 <= 32'he0745b24;
      215: out3 <= 32'he123e6ad;
      216: out3 <= 32'he1d4a2c8;
      217: out3 <= 32'he28688a4;
      218: out3 <= 32'he3399167;
      219: out3 <= 32'he3edb628;
      220: out3 <= 32'he4a2eff6;
      221: out3 <= 32'he55937d5;
      222: out3 <= 32'he61086bc;
      223: out3 <= 32'he6c8d59c;
      224: out3 <= 32'he7821d59;
      225: out3 <= 32'he83c56cf;
      226: out3 <= 32'he8f77acf;
      227: out3 <= 32'he9b38223;
      228: out3 <= 32'hea70658a;
      229: out3 <= 32'heb2e1dbe;
      230: out3 <= 32'hebeca36c;
      231: out3 <= 32'hecabef3d;
      232: out3 <= 32'hed6bf9d1;
      233: out3 <= 32'hee2cbbc1;
      234: out3 <= 32'heeee2d9d;
      235: out3 <= 32'hefb047f2;
      236: out3 <= 32'hf0730342;
      237: out3 <= 32'hf136580d;
      238: out3 <= 32'hf1fa3ecb;
      239: out3 <= 32'hf2beafed;
      240: out3 <= 32'hf383a3e2;
      241: out3 <= 32'hf4491311;
      242: out3 <= 32'hf50ef5de;
      243: out3 <= 32'hf5d544a7;
      244: out3 <= 32'hf69bf7c9;
      245: out3 <= 32'hf7630799;
      246: out3 <= 32'hf82a6c6a;
      247: out3 <= 32'hf8f21e8e;
      248: out3 <= 32'hf9ba1651;
      249: out3 <= 32'hfa824bfd;
      250: out3 <= 32'hfb4ab7db;
      251: out3 <= 32'hfc135231;
      252: out3 <= 32'hfcdc1342;
      253: out3 <= 32'hfda4f351;
      254: out3 <= 32'hfe6deaa1;
      255: out3 <= 32'hff36f170;
      default: out3 <= 0;
   endcase
   end
// synthesis attribute rom_style of out3 is "block"
endmodule



module D8_82762(addr, out, clk);
   input clk;
   output [31:0] out;
   reg [31:0] out, out2, out3;
   input [7:0] addr;

   always @(posedge clk) begin
      out2 <= out3;
      out <= out2;
   case(addr)
      0: out3 <= 32'h0;
      1: out3 <= 32'hff9b783c;
      2: out3 <= 32'hff36f170;
      3: out3 <= 32'hfed26c94;
      4: out3 <= 32'hfe6deaa1;
      5: out3 <= 32'hfe096c8d;
      6: out3 <= 32'hfda4f351;
      7: out3 <= 32'hfd407fe6;
      8: out3 <= 32'hfcdc1342;
      9: out3 <= 32'hfc77ae5e;
      10: out3 <= 32'hfc135231;
      11: out3 <= 32'hfbaeffb3;
      12: out3 <= 32'hfb4ab7db;
      13: out3 <= 32'hfae67ba2;
      14: out3 <= 32'hfa824bfd;
      15: out3 <= 32'hfa1e29e5;
      16: out3 <= 32'hf9ba1651;
      17: out3 <= 32'hf9561237;
      18: out3 <= 32'hf8f21e8e;
      19: out3 <= 32'hf88e3c4d;
      20: out3 <= 32'hf82a6c6a;
      21: out3 <= 32'hf7c6afdc;
      22: out3 <= 32'hf7630799;
      23: out3 <= 32'hf6ff7496;
      24: out3 <= 32'hf69bf7c9;
      25: out3 <= 32'hf6389228;
      26: out3 <= 32'hf5d544a7;
      27: out3 <= 32'hf572103d;
      28: out3 <= 32'hf50ef5de;
      29: out3 <= 32'hf4abf67e;
      30: out3 <= 32'hf4491311;
      31: out3 <= 32'hf3e64c8c;
      32: out3 <= 32'hf383a3e2;
      33: out3 <= 32'hf3211a07;
      34: out3 <= 32'hf2beafed;
      35: out3 <= 32'hf25c6688;
      36: out3 <= 32'hf1fa3ecb;
      37: out3 <= 32'hf19839a6;
      38: out3 <= 32'hf136580d;
      39: out3 <= 32'hf0d49af1;
      40: out3 <= 32'hf0730342;
      41: out3 <= 32'hf01191f3;
      42: out3 <= 32'hefb047f2;
      43: out3 <= 32'hef4f2630;
      44: out3 <= 32'heeee2d9d;
      45: out3 <= 32'hee8d5f29;
      46: out3 <= 32'hee2cbbc1;
      47: out3 <= 32'hedcc4454;
      48: out3 <= 32'hed6bf9d1;
      49: out3 <= 32'hed0bdd25;
      50: out3 <= 32'hecabef3d;
      51: out3 <= 32'hec4c3106;
      52: out3 <= 32'hebeca36c;
      53: out3 <= 32'heb8d475b;
      54: out3 <= 32'heb2e1dbe;
      55: out3 <= 32'heacf277f;
      56: out3 <= 32'hea70658a;
      57: out3 <= 32'hea11d8c8;
      58: out3 <= 32'he9b38223;
      59: out3 <= 32'he9556282;
      60: out3 <= 32'he8f77acf;
      61: out3 <= 32'he899cbf1;
      62: out3 <= 32'he83c56cf;
      63: out3 <= 32'he7df1c50;
      64: out3 <= 32'he7821d59;
      65: out3 <= 32'he7255ad1;
      66: out3 <= 32'he6c8d59c;
      67: out3 <= 32'he66c8e9f;
      68: out3 <= 32'he61086bc;
      69: out3 <= 32'he5b4bed8;
      70: out3 <= 32'he55937d5;
      71: out3 <= 32'he4fdf294;
      72: out3 <= 32'he4a2eff6;
      73: out3 <= 32'he44830dd;
      74: out3 <= 32'he3edb628;
      75: out3 <= 32'he39380b6;
      76: out3 <= 32'he3399167;
      77: out3 <= 32'he2dfe917;
      78: out3 <= 32'he28688a4;
      79: out3 <= 32'he22d70eb;
      80: out3 <= 32'he1d4a2c8;
      81: out3 <= 32'he17c1f15;
      82: out3 <= 32'he123e6ad;
      83: out3 <= 32'he0cbfa6a;
      84: out3 <= 32'he0745b24;
      85: out3 <= 32'he01d09b4;
      86: out3 <= 32'hdfc606f1;
      87: out3 <= 32'hdf6f53b3;
      88: out3 <= 32'hdf18f0ce;
      89: out3 <= 32'hdec2df18;
      90: out3 <= 32'hde6d1f65;
      91: out3 <= 32'hde17b28a;
      92: out3 <= 32'hddc29958;
      93: out3 <= 32'hdd6dd4a2;
      94: out3 <= 32'hdd196538;
      95: out3 <= 32'hdcc54bec;
      96: out3 <= 32'hdc71898d;
      97: out3 <= 32'hdc1e1ee9;
      98: out3 <= 32'hdbcb0cce;
      99: out3 <= 32'hdb785409;
      100: out3 <= 32'hdb25f566;
      101: out3 <= 32'hdad3f1b1;
      102: out3 <= 32'hda8249b4;
      103: out3 <= 32'hda30fe38;
      104: out3 <= 32'hd9e01006;
      105: out3 <= 32'hd98f7fe6;
      106: out3 <= 32'hd93f4e9e;
      107: out3 <= 32'hd8ef7cf4;
      108: out3 <= 32'hd8a00bae;
      109: out3 <= 32'hd850fb8e;
      110: out3 <= 32'hd8024d59;
      111: out3 <= 32'hd7b401d1;
      112: out3 <= 32'hd76619b6;
      113: out3 <= 32'hd71895c9;
      114: out3 <= 32'hd6cb76c9;
      115: out3 <= 32'hd67ebd74;
      116: out3 <= 32'hd6326a88;
      117: out3 <= 32'hd5e67ec1;
      118: out3 <= 32'hd59afadb;
      119: out3 <= 32'hd54fdf8f;
      120: out3 <= 32'hd5052d97;
      121: out3 <= 32'hd4bae5ab;
      122: out3 <= 32'hd4710883;
      123: out3 <= 32'hd42796d5;
      124: out3 <= 32'hd3de9156;
      125: out3 <= 32'hd395f8ba;
      126: out3 <= 32'hd34dcdb4;
      127: out3 <= 32'hd30610f7;
      128: out3 <= 32'hd2bec333;
      129: out3 <= 32'hd277e518;
      130: out3 <= 32'hd2317756;
      131: out3 <= 32'hd1eb7a9a;
      132: out3 <= 32'hd1a5ef90;
      133: out3 <= 32'hd160d6e5;
      134: out3 <= 32'hd11c3142;
      135: out3 <= 32'hd0d7ff51;
      136: out3 <= 32'hd09441bb;
      137: out3 <= 32'hd050f926;
      138: out3 <= 32'hd00e2639;
      139: out3 <= 32'hcfcbc999;
      140: out3 <= 32'hcf89e3e8;
      141: out3 <= 32'hcf4875ca;
      142: out3 <= 32'hcf077fe1;
      143: out3 <= 32'hcec702cb;
      144: out3 <= 32'hce86ff2a;
      145: out3 <= 32'hce47759a;
      146: out3 <= 32'hce0866b8;
      147: out3 <= 32'hcdc9d320;
      148: out3 <= 32'hcd8bbb6d;
      149: out3 <= 32'hcd4e2037;
      150: out3 <= 32'hcd110216;
      151: out3 <= 32'hccd461a2;
      152: out3 <= 32'hcc983f70;
      153: out3 <= 32'hcc5c9c14;
      154: out3 <= 32'hcc217822;
      155: out3 <= 32'hcbe6d42b;
      156: out3 <= 32'hcbacb0bf;
      157: out3 <= 32'hcb730e70;
      158: out3 <= 32'hcb39edca;
      159: out3 <= 32'hcb014f5b;
      160: out3 <= 32'hcac933ae;
      161: out3 <= 32'hca919b4e;
      162: out3 <= 32'hca5a86c4;
      163: out3 <= 32'hca23f698;
      164: out3 <= 32'hc9edeb50;
      165: out3 <= 32'hc9b86572;
      166: out3 <= 32'hc9836582;
      167: out3 <= 32'hc94eec03;
      168: out3 <= 32'hc91af976;
      169: out3 <= 32'hc8e78e5b;
      170: out3 <= 32'hc8b4ab32;
      171: out3 <= 32'hc8825077;
      172: out3 <= 32'hc8507ea7;
      173: out3 <= 32'hc81f363d;
      174: out3 <= 32'hc7ee77b3;
      175: out3 <= 32'hc7be4381;
      176: out3 <= 32'hc78e9a1d;
      177: out3 <= 32'hc75f7bfe;
      178: out3 <= 32'hc730e997;
      179: out3 <= 32'hc702e35c;
      180: out3 <= 32'hc6d569be;
      181: out3 <= 32'hc6a87d2d;
      182: out3 <= 32'hc67c1e18;
      183: out3 <= 32'hc6504ced;
      184: out3 <= 32'hc6250a18;
      185: out3 <= 32'hc5fa5603;
      186: out3 <= 32'hc5d03118;
      187: out3 <= 32'hc5a69bbe;
      188: out3 <= 32'hc57d965d;
      189: out3 <= 32'hc555215a;
      190: out3 <= 32'hc52d3d18;
      191: out3 <= 32'hc505e9fb;
      192: out3 <= 32'hc4df2862;
      193: out3 <= 32'hc4b8f8ad;
      194: out3 <= 32'hc4935b3c;
      195: out3 <= 32'hc46e5069;
      196: out3 <= 32'hc449d892;
      197: out3 <= 32'hc425f410;
      198: out3 <= 32'hc402a33c;
      199: out3 <= 32'hc3dfe66c;
      200: out3 <= 32'hc3bdbdf6;
      201: out3 <= 32'hc39c2a2f;
      202: out3 <= 32'hc37b2b6a;
      203: out3 <= 32'hc35ac1f7;
      204: out3 <= 32'hc33aee27;
      205: out3 <= 32'hc31bb049;
      206: out3 <= 32'hc2fd08a9;
      207: out3 <= 32'hc2def794;
      208: out3 <= 32'hc2c17d52;
      209: out3 <= 32'hc2a49a2e;
      210: out3 <= 32'hc2884e6e;
      211: out3 <= 32'hc26c9a58;
      212: out3 <= 32'hc2517e31;
      213: out3 <= 32'hc236fa3b;
      214: out3 <= 32'hc21d0eb8;
      215: out3 <= 32'hc203bbe8;
      216: out3 <= 32'hc1eb0209;
      217: out3 <= 32'hc1d2e158;
      218: out3 <= 32'hc1bb5a11;
      219: out3 <= 32'hc1a46c6e;
      220: out3 <= 32'hc18e18a7;
      221: out3 <= 32'hc1785ef4;
      222: out3 <= 32'hc1633f8a;
      223: out3 <= 32'hc14eba9d;
      224: out3 <= 32'hc13ad060;
      225: out3 <= 32'hc1278104;
      226: out3 <= 32'hc114ccb9;
      227: out3 <= 32'hc102b3ac;
      228: out3 <= 32'hc0f1360b;
      229: out3 <= 32'hc0e05401;
      230: out3 <= 32'hc0d00db6;
      231: out3 <= 32'hc0c06355;
      232: out3 <= 32'hc0b15502;
      233: out3 <= 32'hc0a2e2e3;
      234: out3 <= 32'hc0950d1d;
      235: out3 <= 32'hc087d3d0;
      236: out3 <= 32'hc07b371e;
      237: out3 <= 32'hc06f3726;
      238: out3 <= 32'hc063d405;
      239: out3 <= 32'hc0590dd8;
      240: out3 <= 32'hc04ee4b8;
      241: out3 <= 32'hc04558c0;
      242: out3 <= 32'hc03c6a07;
      243: out3 <= 32'hc03418a2;
      244: out3 <= 32'hc02c64a6;
      245: out3 <= 32'hc0254e27;
      246: out3 <= 32'hc01ed535;
      247: out3 <= 32'hc018f9e1;
      248: out3 <= 32'hc013bc39;
      249: out3 <= 32'hc00f1c4a;
      250: out3 <= 32'hc00b1a20;
      251: out3 <= 32'hc007b5c4;
      252: out3 <= 32'hc004ef3f;
      253: out3 <= 32'hc002c697;
      254: out3 <= 32'hc0013bd3;
      255: out3 <= 32'hc0004ef5;
      default: out3 <= 0;
   endcase
   end
// synthesis attribute rom_style of out3 is "block"
endmodule



module D5_83278(addr, out, clk);
   input clk;
   output [31:0] out;
   reg [31:0] out, out2, out3;
   input [7:0] addr;

   always @(posedge clk) begin
      out2 <= out3;
      out <= out2;
   case(addr)
      0: out3 <= 32'h40000000;
      1: out3 <= 32'h3ffec42d;
      2: out3 <= 32'h3ffb10c1;
      3: out3 <= 32'h3ff4e5e0;
      4: out3 <= 32'h3fec43c7;
      5: out3 <= 32'h3fe12acb;
      6: out3 <= 32'h3fd39b5a;
      7: out3 <= 32'h3fc395f9;
      8: out3 <= 32'h3fb11b48;
      9: out3 <= 32'h3f9c2bfb;
      10: out3 <= 32'h3f84c8e2;
      11: out3 <= 32'h3f6af2e3;
      12: out3 <= 32'h3f4eaafe;
      13: out3 <= 32'h3f2ff24a;
      14: out3 <= 32'h3f0ec9f5;
      15: out3 <= 32'h3eeb3347;
      16: out3 <= 32'h3ec52fa0;
      17: out3 <= 32'h3e9cc076;
      18: out3 <= 32'h3e71e759;
      19: out3 <= 32'h3e44a5ef;
      20: out3 <= 32'h3e14fdf7;
      21: out3 <= 32'h3de2f148;
      22: out3 <= 32'h3dae81cf;
      23: out3 <= 32'h3d77b192;
      24: out3 <= 32'h3d3e82ae;
      25: out3 <= 32'h3d02f757;
      26: out3 <= 32'h3cc511d9;
      27: out3 <= 32'h3c84d496;
      28: out3 <= 32'h3c42420a;
      29: out3 <= 32'h3bfd5cc4;
      30: out3 <= 32'h3bb6276e;
      31: out3 <= 32'h3b6ca4c4;
      32: out3 <= 32'h3b20d79e;
      33: out3 <= 32'h3ad2c2e8;
      34: out3 <= 32'h3a8269a3;
      35: out3 <= 32'h3a2fcee8;
      36: out3 <= 32'h39daf5e8;
      37: out3 <= 32'h3983e1e8;
      38: out3 <= 32'h392a9642;
      39: out3 <= 32'h38cf1669;
      40: out3 <= 32'h387165e3;
      41: out3 <= 32'h3811884d;
      42: out3 <= 32'h37af8159;
      43: out3 <= 32'h374b54ce;
      44: out3 <= 32'h36e5068a;
      45: out3 <= 32'h367c9a7e;
      46: out3 <= 32'h361214b0;
      47: out3 <= 32'h35a5793c;
      48: out3 <= 32'h3536cc52;
      49: out3 <= 32'h34c61236;
      50: out3 <= 32'h34534f41;
      51: out3 <= 32'h33de87de;
      52: out3 <= 32'h3367c090;
      53: out3 <= 32'h32eefdea;
      54: out3 <= 32'h32744493;
      55: out3 <= 32'h31f79948;
      56: out3 <= 32'h317900d6;
      57: out3 <= 32'h30f8801f;
      58: out3 <= 32'h30761c18;
      59: out3 <= 32'h2ff1d9c7;
      60: out3 <= 32'h2f6bbe45;
      61: out3 <= 32'h2ee3cebe;
      62: out3 <= 32'h2e5a1070;
      63: out3 <= 32'h2dce88aa;
      64: out3 <= 32'h2d413ccd;
      65: out3 <= 32'h2cb2324c;
      66: out3 <= 32'h2c216eaa;
      67: out3 <= 32'h2b8ef77d;
      68: out3 <= 32'h2afad269;
      69: out3 <= 32'h2a650525;
      70: out3 <= 32'h29cd9578;
      71: out3 <= 32'h29348937;
      72: out3 <= 32'h2899e64a;
      73: out3 <= 32'h27fdb2a7;
      74: out3 <= 32'h275ff452;
      75: out3 <= 32'h26c0b162;
      76: out3 <= 32'h261feffa;
      77: out3 <= 32'h257db64c;
      78: out3 <= 32'h24da0a9a;
      79: out3 <= 32'h2434f332;
      80: out3 <= 32'h238e7673;
      81: out3 <= 32'h22e69ac8;
      82: out3 <= 32'h223d66a8;
      83: out3 <= 32'h2192e09b;
      84: out3 <= 32'h20e70f32;
      85: out3 <= 32'h2039f90f;
      86: out3 <= 32'h1f8ba4dc;
      87: out3 <= 32'h1edc1953;
      88: out3 <= 32'h1e2b5d38;
      89: out3 <= 32'h1d79775c;
      90: out3 <= 32'h1cc66e99;
      91: out3 <= 32'h1c1249d8;
      92: out3 <= 32'h1b5d100a;
      93: out3 <= 32'h1aa6c82b;
      94: out3 <= 32'h19ef7944;
      95: out3 <= 32'h19372a64;
      96: out3 <= 32'h187de2a7;
      97: out3 <= 32'h17c3a931;
      98: out3 <= 32'h17088531;
      99: out3 <= 32'h164c7ddd;
      100: out3 <= 32'h158f9a76;
      101: out3 <= 32'h14d1e242;
      102: out3 <= 32'h14135c94;
      103: out3 <= 32'h135410c3;
      104: out3 <= 32'h1294062f;
      105: out3 <= 32'h11d3443f;
      106: out3 <= 32'h1111d263;
      107: out3 <= 32'h104fb80e;
      108: out3 <= 32'hf8cfcbe;
      109: out3 <= 32'hec9a7f3;
      110: out3 <= 32'he05c135;
      111: out3 <= 32'hd415013;
      112: out3 <= 32'hc7c5c1e;
      113: out3 <= 32'hbb6ecef;
      114: out3 <= 32'haf10a22;
      115: out3 <= 32'ha2abb59;
      116: out3 <= 32'h9640837;
      117: out3 <= 32'h89cf867;
      118: out3 <= 32'h7d59396;
      119: out3 <= 32'h70de172;
      120: out3 <= 32'h645e9af;
      121: out3 <= 32'h57db403;
      122: out3 <= 32'h4b54825;
      123: out3 <= 32'h3ecadcf;
      124: out3 <= 32'h323ecbe;
      125: out3 <= 32'h25b0caf;
      126: out3 <= 32'h192155f;
      127: out3 <= 32'hc90e90;
      128: out3 <= 32'h0;
      129: out3 <= 32'hff36f170;
      130: out3 <= 32'hfe6deaa1;
      131: out3 <= 32'hfda4f351;
      132: out3 <= 32'hfcdc1342;
      133: out3 <= 32'hfc135231;
      134: out3 <= 32'hfb4ab7db;
      135: out3 <= 32'hfa824bfd;
      136: out3 <= 32'hf9ba1651;
      137: out3 <= 32'hf8f21e8e;
      138: out3 <= 32'hf82a6c6a;
      139: out3 <= 32'hf7630799;
      140: out3 <= 32'hf69bf7c9;
      141: out3 <= 32'hf5d544a7;
      142: out3 <= 32'hf50ef5de;
      143: out3 <= 32'hf4491311;
      144: out3 <= 32'hf383a3e2;
      145: out3 <= 32'hf2beafed;
      146: out3 <= 32'hf1fa3ecb;
      147: out3 <= 32'hf136580d;
      148: out3 <= 32'hf0730342;
      149: out3 <= 32'hefb047f2;
      150: out3 <= 32'heeee2d9d;
      151: out3 <= 32'hee2cbbc1;
      152: out3 <= 32'hed6bf9d1;
      153: out3 <= 32'hecabef3d;
      154: out3 <= 32'hebeca36c;
      155: out3 <= 32'heb2e1dbe;
      156: out3 <= 32'hea70658a;
      157: out3 <= 32'he9b38223;
      158: out3 <= 32'he8f77acf;
      159: out3 <= 32'he83c56cf;
      160: out3 <= 32'he7821d59;
      161: out3 <= 32'he6c8d59c;
      162: out3 <= 32'he61086bc;
      163: out3 <= 32'he55937d5;
      164: out3 <= 32'he4a2eff6;
      165: out3 <= 32'he3edb628;
      166: out3 <= 32'he3399167;
      167: out3 <= 32'he28688a4;
      168: out3 <= 32'he1d4a2c8;
      169: out3 <= 32'he123e6ad;
      170: out3 <= 32'he0745b24;
      171: out3 <= 32'hdfc606f1;
      172: out3 <= 32'hdf18f0ce;
      173: out3 <= 32'hde6d1f65;
      174: out3 <= 32'hddc29958;
      175: out3 <= 32'hdd196538;
      176: out3 <= 32'hdc71898d;
      177: out3 <= 32'hdbcb0cce;
      178: out3 <= 32'hdb25f566;
      179: out3 <= 32'hda8249b4;
      180: out3 <= 32'hd9e01006;
      181: out3 <= 32'hd93f4e9e;
      182: out3 <= 32'hd8a00bae;
      183: out3 <= 32'hd8024d59;
      184: out3 <= 32'hd76619b6;
      185: out3 <= 32'hd6cb76c9;
      186: out3 <= 32'hd6326a88;
      187: out3 <= 32'hd59afadb;
      188: out3 <= 32'hd5052d97;
      189: out3 <= 32'hd4710883;
      190: out3 <= 32'hd3de9156;
      191: out3 <= 32'hd34dcdb4;
      192: out3 <= 32'hd2bec333;
      193: out3 <= 32'hd2317756;
      194: out3 <= 32'hd1a5ef90;
      195: out3 <= 32'hd11c3142;
      196: out3 <= 32'hd09441bb;
      197: out3 <= 32'hd00e2639;
      198: out3 <= 32'hcf89e3e8;
      199: out3 <= 32'hcf077fe1;
      200: out3 <= 32'hce86ff2a;
      201: out3 <= 32'hce0866b8;
      202: out3 <= 32'hcd8bbb6d;
      203: out3 <= 32'hcd110216;
      204: out3 <= 32'hcc983f70;
      205: out3 <= 32'hcc217822;
      206: out3 <= 32'hcbacb0bf;
      207: out3 <= 32'hcb39edca;
      208: out3 <= 32'hcac933ae;
      209: out3 <= 32'hca5a86c4;
      210: out3 <= 32'hc9edeb50;
      211: out3 <= 32'hc9836582;
      212: out3 <= 32'hc91af976;
      213: out3 <= 32'hc8b4ab32;
      214: out3 <= 32'hc8507ea7;
      215: out3 <= 32'hc7ee77b3;
      216: out3 <= 32'hc78e9a1d;
      217: out3 <= 32'hc730e997;
      218: out3 <= 32'hc6d569be;
      219: out3 <= 32'hc67c1e18;
      220: out3 <= 32'hc6250a18;
      221: out3 <= 32'hc5d03118;
      222: out3 <= 32'hc57d965d;
      223: out3 <= 32'hc52d3d18;
      224: out3 <= 32'hc4df2862;
      225: out3 <= 32'hc4935b3c;
      226: out3 <= 32'hc449d892;
      227: out3 <= 32'hc402a33c;
      228: out3 <= 32'hc3bdbdf6;
      229: out3 <= 32'hc37b2b6a;
      230: out3 <= 32'hc33aee27;
      231: out3 <= 32'hc2fd08a9;
      232: out3 <= 32'hc2c17d52;
      233: out3 <= 32'hc2884e6e;
      234: out3 <= 32'hc2517e31;
      235: out3 <= 32'hc21d0eb8;
      236: out3 <= 32'hc1eb0209;
      237: out3 <= 32'hc1bb5a11;
      238: out3 <= 32'hc18e18a7;
      239: out3 <= 32'hc1633f8a;
      240: out3 <= 32'hc13ad060;
      241: out3 <= 32'hc114ccb9;
      242: out3 <= 32'hc0f1360b;
      243: out3 <= 32'hc0d00db6;
      244: out3 <= 32'hc0b15502;
      245: out3 <= 32'hc0950d1d;
      246: out3 <= 32'hc07b371e;
      247: out3 <= 32'hc063d405;
      248: out3 <= 32'hc04ee4b8;
      249: out3 <= 32'hc03c6a07;
      250: out3 <= 32'hc02c64a6;
      251: out3 <= 32'hc01ed535;
      252: out3 <= 32'hc013bc39;
      253: out3 <= 32'hc00b1a20;
      254: out3 <= 32'hc004ef3f;
      255: out3 <= 32'hc0013bd3;
      default: out3 <= 0;
   endcase
   end
// synthesis attribute rom_style of out3 is "block"
endmodule



module D10_83536(addr, out, clk);
   input clk;
   output [31:0] out;
   reg [31:0] out, out2, out3;
   input [7:0] addr;

   always @(posedge clk) begin
      out2 <= out3;
      out <= out2;
   case(addr)
      0: out3 <= 32'h0;
      1: out3 <= 32'hfed26c94;
      2: out3 <= 32'hfda4f351;
      3: out3 <= 32'hfc77ae5e;
      4: out3 <= 32'hfb4ab7db;
      5: out3 <= 32'hfa1e29e5;
      6: out3 <= 32'hf8f21e8e;
      7: out3 <= 32'hf7c6afdc;
      8: out3 <= 32'hf69bf7c9;
      9: out3 <= 32'hf572103d;
      10: out3 <= 32'hf4491311;
      11: out3 <= 32'hf3211a07;
      12: out3 <= 32'hf1fa3ecb;
      13: out3 <= 32'hf0d49af1;
      14: out3 <= 32'hefb047f2;
      15: out3 <= 32'hee8d5f29;
      16: out3 <= 32'hed6bf9d1;
      17: out3 <= 32'hec4c3106;
      18: out3 <= 32'heb2e1dbe;
      19: out3 <= 32'hea11d8c8;
      20: out3 <= 32'he8f77acf;
      21: out3 <= 32'he7df1c50;
      22: out3 <= 32'he6c8d59c;
      23: out3 <= 32'he5b4bed8;
      24: out3 <= 32'he4a2eff6;
      25: out3 <= 32'he39380b6;
      26: out3 <= 32'he28688a4;
      27: out3 <= 32'he17c1f15;
      28: out3 <= 32'he0745b24;
      29: out3 <= 32'hdf6f53b3;
      30: out3 <= 32'hde6d1f65;
      31: out3 <= 32'hdd6dd4a2;
      32: out3 <= 32'hdc71898d;
      33: out3 <= 32'hdb785409;
      34: out3 <= 32'hda8249b4;
      35: out3 <= 32'hd98f7fe6;
      36: out3 <= 32'hd8a00bae;
      37: out3 <= 32'hd7b401d1;
      38: out3 <= 32'hd6cb76c9;
      39: out3 <= 32'hd5e67ec1;
      40: out3 <= 32'hd5052d97;
      41: out3 <= 32'hd42796d5;
      42: out3 <= 32'hd34dcdb4;
      43: out3 <= 32'hd277e518;
      44: out3 <= 32'hd1a5ef90;
      45: out3 <= 32'hd0d7ff51;
      46: out3 <= 32'hd00e2639;
      47: out3 <= 32'hcf4875ca;
      48: out3 <= 32'hce86ff2a;
      49: out3 <= 32'hcdc9d320;
      50: out3 <= 32'hcd110216;
      51: out3 <= 32'hcc5c9c14;
      52: out3 <= 32'hcbacb0bf;
      53: out3 <= 32'hcb014f5b;
      54: out3 <= 32'hca5a86c4;
      55: out3 <= 32'hc9b86572;
      56: out3 <= 32'hc91af976;
      57: out3 <= 32'hc8825077;
      58: out3 <= 32'hc7ee77b3;
      59: out3 <= 32'hc75f7bfe;
      60: out3 <= 32'hc6d569be;
      61: out3 <= 32'hc6504ced;
      62: out3 <= 32'hc5d03118;
      63: out3 <= 32'hc555215a;
      64: out3 <= 32'hc4df2862;
      65: out3 <= 32'hc46e5069;
      66: out3 <= 32'hc402a33c;
      67: out3 <= 32'hc39c2a2f;
      68: out3 <= 32'hc33aee27;
      69: out3 <= 32'hc2def794;
      70: out3 <= 32'hc2884e6e;
      71: out3 <= 32'hc236fa3b;
      72: out3 <= 32'hc1eb0209;
      73: out3 <= 32'hc1a46c6e;
      74: out3 <= 32'hc1633f8a;
      75: out3 <= 32'hc1278104;
      76: out3 <= 32'hc0f1360b;
      77: out3 <= 32'hc0c06355;
      78: out3 <= 32'hc0950d1d;
      79: out3 <= 32'hc06f3726;
      80: out3 <= 32'hc04ee4b8;
      81: out3 <= 32'hc03418a2;
      82: out3 <= 32'hc01ed535;
      83: out3 <= 32'hc00f1c4a;
      84: out3 <= 32'hc004ef3f;
      85: out3 <= 32'hc0004ef5;
      86: out3 <= 32'hc0013bd3;
      87: out3 <= 32'hc007b5c4;
      88: out3 <= 32'hc013bc39;
      89: out3 <= 32'hc0254e27;
      90: out3 <= 32'hc03c6a07;
      91: out3 <= 32'hc0590dd8;
      92: out3 <= 32'hc07b371e;
      93: out3 <= 32'hc0a2e2e3;
      94: out3 <= 32'hc0d00db6;
      95: out3 <= 32'hc102b3ac;
      96: out3 <= 32'hc13ad060;
      97: out3 <= 32'hc1785ef4;
      98: out3 <= 32'hc1bb5a11;
      99: out3 <= 32'hc203bbe8;
      100: out3 <= 32'hc2517e31;
      101: out3 <= 32'hc2a49a2e;
      102: out3 <= 32'hc2fd08a9;
      103: out3 <= 32'hc35ac1f7;
      104: out3 <= 32'hc3bdbdf6;
      105: out3 <= 32'hc425f410;
      106: out3 <= 32'hc4935b3c;
      107: out3 <= 32'hc505e9fb;
      108: out3 <= 32'hc57d965d;
      109: out3 <= 32'hc5fa5603;
      110: out3 <= 32'hc67c1e18;
      111: out3 <= 32'hc702e35c;
      112: out3 <= 32'hc78e9a1d;
      113: out3 <= 32'hc81f363d;
      114: out3 <= 32'hc8b4ab32;
      115: out3 <= 32'hc94eec03;
      116: out3 <= 32'hc9edeb50;
      117: out3 <= 32'hca919b4e;
      118: out3 <= 32'hcb39edca;
      119: out3 <= 32'hcbe6d42b;
      120: out3 <= 32'hcc983f70;
      121: out3 <= 32'hcd4e2037;
      122: out3 <= 32'hce0866b8;
      123: out3 <= 32'hcec702cb;
      124: out3 <= 32'hcf89e3e8;
      125: out3 <= 32'hd050f926;
      126: out3 <= 32'hd11c3142;
      127: out3 <= 32'hd1eb7a9a;
      128: out3 <= 32'hd2bec333;
      129: out3 <= 32'hd395f8ba;
      130: out3 <= 32'hd4710883;
      131: out3 <= 32'hd54fdf8f;
      132: out3 <= 32'hd6326a88;
      133: out3 <= 32'hd71895c9;
      134: out3 <= 32'hd8024d59;
      135: out3 <= 32'hd8ef7cf4;
      136: out3 <= 32'hd9e01006;
      137: out3 <= 32'hdad3f1b1;
      138: out3 <= 32'hdbcb0cce;
      139: out3 <= 32'hdcc54bec;
      140: out3 <= 32'hddc29958;
      141: out3 <= 32'hdec2df18;
      142: out3 <= 32'hdfc606f1;
      143: out3 <= 32'he0cbfa6a;
      144: out3 <= 32'he1d4a2c8;
      145: out3 <= 32'he2dfe917;
      146: out3 <= 32'he3edb628;
      147: out3 <= 32'he4fdf294;
      148: out3 <= 32'he61086bc;
      149: out3 <= 32'he7255ad1;
      150: out3 <= 32'he83c56cf;
      151: out3 <= 32'he9556282;
      152: out3 <= 32'hea70658a;
      153: out3 <= 32'heb8d475b;
      154: out3 <= 32'hecabef3d;
      155: out3 <= 32'hedcc4454;
      156: out3 <= 32'heeee2d9d;
      157: out3 <= 32'hf01191f3;
      158: out3 <= 32'hf136580d;
      159: out3 <= 32'hf25c6688;
      160: out3 <= 32'hf383a3e2;
      161: out3 <= 32'hf4abf67e;
      162: out3 <= 32'hf5d544a7;
      163: out3 <= 32'hf6ff7496;
      164: out3 <= 32'hf82a6c6a;
      165: out3 <= 32'hf9561237;
      166: out3 <= 32'hfa824bfd;
      167: out3 <= 32'hfbaeffb3;
      168: out3 <= 32'hfcdc1342;
      169: out3 <= 32'hfe096c8d;
      170: out3 <= 32'hff36f170;
      171: out3 <= 32'h6487c4;
      172: out3 <= 32'h192155f;
      173: out3 <= 32'h2bf801a;
      174: out3 <= 32'h3ecadcf;
      175: out3 <= 32'h519845e;
      176: out3 <= 32'h645e9af;
      177: out3 <= 32'h771c3b3;
      178: out3 <= 32'h89cf867;
      179: out3 <= 32'h9c76dd8;
      180: out3 <= 32'haf10a22;
      181: out3 <= 32'hc19b374;
      182: out3 <= 32'hd415013;
      183: out3 <= 32'he67c65a;
      184: out3 <= 32'hf8cfcbe;
      185: out3 <= 32'h10b0d9d0;
      186: out3 <= 32'h11d3443f;
      187: out3 <= 32'h12f422db;
      188: out3 <= 32'h14135c94;
      189: out3 <= 32'h1530d881;
      190: out3 <= 32'h164c7ddd;
      191: out3 <= 32'h1766340f;
      192: out3 <= 32'h187de2a7;
      193: out3 <= 32'h19937161;
      194: out3 <= 32'h1aa6c82b;
      195: out3 <= 32'h1bb7cf23;
      196: out3 <= 32'h1cc66e99;
      197: out3 <= 32'h1dd28f15;
      198: out3 <= 32'h1edc1953;
      199: out3 <= 32'h1fe2f64c;
      200: out3 <= 32'h20e70f32;
      201: out3 <= 32'h21e84d76;
      202: out3 <= 32'h22e69ac8;
      203: out3 <= 32'h23e1e117;
      204: out3 <= 32'h24da0a9a;
      205: out3 <= 32'h25cf01c8;
      206: out3 <= 32'h26c0b162;
      207: out3 <= 32'h27af0472;
      208: out3 <= 32'h2899e64a;
      209: out3 <= 32'h2981428c;
      210: out3 <= 32'h2a650525;
      211: out3 <= 32'h2b451a55;
      212: out3 <= 32'h2c216eaa;
      213: out3 <= 32'h2cf9ef09;
      214: out3 <= 32'h2dce88aa;
      215: out3 <= 32'h2e9f291b;
      216: out3 <= 32'h2f6bbe45;
      217: out3 <= 32'h30343667;
      218: out3 <= 32'h30f8801f;
      219: out3 <= 32'h31b88a66;
      220: out3 <= 32'h32744493;
      221: out3 <= 32'h332b9e5e;
      222: out3 <= 32'h33de87de;
      223: out3 <= 32'h348cf190;
      224: out3 <= 32'h3536cc52;
      225: out3 <= 32'h35dc0968;
      226: out3 <= 32'h367c9a7e;
      227: out3 <= 32'h371871a5;
      228: out3 <= 32'h37af8159;
      229: out3 <= 32'h3841bc7f;
      230: out3 <= 32'h38cf1669;
      231: out3 <= 32'h395782d3;
      232: out3 <= 32'h39daf5e8;
      233: out3 <= 32'h3a596442;
      234: out3 <= 32'h3ad2c2e8;
      235: out3 <= 32'h3b470753;
      236: out3 <= 32'h3bb6276e;
      237: out3 <= 32'h3c201994;
      238: out3 <= 32'h3c84d496;
      239: out3 <= 32'h3ce44fb7;
      240: out3 <= 32'h3d3e82ae;
      241: out3 <= 32'h3d9365a8;
      242: out3 <= 32'h3de2f148;
      243: out3 <= 32'h3e2d1ea8;
      244: out3 <= 32'h3e71e759;
      245: out3 <= 32'h3eb14563;
      246: out3 <= 32'h3eeb3347;
      247: out3 <= 32'h3f1fabff;
      248: out3 <= 32'h3f4eaafe;
      249: out3 <= 32'h3f782c30;
      250: out3 <= 32'h3f9c2bfb;
      251: out3 <= 32'h3fbaa740;
      252: out3 <= 32'h3fd39b5a;
      253: out3 <= 32'h3fe7061f;
      254: out3 <= 32'h3ff4e5e0;
      255: out3 <= 32'h3ffd3969;
      default: out3 <= 0;
   endcase
   end
// synthesis attribute rom_style of out3 is "block"
endmodule



module D6_84052(addr, out, clk);
   input clk;
   output [31:0] out;
   reg [31:0] out, out2, out3;
   input [7:0] addr;

   always @(posedge clk) begin
      out2 <= out3;
      out <= out2;
   case(addr)
      0: out3 <= 32'h40000000;
      1: out3 <= 32'h3ffd3969;
      2: out3 <= 32'h3ff4e5e0;
      3: out3 <= 32'h3fe7061f;
      4: out3 <= 32'h3fd39b5a;
      5: out3 <= 32'h3fbaa740;
      6: out3 <= 32'h3f9c2bfb;
      7: out3 <= 32'h3f782c30;
      8: out3 <= 32'h3f4eaafe;
      9: out3 <= 32'h3f1fabff;
      10: out3 <= 32'h3eeb3347;
      11: out3 <= 32'h3eb14563;
      12: out3 <= 32'h3e71e759;
      13: out3 <= 32'h3e2d1ea8;
      14: out3 <= 32'h3de2f148;
      15: out3 <= 32'h3d9365a8;
      16: out3 <= 32'h3d3e82ae;
      17: out3 <= 32'h3ce44fb7;
      18: out3 <= 32'h3c84d496;
      19: out3 <= 32'h3c201994;
      20: out3 <= 32'h3bb6276e;
      21: out3 <= 32'h3b470753;
      22: out3 <= 32'h3ad2c2e8;
      23: out3 <= 32'h3a596442;
      24: out3 <= 32'h39daf5e8;
      25: out3 <= 32'h395782d3;
      26: out3 <= 32'h38cf1669;
      27: out3 <= 32'h3841bc7f;
      28: out3 <= 32'h37af8159;
      29: out3 <= 32'h371871a5;
      30: out3 <= 32'h367c9a7e;
      31: out3 <= 32'h35dc0968;
      32: out3 <= 32'h3536cc52;
      33: out3 <= 32'h348cf190;
      34: out3 <= 32'h33de87de;
      35: out3 <= 32'h332b9e5e;
      36: out3 <= 32'h32744493;
      37: out3 <= 32'h31b88a66;
      38: out3 <= 32'h30f8801f;
      39: out3 <= 32'h30343667;
      40: out3 <= 32'h2f6bbe45;
      41: out3 <= 32'h2e9f291b;
      42: out3 <= 32'h2dce88aa;
      43: out3 <= 32'h2cf9ef09;
      44: out3 <= 32'h2c216eaa;
      45: out3 <= 32'h2b451a55;
      46: out3 <= 32'h2a650525;
      47: out3 <= 32'h2981428c;
      48: out3 <= 32'h2899e64a;
      49: out3 <= 32'h27af0472;
      50: out3 <= 32'h26c0b162;
      51: out3 <= 32'h25cf01c8;
      52: out3 <= 32'h24da0a9a;
      53: out3 <= 32'h23e1e117;
      54: out3 <= 32'h22e69ac8;
      55: out3 <= 32'h21e84d76;
      56: out3 <= 32'h20e70f32;
      57: out3 <= 32'h1fe2f64c;
      58: out3 <= 32'h1edc1953;
      59: out3 <= 32'h1dd28f15;
      60: out3 <= 32'h1cc66e99;
      61: out3 <= 32'h1bb7cf23;
      62: out3 <= 32'h1aa6c82b;
      63: out3 <= 32'h19937161;
      64: out3 <= 32'h187de2a7;
      65: out3 <= 32'h1766340f;
      66: out3 <= 32'h164c7ddd;
      67: out3 <= 32'h1530d881;
      68: out3 <= 32'h14135c94;
      69: out3 <= 32'h12f422db;
      70: out3 <= 32'h11d3443f;
      71: out3 <= 32'h10b0d9d0;
      72: out3 <= 32'hf8cfcbe;
      73: out3 <= 32'he67c65a;
      74: out3 <= 32'hd415013;
      75: out3 <= 32'hc19b374;
      76: out3 <= 32'haf10a22;
      77: out3 <= 32'h9c76dd8;
      78: out3 <= 32'h89cf867;
      79: out3 <= 32'h771c3b3;
      80: out3 <= 32'h645e9af;
      81: out3 <= 32'h519845e;
      82: out3 <= 32'h3ecadcf;
      83: out3 <= 32'h2bf801a;
      84: out3 <= 32'h192155f;
      85: out3 <= 32'h6487c4;
      86: out3 <= 32'hff36f170;
      87: out3 <= 32'hfe096c8d;
      88: out3 <= 32'hfcdc1342;
      89: out3 <= 32'hfbaeffb3;
      90: out3 <= 32'hfa824bfd;
      91: out3 <= 32'hf9561237;
      92: out3 <= 32'hf82a6c6a;
      93: out3 <= 32'hf6ff7496;
      94: out3 <= 32'hf5d544a7;
      95: out3 <= 32'hf4abf67e;
      96: out3 <= 32'hf383a3e2;
      97: out3 <= 32'hf25c6688;
      98: out3 <= 32'hf136580d;
      99: out3 <= 32'hf01191f3;
      100: out3 <= 32'heeee2d9d;
      101: out3 <= 32'hedcc4454;
      102: out3 <= 32'hecabef3d;
      103: out3 <= 32'heb8d475b;
      104: out3 <= 32'hea70658a;
      105: out3 <= 32'he9556282;
      106: out3 <= 32'he83c56cf;
      107: out3 <= 32'he7255ad1;
      108: out3 <= 32'he61086bc;
      109: out3 <= 32'he4fdf294;
      110: out3 <= 32'he3edb628;
      111: out3 <= 32'he2dfe917;
      112: out3 <= 32'he1d4a2c8;
      113: out3 <= 32'he0cbfa6a;
      114: out3 <= 32'hdfc606f1;
      115: out3 <= 32'hdec2df18;
      116: out3 <= 32'hddc29958;
      117: out3 <= 32'hdcc54bec;
      118: out3 <= 32'hdbcb0cce;
      119: out3 <= 32'hdad3f1b1;
      120: out3 <= 32'hd9e01006;
      121: out3 <= 32'hd8ef7cf4;
      122: out3 <= 32'hd8024d59;
      123: out3 <= 32'hd71895c9;
      124: out3 <= 32'hd6326a88;
      125: out3 <= 32'hd54fdf8f;
      126: out3 <= 32'hd4710883;
      127: out3 <= 32'hd395f8ba;
      128: out3 <= 32'hd2bec333;
      129: out3 <= 32'hd1eb7a9a;
      130: out3 <= 32'hd11c3142;
      131: out3 <= 32'hd050f926;
      132: out3 <= 32'hcf89e3e8;
      133: out3 <= 32'hcec702cb;
      134: out3 <= 32'hce0866b8;
      135: out3 <= 32'hcd4e2037;
      136: out3 <= 32'hcc983f70;
      137: out3 <= 32'hcbe6d42b;
      138: out3 <= 32'hcb39edca;
      139: out3 <= 32'hca919b4e;
      140: out3 <= 32'hc9edeb50;
      141: out3 <= 32'hc94eec03;
      142: out3 <= 32'hc8b4ab32;
      143: out3 <= 32'hc81f363d;
      144: out3 <= 32'hc78e9a1d;
      145: out3 <= 32'hc702e35c;
      146: out3 <= 32'hc67c1e18;
      147: out3 <= 32'hc5fa5603;
      148: out3 <= 32'hc57d965d;
      149: out3 <= 32'hc505e9fb;
      150: out3 <= 32'hc4935b3c;
      151: out3 <= 32'hc425f410;
      152: out3 <= 32'hc3bdbdf6;
      153: out3 <= 32'hc35ac1f7;
      154: out3 <= 32'hc2fd08a9;
      155: out3 <= 32'hc2a49a2e;
      156: out3 <= 32'hc2517e31;
      157: out3 <= 32'hc203bbe8;
      158: out3 <= 32'hc1bb5a11;
      159: out3 <= 32'hc1785ef4;
      160: out3 <= 32'hc13ad060;
      161: out3 <= 32'hc102b3ac;
      162: out3 <= 32'hc0d00db6;
      163: out3 <= 32'hc0a2e2e3;
      164: out3 <= 32'hc07b371e;
      165: out3 <= 32'hc0590dd8;
      166: out3 <= 32'hc03c6a07;
      167: out3 <= 32'hc0254e27;
      168: out3 <= 32'hc013bc39;
      169: out3 <= 32'hc007b5c4;
      170: out3 <= 32'hc0013bd3;
      171: out3 <= 32'hc0004ef5;
      172: out3 <= 32'hc004ef3f;
      173: out3 <= 32'hc00f1c4a;
      174: out3 <= 32'hc01ed535;
      175: out3 <= 32'hc03418a2;
      176: out3 <= 32'hc04ee4b8;
      177: out3 <= 32'hc06f3726;
      178: out3 <= 32'hc0950d1d;
      179: out3 <= 32'hc0c06355;
      180: out3 <= 32'hc0f1360b;
      181: out3 <= 32'hc1278104;
      182: out3 <= 32'hc1633f8a;
      183: out3 <= 32'hc1a46c6e;
      184: out3 <= 32'hc1eb0209;
      185: out3 <= 32'hc236fa3b;
      186: out3 <= 32'hc2884e6e;
      187: out3 <= 32'hc2def794;
      188: out3 <= 32'hc33aee27;
      189: out3 <= 32'hc39c2a2f;
      190: out3 <= 32'hc402a33c;
      191: out3 <= 32'hc46e5069;
      192: out3 <= 32'hc4df2862;
      193: out3 <= 32'hc555215a;
      194: out3 <= 32'hc5d03118;
      195: out3 <= 32'hc6504ced;
      196: out3 <= 32'hc6d569be;
      197: out3 <= 32'hc75f7bfe;
      198: out3 <= 32'hc7ee77b3;
      199: out3 <= 32'hc8825077;
      200: out3 <= 32'hc91af976;
      201: out3 <= 32'hc9b86572;
      202: out3 <= 32'hca5a86c4;
      203: out3 <= 32'hcb014f5b;
      204: out3 <= 32'hcbacb0bf;
      205: out3 <= 32'hcc5c9c14;
      206: out3 <= 32'hcd110216;
      207: out3 <= 32'hcdc9d320;
      208: out3 <= 32'hce86ff2a;
      209: out3 <= 32'hcf4875ca;
      210: out3 <= 32'hd00e2639;
      211: out3 <= 32'hd0d7ff51;
      212: out3 <= 32'hd1a5ef90;
      213: out3 <= 32'hd277e518;
      214: out3 <= 32'hd34dcdb4;
      215: out3 <= 32'hd42796d5;
      216: out3 <= 32'hd5052d97;
      217: out3 <= 32'hd5e67ec1;
      218: out3 <= 32'hd6cb76c9;
      219: out3 <= 32'hd7b401d1;
      220: out3 <= 32'hd8a00bae;
      221: out3 <= 32'hd98f7fe6;
      222: out3 <= 32'hda8249b4;
      223: out3 <= 32'hdb785409;
      224: out3 <= 32'hdc71898d;
      225: out3 <= 32'hdd6dd4a2;
      226: out3 <= 32'hde6d1f65;
      227: out3 <= 32'hdf6f53b3;
      228: out3 <= 32'he0745b24;
      229: out3 <= 32'he17c1f15;
      230: out3 <= 32'he28688a4;
      231: out3 <= 32'he39380b6;
      232: out3 <= 32'he4a2eff6;
      233: out3 <= 32'he5b4bed8;
      234: out3 <= 32'he6c8d59c;
      235: out3 <= 32'he7df1c50;
      236: out3 <= 32'he8f77acf;
      237: out3 <= 32'hea11d8c8;
      238: out3 <= 32'heb2e1dbe;
      239: out3 <= 32'hec4c3106;
      240: out3 <= 32'hed6bf9d1;
      241: out3 <= 32'hee8d5f29;
      242: out3 <= 32'hefb047f2;
      243: out3 <= 32'hf0d49af1;
      244: out3 <= 32'hf1fa3ecb;
      245: out3 <= 32'hf3211a07;
      246: out3 <= 32'hf4491311;
      247: out3 <= 32'hf572103d;
      248: out3 <= 32'hf69bf7c9;
      249: out3 <= 32'hf7c6afdc;
      250: out3 <= 32'hf8f21e8e;
      251: out3 <= 32'hfa1e29e5;
      252: out3 <= 32'hfb4ab7db;
      253: out3 <= 32'hfc77ae5e;
      254: out3 <= 32'hfda4f351;
      255: out3 <= 32'hfed26c94;
      default: out3 <= 0;
   endcase
   end
// synthesis attribute rom_style of out3 is "block"
endmodule



// Latency: 12
// Gap: 1
module codeBlock81668(clk, reset, next_in, next_out,
   i1_in,
   X0_in, Y0,
   X1_in, Y1,
   X2_in, Y2,
   X3_in, Y3,
   X4_in, Y4,
   X5_in, Y5,
   X6_in, Y6,
   X7_in, Y7);

   output next_out;
   input clk, reset, next_in;

   reg next;
   input [7:0] i1_in;
   reg [7:0] i1;

   input [31:0] X0_in,
      X1_in,
      X2_in,
      X3_in,
      X4_in,
      X5_in,
      X6_in,
      X7_in;

   reg   [31:0] X0,
      X1,
      X2,
      X3,
      X4,
      X5,
      X6,
      X7;

   output [31:0] Y0,
      Y1,
      Y2,
      Y3,
      Y4,
      Y5,
      Y6,
      Y7;

   shiftRegFIFO #(11, 1) shiftFIFO_85782(.X(next), .Y(next_out), .clk(clk));


   wire signed [31:0] a105;
   wire signed [31:0] a82;
   wire signed [31:0] a108;
   wire signed [31:0] a86;
   wire signed [31:0] a109;
   wire signed [31:0] a110;
   wire signed [31:0] a113;
   wire signed [31:0] a114;
   wire signed [31:0] a117;
   wire signed [31:0] a118;
   reg signed [31:0] tm362;
   reg signed [31:0] tm366;
   reg signed [31:0] tm378;
   reg signed [31:0] tm382;
   reg signed [31:0] tm394;
   reg signed [31:0] tm398;
   reg signed [31:0] tm410;
   reg signed [31:0] tm421;
   reg signed [31:0] tm363;
   reg signed [31:0] tm367;
   reg signed [31:0] tm379;
   reg signed [31:0] tm383;
   reg signed [31:0] tm395;
   reg signed [31:0] tm399;
   reg signed [31:0] tm411;
   reg signed [31:0] tm422;
   wire signed [31:0] tm26;
   wire signed [31:0] a87;
   wire signed [31:0] tm27;
   wire signed [31:0] a89;
   wire signed [31:0] tm28;
   wire signed [31:0] a93;
   wire signed [31:0] tm29;
   wire signed [31:0] a95;
   wire signed [31:0] tm30;
   wire signed [31:0] a99;
   wire signed [31:0] tm31;
   wire signed [31:0] a101;
   reg signed [31:0] tm364;
   reg signed [31:0] tm368;
   reg signed [31:0] tm380;
   reg signed [31:0] tm384;
   reg signed [31:0] tm396;
   reg signed [31:0] tm400;
   reg signed [31:0] tm412;
   reg signed [31:0] tm423;
   reg signed [31:0] tm84;
   reg signed [31:0] tm85;
   reg signed [31:0] tm88;
   reg signed [31:0] tm89;
   reg signed [31:0] tm92;
   reg signed [31:0] tm93;
   reg signed [31:0] tm365;
   reg signed [31:0] tm369;
   reg signed [31:0] tm381;
   reg signed [31:0] tm385;
   reg signed [31:0] tm397;
   reg signed [31:0] tm401;
   reg signed [31:0] tm413;
   reg signed [31:0] tm424;
   reg signed [31:0] tm414;
   reg signed [31:0] tm425;
   reg signed [31:0] tm415;
   reg signed [31:0] tm426;
   reg signed [31:0] tm416;
   reg signed [31:0] tm427;
   reg signed [31:0] tm417;
   reg signed [31:0] tm428;
   reg signed [31:0] tm418;
   reg signed [31:0] tm429;
   wire signed [31:0] a88;
   wire signed [31:0] a90;
   wire signed [31:0] a91;
   wire signed [31:0] a92;
   wire signed [31:0] a94;
   wire signed [31:0] a96;
   wire signed [31:0] a97;
   wire signed [31:0] a98;
   wire signed [31:0] a100;
   wire signed [31:0] a102;
   wire signed [31:0] a103;
   wire signed [31:0] a104;
   reg signed [31:0] tm419;
   reg signed [31:0] tm430;
   wire signed [31:0] Y0;
   wire signed [31:0] Y1;
   wire signed [31:0] Y2;
   wire signed [31:0] Y3;
   wire signed [31:0] Y4;
   wire signed [31:0] Y5;
   wire signed [31:0] Y6;
   wire signed [31:0] Y7;
   reg signed [31:0] tm420;
   reg signed [31:0] tm431;


   assign a105 = X0;
   assign a82 = a105;
   assign a108 = X1;
   assign a86 = a108;
   assign a109 = X2;
   assign a110 = X3;
   assign a113 = X4;
   assign a114 = X5;
   assign a117 = X6;
   assign a118 = X7;
   assign a87 = tm26;
   assign a89 = tm27;
   assign a93 = tm28;
   assign a95 = tm29;
   assign a99 = tm30;
   assign a101 = tm31;
   assign Y0 = tm420;
   assign Y1 = tm431;

   D4_82246 instD4inst0_82246(.addr(i1[7:0]), .out(tm26), .clk(clk));

   D9_82504 instD9inst0_82504(.addr(i1[7:0]), .out(tm29), .clk(clk));

   D8_82762 instD8inst0_82762(.addr(i1[7:0]), .out(tm27), .clk(clk));

   D5_83278 instD5inst0_83278(.addr(i1[7:0]), .out(tm28), .clk(clk));

   D10_83536 instD10inst0_83536(.addr(i1[7:0]), .out(tm31), .clk(clk));

   D6_84052 instD6inst0_84052(.addr(i1[7:0]), .out(tm30), .clk(clk));

    multfix #(32, 6) m81767(.a(tm84), .b(tm365), .clk(clk), .q_sc(a88), .q_unsc(), .rst(reset));
    multfix #(32, 6) m81789(.a(tm85), .b(tm369), .clk(clk), .q_sc(a90), .q_unsc(), .rst(reset));
    multfix #(32, 6) m81807(.a(tm85), .b(tm365), .clk(clk), .q_sc(a91), .q_unsc(), .rst(reset));
    multfix #(32, 6) m81818(.a(tm84), .b(tm369), .clk(clk), .q_sc(a92), .q_unsc(), .rst(reset));
    multfix #(32, 6) m81847(.a(tm88), .b(tm381), .clk(clk), .q_sc(a94), .q_unsc(), .rst(reset));
    multfix #(32, 6) m81869(.a(tm89), .b(tm385), .clk(clk), .q_sc(a96), .q_unsc(), .rst(reset));
    multfix #(32, 6) m81887(.a(tm89), .b(tm381), .clk(clk), .q_sc(a97), .q_unsc(), .rst(reset));
    multfix #(32, 6) m81898(.a(tm88), .b(tm385), .clk(clk), .q_sc(a98), .q_unsc(), .rst(reset));
    multfix #(32, 6) m81927(.a(tm92), .b(tm397), .clk(clk), .q_sc(a100), .q_unsc(), .rst(reset));
    multfix #(32, 6) m81949(.a(tm93), .b(tm401), .clk(clk), .q_sc(a102), .q_unsc(), .rst(reset));
    multfix #(32, 6) m81967(.a(tm93), .b(tm397), .clk(clk), .q_sc(a103), .q_unsc(), .rst(reset));
    multfix #(32, 6) m81978(.a(tm92), .b(tm401), .clk(clk), .q_sc(a104), .q_unsc(), .rst(reset));
    subfxp #(32, 1) sub81796(.a(a88), .b(a90), .clk(clk), .q(Y2));    // 10
    addfxp #(32, 1) add81825(.a(a91), .b(a92), .clk(clk), .q(Y3));    // 10
    subfxp #(32, 1) sub81876(.a(a94), .b(a96), .clk(clk), .q(Y4));    // 10
    addfxp #(32, 1) add81905(.a(a97), .b(a98), .clk(clk), .q(Y5));    // 10
    subfxp #(32, 1) sub81956(.a(a100), .b(a102), .clk(clk), .q(Y6));    // 10
    addfxp #(32, 1) add81985(.a(a103), .b(a104), .clk(clk), .q(Y7));    // 10


   always @(posedge clk) begin
      if (reset == 1) begin
         tm84 <= 0;
         tm365 <= 0;
         tm85 <= 0;
         tm369 <= 0;
         tm85 <= 0;
         tm365 <= 0;
         tm84 <= 0;
         tm369 <= 0;
         tm88 <= 0;
         tm381 <= 0;
         tm89 <= 0;
         tm385 <= 0;
         tm89 <= 0;
         tm381 <= 0;
         tm88 <= 0;
         tm385 <= 0;
         tm92 <= 0;
         tm397 <= 0;
         tm93 <= 0;
         tm401 <= 0;
         tm93 <= 0;
         tm397 <= 0;
         tm92 <= 0;
         tm401 <= 0;
      end
      else begin
         i1 <= i1_in;
         X0 <= X0_in;
         X1 <= X1_in;
         X2 <= X2_in;
         X3 <= X3_in;
         X4 <= X4_in;
         X5 <= X5_in;
         X6 <= X6_in;
         X7 <= X7_in;
         next <= next_in;
         tm362 <= a109;
         tm366 <= a110;
         tm378 <= a113;
         tm382 <= a114;
         tm394 <= a117;
         tm398 <= a118;
         tm410 <= a82;
         tm421 <= a86;
         tm363 <= tm362;
         tm367 <= tm366;
         tm379 <= tm378;
         tm383 <= tm382;
         tm395 <= tm394;
         tm399 <= tm398;
         tm411 <= tm410;
         tm422 <= tm421;
         tm364 <= tm363;
         tm368 <= tm367;
         tm380 <= tm379;
         tm384 <= tm383;
         tm396 <= tm395;
         tm400 <= tm399;
         tm412 <= tm411;
         tm423 <= tm422;
         tm84 <= a87;
         tm85 <= a89;
         tm88 <= a93;
         tm89 <= a95;
         tm92 <= a99;
         tm93 <= a101;
         tm365 <= tm364;
         tm369 <= tm368;
         tm381 <= tm380;
         tm385 <= tm384;
         tm397 <= tm396;
         tm401 <= tm400;
         tm413 <= tm412;
         tm424 <= tm423;
         tm414 <= tm413;
         tm425 <= tm424;
         tm415 <= tm414;
         tm426 <= tm425;
         tm416 <= tm415;
         tm427 <= tm426;
         tm417 <= tm416;
         tm428 <= tm427;
         tm418 <= tm417;
         tm429 <= tm428;
         tm419 <= tm418;
         tm430 <= tm429;
         tm420 <= tm419;
         tm431 <= tm430;
      end
   end
endmodule

// Latency: 3
// Gap: 1
module codeBlock84057(clk, reset, next_in, next_out,
   X0_in, Y0,
   X1_in, Y1,
   X2_in, Y2,
   X3_in, Y3,
   X4_in, Y4,
   X5_in, Y5,
   X6_in, Y6,
   X7_in, Y7);

   output next_out;
   input clk, reset, next_in;

   reg next;

   input [31:0] X0_in,
      X1_in,
      X2_in,
      X3_in,
      X4_in,
      X5_in,
      X6_in,
      X7_in;

   reg   [31:0] X0,
      X1,
      X2,
      X3,
      X4,
      X5,
      X6,
      X7;

   output [31:0] Y0,
      Y1,
      Y2,
      Y3,
      Y4,
      Y5,
      Y6,
      Y7;

   shiftRegFIFO #(2, 1) shiftFIFO_85785(.X(next), .Y(next_out), .clk(clk));


   wire signed [31:0] a17;
   wire signed [31:0] a18;
   wire signed [31:0] a19;
   wire signed [31:0] a20;
   wire signed [31:0] a25;
   wire signed [31:0] a26;
   wire signed [31:0] a27;
   wire signed [31:0] a28;
   wire signed [31:0] t113;
   wire signed [31:0] t114;
   wire signed [31:0] t115;
   wire signed [31:0] t116;
   wire signed [31:0] t117;
   wire signed [31:0] t118;
   wire signed [31:0] t119;
   wire signed [31:0] t120;
   wire signed [31:0] t121;
   wire signed [31:0] t122;
   wire signed [31:0] t123;
   wire signed [31:0] t124;
   wire signed [31:0] Y0;
   wire signed [31:0] Y1;
   wire signed [31:0] Y4;
   wire signed [31:0] Y5;
   wire signed [31:0] t125;
   wire signed [31:0] t126;
   wire signed [31:0] t127;
   wire signed [31:0] t128;
   wire signed [31:0] Y2;
   wire signed [31:0] Y3;
   wire signed [31:0] Y6;
   wire signed [31:0] Y7;


   assign a17 = X0;
   assign a18 = X4;
   assign a19 = X1;
   assign a20 = X5;
   assign a25 = X2;
   assign a26 = X6;
   assign a27 = X3;
   assign a28 = X7;
   assign Y0 = t121;
   assign Y1 = t122;
   assign Y4 = t123;
   assign Y5 = t124;
   assign Y2 = t125;
   assign Y3 = t126;
   assign Y6 = t127;
   assign Y7 = t128;

    addfxp #(32, 1) add84069(.a(a17), .b(a18), .clk(clk), .q(t113));    // 0
    addfxp #(32, 1) add84084(.a(a19), .b(a20), .clk(clk), .q(t114));    // 0
    subfxp #(32, 1) sub84099(.a(a17), .b(a18), .clk(clk), .q(t115));    // 0
    subfxp #(32, 1) sub84114(.a(a19), .b(a20), .clk(clk), .q(t116));    // 0
    addfxp #(32, 1) add84129(.a(a25), .b(a26), .clk(clk), .q(t117));    // 0
    addfxp #(32, 1) add84144(.a(a27), .b(a28), .clk(clk), .q(t118));    // 0
    subfxp #(32, 1) sub84159(.a(a25), .b(a26), .clk(clk), .q(t119));    // 0
    subfxp #(32, 1) sub84174(.a(a27), .b(a28), .clk(clk), .q(t120));    // 0
    addfxp #(32, 1) add84181(.a(t113), .b(t117), .clk(clk), .q(t121));    // 1
    addfxp #(32, 1) add84188(.a(t114), .b(t118), .clk(clk), .q(t122));    // 1
    subfxp #(32, 1) sub84195(.a(t113), .b(t117), .clk(clk), .q(t123));    // 1
    subfxp #(32, 1) sub84202(.a(t114), .b(t118), .clk(clk), .q(t124));    // 1
    addfxp #(32, 1) add84225(.a(t115), .b(t120), .clk(clk), .q(t125));    // 1
    subfxp #(32, 1) sub84232(.a(t116), .b(t119), .clk(clk), .q(t126));    // 1
    subfxp #(32, 1) sub84239(.a(t115), .b(t120), .clk(clk), .q(t127));    // 1
    addfxp #(32, 1) add84246(.a(t116), .b(t119), .clk(clk), .q(t128));    // 1


   always @(posedge clk) begin
      if (reset == 1) begin
      end
      else begin
         X0 <= X0_in;
         X1 <= X1_in;
         X2 <= X2_in;
         X3 <= X3_in;
         X4 <= X4_in;
         X5 <= X5_in;
         X6 <= X6_in;
         X7 <= X7_in;
         next <= next_in;
      end
   end
endmodule

// Latency: 197
// Gap: 256
module rc84270(clk, reset, next, next_out,
   X0, Y0,
   X1, Y1,
   X2, Y2,
   X3, Y3,
   X4, Y4,
   X5, Y5,
   X6, Y6,
   X7, Y7);

   output next_out;
   input clk, reset, next;

   input [31:0] X0,
      X1,
      X2,
      X3,
      X4,
      X5,
      X6,
      X7;

   output [31:0] Y0,
      Y1,
      Y2,
      Y3,
      Y4,
      Y5,
      Y6,
      Y7;

   wire [63:0] t0;
   wire [63:0] s0;
   assign t0 = {X0, X1};
   wire [63:0] t1;
   wire [63:0] s1;
   assign t1 = {X2, X3};
   wire [63:0] t2;
   wire [63:0] s2;
   assign t2 = {X4, X5};
   wire [63:0] t3;
   wire [63:0] s3;
   assign t3 = {X6, X7};
   assign Y0 = s0[63:32];
   assign Y1 = s0[31:0];
   assign Y2 = s1[63:32];
   assign Y3 = s1[31:0];
   assign Y4 = s2[63:32];
   assign Y5 = s2[31:0];
   assign Y6 = s3[63:32];
   assign Y7 = s3[31:0];

   perm84268 instPerm85786(.x0(t0), .y0(s0),
    .x1(t1), .y1(s1),
    .x2(t2), .y2(s2),
    .x3(t3), .y3(s3),
   .clk(clk), .next(next), .next_out(next_out), .reset(reset)
);



endmodule

// Latency: 197
// Gap: 256
module perm84268(clk, next, reset, next_out,
   x0, y0,
   x1, y1,
   x2, y2,
   x3, y3);
   parameter numBanks = 4;
   parameter logBanks = 2;
   parameter depth = 256;
   parameter logDepth = 8;
   parameter width = 64;

   input [width-1:0]  x0;
   output [width-1:0]  y0;
   wire [width-1:0]  ybuff0;
   input [width-1:0]  x1;
   output [width-1:0]  y1;
   wire [width-1:0]  ybuff1;
   input [width-1:0]  x2;
   output [width-1:0]  y2;
   wire [width-1:0]  ybuff2;
   input [width-1:0]  x3;
   output [width-1:0]  y3;
   wire [width-1:0]  ybuff3;
   input 	      clk, next, reset;
   output 	     next_out;

   wire    	     next0;

   reg              inFlip0, outFlip0;
   reg              inActive, outActive;

   wire [logBanks-1:0] inBank0, outBank0;
   wire [logDepth-1:0] inAddr0, outAddr0;
   wire [logBanks-1:0] outBank_a0;
   wire [logDepth-1:0] outAddr_a0;
   wire [logDepth+logBanks-1:0] addr0, addr0b, addr0c;
   wire [logBanks-1:0] inBank1, outBank1;
   wire [logDepth-1:0] inAddr1, outAddr1;
   wire [logBanks-1:0] outBank_a1;
   wire [logDepth-1:0] outAddr_a1;
   wire [logDepth+logBanks-1:0] addr1, addr1b, addr1c;
   wire [logBanks-1:0] inBank2, outBank2;
   wire [logDepth-1:0] inAddr2, outAddr2;
   wire [logBanks-1:0] outBank_a2;
   wire [logDepth-1:0] outAddr_a2;
   wire [logDepth+logBanks-1:0] addr2, addr2b, addr2c;
   wire [logBanks-1:0] inBank3, outBank3;
   wire [logDepth-1:0] inAddr3, outAddr3;
   wire [logBanks-1:0] outBank_a3;
   wire [logDepth-1:0] outAddr_a3;
   wire [logDepth+logBanks-1:0] addr3, addr3b, addr3c;


   reg [logDepth-1:0]  inCount, outCount, outCount_d, outCount_dd, outCount_for_rd_addr, outCount_for_rd_data;  

   assign    addr0 = {inCount, 2'd0};
   assign    addr0b = {outCount, 2'd0};
   assign    addr0c = {outCount_for_rd_addr, 2'd0};
   assign    addr1 = {inCount, 2'd1};
   assign    addr1b = {outCount, 2'd1};
   assign    addr1c = {outCount_for_rd_addr, 2'd1};
   assign    addr2 = {inCount, 2'd2};
   assign    addr2b = {outCount, 2'd2};
   assign    addr2c = {outCount_for_rd_addr, 2'd2};
   assign    addr3 = {inCount, 2'd3};
   assign    addr3b = {outCount, 2'd3};
   assign    addr3c = {outCount_for_rd_addr, 2'd3};
    wire [width+logDepth-1:0] w_0_0, w_0_1, w_0_2, w_0_3, w_1_0, w_1_1, w_1_2, w_1_3, w_2_0, w_2_1, w_2_2, w_2_3;

    reg [width-1:0] z_0_0;
    reg [width-1:0] z_0_1;
    reg [width-1:0] z_0_2;
    reg [width-1:0] z_0_3;
    wire [width-1:0] z_1_0, z_1_1, z_1_2, z_1_3, z_2_0, z_2_1, z_2_2, z_2_3;

    wire [logDepth-1:0] u_0_0, u_0_1, u_0_2, u_0_3, u_1_0, u_1_1, u_1_2, u_1_3, u_2_0, u_2_1, u_2_2, u_2_3;

    reg inFlip1, outFlip1;
    always @(posedge clk) begin
        inFlip1 <= inFlip0;
        outFlip1 <= outFlip0;
    end

   assign inBank0[0] = addr0[2] ^ addr0[0];
   assign inBank0[1] = addr0[3] ^ addr0[1];
   assign inAddr0[0] = addr0[4];
   assign inAddr0[1] = addr0[5];
   assign inAddr0[2] = addr0[6];
   assign inAddr0[3] = addr0[7];
   assign inAddr0[4] = addr0[8];
   assign inAddr0[5] = addr0[9];
   assign inAddr0[6] = addr0[0];
   assign inAddr0[7] = addr0[1];
   assign outBank0[0] = addr0b[8] ^ addr0b[0];
   assign outBank0[1] = addr0b[9] ^ addr0b[1];
   assign outAddr0[0] = addr0b[2];
   assign outAddr0[1] = addr0b[3];
   assign outAddr0[2] = addr0b[4];
   assign outAddr0[3] = addr0b[5];
   assign outAddr0[4] = addr0b[6];
   assign outAddr0[5] = addr0b[7];
   assign outAddr0[6] = addr0b[8];
   assign outAddr0[7] = addr0b[9];
   assign outBank_a0[0] = addr0c[8] ^ addr0c[0];
   assign outBank_a0[1] = addr0c[9] ^ addr0c[1];
   assign outAddr_a0[0] = addr0c[2];
   assign outAddr_a0[1] = addr0c[3];
   assign outAddr_a0[2] = addr0c[4];
   assign outAddr_a0[3] = addr0c[5];
   assign outAddr_a0[4] = addr0c[6];
   assign outAddr_a0[5] = addr0c[7];
   assign outAddr_a0[6] = addr0c[8];
   assign outAddr_a0[7] = addr0c[9];

   assign inBank1[0] = addr1[2] ^ addr1[0];
   assign inBank1[1] = addr1[3] ^ addr1[1];
   assign inAddr1[0] = addr1[4];
   assign inAddr1[1] = addr1[5];
   assign inAddr1[2] = addr1[6];
   assign inAddr1[3] = addr1[7];
   assign inAddr1[4] = addr1[8];
   assign inAddr1[5] = addr1[9];
   assign inAddr1[6] = addr1[0];
   assign inAddr1[7] = addr1[1];
   assign outBank1[0] = addr1b[8] ^ addr1b[0];
   assign outBank1[1] = addr1b[9] ^ addr1b[1];
   assign outAddr1[0] = addr1b[2];
   assign outAddr1[1] = addr1b[3];
   assign outAddr1[2] = addr1b[4];
   assign outAddr1[3] = addr1b[5];
   assign outAddr1[4] = addr1b[6];
   assign outAddr1[5] = addr1b[7];
   assign outAddr1[6] = addr1b[8];
   assign outAddr1[7] = addr1b[9];
   assign outBank_a1[0] = addr1c[8] ^ addr1c[0];
   assign outBank_a1[1] = addr1c[9] ^ addr1c[1];
   assign outAddr_a1[0] = addr1c[2];
   assign outAddr_a1[1] = addr1c[3];
   assign outAddr_a1[2] = addr1c[4];
   assign outAddr_a1[3] = addr1c[5];
   assign outAddr_a1[4] = addr1c[6];
   assign outAddr_a1[5] = addr1c[7];
   assign outAddr_a1[6] = addr1c[8];
   assign outAddr_a1[7] = addr1c[9];

   assign inBank2[0] = addr2[2] ^ addr2[0];
   assign inBank2[1] = addr2[3] ^ addr2[1];
   assign inAddr2[0] = addr2[4];
   assign inAddr2[1] = addr2[5];
   assign inAddr2[2] = addr2[6];
   assign inAddr2[3] = addr2[7];
   assign inAddr2[4] = addr2[8];
   assign inAddr2[5] = addr2[9];
   assign inAddr2[6] = addr2[0];
   assign inAddr2[7] = addr2[1];
   assign outBank2[0] = addr2b[8] ^ addr2b[0];
   assign outBank2[1] = addr2b[9] ^ addr2b[1];
   assign outAddr2[0] = addr2b[2];
   assign outAddr2[1] = addr2b[3];
   assign outAddr2[2] = addr2b[4];
   assign outAddr2[3] = addr2b[5];
   assign outAddr2[4] = addr2b[6];
   assign outAddr2[5] = addr2b[7];
   assign outAddr2[6] = addr2b[8];
   assign outAddr2[7] = addr2b[9];
   assign outBank_a2[0] = addr2c[8] ^ addr2c[0];
   assign outBank_a2[1] = addr2c[9] ^ addr2c[1];
   assign outAddr_a2[0] = addr2c[2];
   assign outAddr_a2[1] = addr2c[3];
   assign outAddr_a2[2] = addr2c[4];
   assign outAddr_a2[3] = addr2c[5];
   assign outAddr_a2[4] = addr2c[6];
   assign outAddr_a2[5] = addr2c[7];
   assign outAddr_a2[6] = addr2c[8];
   assign outAddr_a2[7] = addr2c[9];

   assign inBank3[0] = addr3[2] ^ addr3[0];
   assign inBank3[1] = addr3[3] ^ addr3[1];
   assign inAddr3[0] = addr3[4];
   assign inAddr3[1] = addr3[5];
   assign inAddr3[2] = addr3[6];
   assign inAddr3[3] = addr3[7];
   assign inAddr3[4] = addr3[8];
   assign inAddr3[5] = addr3[9];
   assign inAddr3[6] = addr3[0];
   assign inAddr3[7] = addr3[1];
   assign outBank3[0] = addr3b[8] ^ addr3b[0];
   assign outBank3[1] = addr3b[9] ^ addr3b[1];
   assign outAddr3[0] = addr3b[2];
   assign outAddr3[1] = addr3b[3];
   assign outAddr3[2] = addr3b[4];
   assign outAddr3[3] = addr3b[5];
   assign outAddr3[4] = addr3b[6];
   assign outAddr3[5] = addr3b[7];
   assign outAddr3[6] = addr3b[8];
   assign outAddr3[7] = addr3b[9];
   assign outBank_a3[0] = addr3c[8] ^ addr3c[0];
   assign outBank_a3[1] = addr3c[9] ^ addr3c[1];
   assign outAddr_a3[0] = addr3c[2];
   assign outAddr_a3[1] = addr3c[3];
   assign outAddr_a3[2] = addr3c[4];
   assign outAddr_a3[3] = addr3c[5];
   assign outAddr_a3[4] = addr3c[6];
   assign outAddr_a3[5] = addr3c[7];
   assign outAddr_a3[6] = addr3c[8];
   assign outAddr_a3[7] = addr3c[9];

   nextReg #(193, 8) nextReg_85791(.X(next), .Y(next0), .reset(reset), .clk(clk));


   shiftRegFIFO #(4, 1) shiftFIFO_85794(.X(next0), .Y(next_out), .clk(clk));


   memArray1024_84268 #(numBanks, logBanks, depth, logDepth, width)
     memSys(.inFlip(inFlip1), .outFlip(outFlip1), .next(next), .reset(reset),
        .x0(w_2_0[width+logDepth-1:logDepth]), .y0(ybuff0),
        .inAddr0(w_2_0[logDepth-1:0]),
        .outAddr0(u_2_0), 
        .x1(w_2_1[width+logDepth-1:logDepth]), .y1(ybuff1),
        .inAddr1(w_2_1[logDepth-1:0]),
        .outAddr1(u_2_1), 
        .x2(w_2_2[width+logDepth-1:logDepth]), .y2(ybuff2),
        .inAddr2(w_2_2[logDepth-1:0]),
        .outAddr2(u_2_2), 
        .x3(w_2_3[width+logDepth-1:logDepth]), .y3(ybuff3),
        .inAddr3(w_2_3[logDepth-1:0]),
        .outAddr3(u_2_3), 
        .clk(clk));

   always @(posedge clk) begin
      if (reset == 1) begin
      z_0_0 <= 0;
      z_0_1 <= 0;
      z_0_2 <= 0;
      z_0_3 <= 0;
         inFlip0 <= 0; outFlip0 <= 1; outCount <= 0; inCount <= 0;
        outCount_for_rd_addr <= 0;
        outCount_for_rd_data <= 0;
      end
      else begin
          outCount_d <= outCount;
          outCount_dd <= outCount_d;
         if (inCount == 192)
            outCount_for_rd_addr <= 0;
         else
            outCount_for_rd_addr <= outCount_for_rd_addr+1;
         if (inCount == 195)
            outCount_for_rd_data <= 0;
         else
            outCount_for_rd_data <= outCount_for_rd_data+1;
      z_0_0 <= ybuff0;
      z_0_1 <= ybuff1;
      z_0_2 <= ybuff2;
      z_0_3 <= ybuff3;
         if (inCount == 192) begin
            outFlip0 <= ~outFlip0;
            outCount <= 0;
         end
         else
            outCount <= outCount+1;
         if (inCount == 255) begin
            inFlip0 <= ~inFlip0;
         end
         if (next == 1) begin
            if (inCount >= 192)
               inFlip0 <= ~inFlip0;
            inCount <= 0;
         end
         else
            inCount <= inCount + 1;
      end
   end
    assign w_0_0 = {x0, inAddr0};
    assign w_0_1 = {x1, inAddr1};
    assign w_0_2 = {x2, inAddr2};
    assign w_0_3 = {x3, inAddr3};
    assign y0 = z_2_0;
    assign y1 = z_2_1;
    assign y2 = z_2_2;
    assign y3 = z_2_3;
    assign u_0_0 = outAddr_a0;
    assign u_0_1 = outAddr_a1;
    assign u_0_2 = outAddr_a2;
    assign u_0_3 = outAddr_a3;
    wire wr_ctrl_st_0;
    assign wr_ctrl_st_0 = inCount[1];

    switch #(logDepth+width) in_sw_0_0(.x0(w_0_0), .x1(w_0_2), .y0(w_1_0), .y1(w_1_2), .ctrl(wr_ctrl_st_0));
    switch #(logDepth+width) in_sw_0_1(.x0(w_0_1), .x1(w_0_3), .y0(w_1_1), .y1(w_1_3), .ctrl(wr_ctrl_st_0));
    reg [width+logDepth-1:0] w_1_0_pipe;
    reg [width+logDepth-1:0] w_1_1_pipe;
    reg [width+logDepth-1:0] w_1_2_pipe;
    reg [width+logDepth-1:0] w_1_3_pipe;

    always @(posedge clk) begin
        w_1_0_pipe <= w_1_0;
        w_1_1_pipe <= w_1_1;
        w_1_2_pipe <= w_1_2;
        w_1_3_pipe <= w_1_3;
    end

    wire wr_ctrl_st_1;
    reg wr_ctrl_st_1_1;
    always @(posedge clk) begin
        wr_ctrl_st_1_1 <= inCount[0];
    end
    assign wr_ctrl_st_1 = wr_ctrl_st_1_1;

    switch #(logDepth+width) in_sw_1_0(.x0(w_1_0_pipe), .x1(w_1_1_pipe), .y0(w_2_0), .y1(w_2_1), .ctrl(wr_ctrl_st_1));
    switch #(logDepth+width) in_sw_1_1(.x0(w_1_2_pipe), .x1(w_1_3_pipe), .y0(w_2_2), .y1(w_2_3), .ctrl(wr_ctrl_st_1));
    wire rdd_ctrl_st_0;
    assign rdd_ctrl_st_0 = outCount_for_rd_data[7];

    switch #(width) out_sw_0_0(.x0(z_0_0), .x1(z_0_2), .y0(z_1_0), .y1(z_1_2), .ctrl(rdd_ctrl_st_0));
    switch #(width) out_sw_0_1(.x0(z_0_1), .x1(z_0_3), .y0(z_1_1), .y1(z_1_3), .ctrl(rdd_ctrl_st_0));
    reg [width-1:0] z_1_0_pipe;
    reg [width-1:0] z_1_1_pipe;
    reg [width-1:0] z_1_2_pipe;
    reg [width-1:0] z_1_3_pipe;

    always @(posedge clk) begin
        z_1_0_pipe <= z_1_0;
        z_1_1_pipe <= z_1_1;
        z_1_2_pipe <= z_1_2;
        z_1_3_pipe <= z_1_3;
    end

    wire rdd_ctrl_st_1;
    reg rdd_ctrl_st_1_1;
    always @(posedge clk) begin
        rdd_ctrl_st_1_1 <= outCount_for_rd_data[6];

    end
    assign rdd_ctrl_st_1 = rdd_ctrl_st_1_1;

    switch #(width) out_sw_1_0(.x0(z_1_0_pipe), .x1(z_1_1_pipe), .y0(z_2_0), .y1(z_2_1), .ctrl(rdd_ctrl_st_1));
    switch #(width) out_sw_1_1(.x0(z_1_2_pipe), .x1(z_1_3_pipe), .y0(z_2_2), .y1(z_2_3), .ctrl(rdd_ctrl_st_1));
    wire rda_ctrl_st_0;
    assign rda_ctrl_st_0 = outCount_for_rd_addr[7];

    switch #(logDepth) rdaddr_sw_0_0(.x0(u_0_0), .x1(u_0_2), .y0(u_1_0), .y1(u_1_2), .ctrl(rda_ctrl_st_0));
    switch #(logDepth) rdaddr_sw_0_1(.x0(u_0_1), .x1(u_0_3), .y0(u_1_1), .y1(u_1_3), .ctrl(rda_ctrl_st_0));
    reg [logDepth-1:0] u_1_0_pipe;
    reg [logDepth-1:0] u_1_1_pipe;
    reg [logDepth-1:0] u_1_2_pipe;
    reg [logDepth-1:0] u_1_3_pipe;

    always @(posedge clk) begin
        u_1_0_pipe <= u_1_0;
        u_1_1_pipe <= u_1_1;
        u_1_2_pipe <= u_1_2;
        u_1_3_pipe <= u_1_3;
    end

    wire rda_ctrl_st_1;
    reg rda_ctrl_st_1_1;
    always @(posedge clk) begin
        rda_ctrl_st_1_1 <= outCount_for_rd_addr[6];

    end
    assign rda_ctrl_st_1 = rda_ctrl_st_1_1;

    switch #(logDepth) rdaddr_sw_1_0(.x0(u_1_0_pipe), .x1(u_1_1_pipe), .y0(u_2_0), .y1(u_2_1), .ctrl(rda_ctrl_st_1));
    switch #(logDepth) rdaddr_sw_1_1(.x0(u_1_2_pipe), .x1(u_1_3_pipe), .y0(u_2_2), .y1(u_2_3), .ctrl(rda_ctrl_st_1));
endmodule

module memArray1024_84268(next, reset,
                x0, y0,
                inAddr0,
                outAddr0,
                x1, y1,
                inAddr1,
                outAddr1,
                x2, y2,
                inAddr2,
                outAddr2,
                x3, y3,
                inAddr3,
                outAddr3,
                clk, inFlip, outFlip);

   parameter numBanks = 4;
   parameter logBanks = 2;
   parameter depth = 256;
   parameter logDepth = 8;
   parameter width = 64;
         
   input     clk, next, reset;
   input    inFlip, outFlip;
   wire    next0;
   
   input [width-1:0]   x0;
   output [width-1:0]  y0;
   input [logDepth-1:0] inAddr0, outAddr0;
   input [width-1:0]   x1;
   output [width-1:0]  y1;
   input [logDepth-1:0] inAddr1, outAddr1;
   input [width-1:0]   x2;
   output [width-1:0]  y2;
   input [logDepth-1:0] inAddr2, outAddr2;
   input [width-1:0]   x3;
   output [width-1:0]  y3;
   input [logDepth-1:0] inAddr3, outAddr3;
   nextReg #(256, 8) nextReg_85799(.X(next), .Y(next0), .reset(reset), .clk(clk));


   memMod #(depth*2, width, logDepth+1) 
     memMod0(.in(x0), .out(y0), .inAddr({inFlip, inAddr0}),
	   .outAddr({outFlip, outAddr0}), .writeSel(1'b1), .clk(clk));   
   memMod #(depth*2, width, logDepth+1) 
     memMod1(.in(x1), .out(y1), .inAddr({inFlip, inAddr1}),
	   .outAddr({outFlip, outAddr1}), .writeSel(1'b1), .clk(clk));   
   memMod #(depth*2, width, logDepth+1) 
     memMod2(.in(x2), .out(y2), .inAddr({inFlip, inAddr2}),
	   .outAddr({outFlip, outAddr2}), .writeSel(1'b1), .clk(clk));   
   memMod #(depth*2, width, logDepth+1) 
     memMod3(.in(x3), .out(y3), .inAddr({inFlip, inAddr3}),
	   .outAddr({outFlip, outAddr3}), .writeSel(1'b1), .clk(clk));   
endmodule


						module multfix(clk, rst, a, b, q_sc, q_unsc);
						   parameter WIDTH=35, CYCLES=6;

						   input signed [WIDTH-1:0]    a,b;
						   output [WIDTH-1:0]          q_sc;
						   output [WIDTH-1:0]              q_unsc;

						   input                       clk, rst;
						   
						   reg signed [2*WIDTH-1:0]    q[CYCLES-1:0];
						   wire signed [2*WIDTH-1:0]   res;   
						   integer                     i;

						   assign                      res = q[CYCLES-1];   
						   
						   assign                      q_unsc = res[WIDTH-1:0];
						   assign                      q_sc = {res[2*WIDTH-1], res[2*WIDTH-4:WIDTH-2]};
						      
						   always @(posedge clk) begin
						      q[0] <= a * b;
						      for (i = 1; i < CYCLES; i=i+1) begin
						         q[i] <= q[i-1];
						      end
						   end
						                  
						endmodule 
module addfxp(a, b, q, clk);

   parameter width = 16, cycles=1;
   
   input signed [width-1:0]  a, b;
   input                     clk;   
   output signed [width-1:0] q;
   reg signed [width-1:0]    res[cycles-1:0];

   assign                    q = res[cycles-1];
   
   integer                   i;   
   
   always @(posedge clk) begin
     res[0] <= a+b;
      for (i=1; i < cycles; i = i+1)
        res[i] <= res[i-1];
      
   end
   
endmodule

module subfxp(a, b, q, clk);

   parameter width = 16, cycles=1;
   
   input signed [width-1:0]  a, b;
   input                     clk;   
   output signed [width-1:0] q;
   reg signed [width-1:0]    res[cycles-1:0];

   assign                    q = res[cycles-1];
   
   integer                   i;   
   
   always @(posedge clk) begin
     res[0] <= a-b;
      for (i=1; i < cycles; i = i+1)
        res[i] <= res[i-1];
      
   end
  
endmodule