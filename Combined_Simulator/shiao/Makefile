# Makefile

TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(shell pwd)/processing_elements/rtl_toplevel/seizure_pipe.v
VERILOG_SOURCES += $(shell pwd)/processing_elements/rtl_PEs/spiral_fft_8192.v
TOPLEVEL = seizure_pipe
# MODULE = pipeline
MODULE = pipeline_trainedSVM
include $(shell cocotb-config --makefiles)/Makefile.sim