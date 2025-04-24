`timescale 1ns / 1ps

module svm (
    input wire clk,
    // Weights a0 to a31
    input wire signed [31:0] a0, a1, a2, a3, a4, a5, a6, a7, a8, a9,
    input wire signed [31:0] a10, a11, a12, a13, a14, a15,
    input wire signed [31:0] a16, a17, a18, a19, a20, a21, a22, a23, a24, a25,
    input wire signed [31:0] a26, a27, a28, a29, a30, a31,
    
    // Input features x0 to x31
    input wire signed [31:0] x0, x1, x2, x3, x4, x5, x6, x7, x8, x9,
    input wire signed [31:0] x10, x11, x12, x13, x14, x15,
    input wire signed [31:0] x16, x17, x18, x19, x20, x21, x22, x23, x24, x25,
    input wire signed [31:0] x26, x27, x28, x29, x30, x31,
    
    output reg signed [63:0] y
);

    // Internal registers for partial sums to improve timing
    wire [63:0] sum_0_15;    // Sum for inputs 0-15
    wire [63:0] sum_16_31;   // Sum for inputs 16-31

    assign sum_0_15 = (a0 * x0) + (a1 * x1) + (a2 * x2) + (a3 * x3) + (a4 * x4) +
                    (a5 * x5) + (a6 * x6) + (a7 * x7) + (a8 * x8) + (a9 * x9) +
                    (a10 * x10) + (a11 * x11) + (a12 * x12) + (a13 * x13) + (a14 * x14) +
                    (a15 * x15);
        
    // Second half (16-31)
    assign sum_16_31 = (a16 * x16) + (a17 * x17) + (a18 * x18) + (a19 * x19) + (a20 * x20) +
                    (a21 * x21) + (a22 * x22) + (a23 * x23) + (a24 * x24) + (a25 * x25) +
                    (a26 * x26) + (a27 * x27) + (a28 * x28) + (a29 * x29) + (a30 * x30) +
                    (a31 * x31);

    // Pipeline register for final sum
    // reg signed [63:0] final_sum;

    always @(posedge clk) begin
        
        // Second stage: Combine partial sums
        y <= sum_0_15 + sum_16_31;
        
    end

endmodule