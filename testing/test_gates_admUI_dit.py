# test_gates.py

from sys import path
path.insert(0,"..")

import BROJA_2PID as BROJA
from BROJA_2PID import BROJA_2PID_Exception

path.insert(0, "../../computeUI/python/")
from admUI import computeQUI
from dit import *
import time 


# AND gate
andgate = dict()
andgate[ (0,0,0) ] = .25
andgate[ (0,0,1) ] = .25
andgate[ (0,1,0) ] = .25
andgate[ (1,1,1) ] = .25

dirty_andgate = andgate.copy()
dirty_andgate[ (1,1,0) ] = 0

# XOR gate
xorgate = dict()
xorgate[ (0,0,0) ] = .25
xorgate[ (1,1,0) ] = .25
xorgate[ (1,0,1) ] = .25
xorgate[ (0,1,1) ] = .25

dirty_xorgate = xorgate.copy()
xorgate[ (0,1,0) ] = 0.

# RDN gate
rdngate = dict()
rdngate[ (0,0,0) ] = .5
rdngate[ (1,1,1) ] = .5

dirty_rdngate = rdngate.copy()
dirty_rdngate[ (0,0,1) ] = 0.

# UNQ gate
unqgate = dict()
unqgate[ ((0,0),0,0) ] = .25
unqgate[ ((1,0),1,0) ] = .25
unqgate[ ((0,1),0,1) ] = .25
unqgate[ ((1,1),1,1) ] = .25

dirty_unqgate = unqgate.copy()
dirty_unqgate[ ((0,0),1,1) ] = 0.

# RDNXOR gate
rdnxorgate = dict()
rdnxorgate[ ((0,0), (0,0), (0,0)) ] = .125
rdnxorgate[ ((1,0), (0,0), (1,0)) ] = .125
rdnxorgate[ ((1,0), (1,0), (0,0)) ] = .125
rdnxorgate[ ((0,0), (1,0), (1,0)) ] = .125
rdnxorgate[ ((0,1), (0,1), (0,1)) ] = .125
rdnxorgate[ ((1,1), (0,1), (1,1)) ] = .125
rdnxorgate[ ((1,1), (1,1), (0,1)) ] = .125
rdnxorgate[ ((0,1), (1,1), (1,1)) ] = .125

dirty_rdnxorgate = rdnxorgate.copy()
dirty_rdnxorgate[ ((0,0), (0,0), (1,1)) ] = 0.

# RDNUNQXOR gate
rdnunqxorgate = dict()
rdnunqxorgate[ ((0,0,0,0), (0,0), (0,0)) ] = 1/32
rdnunqxorgate[ ((1,0,0,0), (0,0), (1,0)) ] = 1/32
rdnunqxorgate[ ((0,0,1,0), (0,0), (2,0)) ] = 1/32
rdnunqxorgate[ ((1,0,1,0), (0,0), (3,0)) ] = 1/32
rdnunqxorgate[ ((1,0,0,0), (1,0), (0,0)) ] = 1/32
rdnunqxorgate[ ((0,0,0,0), (1,0), (1,0)) ] = 1/32
rdnunqxorgate[ ((1,0,1,0), (1,0), (2,0)) ] = 1/32
rdnunqxorgate[ ((0,0,1,0), (1,0), (3,0)) ] = 1/32
rdnunqxorgate[ ((0,1,0,0), (2,0), (0,0)) ] = 1/32
rdnunqxorgate[ ((1,1,0,0), (2,0), (1,0)) ] = 1/32
rdnunqxorgate[ ((0,1,1,0), (2,0), (2,0)) ] = 1/32
rdnunqxorgate[ ((1,1,1,0), (2,0), (3,0)) ] = 1/32
rdnunqxorgate[ ((1,1,0,0), (3,0), (0,0)) ] = 1/32
rdnunqxorgate[ ((0,1,0,0), (3,0), (1,0)) ] = 1/32
rdnunqxorgate[ ((1,1,1,0), (3,0), (2,0)) ] = 1/32
rdnunqxorgate[ ((0,1,1,0), (3,0), (3,0)) ] = 1/32
rdnunqxorgate[ ((0,0,0,1), (0,1), (0,1)) ] = 1/32
rdnunqxorgate[ ((1,0,0,1), (0,1), (1,1)) ] = 1/32
rdnunqxorgate[ ((0,0,1,1), (0,1), (2,1)) ] = 1/32
rdnunqxorgate[ ((1,0,1,1), (0,1), (3,1)) ] = 1/32
rdnunqxorgate[ ((1,0,0,1), (1,1), (0,1)) ] = 1/32
rdnunqxorgate[ ((0,0,0,1), (1,1), (1,1)) ] = 1/32
rdnunqxorgate[ ((1,0,1,1), (1,1), (2,1)) ] = 1/32
rdnunqxorgate[ ((0,0,1,1), (1,1), (3,1)) ] = 1/32
rdnunqxorgate[ ((0,1,0,1), (2,1), (0,1)) ] = 1/32
rdnunqxorgate[ ((1,1,0,1), (2,1), (1,1)) ] = 1/32
rdnunqxorgate[ ((0,1,1,1), (2,1), (2,1)) ] = 1/32
rdnunqxorgate[ ((1,1,1,1), (2,1), (3,1)) ] = 1/32
rdnunqxorgate[ ((1,1,0,1), (3,1), (0,1)) ] = 1/32
rdnunqxorgate[ ((0,1,0,1), (3,1), (1,1)) ] = 1/32
rdnunqxorgate[ ((1,1,1,1), (3,1), (2,1)) ] = 1/32
rdnunqxorgate[ ((0,1,1,1), (3,1), (3,1)) ] = 1/32

