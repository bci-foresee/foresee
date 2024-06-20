module bit_check (
    input wire [7:0] in,
    output wire out
);

assign out = in[2] & in[3];

endmodule
