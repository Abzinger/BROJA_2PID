# tester.py

from broja_2pid import pid, BROJA_2PID_Exception

andgate = dict()
andgate[ (0,0,0) ] = .25
andgate[ (0,0,1) ] = .25
andgate[ (0,1,0) ] = .25
andgate[ (1,1,1) ] = .25

dirty_andgate = andgate.copy()
dirty_andgate[ (1,1,0) ] = 0

xorgate = dict()
xorgate[ (0,0,0) ] = .25
xorgate[ (1,1,0) ] = .25
xorgate[ (1,0,1) ] = .25
xorgate[ (0,1,1) ] = .25

dirty_xorgate = xorgate.copy()
xorgate[ (0,1,0) ] = 0.

print("Quiet mode")
print("==========")
print("AND gate: ",pid(andgate) )
print("XOR gate: ",pid(xorgate) )
print("AND gate (dirty): ",pid(dirty_andgate) )
print("XOR gate (dirty: ",pid(dirty_xorgate) )

print("Output level 1")
print("==============")
print("AND gate: ",pid(andgate, output=1) )
print("XOR gate: ",pid(xorgate, output=1) )
print("AND gate (dirty): ",pid(dirty_andgate, output=1) )
print("XOR gate (dirty: ",pid(dirty_xorgate, output=1) )

print("Output level 2")
print("==============")
print("AND gate: ",pid(andgate, output=2) )
print("XOR gate: ",pid(xorgate, output=2) )
print("AND gate (dirty): ",pid(dirty_andgate, output=2) )
print("XOR gate (dirty: ",pid(dirty_xorgate, output=2) )

print("Quiet, but save solver")
print("======================")
print("AND gate: ",pid(andgate, keep_solver_object=True) )
print("XOR gate: ",pid(xorgate, keep_solver_object=True) )
print("AND gate (dirty): ",pid(dirty_andgate, keep_solver_object=True) )
print("XOR gate (dirty: ",pid(dirty_xorgate, keep_solver_object=True) )
