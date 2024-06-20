module counter (
    input wire clk,
    input wire rst,
    output reg [7:0] out
);

always @(posedge clk or posedge rst) begin
    if (rst)
        out <= 8'b0;
    else
        out <= out + 1;
end

endmodule
