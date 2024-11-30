`timescale 1ns / 1ps

module svm #(
    parameter N = 10  // Size of the input and weight arrays
)(
    input  wire                  clk,
    input  wire                  reset,
    input  wire                  valid_in,
    input  wire [N*32 -1:0]      input_array_flat,  // Flattened input array
    input  wire [N*32 -1:0]      weights_flat,      // Flattened weights array
    output reg  [63:0]           acc,
    output reg                   valid_out
);

    // Internal arrays
    reg [31:0] input_array [0:N-1];
    reg [31:0] weights [0:N-1];

    // Temporary variables
    integer i;
    reg [63:0] acc_next;

    // Unpack input_array_flat and weights_flat into arrays using shifts and masks
    always @(*) begin
        for (i = 0; i < N; i = i + 1) begin
            input_array[i] = (input_array_flat >> (i * 32)) & 32'hFFFFFFFF;
            weights[i]     = (weights_flat     >> (i * 32)) & 32'hFFFFFFFF;
        end
    end

    // Combinational logic to compute the dot product
    always @(*) begin
        acc_next = 64'd0;
        if (valid_in) begin
            for (i = 0; i < N; i = i + 1) begin
                acc_next = acc_next + (weights[i] * input_array[i]);
            end
        end
    end

    // Sequential logic to register the output
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            acc       <= 64'd0;
            valid_out <= 1'b0;
        end else if (valid_in) begin
            acc       <= acc_next;
            valid_out <= 1'b1;
        end else begin
            valid_out <= 1'b0;
        end
    end

endmodule
