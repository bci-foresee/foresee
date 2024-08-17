module subtractor_testbench;

    //module name
    parameter MAX_NAME_LENGTH = 40;
    reg [8*MAX_NAME_LENGTH:1] name = "subtractor";

    //i/o ports. i - registers so vals can be saved, o - wires from PE modules
    reg [31:0] in1, in2;
    wire [31:0] out;
    // instantiate the PE module
    subtractor subtractor_instance(
        .in1(in1),
        .in2(in2),
        .out(out)
    );

    // read write from i/o text files
    integer infile, outfile, r;
    initial begin
        infile =  $fopen({name, "_input_buffer.txt"} , "r"); // open files
        outfile = $fopen({name, "_output_buffer.txt"}, "w");

        r = $fscanf(infile, "%h %h", in1, in2); //read data

        //computation occurs here, when inputs are set.

        $fwrite(outfile, "%h\n", out); //write output to file

        $fclose(infile); //close files
        $fclose(outfile);
        $finish;
    end
endmodule

//PE module
module subtractor(
    input [31:0] in1,
    input [31:0] in2,
    output [31:0] out
);
    assign out = in1 - in2;
endmodule