dirty_rdnunqxorgate = rdnunqxorgate.copy()
dirty_rdnunqxorgate[ ((0,0,0,0), (0,0), (1,1)) ] = 0.

# XORAND gate
xorandgate = dict()
xorandgate[ ((0,0), 0, 0) ] = .25
xorandgate[ ((1,0), 0, 1) ] = .25
xorandgate[ ((1,0), 1, 0) ] = .25
xorandgate[ ((0,1), 1, 1) ] = .25

dirty_xorandgate = xorandgate.copy()
dirty_xorandgate[ ((0,0), 1, 1) ] = 0.


# Run it
print("Run BROJA_2PID.pid().")

itic_us_and = time.process_time()
res = BROJA.pid(andgate)
print("AND gate: ", res)
itoc_us_and = time.process_time()
print("Time: ",itoc_us_and-itic_us_and,"secs")
print("Check results")
print("=============")
print("AND gate:       CI - true_CI = ", res["CI"] - .5)
print("                SI - true_SI = ", res["SI"] - .311278124459132843017578125)


itic_us_xor = time.process_time()
res = BROJA.pid(xorgate)
print("XOR gate: ",res )
itoc_us_xor = time.process_time()
print("Time: ",itoc_us_xor-itic_us_xor,"secs")
print("Check results")
print("=============")
print("XOR gate:       CI - true_CI = ", res["CI"] - 1.)
print("                SI - true_SI = ", res["SI"] - 0.)


itic_us_rdn = time.process_time()
res = BROJA.pid(rdngate)
print("RDN gate: ",      res )
itoc_us_rdn = time.process_time()
print("Time: ",itoc_us_rdn-itic_us_rdn,"secs")
print("Check results")
print("=============")
print("RDN gate:       CI - true_CI = ", res["CI"] - 0.)
print("                SI - true_SI = ", res["SI"] - 1.)


itic_us_unq = time.process_time()
res = BROJA.pid(unqgate)
print("UNQ gate: ",      res )
itoc_us_unq = time.process_time()
print("Time: ",itoc_us_unq-itic_us_unq,"secs")
print("Check results")
print("=============")
print("UNQ gate:       CI - true_CI = ", res["CI"] - 0.)
print("                SI - true_SI = ", res["SI"] - 0.)


itic_us_rdnx = time.process_time()
res =  BROJA.pid(rdnxorgate)
print("RDNXOR gate: ", res  )
itoc_us_rdnx = time.process_time()
print("Time: ",itoc_us_rdnx-itic_us_rdnx,"secs")
print("Check results")
print("=============")
print("RDNXOR gate:    CI - true_CI = ", res["CI"] - 1.)
print("                SI - true_SI = ", res["SI"] - 1.)


