`timescale 1ns/1ps

module svm_testbench;

    // Clock
    reg clk = 0;
    always #10 clk = ~clk;  // 50MHz clock

    // We'll assume we have 10 inputs/weights for the new SVM module
    // (Matching the new `svm_10` definition)
    reg signed [31:0] a0, a1, a2, a3, a4, a5, a6, a7, a8, a9;
    reg signed [31:0] x0, x1, x2, x3, x4, x5, x6, x7, x8, x9;
    wire signed [63:0] y;

    // Arrays for file reading
    reg [31:0] input_data   [0:9];
    reg [31:0] weights_data [0:9];

    // File handling
    integer buffer_in, buffer_weights, buffer_out;
    integer r, i;

    // Instantiate the new SVM module
    svm svm_inst (
        .clk(clk),
        .a0(a0), .a1(a1), .a2(a2), .a3(a3), .a4(a4),
        .a5(a5), .a6(a6), .a7(a7), .a8(a8), .a9(a9),
        .x0(x0), .x1(x1), .x2(x2), .x3(x3), .x4(x4),
        .x5(x5), .x6(x6), .x7(x7), .x8(x8), .x9(x9),
        .y(y)
    );

    initial begin
        $display("Starting simulation...");

        // Open files
        buffer_in      = $fopen("input_data.txt", "r");
        buffer_weights = $fopen("weights_data.txt", "r");
        buffer_out     = $fopen("output_result.txt", "w");

        if (buffer_in == 0 || buffer_weights == 0) begin
            $display("Could not open input or weights file.");
            $finish;
        end

        // Read input data into array
        for (i = 0; i < 10; i = i + 1) begin
            r = $fscanf(buffer_in, "%h\n", input_data[i]);
            if (r == 0) begin
                $display("Error reading input_data.txt at line %0d", i+1);
                $finish;
            end
        end
        $fclose(buffer_in);

        // Read weights data into array
        for (i = 0; i < 10; i = i + 1) begin
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
        x0=0; x1=0; x2=0; x3=0; x4=0; x5=0; x6=0; x7=0; x8=0; x9=0;

        // Wait a few cycles
        repeat(5) @(posedge clk);

        // Assign weights_data to a0..a9, input_data to x0..x9
        a0 = weights_data[0]; a1 = weights_data[1]; a2 = weights_data[2];
        a3 = weights_data[3]; a4 = weights_data[4]; a5 = weights_data[5];
        a6 = weights_data[6]; a7 = weights_data[7]; a8 = weights_data[8];
        a9 = weights_data[9];

        x0 = input_data[0];  x1 = input_data[1];  x2 = input_data[2];
        x3 = input_data[3];  x4 = input_data[4];  x5 = input_data[5];
        x6 = input_data[6];  x7 = input_data[7];  x8 = input_data[8];
        x9 = input_data[9];

        $display("Starting SVM computation...");
        // Wait a few clock cycles so the multiplication/summation can settle
        repeat(5) @(posedge clk);

        $display("Computation finished. y = %d", y);
        $fdisplay(buffer_out, "%d", y);
        $fclose(buffer_out);

        $display("Simulation complete.");
        $finish;
    end

endmodule
