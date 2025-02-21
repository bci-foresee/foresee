module bbf (
    input wire clk,
    input wire rst,
    input wire [15:0] data_in,    // Assuming 16-bit input values
    input wire data_valid,        // Input data valid signal
    output reg [31:0] power,      // Output sum (larger width to accommodate sum of squares)
    output reg valid_out          // Output valid signal
);

    // Parameters
    localparam ARRAY_SIZE = 13;   // log2(8192) = 13
    
    // Registers
    reg [ARRAY_SIZE-1:0] counter;
    reg [31:0] sum;
    wire [31:0] square;
    
    // Calculate square of input
    // **ESTIMATION of BBF power** use cadence/proprietary tool to generate given c-file's rtl for more accurate results
    assign square = data_in * data_in;
    
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            counter <= 0;
            sum <= 0;
            power <= 0;
            valid_out <= 0;
        end
        else begin
            if (data_valid) begin
                // Add square to running sum
                sum <= sum + square;
                
                // Increment counter
                counter <= counter + 1;
                
                // Reset valid_out
                valid_out <= 0;
                
                // Check if we've received all 8192 values
                if (counter == 13'h1fff) begin  // 8191 (8192nd value being processed)
                    power <= sum + square;      // Output final sum
                    valid_out <= 1;            // Assert valid_out
                    counter <= 0;              // Reset counter for next batch
                    sum <= 0;                  // Reset sum for next batch
                end
            end
        end
    end

endmodule