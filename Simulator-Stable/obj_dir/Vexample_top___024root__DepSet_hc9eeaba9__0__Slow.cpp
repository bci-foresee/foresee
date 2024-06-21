// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vexample_top.h for the primary calling header

#include "Vexample_top__pch.h"
#include "Vexample_top___024root.h"

VL_ATTR_COLD void Vexample_top___024root___eval_static(Vexample_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vexample_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vexample_top___024root___eval_static\n"); );
}

VL_ATTR_COLD void Vexample_top___024root___eval_initial(Vexample_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vexample_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vexample_top___024root___eval_initial\n"); );
    // Body
    vlSelf->__Vtrigprevexpr___TOP__clk_adder__0 = vlSelf->clk_adder;
}

VL_ATTR_COLD void Vexample_top___024root___eval_final(Vexample_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vexample_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vexample_top___024root___eval_final\n"); );
}

VL_ATTR_COLD void Vexample_top___024root___eval_settle(Vexample_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vexample_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vexample_top___024root___eval_settle\n"); );
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vexample_top___024root___dump_triggers__act(Vexample_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vexample_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vexample_top___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ vlSelf->__VactTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelf->__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 0 is active: @(posedge clk_adder)\n");
    }
}
#endif  // VL_DEBUG

#ifdef VL_DEBUG
VL_ATTR_COLD void Vexample_top___024root___dump_triggers__nba(Vexample_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vexample_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vexample_top___024root___dump_triggers__nba\n"); );
    // Body
    if ((1U & (~ vlSelf->__VnbaTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelf->__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 0 is active: @(posedge clk_adder)\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vexample_top___024root___ctor_var_reset(Vexample_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vexample_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vexample_top___024root___ctor_var_reset\n"); );
    // Body
    vlSelf->clk_adder = VL_RAND_RESET_I(1);
    vlSelf->adder_op_a = VL_RAND_RESET_I(16);
    vlSelf->adder_op_b = VL_RAND_RESET_I(16);
    vlSelf->adder_sum = VL_RAND_RESET_I(16);
    vlSelf->__Vtrigprevexpr___TOP__clk_adder__0 = VL_RAND_RESET_I(1);
}
