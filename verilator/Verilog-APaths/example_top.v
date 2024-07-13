module example_top(
    // code style:
    // break into PE chunks, and provide their I/O in that chunk

    // --------- general -----------

    // --------- FFT PE ----------- 
    input fft_clk,
    input fft_reset,
    input fft_next_in, //asserted high is used to tell the system that the next input will appear on the following cycle

    output fft_next_out, //output will start streaming out the cycle following this asserted high

    input[31:0] fft_input_real_0, // imaginary and real parts of inputs for fft
    input[31:0] fft_input_real_1,
    input[31:0] fft_input_real_2,
    input[31:0] fft_input_real_3,

    input[31:0] fft_input_imag_0,
    input[31:0] fft_input_imag_1,
    input[31:0] fft_input_imag_2,
    input[31:0] fft_input_imag_3,

    output[31:0] fft_output_real_0, // imaginary and real parts of outputs for fft
    output[31:0] fft_output_real_1,
    output[31:0] fft_output_real_2,
    output[31:0] fft_output_real_3,

    output[31:0] fft_output_imag_0,
    output[31:0] fft_output_imag_1,
    output[31:0] fft_output_imag_2,
    output[31:0] fft_output_imag_3


);

// add dataflow path

    dft_top spiral_fft (
        .clk(fft_clk),
        .reset(fft_reset),
        .next(fft_next_in),
        .next_out(fft_next_out),

        .X0(fft_input_real_0), .Y0(fft_output_real_0),
        .X1(fft_input_imag_0), .Y1(fft_output_imag_0),

        .X2(fft_input_real_1), .Y2(fft_output_real_1),
        .X3(fft_input_imag_1), .Y3(fft_output_imag_1),

        .X4(fft_input_real_2), .Y4(fft_output_real_2),
        .X5(fft_input_imag_2), .Y5(fft_output_imag_2),

        .X6(fft_input_real_3), .Y6(fft_output_real_3),
        .X7(fft_input_imag_3), .Y7(fft_output_imag_3)
    );

endmodule

