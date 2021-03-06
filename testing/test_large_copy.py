# test_large_copy.py

from sys import path
path.insert(0,"..")

import BROJA_2PID as BROJA
from BROJA_2PID import BROJA_2PID_Exception

import time
from math import log2

for n_Y in range(10,1000,10):
    for n_Z in [10,25]:
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
        print("Deviation from analytical results:")
        print("    UIY:", 100*abs(pid["UIY"]-log2(n_Y))/log2(n_Y), "%")
        print("    UIZ:", 100*abs(pid["UIZ"]-log2(n_Z))/log2(n_Z), "%")
        print("Time: ",toc-tic,"secs")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #^ for n_Z
#^ for n_Y
#EOF
