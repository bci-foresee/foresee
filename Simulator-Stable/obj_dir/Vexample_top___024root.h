// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vexample_top.h for the primary calling header

#ifndef VERILATED_VEXAMPLE_TOP___024ROOT_H_
#define VERILATED_VEXAMPLE_TOP___024ROOT_H_  // guard

#include "verilated.h"


class Vexample_top__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vexample_top___024root final : public VerilatedModule {
  public:

    // DESIGN SPECIFIC STATE
    VL_IN8(clk_adder,0,0);
    CData/*0:0*/ __Vtrigprevexpr___TOP__clk_adder__0;
    CData/*0:0*/ __VactContinue;
    VL_IN16(adder_op_a,15,0);
    VL_IN16(adder_op_b,15,0);
    VL_OUT16(adder_sum,15,0);
    IData/*31:0*/ __VactIterCount;
    VlTriggerVec<1> __VactTriggered;
    VlTriggerVec<1> __VnbaTriggered;

    // INTERNAL VARIABLES
    Vexample_top__Syms* const vlSymsp;

    // CONSTRUCTORS
    Vexample_top___024root(Vexample_top__Syms* symsp, const char* v__name);
    ~Vexample_top___024root();
    VL_UNCOPYABLE(Vexample_top___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
