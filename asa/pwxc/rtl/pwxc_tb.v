`timescale 1ns/1ps

module pwxc_testbench;

    // Inputs to the module
    reg clk = 0;
    reg reset = 0;
    reg start = 0;
    reg signed [15:0] x_in = 0;
    reg signed [15:0] y_in = 0;

    // Outputs from the module
    wire [12:0] addr;
    wire done;
    wire signed [47:0] result;

    // Helper variables
    integer i;
    integer buffer_x_in, buffer_y_in, buffer_out, r;

    // Initialize clock (adjust the period as needed)
    always #10000 clk = ~clk; // 50MHz clock frequency

    // Count number of clock cycles
    reg [31:0] cycles;
    always @(posedge clk) begin
        if (reset) cycles <= 0;
        else cycles <= cycles + 1;
    end

    // Instantiate the cross-correlation module
    pwxc cross_corr_inst (
        .clk(clk),
        .reset(reset),
        .start(start),
        .x_in(x_in),
        .y_in(y_in),
        .addr(addr),
        .done(done),
        .result(result)
    );

    // Arrays to hold input data
    reg signed [15:0] x_data [0:8191];
    reg signed [15:0] y_data [0:8191];

    initial begin
        // Create a VCD file for waveform analysis
      //   $dumpfile("sim.vcd");
      //   $dumpvars(0, pwxc_testbench);
        $display("Starting simulation...");

        // Open input and output files
        buffer_x_in = $fopen("input_x_buffer.txt", "r");
        buffer_y_in = $fopen("input_y_buffer.txt", "r");
        buffer_out = $fopen("output_result.txt", "w");

        // Check if files are opened successfully
        if (buffer_x_in == 0 || buffer_y_in == 0) begin
            $display("Failed to open input files.");
            $finish;
        end

        // Read input data into arrays
        $display("Reading input data...");
        for (i = 0; i < 8192; i = i + 1) begin
            r = $fscanf(buffer_x_in, "%h\n", x_data[i]);
            r = $fscanf(buffer_y_in, "%h\n", y_data[i]);
            // $display("x_data[%0d] = %d, y_data[%0d] = %d", i, x_data[i], i, y_data[i]);
        end

        // Close input files
        $fclose(buffer_x_in);
        $fclose(buffer_y_in);

        $display("Input data read successfully.");

        // Reset the module
        @(posedge clk) reset <= 1;
        @(posedge clk) #1;
        reset <= 0;

        $display("Module reset.");

        // Start the cross-correlation process
        start <= 1;
        @(posedge clk) #1;
        start <= 0;
        
         $display("Cross-correlation process started.");
        // Wait for the computation to complete
        wait(done == 1);
        @(posedge clk) #1;

        $display("Cross-correlation process completed.");

        // Write the result to the output file
        $display("Writing result to output file...");
        $fdisplay(buffer_out, "%d", result);

        // Close the output file
        $fclose(buffer_out);

        $display("Simulation complete.");
        $finish;
    end

    // Provide data to x_in and y_in based on the addr output from the module
    always @(posedge clk) begin

         if (done == 1) begin
             $display("Computation done at cycle %d", cycles);
         end

        if (!reset) begin
            x_in <= x_data[addr];
            y_in <= y_data[addr];
        end else begin
            x_in <= 0;
            y_in <= 0;
        end
      //   $display("addr = %d, x_in = %d, y_in = %d", addr, x_in, y_in);
    end

endmodule
