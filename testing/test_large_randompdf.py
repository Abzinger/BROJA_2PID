# test_large_randompdf.py

import broja_2pid as BROJA
from broja_2pid import BROJA_2PID_Exception

import time
from random import random
from sys import argv

print("test_large_randompdf.py -- part of BROJA_2PID (https://github.com/dot-at/BROJA_2PID/)")
if len(argv) < 4:
    print("Usage: python3 test_large_randompdf.py x y z")
    print("Where:   x is the size of the range of X;")
    print("Where:   y is the size of the range of Y;")
    print("Where:   z is the size of the range of Z.")
    exit(0)
#^ if
try:
    nX = int(argv[1])
    nY = int(argv[2])
    nZ = int(argv[3])
except:
    print("I couldn't parse one of the arguments (they must all be integers)")
    exit(1)
#^except

if min(nX,nY,nZ) < 2:
    print("All sizes of ranges must be at least 2.")
    exit(1)
#^ if

tic = time.process_time()
for iter in range(250):
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
    print("Run BROJA_2PID.pid().")
    itic = time.process_time()
    pid = BROJA.pid(pdf,output=0)
    itoc = time.process_time()
    print("Partial information decomposition: ",pid)
    print("Time: ",itoc-itic,"secs")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#^ for iter
toc = time.process_time()
print("**********************************************************************")
print("Average time: ",(toc-tic)/nX/nY/nZ,"secs")
#EOF
