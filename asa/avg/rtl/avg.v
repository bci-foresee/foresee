// Average Calculator Module
module average_calculator (
    input wire clk,
    input wire reset,
    input wire [15:0] x_in,      // 16-bit input signal
    input wire valid_in,         // Input data valid signal
    output reg [31:0] avg_out,   // 32-bit average output (scaled up to maintain precision)
    output reg valid_out         // Output data valid signal
);

    // Parameters
    parameter TOTAL_SAMPLES = 8192;
    parameter LOG2_SAMPLES = 13;  // log2(8192)

    // Internal registers
    reg [31:0] accumulator;
    reg [LOG2_SAMPLES-1:0] sample_count;
    reg calculating;

    // State definitions
    localparam IDLE = 2'b00;
    localparam ACCUMULATE = 2'b01;
    localparam COMPUTE = 2'b10;
    reg [1:0] state;

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            accumulator <= 32'd0;
            sample_count <= 0;
            avg_out <= 32'd0;
            valid_out <= 1'b0;
            calculating <= 1'b0;
            state <= IDLE;
        end else begin
            case (state)
                IDLE: begin
                    if (valid_in) begin
                        state <= ACCUMULATE;
                        accumulator <= {16'd0, x_in};  // Zero-extend input
                        sample_count <= 1;
                        valid_out <= 1'b0;
                        calculating <= 1'b1;
                    end
                end

                ACCUMULATE: begin
                    if (valid_in) begin
                        accumulator <= accumulator + {16'd0, x_in};
                        sample_count <= sample_count + 1;
                        
                        if (sample_count == TOTAL_SAMPLES - 1) begin
                            state <= COMPUTE;
                        end
                    end
                end

                COMPUTE: begin
                    // Division by shifting (since TOTAL_SAMPLES is power of 2)
                    avg_out <= accumulator >> LOG2_SAMPLES;
                    valid_out <= 1'b1;
                    state <= IDLE;
                    calculating <= 1'b0;
                end

                default: state <= IDLE;
            endcase
        end
    end
endmodule
