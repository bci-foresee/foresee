module adder_testbench; //adder testbench
    //set up i/o ports for module
    // all inputs are registers so we can store values to them from txt files
    // all outputs are wires that attach to the PE modules.
    reg [31:0] in1, in2;
    wire [31:0] out;

    // instantiate the PE module
    adder adder_instance(
        .in1(in1),
        .in2(in2),
        .out(out)
    );

    // read inputs for computation to happen.
    integer infile, outfile, r;
    initial begin
        //open i/o files
        infile = $fopen("adder_input.txt", "r");
        outfile = $fopen("adder_output.txt", "w");
        // Read inputs from file
        r = $fscanf(infile, "%h %h", in1, in2);
        // let computation happen (maybe need a delay here)
        // Write output to file
        $fwrite(outfile, "%h\n", out);
        //close files
        $fclose(infile);
        $fclose(outfile);
        $finish;
    end
endmodule


// place your verilog PE here.
module adder(
    input [31:0] in1,
    input [31:0] in2,
    output [31:0] out
);
    assign out = in1 + in2;
endmodule
