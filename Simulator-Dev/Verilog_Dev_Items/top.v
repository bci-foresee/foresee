module top (
    input clk,
    input reset,
    output[3:0] count,
    output bit_check
);
    // wire [3:0] count;

    counter u_counter (
        .clk(clk),
        .reset(reset),
        .count(count)
    );

    bit_checker u_bit_checker (
        .data_in(count),
        .bit_check(bit_check)
    );

endmodule