itic_us_rdnu = time.process_time()
res = BROJA.pid(rdnunqxorgate)
print("RDNUNQXOR gate: ",res )
itoc_us_rdnu = time.process_time()
print("Time: ",itoc_us_rdnu-itic_us_rdnu,"secs")
print("Check results")
print("=============")

print("RDNUNQXOR gate: CI - true_CI = ", res["CI"] - 1.)
print("                SI - true_SI = ", res["SI"] - 1.)

itic_us_xand = time.process_time()
res =  BROJA.pid(xorandgate)
print("XORAND gate: ",  res )
itoc_us_xand = time.process_time()
print("Time: ",itoc_us_xand-itic_us_xand,"secs")
print("Check results")
print("=============")
print("XORAND gate:    CI - true_CI = ", res["CI"] - 1.)
print("                SI - true_SI = ", res["SI"] - .5)


print("Run computeQUI().")

print("AND gate:")

itic_comUI = time.process_time()
dpdf = Distribution(andgate)
dpdf.set_rv_names('SXY')
Q = computeQUI(distSXY = dpdf, DEBUG = True)
UIY = dit.shannon.conditional_entropy(Q, 'S', 'Y') + dit.shannon.conditional_entropy(Q, 'X', 'Y') \
      - dit.shannon.conditional_entropy(Q, 'SX', 'Y')
UIZ = dit.shannon.conditional_entropy(Q, 'S', 'X') + dit.shannon.conditional_entropy(Q, 'Y', 'X') \
      - dit.shannon.conditional_entropy(Q, 'SY', 'X')
CI = dit.shannon.conditional_entropy(Q, 'S', 'XY') - dit.shannon.conditional_entropy(dpdf, 'S', 'XY')
SI = dit.shannon.entropy(Q, 'S')\
     -dit.shannon.conditional_entropy(Q, 'S', 'XY') \
     - dit.shannon.conditional_entropy(Q, 'S', 'Y') - dit.shannon.conditional_entropy(Q, 'X', 'Y') \
     + dit.shannon.conditional_entropy(Q, 'SX', 'Y')\
     - dit.shannon.conditional_entropy(Q, 'S', 'X') - dit.shannon.conditional_entropy(Q, 'Y', 'X') \
     + dit.shannon.conditional_entropy(Q, 'SY', 'X')
itoc_comUI = time.process_time()
print("Time_comUI: ",itoc_comUI-itic_comUI,"secs")
print("Check results")
print("=============")
print("AND gate:       CI - true_CI = ", CI - .5)
print("                SI - true_SI = ", SI - .311278124459132843017578125)

print("XOR gate:")
itic_comUI = time.process_time()
dpdf = Distribution(xorgate)
dpdf.set_rv_names('SXY')
Q = computeQUI(distSXY = dpdf, DEBUG = True)
UIY = dit.shannon.conditional_entropy(Q, 'S', 'Y') + dit.shannon.conditional_entropy(Q, 'X', 'Y') \
      - dit.shannon.conditional_entropy(Q, 'SX', 'Y')
UIZ = dit.shannon.conditional_entropy(Q, 'S', 'X') + dit.shannon.conditional_entropy(Q, 'Y', 'X') \
      - dit.shannon.conditional_entropy(Q, 'SY', 'X')
CI = dit.shannon.conditional_entropy(Q, 'S', 'XY') - dit.shannon.conditional_entropy(dpdf, 'S', 'XY')
SI = dit.shannon.entropy(Q, 'S')\
     -dit.shannon.conditional_entropy(Q, 'S', 'XY') \
     - dit.shannon.conditional_entropy(Q, 'S', 'Y') - dit.shannon.conditional_entropy(Q, 'X', 'Y') \
     + dit.shannon.conditional_entropy(Q, 'SX', 'Y')\
     - dit.shannon.conditional_entropy(Q, 'S', 'X') - dit.shannon.conditional_entropy(Q, 'Y', 'X') \
     + dit.shannon.conditional_entropy(Q, 'SY', 'X')
