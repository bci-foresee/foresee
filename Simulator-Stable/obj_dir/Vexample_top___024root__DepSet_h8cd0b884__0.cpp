// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vexample_top.h for the primary calling header

#include "Vexample_top__pch.h"
#include "Vexample_top__Syms.h"
#include "Vexample_top___024root.h"

#ifdef VL_DEBUG
VL_ATTR_COLD void Vexample_top___024root___dump_triggers__act(Vexample_top___024root* vlSelf);
#endif  // VL_DEBUG

void Vexample_top___024root___eval_triggers__act(Vexample_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vexample_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vexample_top___024root___eval_triggers__act\n"); );
    // Body
    vlSelf->__VactTriggered.set(0U, ((IData)(vlSelf->clk_adder) 
                                     & (~ (IData)(vlSelf->__Vtrigprevexpr___TOP__clk_adder__0))));
    vlSelf->__Vtrigprevexpr___TOP__clk_adder__0 = vlSelf->clk_adder;
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vexample_top___024root___dump_triggers__act(vlSelf);
    }
#endif
}
