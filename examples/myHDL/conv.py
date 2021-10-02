from myhdl import *
from top import top

clk = Signal(bool(0)) 
we  = Signal(bool(0))
sel  = Signal(bool(0))


din  = Signal(intbv(0)[8:])
addr = Signal(intbv(0)[8:])
dout = Signal(intbv(0)[8:])

CONTENT = (0,1,2,3,4,5,6)

top_inst = top(clk,we, din, addr,dout,sel, CONTENT)
top_inst.convert("VHDL")