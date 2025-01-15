module tkeo_operator (
    input wire clk,
    input wire reset,
    input wire [15:0] x_in,       // 16-bit input signal
    input wire valid_in,          // Input data valid signal
    output reg [31:0] tkeo_out,   // 32-bit TKEO output
    output reg valid_out          // Output data valid signal
);
    // Internal registers to store samples
    reg [15:0] x_n_minus_1;
    reg [15:0] x_n;
    reg [15:0] x_n_plus_1;

    // Internal wires for intermediate calculations
    wire [31:0] x_n_squared;
    wire [31:0] product;

    // Compute x[n]^2
    assign x_n_squared = x_n * x_n;

    // Compute x[n+1] * x[n-1]
    assign product = x_n_plus_1 * x_n_minus_1;

    // Sequential logic to update samples
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            // Reset internal state
            x_n_minus_1 <= 16'd0;
            x_n <= 16'd0;
            x_n_plus_1 <= 16'd0;
            tkeo_out <= 32'd0;
            valid_out <= 1'b0;
        end else begin
            if (valid_in) begin
                // Update sample registers
                x_n_minus_1 <= x_n;
                x_n <= x_n_plus_1;
                x_n_plus_1 <= x_in;

                // Compute TKEO
                tkeo_out <= x_n_squared - product;
                valid_out <= 1'b1;  // Assert valid_out when valid_in is true
            end else begin
                valid_out <= 1'b0;  // Deassert valid_out when valid_in is false
            end
        end
    end
endmodule
