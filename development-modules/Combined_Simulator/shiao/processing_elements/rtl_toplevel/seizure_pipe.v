module seizure_pipe(
    // fft i/o -----------------------------------------------------------------
    input fft_clk,
    input fft_reset,
    input fft_next,
    output fft_next_out,
    input [31:0] fft_X0, fft_X1, fft_X2, fft_X3, fft_X4, fft_X5, fft_X6, fft_X7,
    output [31:0] fft_Y0, fft_Y1, fft_Y2, fft_Y3, fft_Y4, fft_Y5, fft_Y6, fft_Y7
);

    // fft_instance ------------------------------------------------------------
    dft_top fft_instance(
        .clk(fft_clk),
        .reset(fft_reset),
        .next(fft_next),
        .next_out(fft_next_out),
        .X0(fft_X0),
        .X1(fft_X1),
        .X2(fft_X2),
        .X3(fft_X3),
        .X4(fft_X4),
        .X5(fft_X5),
        .X6(fft_X6),
        .X7(fft_X7),
        .Y0(fft_Y0),
        .Y1(fft_Y1),
        .Y2(fft_Y2),
        .Y3(fft_Y3),
        .Y4(fft_Y4),
        .Y5(fft_Y5),
        .Y6(fft_Y6),
        .Y7(fft_Y7)
    );

endmodule