`timescale 1ns/1ps
module tb_svm_10;

    // Clock
    reg clk;

    // Inputs to DUT
    reg signed [31:0] a0;
    reg signed [31:0] a1;
    reg signed [31:0] a2;
    reg signed [31:0] a3;
    reg signed [31:0] a4;
    reg signed [31:0] a5;
    reg signed [31:0] a6;
    reg signed [31:0] a7;
    reg signed [31:0] a8;
    reg signed [31:0] a9;
    reg signed [31:0] x0;
    reg signed [31:0] x1;
    reg signed [31:0] x2;
    reg signed [31:0] x3;
    reg signed [31:0] x4;
    reg signed [31:0] x5;
    reg signed [31:0] x6;
    reg signed [31:0] x7;
    reg signed [31:0] x8;
    reg signed [31:0] x9;

    // Output from DUT
    wire signed [63:0] y;

    // Instantiate DUT
    svm dut (
        .clk(clk),
        .a0(a0),
        .a1(a1),
        .a2(a2),
        .a3(a3),
        .a4(a4),
        .a5(a5),
        .a6(a6),
        .a7(a7),
        .a8(a8),
        .a9(a9),
        .x0(x0),
        .x1(x1),
        .x2(x2),
        .x3(x3),
        .x4(x4),
        .x5(x5),
        .x6(x6),
        .x7(x7),
        .x8(x8),
        .x9(x9),
        .y(y)
    );

    // Generate clock
    always #5 clk = ~clk;

    initial begin
        clk = 0;

        // Initialize all inputs to 0
        a0 = 0; a1 = 0; a2 = 0; a3 = 0; a4 = 0;
        a5 = 0; a6 = 0; a7 = 0; a8 = 0; a9 = 0;
        x0 = 0; x1 = 0; x2 = 0; x3 = 0; x4 = 0;
        x5 = 0; x6 = 0; x7 = 0; x8 = 0; x9 = 0;

        // Wait a couple of cycles
        #10;

        // Apply some stimulus
        a0 = 32'sd1;   x0 = 32'sd10;
        a1 = 32'sd2;   x1 = 32'sd20;
        a2 = 32'sd3;   x2 = 32'sd30;
        a3 = 32'sd4;   x3 = 32'sd40;
        a4 = 32'sd5;   x4 = 32'sd50;
        a5 = 32'sd6;   x5 = 32'sd60;
        a6 = 32'sd7;   x6 = 32'sd70;
        a7 = 32'sd8;   x7 = 32'sd80;
        a8 = 32'sd9;   x8 = 32'sd90;
        a9 = 32'sd10;  x9 = 32'sd100;

        #20;
        $display("Time=%0t: After first scenario, y=%d (expected 3850)", $time, y);

        // Check another set of inputs
        a0 = -32'sd1;  x0 = 32'sd11;
        a1 = -32'sd2;  x1 = 32'sd21;
        a2 = -32'sd3;  x2 = 32'sd31;
        a3 = 32'sd0;   x3 = 32'sd41;
        a4 = 32'sd1;   x4 = -32'sd1;
        a5 = 32'sd2;   x5 = -32'sd2;
        a6 = 32'sd3;   x6 = -32'sd3;
        a7 = -32'sd4;  x7 = 32'sd44;
        a8 = -32'sd5;  x8 = 32'sd55;
        a9 = 32'sd6;   x9 = 32'sd66;

        #20;
        $display("Time=%0t: After second scenario, y=%d (expected -215)", $time, y);

        // Finish
        $finish;
    end

endmodule
