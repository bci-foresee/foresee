module thr (
    input clk,              // Clock signal
    input reset,            // Synchronous reset signal
    input [31:0] input_val, // 32-bit input value
    input [31:0] lower_bound, // 32-bit lower bound
    input [31:0] upper_bound, // 32-bit upper bound
    output result_wire            // Output result, latched on the clock edge
);

reg result;          // Output result, latched on the clock edge
assign result_wire = result;

always @(posedge clk) begin
    if (reset) begin
        result <= 1'b0;          // Reset result to 0
    end else begin
        if ((input_val >= lower_bound) && (input_val <= upper_bound)) begin
            result <= 1'b1;      // Set result to 1 if within bounds
        end else begin
            result <= 1'b0;      // Set result to 0 otherwise
        end
    end
end

endmodule
