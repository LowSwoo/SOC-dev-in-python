from myhdl import *
from ram import RAM
from rom import ROM
from mux import mux

@block
def top(clk, we, din, addr, dout,sel, CONTENT):
    """
    clk - clock signal
    we  - write enable signal for ram
    din - data input signal for ram
    addr - address signal for ram or rom
    dout - data output signal for ram or rom
    CONTENT - constant data for rom interface
    sel - select signal. provice choose between ram n rom

    """
    dout0 = Signal(intbv(0)[8:])
    dout1 = Signal(intbv(0)[8:])
    rom_inst = ROM(dout0, addr, CONTENT)
    ram_inst = RAM(dout1, din, addr, we, clk)
    mux_inst = mux(sel, dout0, dout1, dout)

    return rom_inst, ram_inst, mux_inst

   

