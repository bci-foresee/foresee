module adder;
    reg [7:0] a, b;
    reg [8:0] sum;
    integer input_file, output_file;
    integer scan_file;

    initial begin
        input_file = $fopen("input.txt", "r");
        output_file = $fopen("output.txt", "w");

        if (input_file == 0 || output_file == 0) begin
            $display("Error opening file");
            $finish;
        end

        scan_file = $fscanf(input_file, "a %d\n", a);
        scan_file = $fscanf(input_file, "b %d\n", b);

        sum = a + b;

        $fwrite(output_file, "sum %d\n", sum);

        $fclose(input_file);
        $fclose(output_file);
        $finish;
    end
endmodule