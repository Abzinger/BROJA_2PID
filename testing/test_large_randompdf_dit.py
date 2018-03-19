# test_large_randompdf.py

from sys import path
path.insert(0, "..")

import BROJA_2PID as BROJA
from BROJA_2PID import BROJA_2PID_Exception

path.insert(0, "../../computeUI/python/")
from admUI import computeQUI
from dit import *
import time
from random import random
from sys import argv

print("test_large_randompdf.py -- part of BROJA_2PID (https://github.com/dot-at/BROJA_2PID/)")
if len(argv) < 4 or len(argv)>5:
    print("Usage: python3 test_large_randompdf.py x y z [iter]")
    print("Where:   x    is the size of the range of X;")
    print("         y    is the size of the range of Y;")
    print("         z    is the size of the range of Z;")
    print("         iter is the number of iterations")
    print("              (defaults to 250).")
    exit(0)
#^ if
try:
    nX = int(argv[1])
    nY = int(argv[2])
    nZ = int(argv[3])
    if len(argv)==5:    maxiter = int(argv[4])
    else:               maxiter = 250
except:
    print("I couldn't parse one of the arguments (they must all be integers)")
    exit(1)
#^except

if min(nX,nY,nZ) < 2:
    print("All sizes of ranges must be at least 2.")
    exit(1)
#^ if

if maxiter < 1:
    print("# iterations must be >= 1.")
    exit(1)
#^ if

# tic = time.process_time()
time_us = 0
time_comUI = 0
time_dit = 0 
for iter in range(maxiter):
    print("Random PDFs   with |X| =",nX,"|Y| =",nY," |Z| =",nZ)
    print("______________________________________________________________________")
    print("Create pdf #",iter)
    pdf = dict()
    pts = [ random() for j in range(1,nX*nY*nZ) ]
    pts.append(0.)
    pts.sort()
    val = 1.
    for x in range(nX):
        for y in range(nY):
            for z in range(nZ):
                newval = pts.pop()
                pdf[ (x,y,z) ] = val - newval
                val = newval
            #^ for z
        #^ for y
    #^ for x
    # Compute PID using BROJA_2PID 
    print("Run BROJA_2PID.pid().")
    itic_us = time.process_time()
    pid_ = BROJA.pid(pdf,output=0)
    print("Partial information decomposition BROJA_2PID: ")
    print("UIY: ", pid_['UIY'])
    print("UIZ: ", pid_['UIZ'])
    print("CI: ", pid_['CI'])
    print("SI: ", pid_['SI'])
    itoc_us = time.process_time()
    temp_us = itoc_us-itic_us
    time_us += temp_us
    print("Time: ",itoc_us-itic_us,"secs")
    # Compute PID using ComputeUI
    print("Run ComputeUI.computeQUI()")
    itic_comUI = time.process_time()
    dpdf = Distribution(pdf)
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
    # print("optimal pdf", Q)
    print("Partial information decomposition ComputeUI: ")
    print("UIY_comUI: ", UIY)
    print("UIZ_comUI: ", UIZ)
    print("CI_comUI: ", CI)
    print("SI_comUI: ", SI)
    temp_comUI = itoc_comUI-itic_comUI
    time_comUI += temp_comUI
    print("Time_comUI: ",itoc_comUI-itic_comUI,"secs")
    print("Run dit broja")
    itic_dit = time.process_time()
    pid_dit = pid.ibroja.i_broja(dpdf, ['X', 'Y'], 'S')
    print("Partial information decomposition dit:")
    print("UIY_dit:", pid_dit['X'])
    print("UIZ_dit:", pid_dit['Y'])
    itoc_dit = time.process_time()
    temp_dit = itoc_dit-itic_dit
    time_dit += temp_dit
    print("Time_dit: ",itoc_dit-itic_dit,"secs")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#^ for iter
toc = time.process_time()
print("**********************************************************************")
print("BROJA_2PID Average time: ", (time_us)/maxiter, "secs")
print("ComputeUI Average time: ", (time_comUI)/maxiter, "secs")
print("dit Average time: ", (time_dit)/maxiter, "secs")
# EOF
