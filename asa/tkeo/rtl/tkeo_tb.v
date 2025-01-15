`timescale 1ns/1ps

module tkeo_testbench;
    // Clock and reset
    reg clk = 0;
    reg reset = 1;
    always #10 clk = ~clk; // 50MHz clock

    // Input and output signals
    reg [15:0] x_in;
    reg valid_in;
    wire [31:0] tkeo_out;
    wire valid_out;

    // File handling
    integer input_file, output_file;
    integer scan_file, i;
    reg [15:0] input_data [0:8191]; // For 8192 samples

    // Instantiate the TKEO module
    tkeo_operator tkeo_inst (
        .clk(clk),
        .reset(reset),
        .x_in(x_in),
        .valid_in(valid_in),
        .tkeo_out(tkeo_out),
        .valid_out(valid_out)
    );

    initial begin
        $display("Starting TKEO simulation...");

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
            
            // Wait for valid_out to be asserted
            if (valid_out) begin
                $fdisplay(output_file, "%h", tkeo_out);
            end
        end

        // Add a few extra cycles to process the last samples
        valid_in = 0;
        repeat(5) @(posedge clk);
        
        $fclose(output_file);
        $display("Simulation complete.");
        $finish;
    end

    // Optional: Add waveform dumping for debugging
    initial begin
        $dumpfile("tkeo_test.vcd");
        $dumpvars(0, tkeo_testbench);
    end

endmodule