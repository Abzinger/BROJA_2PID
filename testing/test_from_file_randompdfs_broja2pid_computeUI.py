# test_form_file_randompdf_admUI_dit.py

from sys import path
path.insert(0, "..")

import BROJA_2PID as BROJA
from BROJA_2PID import BROJA_2PID_Exception
from dit import *
import time
from random import random
from sys import argv
import pickle
path.insert(0, "../../computeUI/python/")
from admUI import computeQUI

print("test_from_file_randompdf_admUI_dit.py -- part of BROJA_2PID (https://github.com/dot-at/BROJA_2PID/)")
if len(argv)!=7:
    print("Usage: python3 test_large_randompdf.py x y z # pdfs group solver")
    print(" ")
    print("Role :   compute PID using BROJA_2Pid and/or admUI and/or dit")
    print("         of random pdfs stored in the file randompdfs/randompdfs_x_y_z_#pdfs_group.pkl;")
    print(" ")
    print("Where:   x        is the size of the range of X;     ")
    print("         y        is the size of the range of Y;     ")
    print("         z        is the size of the range of Z;     ")
    print("         # pdfs   is the number of pdfs in the file; ")
    print("         group    is the number of the file;         ")
    print("         solver   is the solver to compute PID;      ")
    print("                  BROJA_2pid             if solver=0;")
    print("                  admUI                  if solver=1;")
    print("                  dit                    if solver=2;")
    print("                  BROJA_2pid and admUI   if solver=3;")
    print("                  BROJA_2pid and admUI   if solver=4;")
    print("                  all three solvers      if solver=5.")    
 
    exit(0)
#^ if
try:
    nX      = int(argv[1])
    nY      = int(argv[2])
    nZ      = int(argv[3])
    maxiter = int(argv[4])
    group   = int(argv[5])
    solver  = int(argv[6])
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
if group < 1:
    print("group number is positive")
    exit(1)
#^ if
if solver not in range(6):
    print(" solver takes values in {0, 1, 2, 3, 4, 5}")
    exit(1)
#^ if
parms = dict()
parms['max_iters'] = 100
time_us = 0
time_comUI = 0
time_dit = 0

# Reads the file

f = open("randompdfs/randompdf_"+str(nX)+"_"+str(nY)+"_"+str(nZ)+"_"+str(maxiter)+"_"+str(group)+".pkl", "rb")

# Starts Computing

for iter in range(maxiter):
    print("Random PDFs   with |X| =",nX,"|Y| =",nY," |Z| =",nZ)
    print("______________________________________________________________________")
    print("Read pdf #",maxiter*(group - 1) + iter)
    pdf = pickle.load(f)

    # Compute PID using BROJA_2PID
    
    if s == 0 or s == 3 or s == 5:
        print("Run BROJA_2PID.pid().")
        itic_us = time.process_time()
        pid_ = BROJA.pid(pdf,output=0,**parms)
        print("Partial information decomposition BROJA_2PID: ")
        print("UIY: ", pid_['UIY'])
        print("UIZ: ", pid_['UIZ'])
        print("CI: ", pid_['CI'])
        print("SI: ", pid_['SI'])
        itoc_us = time.process_time()
        temp_us = itoc_us-itic_us
        time_us += temp_us
        print("Time: ",itoc_us-itic_us,"secs")
    #^ if
    
    # Prepare pdf for admUI or dit 

    if s != 0:
        dpdf = Distribution(pdf)
        dpdf.set_rv_names('SXY')
    #^ if
    
    # Compute PID using ComputeUI
    
    if s == 1 or s == 3 or s == 5: 
        print("Run ComputeUI.computeQUI()")
        itic_comUI = time.process_time()
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
        print("Partial information decomposition ComputeUI: ")
        print("UIY_comUI: ", UIY)
        print("UIZ_comUI: ", UIZ)
        print("CI_comUI: ", CI)
        print("SI_comUI: ", SI)
        temp_comUI = itoc_comUI-itic_comUI
        time_comUI += temp_comUI
        print("Time_comUI: ",itoc_comUI-itic_comUI,"secs")

        # Compare BROJA_2PID with ComputeUI 

        if s!= 1:
            print("UIY_diff_comUI: ",UIY - pid_['UIY'])
            print("UIZ_diff_comUI: ",UIZ - pid_['UIZ'])
        #^ if
    #^ if

    # Compute PID using dit package

    if s == 2 or s == 4 or s == 5:
        print("Run dit broja")
        itic_dit = time.process_time()
        try:
            pid_dit = pid.ibroja.i_broja(dpdf, ['X', 'Y'], 'S')
        except dit.exceptions.ditException:
            print(maxiter,", nx=ny=nz=",nX , ", pdf # ", i)
            dit_errorcnt = dit_errorcnt + 1
            continue
        else:    
            print("Partial information decomposition dit:")
            print("UIY_dit:", pid_dit['X'])
            print("UIZ_dit:", pid_dit['Y'])
            itoc_dit = time.process_time()
            temp_dit = itoc_dit-itic_dit
            time_dit += temp_dit
            print("Time_dit: ",itoc_dit-itic_dit,"secs")

        # Compare BROJA_2PID with ComputeUI 

        if s != 2:        
            print("UIY_diff_dit: ",pid_dit['X'] - pid_['UIY'])
            print("UIZ_diff_dit: ",pid_dit['Y'] - pid_['UIZ'])
        #^ if
    #^ if
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#^ for iter
f.close()
print("**********************************************************************")

if s != 2 or s != 3: 
    print("BROJA_2PID Average time: ", (time_us)/maxiter, "secs")
#^ if
if s != 0 or s != 2 or s != 4:
    print("ComputeUI Average time: ", (time_comUI)/maxiter, "secs")
#^ if
if s != 0 or s != 1 or s != 3:
    print("dit Average time: ", (time_dit)/maxiter, "secs")
#^ if
# EOF
