
module clocked_adder_testbench; //adder testbench

    //set up i/o ports for module
    // all inputs are registers so we can store values to them from txt files
    // all outputs are wires that attach to the PE modules.
    reg [31:0] in1, in2;
    reg reset = 0;
    wire [31:0] out;

    // initialize clock
    reg clk = 0;
    always #10000 clk = ~clk;

    // count number of clock cycles
    reg[31:0] cycles;
    always @(posedge clk) begin
      if (reset) cycles <= 0;
      else cycles <= cycles+1;
    end

    // instantiate the PE module
    clocked_adder clocked_adder_instance(
        .clk(clk),
        .reset(reset),
        .in1(in1),
        .in2(in2),
        .out(out)
    );

    // read inputs for computation to happen.
    integer buffer_in, buffer_out, r;
    initial begin
        //open i/o files
        buffer_in = $fopen("input_buffer.txt", "r"); 
        buffer_out = $fopen("output_buffer.txt", "w");
        
        // ------ computation ------

        @(posedge clk) reset = 1; // reset module
        @(posedge clk); //let reset propagate
        @(posedge clk) reset = 0; // deassert reset
                    
        // r = $fscanf(buffer_in, "%h %h", in1, in2); // this would read the second line of inputs

        // let computation happen 10 cycle delay, show intermediate results
        repeat(3) begin
            // latch inputs
            r = $fscanf(buffer_in, // buffer to read inputs from
                    "%h %h", // format of inputs
                    in1, // where to latch first input
                    in2); // where to latch second input

            // clock cycle to let computation happen
            @(posedge clk);
            
            // Write output to file
            // $fwrite(buffer_out, "%h\n", out);
            $fdisplay(buffer_out, "%h", out);

        end
    
        // -------------------------
        //close files
        $fclose(buffer_in);
        $fclose(buffer_out);
        $finish;
    end
endmodule


module clocked_adder (
    input clk,                // Clock signal
    input reset,              // Reset signal
    input [31:0] in1, in2,         // 4-bit inputs
    output [31:0] out           // 5-bit output to accommodate carry
);
    reg[31:0] sum; // make sure sizes are the same
    assign out = sum;

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            sum <= 5'b0;               // Reset output to zero
        end else begin
            sum <= in1 + in2;              // Perform addition and latch output
        end
    end

endmodule
