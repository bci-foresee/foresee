`timescale 1ns / 1ps

module pwxc_tb;

  reg clk;
  reg reset;
  reg start;
  reg signed [15:0] x_in;
  reg signed [15:0] y_in;
  wire [12:0] addr;
  wire done;
  wire [47:0] result;

  // Instantiate the module
  pwxc dut (
    .clk(clk),
    .reset(reset),
    .start(start),
    .x_in(x_in),
    .y_in(y_in),
    .addr(addr),
    .done(done),
    .result(result)
  );

  // Clock generation
  always #5 clk = ~clk;

  initial begin
    // Initialize signals
    clk = 0;
    reset = 1;
    start = 0;
    x_in = 0;
    y_in = 0;

    // Reset sequence
    #10;
    reset = 0;
    #10;

    // Test case 0: Constant signals (Positive)
    $display("Test Case 0: Constant Signals (Positive)");
    start = 1;
    x_in = 5;
    y_in = 3;
    #10;
    start = 0;
    repeat (8192) #10;
    #100;
    check_result(dut.result, 8192 * 5 * 3);

    // Test case 1: Constant signals (Negative)
    $display("Test Case 1: Constant Signals (Negative)");
    reset = 1; #10; reset = 0; #10;
    start = 1;
    x_in = -5;
    y_in = 3;
    #10;
    start = 0;
    repeat (8192) #10;
    #100;
    check_result(dut.result, 8192 * -5 * 3);

    // Test case 2: Constant signals (Mixed)
    $display("Test Case 2: Constant Signals (Mixed)");
    reset = 1; #10; reset = 0; #10;
    start = 1;
    x_in = 7;
    y_in = -2;
    #10;
    start = 0;
    repeat (8192) #10;
    #100;
    check_result(dut.result, 8192 * 7 * -2);

    // Test case 3: Zero input
    $display("Test Case 3: Zero Input");
    reset = 1; #10; reset = 0; #10;
    start = 1;
    x_in = 10;
    y_in = 0;
    #10;
    start = 0;
    repeat (8192) #10;
    #100;
    check_result(dut.result, 0);

    // Test case 4: Large values (check for overflow handling)
    $display("Test Case 4: Large Values");
    reset = 1; #10; reset = 0; #10;
    start = 1;
    x_in = 2000;
    y_in = 1500;
    #10;
    start = 0;
    repeat (8192) #10;
    #100;
    check_result(dut.result, 8192 * 2000 * 1500);


    #100;
    $finish;
  end

  // Helper function to check results (Verilog-2001 compatible)
  task check_result(input [47:0] actual_result, input [47:0] expected_result);
    begin // Added begin...end block
      $display("Result: %d", actual_result);
      $display("Expected Result: %d", expected_result);
      if (actual_result == expected_result) begin
        $display("PASS");
      end else begin
        $display("FAIL");
        $error("Test Failed!");
      end
    end // Added end
  endtask

endmodule