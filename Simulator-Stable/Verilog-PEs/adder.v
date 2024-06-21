module adder (
    input wire clock,
    input wire [15:0] a,
    input wire [15:0] b,
    output reg [15:0] sum
);
    always @(posedge clock) begin
        sum <= a + b;
    end
endmodule