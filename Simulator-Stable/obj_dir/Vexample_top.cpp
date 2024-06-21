// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Vexample_top__pch.h"

//============================================================
// Constructors

Vexample_top::Vexample_top(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Vexample_top__Syms(contextp(), _vcname__, this)}
    , clk_adder{vlSymsp->TOP.clk_adder}
    , adder_op_a{vlSymsp->TOP.adder_op_a}
    , adder_op_b{vlSymsp->TOP.adder_op_b}
    , adder_sum{vlSymsp->TOP.adder_sum}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

Vexample_top::Vexample_top(const char* _vcname__)
    : Vexample_top(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Vexample_top::~Vexample_top() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Vexample_top___024root___eval_debug_assertions(Vexample_top___024root* vlSelf);
#endif  // VL_DEBUG
void Vexample_top___024root___eval_static(Vexample_top___024root* vlSelf);
void Vexample_top___024root___eval_initial(Vexample_top___024root* vlSelf);
void Vexample_top___024root___eval_settle(Vexample_top___024root* vlSelf);
void Vexample_top___024root___eval(Vexample_top___024root* vlSelf);

void Vexample_top::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vexample_top::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    Vexample_top___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        vlSymsp->__Vm_didInit = true;
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        Vexample_top___024root___eval_static(&(vlSymsp->TOP));
        Vexample_top___024root___eval_initial(&(vlSymsp->TOP));
        Vexample_top___024root___eval_settle(&(vlSymsp->TOP));
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    Vexample_top___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool Vexample_top::eventsPending() { return false; }

uint64_t Vexample_top::nextTimeSlot() {
    VL_FATAL_MT(__FILE__, __LINE__, "", "%Error: No delays in the design");
    return 0;
}

//============================================================
// Utilities

const char* Vexample_top::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void Vexample_top___024root___eval_final(Vexample_top___024root* vlSelf);

VL_ATTR_COLD void Vexample_top::final() {
    Vexample_top___024root___eval_final(&(vlSymsp->TOP));
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Vexample_top::hierName() const { return vlSymsp->name(); }
const char* Vexample_top::modelName() const { return "Vexample_top"; }
unsigned Vexample_top::threads() const { return 1; }
void Vexample_top::prepareClone() const { contextp()->prepareClone(); }
void Vexample_top::atClone() const {
    contextp()->threadPoolpOnClone();
}
