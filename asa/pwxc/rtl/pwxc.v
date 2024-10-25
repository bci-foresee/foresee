module pwxc(
    input clk,
    input reset,
    input start,
    input signed [15:0] x_in,
    input signed [15:0] y_in,
    output reg [12:0] addr,
    output reg done,
    output reg [47:0] result
);

reg [47:0] accumulator;
reg [1:0] state;

parameter IDLE = 2'b00;
parameter RUN  = 2'b01;
parameter DONE = 2'b10;

always @(posedge clk or posedge reset) begin
    if (reset) begin
        state       <= IDLE;
        addr        <= 0;
        accumulator <= 0;
        done        <= 0;
        result      <= 0;
    end else begin
        case (state)
            IDLE: begin
                if (start) begin
                    state       <= RUN;
                    addr        <= 0;
                    accumulator <= 0;
                    done        <= 0;
                    result      <= 0;
                end
            end
            RUN: begin
                // $display("state: %d", state);
                // Perform multiplication and accumulation
                accumulator <= accumulator + x_in * y_in;
                if (addr == 13'd8191) begin
                    state <= DONE;
                end else begin
                    addr <= addr + 1;
                end
            end
            DONE: begin
                // $display("state: %d", state);
                // In DONE state, set result and done flag
                result <= accumulator;
                done   <= 1;
                if (!start) begin
                    state <= IDLE;
                    // done  <= 0;
                end
            end
        endcase
    end
end

endmodule
