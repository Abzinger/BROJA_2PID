# test_and_gate.py
from sys import path
path.insert(0,"..")

from BROJA_2PID import pid, BROJA_2PID_Exception

# AND gate
andgate = dict()
andgate[ (0,0,0) ] = .25
andgate[ (0,0,1) ] = .25
andgate[ (0,1,0) ] = .25
andgate[ (1,1,1) ] = .25

print("Starting BROJA_2PID.pid() on AND gate.")
try:
  returndict = pid(andgate, output=1) )

  print("Shared information: ",returndict['SI'])
  print("Unique information in Y:,returndict['.......
  ...
  print("Gap between feasible solution value and lower bound: ", returndict['Num_err'][?])
  print("Primal feasibility: ",....
  print("Dual feasibility: ",....

catch BROJA_2PID_Exception ..... : Check how this is done
  ...

print("The End")
