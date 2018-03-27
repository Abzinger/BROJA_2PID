# generate_large_randompdf.py
from random import random
from sys import argv
import pickle

print("generate_large_randompdf.py -- part of BROJA_2PID (https://github.com/dot-at/BROJA_2PID/)")
if len(argv) < 5 or len(argv)>6:
    print("Usage: python3 test_large_randompdf.py x y z [iter]")
    print("Role : creates pdfs are dumped to file randompdf_x_y_z.json")
    print("Where:   x    is the size of the range of X;")
    print("         y    is the size of the range of Y;")
    print("         z    is the size of the range of Z;")
    print("         iter is the number of pdfs to be generated")
    print("         group is the number of the file ")    
    print("              (defaults to 100).")
    exit(0)
#^ if
try:
    nX = int(argv[1])
    nY = int(argv[2])
    nZ = int(argv[3])
    if len(argv)==6:    maxiter = int(argv[4])
    else:               maxiter = 100
    group = int(argv[5])
except:
    print("I couldn't parse one of the arguments (they must all be integers)")
    exit(1)
#^except

if min(nX, nY, nZ) < 2:
    print("All sizes of ranges must be at least 2.")
    exit(1)
#^ if

if maxiter < 1:
    print("# iterations must be >= 1.")
    exit(1)
#^ if
#^ if
if group == 0:
    print("maxiter should be divisible by group 1")
    exit(1)
#^ if
check = maxiter % group
if check != 0:
    print("maxiter should be divisible by group")
    exit(1)
#^ if
num = int(maxiter/group)
if group > 1:
    lis = []
    for i in range(group):
        j = i + 1 
        print("Creating file randompdf_"+str(nX)+"_"+str(nY)+"_"+str(nZ)+"_"+"_"+str(num)+"_"+str(j)+".pkl")
        lis.append(open("randompdf_"+str(nX)+"_"+str(nY)+"_"+str(nZ)+"_"+str(num)+"_"+str(j)+".pkl", "wb"))
else:
    print("Creating file randompdf_"+str(nX)+"_"+str(nY)+"_"+str(nZ)+".pkl")
    f = open("randompdf_"+str(nX)+"_"+str(nY)+"_"+str(nZ)+"_"+str(maxiter)+".pkl", "wb")

# Main Loop  
print("pdfs are being generated and saved...")
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
    # Write pdfs to files
    if group > 1:
        i = int(iter/num)
        pickle.dump(pdf, lis[i])
    else:
        pickle.dump(pdf, f)

#^ for iter
if group > 1:
    for i in range(group):
        lis[i].close()
else:
    f.close()
