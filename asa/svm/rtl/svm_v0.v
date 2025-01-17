`timescale 1ns / 1ps

module svm (
    input  wire                  clk,
    input  wire signed [31:0]    a0,
    input  wire signed [31:0]    a1,
    input  wire signed [31:0]    a2,
    input  wire signed [31:0]    a3,
    input  wire signed [31:0]    a4,
    input  wire signed [31:0]    a5,
    input  wire signed [31:0]    a6,
    input  wire signed [31:0]    a7,
    input  wire signed [31:0]    a8,
    input  wire signed [31:0]    a9,
    input  wire signed [31:0]    x0,
    input  wire signed [31:0]    x1,
    input  wire signed [31:0]    x2,
    input  wire signed [31:0]    x3,
    input  wire signed [31:0]    x4,
    input  wire signed [31:0]    x5,
    input  wire signed [31:0]    x6,
    input  wire signed [31:0]    x7,
    input  wire signed [31:0]    x8,
    input  wire signed [31:0]    x9,
    output reg  signed [63:0]    y
);
    always @(posedge clk) begin
        y <= (a0 * x0) +
             (a1 * x1) +
             (a2 * x2) +
             (a3 * x3) +
             (a4 * x4) +
             (a5 * x5) +
             (a6 * x6) +
             (a7 * x7) +
             (a8 * x8) +
             (a9 * x9);
    end
endmodule