itoc_comUI = time.process_time()
print("Time_comUI: ",itoc_comUI-itic_comUI,"secs")
print("Check results")
print("=============")
print("XOR gate:       CI - true_CI = ", CI - 1.)
print("                SI - true_SI = ", SI - 0.)

print("RDN gate:")
itic_comUI = time.process_time()
dpdf = Distribution(rdngate)
dpdf.set_rv_names('SXY')
Q = computeQUI(distSXY = dpdf, DEBUG = True)
UIY = dit.shannon.conditional_entropy(Q, 'S', 'Y') + dit.shannon.conditional_entropy(Q, 'X', 'Y') \
      - dit.shannon.conditional_entropy(Q, 'SX', 'Y')
UIZ = dit.shannon.conditional_entropy(Q, 'S', 'X') + dit.shannon.conditional_entropy(Q, 'Y', 'X') \
      - dit.shannon.conditional_entropy(Q, 'SY', 'X')
CI = dit.shannon.conditional_entropy(Q, 'S', 'XY') - dit.shannon.conditional_entropy(dpdf, 'S', 'XY')
SI = dit.shannon.entropy(Q, 'S')\
     -dit.shannon.conditional_entropy(Q, 'S', 'XY') \
     - dit.shannon.conditional_entropy(Q, 'S', 'Y') - dit.shannon.conditional_entropy(Q, 'X', 'Y') \
     + dit.shannon.conditional_entropy(Q, 'SX', 'Y')\
     - dit.shannon.conditional_entropy(Q, 'S', 'X') - dit.shannon.conditional_entropy(Q, 'Y', 'X') \
     + dit.shannon.conditional_entropy(Q, 'SY', 'X')
itoc_comUI = time.process_time()
print("Time_comUI: ",itoc_comUI-itic_comUI,"secs")
print("Check results")
print("=============")
print("RDN gate:       CI - true_CI = ", CI - 0.)
print("                SI - true_SI = ", SI - 1.)


print("UNQ gate:")
itic_comUI = time.process_time()
dpdf = Distribution(unqgate)
dpdf.set_rv_names('SXY')
Q = computeQUI(distSXY = dpdf, DEBUG = True)
UIY = dit.shannon.conditional_entropy(Q, 'S', 'Y') + dit.shannon.conditional_entropy(Q, 'X', 'Y') \
      - dit.shannon.conditional_entropy(Q, 'SX', 'Y')
UIZ = dit.shannon.conditional_entropy(Q, 'S', 'X') + dit.shannon.conditional_entropy(Q, 'Y', 'X') \
      - dit.shannon.conditional_entropy(Q, 'SY', 'X')
CI = dit.shannon.conditional_entropy(Q, 'S', 'XY') - dit.shannon.conditional_entropy(dpdf, 'S', 'XY')
SI = dit.shannon.entropy(Q, 'S')\
     -dit.shannon.conditional_entropy(Q, 'S', 'XY') \
     - dit.shannon.conditional_entropy(Q, 'S', 'Y') - dit.shannon.conditional_entropy(Q, 'X', 'Y') \
     + dit.shannon.conditional_entropy(Q, 'SX', 'Y')\
     - dit.shannon.conditional_entropy(Q, 'S', 'X') - dit.shannon.conditional_entropy(Q, 'Y', 'X') \
     + dit.shannon.conditional_entropy(Q, 'SY', 'X')
itoc_comUI = time.process_time()
print("Time_comUI: ",itoc_comUI-itic_comUI,"secs")
print("Check results")
print("=============")
print("UNQ gate:       CI - true_CI = ", CI - 0.)
print("                SI - true_SI = ", SI - 0.)


print("RDNXOR gate:")
itic_comUI = time.process_time()
dpdf = Distribution(rdnxorgate)
dpdf.set_rv_names('SXY')
Q = computeQUI(distSXY = dpdf, DEBUG = True)
UIY = dit.shannon.conditional_entropy(Q, 'S', 'Y') + dit.shannon.conditional_entropy(Q, 'X', 'Y') \
      - dit.shannon.conditional_entropy(Q, 'SX', 'Y')
