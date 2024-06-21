// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vexample_top.h for the primary calling header

#include "Vexample_top__pch.h"
#include "Vexample_top__Syms.h"
#include "Vexample_top___024root.h"

void Vexample_top___024root___ctor_var_reset(Vexample_top___024root* vlSelf);

Vexample_top___024root::Vexample_top___024root(Vexample_top__Syms* symsp, const char* v__name)
    : VerilatedModule{v__name}
    , vlSymsp{symsp}
 {
    // Reset structure values
    Vexample_top___024root___ctor_var_reset(this);
}

void Vexample_top___024root::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

Vexample_top___024root::~Vexample_top___024root() {
}
