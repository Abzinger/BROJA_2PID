# test_gates.py

from sys import path
path.insert(0,"..")

from BROJA_2PID import pid, BROJA_2PID_Exception

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
print("Quiet mode")
print("==========")
print("AND gate: ",      pid(andgate) )
print("XOR gate: ",      pid(xorgate) )
print("RDN gate: ",      pid(rdngate) )
print("UNQ gate: ",      pid(unqgate) )
print("RDNXOR gate: ",   pid(rdnxorgate) )
print("RDNUNQXOR gate: ",pid(rdnunqxorgate) )
print("XORAND gate: ",   pid(xorandgate) )

print("AND gate (dirty): ",      pid(dirty_andgate) )
print("XOR gate (dirty): ",      pid(dirty_xorgate) )
print("RDN gate (dirty): ",      pid(dirty_rdngate) )
print("UNQ gate (dirty): ",      pid(dirty_unqgate) )
print("RDNXOR gate (dirty): ",   pid(dirty_rdnxorgate) )
print("RDNUNQXOR gate (dirty): ",pid(dirty_rdnunqxorgate) )
print("XORAND gate (dirty): ",   pid(dirty_xorandgate) )

print("Output level 1")
print("==============")
print("AND gate: ",      pid(andgate, output=1) )
print("XOR gate: ",      pid(xorgate, output=1) )
print("RDN gate: ",      pid(rdngate, output=1) )
print("UNQ gate: ",      pid(unqgate, output=1) )
print("RDNXOR gate: ",   pid(rdnxorgate, output=1) )
print("RDNUNQXOR gate: ",pid(rdnunqxorgate, output=1) )
print("XORAND gate: ",   pid(xorandgate, output=1) )

print("AND gate (dirty): ",      pid(dirty_andgate, output=1) )
print("XOR gate (dirty): ",      pid(dirty_xorgate, output=1) )
print("RDN gate (dirty): ",      pid(dirty_rdngate, output=1) )
print("UNQ gate (dirty): ",      pid(dirty_unqgate, output=1) )
print("RDNXOR gate (dirty): ",   pid(dirty_rdnxorgate, output=1) )
print("RDNUNQXOR gate (dirty): ",pid(dirty_rdnunqxorgate, output=1) )
print("XORAND gate (dirty): ",   pid(dirty_xorandgate, output=1) )

print("Output level 2")
print("==============")
print("AND gate: ",      pid(andgate, output=2) )
print("XOR gate: ",      pid(xorgate, output=2) )
print("RDN gate: ",      pid(rdngate, output=2) )
print("UNQ gate: ",      pid(unqgate, output=2) )
print("RDNXOR gate: ",   pid(rdnxorgate, output=2) )
print("RDNUNQXOR gate: ",pid(rdnunqxorgate, output=2) )
print("XORAND gate: ",   pid(xorandgate, output=2) )

print("AND gate (dirty): ",      pid(dirty_andgate, output=2) )
print("XOR gate (dirty): ",      pid(dirty_xorgate, output=2) )
print("RDN gate (dirty): ",      pid(dirty_rdngate, output=1) )
print("UNQ gate (dirty): ",      pid(dirty_unqgate, output=1) )
print("RDNXOR gate (dirty): ",   pid(dirty_rdnxorgate, output=2) )
print("RDNUNQXOR gate (dirty): ",pid(dirty_rdnunqxorgate, output=2) )
print("XORAND gate (dirty): ",   pid(dirty_xorandgate, output=2) )


print("Quiet, but save solver")
print("======================")
print("AND gate: ",      pid(andgate, keep_solver_object=True) )
print("XOR gate: ",      pid(xorgate, keep_solver_object=True) )
print("RDN gate: ",      pid(rdngate, keep_solver_object=True) )
print("UNQ gate: ",      pid(unqgate, keep_solver_object=True) )
print("RDNXOR gate: ",   pid(rdnxorgate, keep_solver_object=True) )
print("RDNUNQXOR gate: ",pid(rdnunqxorgate, keep_solver_object=True) )
print("XORAND gate: ",   pid(xorandgate, keep_solver_object=True) )

print("AND gate (dirty): ",      pid(dirty_andgate, keep_solver_object=True) )
print("XOR gate (dirty): ",      pid(dirty_xorgate, keep_solver_object=True) )
print("RDN gate (dirty): ",      pid(dirty_rdngate, keep_solver_object=True) )
print("UNQ gate (dirty): ",      pid(dirty_unqgate, keep_solver_object=True) )
print("RDNXOR gate (dirty): ",   pid(dirty_rdnxorgate, keep_solver_object=True) )
print("RDNUNQXOR gate (dirty): ",pid(dirty_rdnunqxorgate, keep_solver_object=True) )
print("XORAND gate (dirty): ",   pid(dirty_xorandgate, keep_solver_object=True) )

# Check correctness

print("Check results")
print("=============")
print("AND gate:       CI - true_CI = ", pid(andgate)["CI"] - .5)
print("                SI - true_SI = ", pid(andgate)["SI"] - .311278124459132843017578125)

print("XOR gate:       CI - true_CI = ", pid(xorgate)["CI"] - 1.)
print("                SI - true_SI = ", pid(xorgate)["SI"] - 0.)

print("RDN gate:       CI - true_CI = ", pid(rdngate)["CI"] - 0.)
print("                SI - true_SI = ", pid(rdngate)["SI"] - 1.)

print("UNQ gate:       CI - true_CI = ", pid(unqgate)["CI"] - 0.)
print("                SI - true_SI = ", pid(unqgate)["SI"] - 0.)

print("RDNXOR gate:    CI - true_CI = ", pid(rdnxorgate)["CI"] - 1.)
print("                SI - true_SI = ", pid(rdnxorgate)["SI"] - 1.)

print("RDNUNQXOR gate: CI - true_CI = ", pid(rdnunqxorgate)["CI"] - 1.)
print("                SI - true_SI = ", pid(rdnunqxorgate)["SI"] - 1.)

print("XORAND gate:    CI - true_CI = ", pid(xorandgate)["CI"] - 1.)
print("                SI - true_SI = ", pid(xorandgate)["SI"] - .5)
