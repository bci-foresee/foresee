`timescale 1ns/1ps


module thr_tb; //adder testbench

   //set up i/o ports for module
   // all inputs are registers so we can store values to them from buffer txt files
   // all outputs are wires that attach to the PE modules.

    reg [31:0] value; // 32-bit input value
    reg reset = 0;
    reg [31:0] lower_bound; // 32-bit lower bound
    reg [31:0] upper_bound; // 32-bit upper bound

    reg [31:0] val2;
    reg [31:0] lb2;
    reg [31:0] ub2;

    //wire
    wire result;

   //helper variables
   integer j, m;

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
   thr thr(
      .clk(clk),
      .input_val(value),
      .lower_bound(lower_bound),
      .upper_bound(upper_bound),
      .result_wire(result)
   );
    

   // space for buffer i/o
   integer buffer_in, buffer_out, r;

   initial begin
      // Create a VCD file for waveform analysis
      // $dumpfile("sim.vcd"); // Specify the name of the dump file
      // $dumpvars(0, thr_tb); // Dump all variables in the testbench
      $display("Starting simulation...");

      //open i/o files
    //   buffer_in = $fopen("input_buffer.txt", "r"); 
      buffer_in = $fopen("input_buffer.txt", "r");
      buffer_out = $fopen("output_buffer.txt", "w");

      

      // reset module
      @(posedge clk) reset <= 1; // reset module
      @(posedge clk) #1; //let reset propagate
      reset <= 0;

      @(posedge clk) #1; 

      $display("Reading in from buffer...");
      for (j=0; j < 1; j = j+1) begin

         r = $fscanf(buffer_in, 
                     "%x %x %x", 
                     value, lower_bound, upper_bound);

         @(posedge clk) #10;
         // $display("j=%d", j);
      end

      

      @(posedge clk) #1; // wait until computation is done
      @(posedge clk) #1; // wait until computation is done
      @(posedge clk) #1; // wait until computation is done

      // $display("%d %d %d %d", value, lower_bound, upper_bound, result);
       
      // read output
      $display("Writing to buffer...");
      for (m=0; m<1; m=m+1) begin
         $fdisplay(buffer_out,
                   "%h", 
                   result);

         @(posedge clk) #1;
      end
      
      // -------------------------
      //close files
      $display("Simulation complete.");
      $fclose(buffer_in);
      $fclose(buffer_out);
      $finish;
   end
endmodule