`timescale 1ns/1ps

// Testbench for Average Calculator
module average_calculator_tb;
    // Clock and reset
    reg clk = 0;
    reg reset = 1;
    always #10 clk = ~clk; // 50MHz clock

    // Input and output signals
    reg [15:0] x_in;
    reg valid_in;
    wire [31:0] avg_out;
    wire valid_out;

    // File handling
    integer input_file, output_file;
    integer scan_file, i;
    reg [15:0] input_data [0:8191]; // For 8192 samples

    // Instantiate the average calculator
    average_calculator avg_inst (
        .clk(clk),
        .reset(reset),
        .x_in(x_in),
        .valid_in(valid_in),
        .avg_out(avg_out),
        .valid_out(valid_out)
    );

    initial begin
        $display("Starting Average Calculator simulation...");

        // Open files
        input_file = $fopen("input_buffer.txt", "r");
        output_file = $fopen("output_buffer.txt", "w");

        if (input_file == 0) begin
            $display("Could not open input file.");
            $finish;
        end

        // Read input data into array
        for (i = 0; i < 8192; i = i + 1) begin
            scan_file = $fscanf(input_file, "%h\n", input_data[i]);
            if (scan_file == 0) begin
                $display("Error reading input_buffer.txt at line %0d", i+1);
                $finish;
            end
        end
        $fclose(input_file);
        $display("Input file read successfully.");

        // Initialize signals
        x_in = 0;
        valid_in = 0;

        // Wait 5 clock cycles before starting
        repeat(5) @(posedge clk);
        
        // Release reset
        reset = 0;
        
        // Wait 2 more clock cycles after reset
        repeat(2) @(posedge clk);

        // Process all samples
        for (i = 0; i < 8192; i = i + 1) begin
            @(posedge clk);
            x_in = input_data[i];
            valid_in = 1;
        end

        // Wait for computation to complete and valid_out to be asserted
        wait(valid_out);
        $fdisplay(output_file, "%h", avg_out);

        // Add a few extra cycles for safety
        repeat(5) @(posedge clk);
        
        $fclose(output_file);
        $display("Simulation complete. Average computed.");
        $finish;
    end

    // Optional: Add waveform dumping for debugging
    // initial begin
    //     $dumpfile("average_calc_test.vcd");
    //     $dumpvars(0, average_calculator_tb);
    // end

endmodule