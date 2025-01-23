`timescale 1ns/1ps

module svm_testbench;

    // Clock
    reg clk = 0;
    always #10 clk = ~clk;  // 50MHz clock

    // We'll assume we have 10 inputs/weights for the new SVM module
    // (Matching the new `svm_10` definition)
    reg signed [31:0] a0, a1, a2, a3, a4, a5, a6, a7, a8, a9;
    reg signed [31:0] a10, a11, a12, a13, a14, a15;
    reg signed [31:0] a16, a17, a18, a19, a20, a21, a22, a23, a24, a25;
    reg signed [31:0] a26, a27, a28, a29, a30, a31;

    reg signed [31:0] x0, x1, x2, x3, x4, x5, x6, x7, x8, x9;
    reg signed [31:0] x10, x11, x12, x13, x14, x15;
    reg signed [31:0] x16, x17, x18, x19, x20, x21, x22, x23, x24, x25;
    reg signed [31:0] x26, x27, x28, x29, x30, x31;

    wire signed [63:0] y;

    // Arrays for file reading
    reg [31:0] input_data   [0:31];
    reg [31:0] weights_data [0:31];

    // File handling
    integer buffer_in, buffer_weights, buffer_out;
    integer r, i;

    // Instantiate the new SVM module
    svm svm_inst (
        .clk(clk),
        .a0(a0), .a1(a1), .a2(a2), .a3(a3), .a4(a4),
        .a5(a5), .a6(a6), .a7(a7), .a8(a8), .a9(a9),
        .a10(a10), .a11(a11), .a12(a12), .a13(a13), .a14(a14),
        .a15(a15),
        .a16(a16), .a17(a17), .a18(a18), .a19(a19), .a20(a20),
        .a21(a21), .a22(a22), .a23(a23), .a24(a24), .a25(a25),
        .a26(a26), .a27(a27), .a28(a28), .a29(a29), .a30(a30),
        .a31(a31),
        .x0(x0), .x1(x1), .x2(x2), .x3(x3), .x4(x4),
        .x5(x5), .x6(x6), .x7(x7), .x8(x8), .x9(x9),
        .x10(x10), .x11(x11), .x12(x12), .x13(x13), .x14(x14),
        .x15(x15),
        .x16(x16), .x17(x17), .x18(x18), .x19(x19), .x20(x20),
        .x21(x21), .x22(x22), .x23(x23), .x24(x24), .x25(x25),
        .x26(x26), .x27(x27), .x28(x28), .x29(x29), .x30(x30),
        .x31(x31),
        .y(y)
    );

    initial begin
        $display("Starting simulation...");

        // Open files
        buffer_in      = $fopen("input_buffer.txt", "r");
        buffer_weights = $fopen("weights_buffer.txt", "r");
        buffer_out     = $fopen("output_buffer.txt", "w");

        if (buffer_in == 0 || buffer_weights == 0) begin
            $display("Could not open input or weights file.");
            $finish;
        end

        // Read input data into array
        for (i = 0; i < 32; i = i + 1) begin
            r = $fscanf(buffer_in, "%h\n", input_data[i]);
            if (r == 0) begin
                $display("Error reading input_data.txt at line %0d", i+1);
                $finish;
            end
        end
        $fclose(buffer_in);

        // Read weights data into array
        for (i = 0; i < 32; i = i + 1) begin
            r = $fscanf(buffer_weights, "%h\n", weights_data[i]);
            if (r == 0) begin
                $display("Error reading weights_data.txt at line %0d", i+1);
                $finish;
            end
        end
        $fclose(buffer_weights);

        $display("Files read successfully.");

        // Initialize regs to 0 first
        a0=0; a1=0; a2=0; a3=0; a4=0; a5=0; a6=0; a7=0; a8=0; a9=0;
        a10=0; a11=0; a12=0; a13=0; a14=0; a15=0;
        a16=0; a17=0; a18=0; a19=0; a20=0; a21=0; a22=0; a23=0; a24=0; a25=0;
        a26=0; a27=0; a28=0; a29=0; a30=0; a31=0;

        x0=0; x1=0; x2=0; x3=0; x4=0; x5=0; x6=0; x7=0; x8=0; x9=0;
        x10=0; x11=0; x12=0; x13=0; x14=0; x15=0;
        x16=0; x17=0; x18=0; x19=0; x20=0; x21=0; x22=0; x23=0; x24=0; x25=0;
        x26=0; x27=0; x28=0; x29=0; x30=0; x31=0;

        // Wait a few cycles
        repeat(5) @(posedge clk);
        @(posedge clk);
        @(posedge clk);
        @(posedge clk);

        // Assign weights_data to a0..a9, input_data to x0..x9
        a0 = weights_data[0]; a1 = weights_data[1]; a2 = weights_data[2];
        a3 = weights_data[3]; a4 = weights_data[4]; a5 = weights_data[5];
        a6 = weights_data[6]; a7 = weights_data[7]; a8 = weights_data[8];
        a9 = weights_data[9]; a10 = weights_data[10]; a11 = weights_data[11];
        a12 = weights_data[12]; a13 = weights_data[13]; a14 = weights_data[14];
        a15 = weights_data[15];
        a16 = weights_data[16]; a17 = weights_data[17]; a18 = weights_data[18];
        a19 = weights_data[19]; a20 = weights_data[20]; a21 = weights_data[21];
        a22 = weights_data[22]; a23 = weights_data[23]; a24 = weights_data[24];
        a25 = weights_data[25]; a26 = weights_data[26]; a27 = weights_data[27];
        a28 = weights_data[28]; a29 = weights_data[29]; a30 = weights_data[30];
        a31 = weights_data[31];

        x0 = input_data[0];  x1 = input_data[1];  x2 = input_data[2];
        x3 = input_data[3];  x4 = input_data[4];  x5 = input_data[5];
        x6 = input_data[6];  x7 = input_data[7];  x8 = input_data[8];
        x9 = input_data[9];  x10 = input_data[10];  x11 = input_data[11];
        x12 = input_data[12];  x13 = input_data[13];  x14 = input_data[14];
        x15 = input_data[15];
        x16 = input_data[16];  x17 = input_data[17];  x18 = input_data[18];
        x19 = input_data[19];  x20 = input_data[20];  x21 = input_data[21];
        x22 = input_data[22];  x23 = input_data[23];  x24 = input_data[24];
        x25 = input_data[25];  x26 = input_data[26];  x27 = input_data[27];
        x28 = input_data[28];  x29 = input_data[29];  x30 = input_data[30];
        x31 = input_data[31];

        // $display("Input data:");
        // $display("input_data[%0d] = %d", 31, input_data[31]);

        // $display("Weights data:");
        // $display("weights_data[%0d] = %d", 0, weights_data[0]);

        $display("Starting SVM computation...");
        // Wait a few clock cycles so the multiplication/summation can settle
        repeat(5) @(posedge clk);
        @(posedge clk);
        @(posedge clk);
        @(posedge clk);

        // $display("Computation finished. y = %d", y);
        $fdisplay(buffer_out, "%h", y);
        $fclose(buffer_out);

        $display("Simulation complete.");
        $finish;
    end

endmodule
