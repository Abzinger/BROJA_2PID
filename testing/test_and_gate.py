# test_and_gate.py
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

  msg="""Shared information: {SI}
  Unique information in Y: {UIY}
  Unique information in Z: {UIZ}
  Synergistic information: {CI}
  Primal feasibility: {Num_err[0]}
  Dual feasibility: {Num_err[1]}
  Duality Gap: {Num_err[2]}"""
  print(msg.format(**returndata))
  
except BROJA_2PID_Exception:
  print("Cone Programming solver failed to find (near) optimal solution. Please report the input probability density function to abdullah.makkeh@gmail.com")

print("The End")
