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

# ECOS parameters 
parms = dict()
parms['max_iters'] = 10

print("Starting BROJA_2PID.pid() on AND gate.")
try:
  returndict = pid(andgate, cone_solver="ECOS", output=2, **parms)

  print("Shared information: ",returndict['SI'])
  print("Unique information in Y: ",returndict['UIY'])
  print("Unique information in Z: ",returndict['UIZ'])
  print("Synergistic information: ",returndict['CI'])
  print("Gap between feasible solution value and lower bound: ", returndict['Num_err'][2])
  print("Primal feasibility: ", returndict['Num_err'][0])
  print("Dual feasibility: ", returndict['Num_err'][1])

except BROJA_2PID_Exception:
  print("Cone Programming solver failed to find (near) optimal solution. Please report the input probability density function to abdullah.makkeh@gmail.com")

print("The End")
