`timescale 1ns/1ps

module fft_testbench; //adder testbench

   //set up i/o ports for module
   // all inputs are registers so we can store values to them from buffer txt files
   // all outputs are wires that attach to the PE modules.
   reg reset = 0;
   reg next = 0;

   reg [31:0] X0, X1, X2, X3, X4, X5, X6, X7;

   wire [31:0] Y0, Y1, Y2, Y3, Y4, Y5, Y6, Y7;
   wire next_out;

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
   fft fft_inst(
      .clk(clk),
      .reset(reset),
      .next(next),
      .next_out(next_out),
      .X0(X0),
      .Y0(Y0),
      .X1(X1),
      .Y1(Y1),
      .X2(X2),
      .Y2(Y2),
      .X3(X3),
      .Y3(Y3),
      .X4(X4),
      .Y4(Y4),
      .X5(X5),
      .Y5(Y5),
      .X6(X6),
      .Y6(Y6),
      .X7(X7),
      .Y7(Y7)
   );
    

   // space for buffer i/o
   integer buffer_in, buffer_out, r;

   initial begin
      // Create a VCD file for waveform analysis
      $dumpfile("sim.vcd"); // Specify the name of the dump file
      $dumpvars(0, spiral_fft_8192_testbench); // Dump all variables in the testbench
      $display("Starting simulation...");

      //open i/o files
      buffer_in = $fopen("input_buffer.txt", "r"); 
      buffer_out = $fopen("output_buffer.txt", "w");

      //set all inputs to zero
      X0 = 0; X1 = 0; X2 = 0; X3 = 0; X4 = 0; X5 = 0; X6 = 0; X7 = 0;
      
      // reset module
      @(posedge clk) reset <= 1; // reset module
      @(posedge clk) #1; //let reset propagate
      reset <= 0;

      next <= 1; // signal start of computation
      @(posedge clk) #1; 
      next <= 0;

      // 8192 complex words over 2048 cycles
      // 4 complex words per cycle
      $display("Reading in from buffer...");
      for (j=0; j < 2048; j = j+1) begin
         // Input: 4 complex words per cycle
         r = $fscanf(buffer_in, 
                     "%x %x %x %x %x %x %x %x", 
                     X0, X1, X2, X3, X4, X5, X6, X7);

         // $display("Number of values read: %d", r);
         // $display("%x %x %x %x %x %x %x %x", X0, X1, X2, X3, X4, X5, X6, X7);
                     
         @(posedge clk) #10;
         // $display("j=%d", j);
      end

      X0 = 0; X1 = 0; X2 = 0; X3 = 0; X4 = 0; X5 = 0; X6 = 0; X7 = 0;
      @(posedge clk) #1; // wait until computation is done
      
      // wait until computation is done
      @(posedge next_out);
      @(posedge clk) #1;
       
      // read output
      $display("Writing to buffer...");
      for (m=0; m<2048; m=m+1) begin
         $fdisplay(buffer_out,
                   "%h %h %h %h %h %h %h %h", 
                   Y0, Y1, Y2, Y3, Y4, Y5, Y6, Y7);

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