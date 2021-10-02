from myhdl import *

@block
def mux(sel, data0, data1, dout):
    @always_comb
    def logic():
        if sel == 0:
            dout.next = data0
        else:
            dout.next = data1
    return logic