UIZ = dit.shannon.conditional_entropy(Q, 'S', 'X') + dit.shannon.conditional_entropy(Q, 'Y', 'X') \
      - dit.shannon.conditional_entropy(Q, 'SY', 'X')
CI = dit.shannon.conditional_entropy(Q, 'S', 'XY') - dit.shannon.conditional_entropy(dpdf, 'S', 'XY')
SI = dit.shannon.entropy(Q, 'S')\
     -dit.shannon.conditional_entropy(Q, 'S', 'XY') \
     - dit.shannon.conditional_entropy(Q, 'S', 'Y') - dit.shannon.conditional_entropy(Q, 'X', 'Y') \
     + dit.shannon.conditional_entropy(Q, 'SX', 'Y')\
     - dit.shannon.conditional_entropy(Q, 'S', 'X') - dit.shannon.conditional_entropy(Q, 'Y', 'X') \
     + dit.shannon.conditional_entropy(Q, 'SY', 'X')
itoc_comUI = time.process_time()
print("Time_comUI: ",itoc_comUI-itic_comUI,"secs")
print("Check results")
print("=============")
print("RDNXOR gate:    CI - true_CI = ", CI - 1.)
print("                SI - true_SI = ", SI - 1.)

print("RDNUNQXOR gate:")
itic_comUI = time.process_time()
dpdf = Distribution(rdnunqxorgate)
dpdf.set_rv_names('SXY')
Q = computeQUI(distSXY = dpdf, DEBUG = True)
UIY = dit.shannon.conditional_entropy(Q, 'S', 'Y') + dit.shannon.conditional_entropy(Q, 'X', 'Y') \
      - dit.shannon.conditional_entropy(Q, 'SX', 'Y')
UIZ = dit.shannon.conditional_entropy(Q, 'S', 'X') + dit.shannon.conditional_entropy(Q, 'Y', 'X') \
      - dit.shannon.conditional_entropy(Q, 'SY', 'X')
CI = dit.shannon.conditional_entropy(Q, 'S', 'XY') - dit.shannon.conditional_entropy(dpdf, 'S', 'XY')
SI = dit.shannon.entropy(Q, 'S')\
     -dit.shannon.conditional_entropy(Q, 'S', 'XY') \
     - dit.shannon.conditional_entropy(Q, 'S', 'Y') - dit.shannon.conditional_entropy(Q, 'X', 'Y') \
     + dit.shannon.conditional_entropy(Q, 'SX', 'Y')\
     - dit.shannon.conditional_entropy(Q, 'S', 'X') - dit.shannon.conditional_entropy(Q, 'Y', 'X') \
     + dit.shannon.conditional_entropy(Q, 'SY', 'X')
itoc_comUI = time.process_time()
print("Time_comUI: ",itoc_comUI-itic_comUI,"secs")
print("Check results")
print("=============")
print("RDNUNQXOR gate: CI - true_CI = ", CI - 1.)
print("                SI - true_SI = ", SI - 1.)

print("XORAND gate:")
itic_comUI = time.process_time()
dpdf = Distribution(xorandgate)
dpdf.set_rv_names('SXY')
Q = computeQUI(distSXY = dpdf, DEBUG = True)
UIY = dit.shannon.conditional_entropy(Q, 'S', 'Y') + dit.shannon.conditional_entropy(Q, 'X', 'Y') \
      - dit.shannon.conditional_entropy(Q, 'SX', 'Y')
UIZ = dit.shannon.conditional_entropy(Q, 'S', 'X') + dit.shannon.conditional_entropy(Q, 'Y', 'X') \
      - dit.shannon.conditional_entropy(Q, 'SY', 'X')
CI = dit.shannon.conditional_entropy(Q, 'S', 'XY') - dit.shannon.conditional_entropy(dpdf, 'S', 'XY')
SI = dit.shannon.entropy(Q, 'S')\
     -dit.shannon.conditional_entropy(Q, 'S', 'XY') \
     - dit.shannon.conditional_entropy(Q, 'S', 'Y') - dit.shannon.conditional_entropy(Q, 'X', 'Y') \
     + dit.shannon.conditional_entropy(Q, 'SX', 'Y')\
     - dit.shannon.conditional_entropy(Q, 'S', 'X') - dit.shannon.conditional_entropy(Q, 'Y', 'X') \
     + dit.shannon.conditional_entropy(Q, 'SY', 'X')
