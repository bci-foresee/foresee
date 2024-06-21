module example_top(
    // code style:
    // break into PE chunks, and provide their I/O in that chunk

    // --------- general -----------


    // --------- adder PE -----------
    input clk_adder,
    input[15:0] adder_op_a,
    input[15:0] adder_op_b,
    output[15:0] adder_sum
);

// add dataflow path

    // --------- adder PE -----------
    // wire [15:0] adder_sum;
    adder adder_PE(
        .clock(clk_adder),
        .a(adder_op_a),
        .b(adder_op_b),
        .sum(adder_sum)
    );

endmodule

