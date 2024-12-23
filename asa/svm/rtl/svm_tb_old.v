`timescale 1ns/1ps

module svm_testbench;

    // Parameters
    parameter N = 10;  // Size of the input array
    parameter data_width = 32;

    // Inputs to the module
    reg clk = 0;
    // reg reset = 0;
    // reg valid_in = 0;
    reg [N*32 -1 :0] input_array_flat;
    reg [N*32 -1 :0] weights_flat;

    // Outputs from the module
    wire [63:0] acc;
    wire valid_out;

    // Helper variables
    integer i;
    integer buffer_in, buffer_weights, buffer_out, r;

    // Clock generation (adjust the period as needed)
    always #10 clk = ~clk;  // 50MHz clock frequency

    // Instantiate the svm module
    svm #(N) svm_inst (
        .clk(clk),
        .reset(reset),
        .valid_in(valid_in),
        .input_array_flat(input_array_flat),
        .weights_flat(weights_flat),
        .acc(acc),
        .valid_out(valid_out)
    );

    // Arrays to hold input data and weights
    reg [data_width-1:0] input_data [0:N-1];
    reg [data_width-1:0] weights_data [0:N-1];

    initial begin
        // Create a VCD file for waveform analysis (optional)
        // $dumpfile("sim.vcd");
        // $dumpvars(0, svm_testbench);

        $display("Starting simulation...");

        // Open input and output files
        buffer_in = $fopen("input_data.txt", "r");
        buffer_weights = $fopen("weights_data.txt", "r");
        buffer_out = $fopen("output_result.txt", "w");

        // Check if files are opened successfully
        if (buffer_in == 0 || buffer_weights == 0) begin
            $display("Failed to open input or weights file.");
            $finish;
        end

        // Read input data into array
        $display("Reading input data...");
        for (i = 0; i < N; i = i + 1) begin
            r = $fscanf(buffer_in, "%h\n", input_data[i]);
            if (r == 0) begin
                $display("Error reading input_data.txt at line %0d", i+1);
                $finish;
            end
        end

        // Close input file
        $fclose(buffer_in);

        // Read weights data into array
        $display("Reading weights data...");
        for (i = 0; i < N; i = i + 1) begin
            r = $fscanf(buffer_weights, "%h\n", weights_data[i]);
            if (r == 0) begin
                $display("Error reading weights_data.txt at line %0d", i+1);
                $finish;
            end
        end

        // Close weights file
        $fclose(buffer_weights);

        $display("Input data and weights read successfully.");

        // Reset the module
        @(posedge clk) reset <= 1;
        @(posedge clk) #1;
        reset <= 0;

        $display("Module reset.");

        // Pack input_data into input_array_flat using shifts
        input_array_flat = {N*32{1'b0}};  // Initialize to zero
        for (i = 0; i < N; i = i + 1) begin
            input_array_flat = input_array_flat | (input_data[i] << (i * 32));
        end

        // Pack weights_data into weights_flat using shifts
        weights_flat = {N*32{1'b0}};  // Initialize to zero
        for (i = 0; i < N; i = i + 1) begin
            weights_flat = weights_flat | (weights_data[i] << (i * 32));
        end

        // Start computation
        @(posedge clk) valid_in <= 1;
        @(posedge clk) #1;
        valid_in <= 0;

        $display("SVM computation started.");

        // Wait for computation to complete
        wait(valid_out == 1);
        @(posedge clk) #1;

        $display("SVM computation completed.");

        // Write the result to the output file
        $display("Writing result to output file...");
        $fdisplay(buffer_out, "%d", acc);

        // Close the output file
        $fclose(buffer_out);

        $display("Simulation complete.");
        $finish;
    end

endmodule
