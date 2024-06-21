// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef VERILATED_VEXAMPLE_TOP__SYMS_H_
#define VERILATED_VEXAMPLE_TOP__SYMS_H_  // guard

#include "verilated.h"

// INCLUDE MODEL CLASS

#include "Vexample_top.h"

// INCLUDE MODULE CLASSES
#include "Vexample_top___024root.h"

// SYMS CLASS (contains all model state)
class alignas(VL_CACHE_LINE_BYTES)Vexample_top__Syms final : public VerilatedSyms {
  public:
    // INTERNAL STATE
    Vexample_top* const __Vm_modelp;
    VlDeleter __Vm_deleter;
    bool __Vm_didInit = false;

    // MODULE INSTANCE STATE
    Vexample_top___024root         TOP;

    // CONSTRUCTORS
    Vexample_top__Syms(VerilatedContext* contextp, const char* namep, Vexample_top* modelp);
    ~Vexample_top__Syms();

    // METHODS
    const char* name() { return TOP.name(); }
};

#endif  // guard
