# test_large_copy_admUI_dit.py

from sys import path
path.insert(0,"..")

import BROJA_2PID as BROJA
from BROJA_2PID import BROJA_2PID_Exception

#path.insert(0, "../../computeUI/python/")
from admUI import computeQUI
from dit import *
import time
from math import log2
from sys import argv

print("test_large_copy_admUI_dit.py -- part of BROJA_2PID (https://github.com/dot-at/BROJA_2PID/)")
if len(argv) != 8:
    print("Usage: python3 test_large_copy_admUI_dit.py l_y u_y step_y l_z u_z step_z s")
    print(" ")
    print("Role :    compute the PID using BROJA_2pid and/or admUI and/or dit")
    print("          of Copy gates such that                                 ")
    print("                                  |Y| in range(l_y,u_y,step_y)    ")
    print("                             and                                  ")
    print("                                  |Z| in range(l_z,u_z,step_z);   ")
    print(" ")
    print("Where:    s  is the solver to compute PID ;")
    print("             BROJA_2pid             if s=0;")
    print("             admUI                  if s=1;")
    print("             dit                    if s=2;")
    print("             BROJA_2pid and admUI   if s=3;")
    print("             BROJA_2pid and admUI   if s=4;")
    print("             all three solvers      if s=5.")    
    exit(0)
#^ if
try:
    l_Y    = int(argv[1])
    u_Y    = int(argv[2])
    step_Y = int(argv[3])
    l_Z    = int(argv[4])
    u_Z    = int(argv[5])
    step_Z = int(argv[6])    
    s      = int(argv[7])
except:
    print("I couldn't parse one of the arguments (they must all be integers)")
    exit(1)
#^except

if min(l_Y,u_Y,l_Z,u_Z) < 2:
    print("All sizes of ranges must be at least 2.")
    exit(1)
#^ if

if l_Y >= u_Y or l_Z >= u_Z:
    print("l_Y < u_Y and l_Z < u_Y")
    exit(1)
#^ if

if s not in range(6):
    print(" s takes values in {0, 1, 2, 3, 4, 5}")
    exit(1)
#^ if
if step_Y >= u_Y:
    print(" Warning |Y| =", l_Y," since step_Y:", step_Y,"is larger than or equal u_Y:", u_Y)
elif step_Z >= u_Z:
    print(" Warning |Z| =", l_Z," since step_Z:", step_Z," is larger than u_Z:", u_Z)

for n_Y in range(l_Y,u_Y,step_Y):
    for n_Z in range(l_Z,u_Z,step_Z):
        print("______________________________________________________________________")
        print("COPY   with |Y| =",n_Y,", |Z| =",n_Z,":")
        print("Create pdf.")
        pdf = dict()
        for y in range(n_Y):
            for z in range(n_Z):
                x = (y,z)
                pdf[ (x,y,z) ] = 1./(n_Y*n_Z)
            #^ for z
        #^ for y

        # Compute PID using BROJA_2PID
        if s == 0 or s == 3 or s == 4 or s == 5 :
            print("Run BROJA_2PID.pid().")
            tic_us = time.process_time()
            pid_ = BROJA.pid(pdf,output=0)
            toc_us = time.process_time()
            # print("Partial information decomposition: ",pid_)
            print("Deviation from analytical results:")
            print("    UIY: ", 100*abs(pid_["UIY"]-log2(n_Y))/log2(n_Y), "%")
            print("    UIZ: ", 100*abs(pid_["UIZ"]-log2(n_Z))/log2(n_Z), "%")
            print("Time: ",toc_us-tic_us,"secs")

        if s != 0:
            dpdf = Distribution(pdf)
            dpdf.set_rv_names('SXY')

        if s == 1 or s == 3 or s == 5:
            
            # Compute PID using computeUI
        
            print("Run ComputeUI.computeQUI().")
            itic_comUI = time.process_time()
            Q = computeQUI(distSXY = dpdf, DEBUG = True)
            UIY = dit.shannon.conditional_entropy(Q, 'S', 'Y') + dit.shannon.conditional_entropy(Q, 'X', 'Y') \
                  - dit.shannon.conditional_entropy(Q, 'SX', 'Y')
            UIZ = dit.shannon.conditional_entropy(Q, 'S', 'X') + dit.shannon.conditional_entropy(Q, 'Y', 'X') \
                  - dit.shannon.conditional_entropy(Q, 'SY', 'X')
            itoc_comUI = time.process_time()
            # print("optimal pdf", Q)
            print("Deviation from analytical results:")
            print("    UIY: ", 100*abs(UIY - log2(n_Y))/log2(n_Y), "%")
            print("    UIZ: ", 100*abs(UIZ - log2(n_Z))/log2(n_Z), "%")
            print("Time_comUI: ",itoc_comUI-itic_comUI,"secs")
            if s != 1:
                # Comparison
                print("UIY_broja_2pid - UIY_computeUI: ", pid_["UIY"] - UIY)
                print("UIZ_broja_2pid - UIZ_computeUI: ", pid_["UIZ"] - UIZ)


        if s == 2 or s == 4 or s == 5:
            print("Run pid.ibroja.i_broja().")
            itic_comUI = time.process_time()
            itic_dit = time.process_time()
            pid_dit = pid.ibroja.i_broja(dpdf, ['X', 'Y'], 'S')
            itoc_dit = time.process_time()
            print("Deviation from analytical results:")
            print("    UIY: ", 100*abs(pid_dit['X'] - log2(n_Y))/log2(n_Y), "%")
            print("    UIZ: ", 100*abs(pid_dit['Y'] - log2(n_Z))/log2(n_Z), "%")
            print("Time_dit: ",itoc_dit-itic_dit,"secs")
            if s !=2:
                # Comparison
                print("UIY_broja_2pid - UIY_dit: ", pid_["UIY"] - pid_dit['X'])
                print("UIZ_broja_2pid - UIZ_dit: ", pid_["UIZ"] - pid_dit['Y'])

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #^ for n_Z
#^ for n_Y
#EOF
