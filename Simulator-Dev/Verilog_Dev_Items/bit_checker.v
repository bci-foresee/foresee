module bit_checker (
    input [3:0] data_in,
    output bit_check
);
    assign bit_check = data_in[2];
endmodule
