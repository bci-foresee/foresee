module subtractor;
    reg [31:0] in1, in2;
    wire [31:0] out;
    integer infile, outfile, r;

    assign out = in1 - in2;

    initial begin
        infile = $fopen("subtractor_input.txt", "r");
        outfile = $fopen("subtractor_output.txt", "w");

        if (infile == 0 || outfile == 0) begin
            $display("Error opening file.");
            $finish;
        end

        // Read inputs from file
        r = $fscanf(infile, "%h %h", in1, in2);

        #1;  // Small delay to ensure correct computation

        // Write output to file
        $fwrite(outfile, "%h\n", out);

        $fclose(infile);
        $fclose(outfile);
        $finish;
    end
endmodule
