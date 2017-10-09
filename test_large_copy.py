# test_large_copy.py

import broja_2pid as BROJA
from broja_2pid import BROJA_2PID_Exception

import time

n_Y = 10
for n_Z in range(10,1000,10):
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
    print("Run BROJA_2PID.pid().")
    tic = time.process_time()
    pid = BROJA.pid(pdf,output=0)
    toc = time.process_time()
    print("Partial information decomposition: ",pid)
    print("Time: ",toc-tic,"sex")
    Abdullah: Check whether result is correct :)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#^ for n_Z
