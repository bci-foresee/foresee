import re

def extract_latency(report):
    """
    Extracts the worst-case latency (largest data arrival time) from an OpenSTA timing report.
    
    Args:
        report (str): The raw stdout of the OpenSTA timing report.

    Returns:
        float: The worst-case latency in nanoseconds.
    """
    # Refined regex to target the specific "data arrival time" pattern
    pattern = re.compile(r"\s+([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)\s+data arrival time")

    # Find all matches and extract the data arrival times
    arrival_times = [float(match.group(1)) for match in pattern.finditer(report)]

    if arrival_times:
        # Return the largest data arrival time (worst-case latency)
        return max(arrival_times)
    else:
        raise ValueError("No data arrival times found in the timing report.")


# Example Usage
timing_reports = ["""
OpenSTA 2.6.0 f71b38bbce Copyright (c) 2024, Parallax Software, Inc.
License GPLv3: GNU GPL version 3 <http://gnu.org/licenses/gpl.html>

This is free software, and you are free to change and redistribute it
under certain conditions; type `show_copying' for details. 
This program comes with ABSOLUTELY NO WARRANTY; for details type `show_warranty'.
Warning: ../../hardware_lib/sky130_fd_sc_hd__ff_n40C_1v65.lib line 23, default_fanout_load is 0.0.
Warning: constraints.sdc line 7, set_input_delay relative to a clock defined on the same port/pin not allowed.
Warning: constraints.sdc line 8, set_input_delay relative to a clock defined on the same port/pin not allowed.
Group                  Internal  Switching    Leakage      Total
                          Power      Power      Power      Power (Watts)
----------------------------------------------------------------
Sequential             5.81e-07   3.28e-07   1.95e-12   9.08e-07  14.3%
Combinational          3.41e-06   2.01e-06   1.20e-10   5.42e-06  85.7%
Clock                  0.00e+00   0.00e+00   0.00e+00   0.00e+00   0.0%
Macro                  0.00e+00   0.00e+00   0.00e+00   0.00e+00   0.0%
Pad                    0.00e+00   0.00e+00   0.00e+00   0.00e+00   0.0%
----------------------------------------------------------------
Total                  3.99e-06   2.34e-06   1.22e-10   6.33e-06 100.0%
                          63.1%      36.9%       0.0%
Warning: power_analysis.tcl line 29, report_checks -group_count is deprecated. Use -group_path_count instead.
Startpoint: lower_bound[0] (input port clocked by clk)
Endpoint: _817_ (rising edge-triggered flip-flop clocked by clk)
Path Group: clk
Path Type: max

  Delay    Time   Description
---------------------------------------------------------
   0.00    0.00   clock clk (rise edge)
   0.00    0.00   clock network delay (ideal)
   2.00    2.00 v input external delay
   0.00    2.00 v lower_bound[0] (in)
   0.09    2.09 v _649_/X (sky130_fd_sc_hd__lpflow_isobufsrc_1)
   0.24    2.33 v _650_/X (sky130_fd_sc_hd__maj3_1)
   0.25    2.59 v _651_/X (sky130_fd_sc_hd__maj3_1)
   0.25    2.84 v _652_/X (sky130_fd_sc_hd__maj3_1)
   0.25    3.10 v _653_/X (sky130_fd_sc_hd__maj3_1)
   0.25    3.35 v _654_/X (sky130_fd_sc_hd__maj3_1)
   0.25    3.60 v _655_/X (sky130_fd_sc_hd__maj3_1)
   0.25    3.85 v _656_/X (sky130_fd_sc_hd__maj3_1)
   0.14    3.99 ^ _667_/Y (sky130_fd_sc_hd__o221ai_1)
   0.21    4.20 ^ _673_/Y (sky130_fd_sc_hd__nor4b_1)
   0.11    4.31 v _702_/Y (sky130_fd_sc_hd__o2111ai_1)
   0.19    4.50 ^ _816_/Y (sky130_fd_sc_hd__a221oi_1)
   0.00    4.50 ^ _817_/D (sky130_fd_sc_hd__dfxtp_1)
           4.50   data arrival time

  62.50   62.50   clock clk (rise edge)
   0.00   62.50   clock network delay (ideal)
  -0.10   62.40   clock uncertainty
   0.00   62.40   clock reconvergence pessimism
          62.40 ^ _817_/CLK (sky130_fd_sc_hd__dfxtp_1)
  -0.07   62.33   library setup time
          62.33   data required time
---------------------------------------------------------
          62.33   data required time
          -4.50   data arrival time
---------------------------------------------------------
          57.83   slack (MET)
""",
"""
OpenSTA 2.6.0 f71b38bbce Copyright (c) 2024, Parallax Software, Inc.
License GPLv3: GNU GPL version 3 <http://gnu.org/licenses/gpl.html>

This is free software, and you are free to change and redistribute it
under certain conditions; type `show_copying' for details. 
This program comes with ABSOLUTELY NO WARRANTY; for details type `show_warranty'.
Warning: ../../hardware_lib/sky130_fd_sc_hd__ff_n40C_1v65.lib line 23, default_fanout_load is 0.0.
Warning: constraints.sdc line 7, set_input_delay relative to a clock defined on the same port/pin not allowed.
Warning: constraints.sdc line 8, set_input_delay relative to a clock defined on the same port/pin not allowed.
Group                  Internal  Switching    Leakage      Total
                          Power      Power      Power      Power (Watts)
----------------------------------------------------------------
Sequential             2.83e-12   1.29e-12   1.46e-10   1.50e-10  45.5%
Combinational          9.17e-13   1.04e-12   1.78e-10   1.80e-10  54.5%
Clock                  0.00e+00   0.00e+00   0.00e+00   0.00e+00   0.0%
Macro                  0.00e+00   0.00e+00   0.00e+00   0.00e+00   0.0%
Pad                    0.00e+00   0.00e+00   0.00e+00   0.00e+00   0.0%
----------------------------------------------------------------
Total                  3.75e-12   2.34e-12   3.24e-10   3.30e-10 100.0%
                           1.1%       0.7%      98.2%
Warning: power_analysis.tcl line 29, report_checks -group_count is deprecated. Use -group_path_count instead.
Startpoint: reset (input port clocked by clk)
Endpoint: _1023_ (recovery check against rising-edge clock clk)
Path Group: asynchronous
Path Type: max

  Delay    Time   Description
---------------------------------------------------------
   0.00    0.00   clock clk (rise edge)
   0.00    0.00   clock network delay (ideal)
   2.00    2.00 v input external delay
   0.00    2.00 v reset (in)
   0.02    2.02 ^ _0722_/Y (sky130_fd_sc_hd__clkinv_1)
   0.00    2.02 ^ _1023_/RESET_B (sky130_fd_sc_hd__dfrtp_1)
           2.02   data arrival time

1000000000.00 1000000000.00   clock clk (rise edge)
   0.00 1000000000.00   clock network delay (ideal)
  -0.10 1000000000.00   clock uncertainty
   0.00 1000000000.00   clock reconvergence pessimism
        1000000000.00 ^ _1023_/CLK (sky130_fd_sc_hd__dfrtp_1)
   0.19 1000000000.00   library recovery time
        1000000000.00   data required time
---------------------------------------------------------
        1000000000.00   data required time
          -2.02   data arrival time
---------------------------------------------------------
        1000000000.00   slack (MET)


Startpoint: _1025_ (rising edge-triggered flip-flop clocked by clk)
Endpoint: avg_out[0] (output port clocked by clk)
Path Group: clk
Path Type: max

  Delay    Time   Description
---------------------------------------------------------
   0.00    0.00   clock clk (rise edge)
   0.00    0.00   clock network delay (ideal)
   0.00    0.00 ^ _1025_/CLK (sky130_fd_sc_hd__dfrtp_1)
   0.84    0.84 ^ _1025_/Q (sky130_fd_sc_hd__dfrtp_1)
   0.00    0.84 ^ avg_out[0] (out)
           0.84   data arrival time

1000000000.00 1000000000.00   clock clk (rise edge)
   0.00 1000000000.00   clock network delay (ideal)
  -0.10 1000000000.00   clock uncertainty
   0.00 1000000000.00   clock reconvergence pessimism
  -1.50 1000000000.00   output external delay
        1000000000.00   data required time
---------------------------------------------------------
        1000000000.00   data required time
          -0.84   data arrival time
---------------------------------------------------------
        1000000000.00   slack (MET)
"""]

# Call the function to extract the worst-case latency
for timing_report in timing_reports:
    try:
        worst_case_latency = extract_latency(timing_report)
        print(f"Worst-case latency: {worst_case_latency} ns")
    except ValueError as e:
        print(f"Error: {e}")