`timescale 1ns/1ps

module tkeo_operator_tb();

// Test bench signals
reg clk;
reg reset;
reg [15:0] x_in;
reg valid_in;
wire [31:0] tkeo_out;
wire valid_out;

// Instantiate the TKEO operator
tkeo_operator uut (
    .clk(clk),
    .reset(reset),
    .x_in(x_in),
    .valid_in(valid_in),
    .tkeo_out(tkeo_out),
    .valid_out(valid_out)
);

// Clock generation
initial begin
    clk = 0;
    forever #5 clk = ~clk;  // 100MHz clock
end

// Test vectors
reg [15:0] test_data [0:19];  // Increased array size for more test cases
reg [31:0] expected_results [0:19];
integer i;

// Test stimulus
initial begin
    // Initialize waveform dumping
    $dumpfile("tkeo_operator_tb.vcd");
    $dumpvars(0, tkeo_operator_tb);
    
    // Initialize test data with more interesting sequences
    
    // Test Case Set 1: Simple increasing sequence
    test_data[0] = 16'd1;
    test_data[1] = 16'd2;
    test_data[2] = 16'd4;
    test_data[3] = 16'd8;
    test_data[4] = 16'd16;
    
    // Test Case Set 2: Sine-like sequence
    test_data[5] = 16'd5;
    test_data[6] = 16'd10;
    test_data[7] = 16'd15;
    test_data[8] = 16'd10;
    test_data[9] = 16'd5;
    
    // Test Case Set 3: Alternating sequence
    test_data[10] = 16'd20;
    test_data[11] = 16'd10;
    test_data[12] = 16'd30;
    test_data[13] = 16'd15;
    test_data[14] = 16'd25;
    
    // Test Case Set 4: Random-like sequence
    test_data[15] = 16'd8;
    test_data[16] = 16'd12;
    test_data[17] = 16'd6;
    test_data[18] = 16'd18;
    test_data[19] = 16'd9;
    
    // Calculate expected results (TKEO = x[n]^2 - x[n+1]*x[n-1])
    for (i = 1; i < 19; i = i + 1) begin
        expected_results[i] = test_data[i] * test_data[i] - 
                            test_data[i+1] * test_data[i-1];
    end
    
    // Initialize signals
    reset = 1;
    valid_in = 0;
    x_in = 0;
    
    // Wait for 100ns
    #100;
    
    // Release reset
    reset = 0;
    #20;
    
    // Test all sequences
    $display("Starting enhanced test sequences...");
    for (i = 0; i < 20; i = i + 1) begin
        @(posedge clk);
        valid_in = 1;
        x_in = test_data[i];
        #1; // Wait for signals to settle
        
        // Check valid_out assertion
        if (i >= 3 && valid_out !== 1) begin
            $display("Error: valid_out not asserted at i=%d", i);
        end
        
        // Check TKEO output (starting from 4th sample)
        if (i >= 4) begin
            if (tkeo_out !== expected_results[i-2]) begin
                $display("Error at sample %d: Expected %d, Got %d", 
                        i, expected_results[i-2], tkeo_out);
            end else begin
                $display("Sample %d: TKEO output = %d (correct)", 
                        i, tkeo_out);
            end
        end
    end
    
    // Test Case: Invalid Input
    $display("\nTesting invalid input handling...");
    valid_in = 0;
    #20;
    if (valid_out !== 0) begin
        $display("Error: valid_out not deasserted when valid_in is 0");
    end
    
    // Test Case: Reset During Operation
    $display("\nTesting reset during operation...");
    valid_in = 1;
    x_in = 16'hFFFF;
    #10;
    reset = 1;
    #10;
    if (tkeo_out !== 0 || valid_out !== 0) begin
        $display("Error: Reset not working properly");
    end
    
    // End simulation
    #100;
    $display("\nTest completed");
    $finish;
end

// Monitor changes
initial begin
    $monitor("Time=%t reset=%b valid_in=%b x_in=%d tkeo_out=%d valid_out=%b",
             $time, reset, valid_in, x_in, tkeo_out, valid_out);
end

endmodule