itoc_comUI = time.process_time()
print("Time_comUI: ",itoc_comUI-itic_comUI,"secs")
print("Check results")
print("=============")
print("XORAND gate:    CI - true_CI = ", CI - 1.)
print("                SI - true_SI = ", SI - .5)


print("Run dit broja")

print("AND gate:")
itic_dit = time.process_time()
dpdf = Distribution(andgate)
dpdf.set_rv_names('SXY')
pid_dit = pid.ibroja.i_broja(dpdf, ['X', 'Y'], 'S')
print("Partial information decomposition dit:")

print("UIY_dit:", pid_dit['X'])
print("UIZ_dit:", pid_dit['Y'])
 
itoc_dit = time.process_time()
print("Time_dit: ",itoc_dit-itic_dit,"secs")


print("XOR gate:")
itic_dit = time.process_time()
dpdf = Distribution(xorgate)
dpdf.set_rv_names('SXY')
pid_dit = pid.ibroja.i_broja(dpdf, ['X', 'Y'], 'S')
print("Partial information decomposition dit:")

print("UIY_dit:", pid_dit['X'])
print("UIZ_dit:", pid_dit['Y'])
 
itoc_dit = time.process_time()
print("Time_dit: ",itoc_dit-itic_dit,"secs")


print("RDN gate:")
itic_dit = time.process_time()
dpdf = Distribution(rdngate)
dpdf.set_rv_names('SXY')
pid_dit = pid.ibroja.i_broja(dpdf, ['X', 'Y'], 'S')
print("Partial information decomposition dit:")

print("UIY_dit:", pid_dit['X'])
print("UIZ_dit:", pid_dit['Y'])
 
itoc_dit = time.process_time()
print("Time_dit: ",itoc_dit-itic_dit,"secs")


print("UNQ gate:")
itic_dit = time.process_time()
dpdf = Distribution(unqgate)
dpdf.set_rv_names('SXY')
pid_dit = pid.ibroja.i_broja(dpdf, ['X', 'Y'], 'S')
print("Partial information decomposition dit:")

print("UIY_dit:", pid_dit['X'])
print("UIZ_dit:", pid_dit['Y'])
 
itoc_dit = time.process_time()
print("Time_dit: ",itoc_dit-itic_dit,"secs")


print("RDNXOR gate:")
itic_dit = time.process_time()
dpdf = Distribution(rdnxorgate)
dpdf.set_rv_names('SXY')
pid_dit = pid.ibroja.i_broja(dpdf, ['X', 'Y'], 'S')
print("Partial information decomposition dit:")

print("UIY_dit:", pid_dit['X'])
print("UIZ_dit:", pid_dit['Y'])
 
itoc_dit = time.process_time()
print("Time_dit: ",itoc_dit-itic_dit,"secs")


print("RDNUNQXOR gate:")
itic_dit = time.process_time()
dpdf = Distribution(rdnunqxorgate)
dpdf.set_rv_names('SXY')
pid_dit = pid.ibroja.i_broja(dpdf, ['X', 'Y'], 'S')
print("Partial information decomposition dit:")

print("UIY_dit:", pid_dit['X'])
print("UIZ_dit:", pid_dit['Y'])
 
itoc_dit = time.process_time()
print("Time_dit: ",itoc_dit-itic_dit,"secs")

print("XORAND gate:")
itic_dit = time.process_time()
dpdf = Distribution(xorandgate)
dpdf.set_rv_names('SXY')
pid_dit = pid.ibroja.i_broja(dpdf, ['X', 'Y'], 'S')
print("Partial information decomposition dit:")

print("UIY_dit:", pid_dit['X'])
print("UIZ_dit:", pid_dit['Y'])
 
itoc_dit = time.process_time()
print("Time_dit: ",itoc_dit-itic_dit,"secs")
