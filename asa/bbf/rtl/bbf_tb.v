`timescale 1ns/1ps
module bbf_tb;
    // Clock and reset
    reg clk = 0;
    reg rst = 0;
    always #10 clk = ~clk; // 50MHz clock

    // Input and output signals
    reg [15:0] data_in;
    reg data_valid;
    wire [31:0] power;
    wire valid_out;

    // File handling
    integer input_file, output_file;
    integer scan_file;
    reg [15:0] file_data;
    integer i;

    // Instantiate the sum_of_squares module
    bbf bbf_inst (
        .clk(clk),
        .rst(rst),
        .data_in(data_in),
        .data_valid(data_valid),
        .power(power),
        .valid_out(valid_out)
    );

    initial begin
        $display("Starting simulation...");

        // Open files
        input_file = $fopen("input_buffer.txt", "r");
        output_file = $fopen("output_buffer.txt", "w");

        if (input_file == 0) begin
            $display("Could not open input file.");
            $finish;
        end

        // Initial values
        data_in = 0;
        data_valid = 0;

        // Reset pulse
        rst = 1;
        repeat(5) @(posedge clk);
        rst = 0;
        repeat(5) @(posedge clk);

        // Read and process 8192 values
        for (i = 0; i < 8192; i = i + 1) begin
            scan_file = $fscanf(input_file, "%h\n", file_data);
            
            if (scan_file == 0) begin
                $display("Error reading input_data.txt at line %0d", i+1);
                $finish;
            end

            @(posedge clk);
            data_in = file_data;
            data_valid = 1;
            
            // Optional: Add display for debugging
            // if (i % 1000 == 0) begin
            //     $display("Processing input %0d: %0d", i, file_data);
            // end
        end

        // Wait for valid_out
        @(posedge clk);
        data_valid = 0;
        
        wait(valid_out);
        
        // Write result to file
        $fdisplay(output_file, "%h", power);
        
        // Close files
        $fclose(input_file);
        $fclose(output_file);

        $display("Final power result: %h", power);
        $display("Simulation complete.");
        $finish;
    end

endmodule