# BROJA_2PID.py -- Python module
#
# BROJA_2PID: Bertschinger-Rauh-Olbrich-Jost-Ay (BROJA) bivariate Partial Information Decomposition
# https://github.com/Abzinger/BROJA_2PID
# (c) Abdullah Makkeh, Dirk Oliver Theis
# Permission to use and modify with proper attribution
# (Apache License version 2.0)
#
# Information about the algorithm, documentation, and examples are here:
# @Article{makkeh-theis-vicente:pidOpt:2017,
#          author =       {Makkeh, Abdullah and Theis, Dirk Oliver and Vicente, Raul},
#          title =        {BROJA-2PID: A cone-programming based Partial Information Decomposition estimator},
#          journal =      {jo},
#          year =         2017,
#          key =       {key},
#          volume =    {vol},
#          number =    {nr},
#          pages =     {1--2}
# }
# Please cite this paper when you use this software (cf. README.md)
##############################################################################################################

from ecos  import solve
from scipy import sparse
import numpy as np
from numpy import linalg as LA
import math
from collections import defaultdict

log = math.log2
ln  = math.log

# ECOS's exp cone: (r,p,q)   w/   q>0  &  exp(r/q) ≤ p/q
# Translation:     (0,1,2)   w/   2>0  &  0/2      ≤ ln(1/2)
def r_vidx(i):
    return 3*i
def p_vidx(i):
    return 3*i+1
def q_vidx(i):
    return 3*i+2

class BROJA_2PID_Exception(Exception):
    pass


class Solve_w_ECOS:
    # (c) Abdullah Makkeh, Dirk Oliver Theis
    # Permission to use and modify under Apache License version 2.0
    def __init__(self, marg_xy, marg_xz):
        # (c) Abdullah Makkeh, Dirk Oliver Theis
        # Permission to use and modify under Apache License version 2.0

        # ECOS parameters
        self.feastol       = None
        self.abstol        = None
        self.reltol        = None
        self.feastol_inacc = None
        self.abstol_innac  = None
        self.reltol_inacc  = None
        self.max_iters     = None
        self.verbose       = False

        # Data for ECOS
        self.c            = None
        self.G            = None
        self.h            = None
        self.dims         = dict()
        self.A            = None
        self.b            = None

        # ECOS result
        self.sol_rpq    = None
        self.sol_slack  = None #
        self.sol_lambda = None # dual variables for equality constraints
        self.sol_mu     = None # dual variables for generalized ieqs
        self.sol_info   = None

        # Probability density funciton data
        self.b_xy         = dict(marg_xy)
        self.b_xz         = dict(marg_xz)
        self.X            = set( [ x   for x,y in self.b_xy.keys() ] + [ x   for x,z in self.b_xz.keys() ] )
        self.Y            = set( [  y  for x,y in self.b_xy.keys() ] )
        self.Z            = set(                                       [  z  for x,z in self.b_xz.keys() ] )
        self.idx_of_trip  = dict()
        self.trip_of_idx  = []

        # Do stuff:
        for x in self.X:
            for y in self.Y:
                if (x,y) in self.b_xy.keys():
                    for z in self.Z:
                        if (x,z) in self.b_xz.keys():
                            self.idx_of_trip[ (x,y,z) ] = len( self.trip_of_idx )
                            self.trip_of_idx.append( (x,y,z) )
                        #^ if
                    #^ for z
            #^ for y
        #^ for x
    #^ init()

    def create_model(self):
        # (c) Abdullah Makkeh, Dirk Oliver Theis
        # Permission to use and modify under Apache License version 2.0
        n = len(self.trip_of_idx)
        m = len(self.b_xy) + len(self.b_xz)
        n_vars = 3*n
        n_cons = n+m

        #
        # Create the equations: Ax = b
        #
        self.b = np.zeros((n_cons,),dtype=np.double)

        Eqn   = []
        Var   = []
        Coeff = []

        # The q-p coupling equations: q_{*yz} - p_{xyz} = 0
        for i,xyz in enumerate(self.trip_of_idx):
            eqn     = i
            p_var   = p_vidx(i)
            Eqn.append( eqn )
            Var.append( p_var )
            Coeff.append( -1. )

            (x,y,z) = xyz
            for u in self.X:
                if (u,y,z) in self.idx_of_trip.keys():
                    q_var = q_vidx(self.idx_of_trip[ (u,y,z) ])
                    Eqn.append( eqn )
                    Var.append( q_var )
                    Coeff.append( +1. )
                #^ if
            #^ loop *yz
        #^ for xyz

        # running number
        eqn = -1 + len(self.trip_of_idx)

        # The xy marginals q_{xy*} = b^y_{xy}
        for x in self.X:
            for y in self.Y:
                if (x,y) in self.b_xy.keys():
                    eqn += 1
                    for z in self.Z:
                        if (x,y,z) in self.idx_of_trip.keys():
                            q_var = q_vidx(self.idx_of_trip[ (x,y,z) ])
                            Eqn.append( eqn )
                            Var.append( q_var )
                            Coeff.append( 1. )
                        #^ if
                        self.b[eqn] = self.b_xy[ (x,y) ]
                    #^ for z
                #^ if xy exists
            #^ for y
        #^ for x
        # The xz marginals q_{x*z} = b^z_{xz}
        for x in self.X:
            for z in self.Z:
                if (x,z) in self.b_xz.keys():
                    eqn += 1
                    for y in self.Y:
                        if (x,y,z) in self.idx_of_trip.keys():
                            q_var = q_vidx(self.idx_of_trip[ (x,y,z) ])
                            Eqn.append( eqn )
                            Var.append( q_var )
                            Coeff.append( 1. )
                        #^ if
                        self.b[eqn] = self.b_xz[ (x,z) ]
                    #^ for z
                #^ if xz exists
            #^ for y
        #^ for x

        self.A = sparse.csc_matrix( (Coeff, (Eqn,Var)), shape=(n_cons,n_vars), dtype=np.double)

        # Generalized ieqs: gen.nneg of the variable triples (r_i,q_i,p_i), i=0,dots,n-1:
        Ieq   = []
        Var   = []
        Coeff = []
        for i,xyz in enumerate(self.trip_of_idx):
            r_var = r_vidx(i)
            q_var = q_vidx(i)
            p_var = p_vidx(i)

            Ieq.append( len(Ieq) )
            Var.append( r_var )
            Coeff.append( -1. )

            Ieq.append( len(Ieq) )
            Var.append( p_var )
            Coeff.append( -1. )

            Ieq.append( len(Ieq) )
            Var.append( q_var )
            Coeff.append( -1. )
        #^ for xyz

        self.G         = sparse.csc_matrix( (Coeff, (Ieq,Var)), shape=(n_vars,n_vars), dtype=np.double)
        self.h         = np.zeros( (n_vars,),dtype=np.double )
        self.dims['e'] = n

        # Objective function:
        self.c = np.zeros( (n_vars,),dtype=np.double )
        for i,xyz in enumerate(self.trip_of_idx):
            self.c[ r_vidx(i) ] = -1.
        #^ for xyz
    #^ create_model()

    def solve(self):
        # (c) Abdullah Makkeh, Dirk Oliver Theis
        # Permission to use and modify under Apache License version 2.0
        self.marg_yz = None # for cond[]mutinf computation below

        kwargs = dict()
        if self.feastol != None:
            kwargs["feastol"] = self.feastol
        if self.abstol != None:
            kwargs["abstol"] = self.abstol
        if self.reltol != None:
            kwargs["reltol"] = self.reltol
        if self.feastol_inacc != None:
            kwargs["feastol_inacc"] = self.feastol_inacc
        if self.abstol_innac != None:
            kwargs["abstol_innac"] = self.abstol_innac
        if self.reltol_inacc != None:
            kwargs["reltol_inacc"] = self.reltol_inacc
        if self.max_iters != None:
            kwargs["max_iters"] = self.max_iters
        if self.verbose != None:
            kwargs["verbose"] = self.verbose

        solution = solve(self.c, self.G,self.h, self.dims,  self.A,self.b, **kwargs)

        if 'x' in solution.keys():
            self.sol_rpq    = solution['x']
            self.sol_slack  = solution['s']
            self.sol_lambda = solution['y']
            self.sol_mu     = solution['z']
            self.sol_info   = solution['info']
            return "success"
        else: # "x" not in dict solution
            return "What the fuck?!??"
        #^ if/esle
    #^ solve()

    def provide_marginals(self):
        if self.marg_yz == None:
            self.marg_yz = dict()
            self.marg_y  = defaultdict(lambda: 0.)
            self.marg_z  = defaultdict(lambda: 0.)
            for y in self.Y:
                for z in self.Z:
                    zysum = 0.
                    for x in self.X:
                        if (x,y,z) in self.idx_of_trip.keys():
                            q = self.sol_rpq[ q_vidx(self.idx_of_trip[ (x,y,z) ]) ]
                            if q>0:
                                zysum += q
                                self.marg_y[ y ] += q
                                self.marg_z[ z ] += q
                            #^ if q>0
                        #^if
                    #^ for x
                    if zysum > 0. :    self.marg_yz[ (y,z) ] = zysum
                #^ for z
            #^ for y
        #^ if ∄ marg_yz
    #^ provide_marginals()

    def condYmutinf(self):
        self.provide_marginals()

        mysum = 0.
        for x in self.X:
            for z in self.Z:
                if not (x,z) in self.b_xz.keys(): continue
                for y in self.Y:
                    if (x,y,z) in self.idx_of_trip.keys():
                        i = q_vidx(self.idx_of_trip[ (x,y,z) ])
                        q = self.sol_rpq[i]
                        if q > 0:  mysum += q*log( q * self.marg_y[y] / ( self.b_xy[ (x,y) ] * self.marg_yz[ (y,z) ] ) )
                    #^ if
                #^ for i
            #^ for z
        #^ for x
        return mysum
    #^ condYmutinf()

    def condZmutinf(self):
        self.provide_marginals()

        mysum = 0.
        for x in self.X:
            for y in self.Y:
                if not (x,y) in self.b_xy.keys(): continue
                for z in self.Z:
                    if (x,y,z) in self.idx_of_trip.keys():
                        i = q_vidx(self.idx_of_trip[ (x,y,z) ])
                        q = self.sol_rpq[i]
                        if q > 0:  mysum += q*log( q * self.marg_z[z] / ( self.b_xz[ (x,z) ] * self.marg_yz[ (y,z) ] ) )
                    #^ if
                #^ for z
            #^ for y
        #^ for x
        return mysum
    #^ condZmutinf()

    def entropy_X(self,pdf):
        mysum = 0.
        for x in self.X:
            psum = 0.
            for y in self.Y:
                if not (x,y) in self.b_xy:  continue
                for z in self.Z:
                    if (x,y,z) in pdf.keys():
                        psum += pdf[(x,y,z)]
                    #^ if
                #^ for z
            #^ for y
            mysum -= psum * log(psum)
        #^ for x
        return mysum
    #^ entropy_X()

    def condentropy(self):
        # compute cond entropy of the distribution in self.sol_rpq
        mysum = 0.
        for y in self.Y:
            for z in self.Z:
                marg_x = 0.
                q_list = [ q_vidx(self.idx_of_trip[ (x,y,z) ]) for x in self.X if (x,y,z) in self.idx_of_trip.keys()]
                for i in q_list:
                    marg_x += max(0,self.sol_rpq[i])
                for i in q_list:
                    q = self.sol_rpq[i]
                    if q > 0:  mysum -= q*log(q/marg_x)
                #^ for i
            #^ for z
        #^ for y
        return mysum
    #^ condentropy()

    def condentropy__orig(self,pdf):
        mysum = 0.
        for y in self.Y:
            for z in self.Z:
                x_list = [ x  for x in self.X if (x,y,z) in pdf.keys()]
                marg = 0.
                for x in x_list: marg += pdf[(x,y,z)]
                for x in x_list:
                    p = pdf[(x,y,z)]
                    mysum -= p*log(p/marg)
                #^ for xyz
            #^ for z
        #^ for y
        return mysum
    #^ condentropy__orig()

    def dual_value(self):
        return np.dot(self.sol_lambda, self.b)
    #^ dual_value()
    
    def check_feasibility(self): # returns pair (p,d) of primal/dual infeasibility (maxima)
        # Primal infeasiblility
        # ---------------------
        max_q_negativity = 0.
        for i in range(len(self.trip_of_idx)):
            max_q_negativity = max(max_q_negativity, -self.sol_rpq[q_vidx(i)])
        #^ for
        max_violation_of_eqn = 0.
        # xy* - marginals:
        for xy in b_xy.keys():
            mysum = b_xy[xy]
            for z in self.Z:
                x,y = xy
                if (x,y,z) in self.idx_of_trip.keys():
                    i = self.idx_of_trip[(x,y,z)]
                    q = max(0., self.sol_rpq[q_vidx(i)])
                    mysum -= q
                #^ if
            #^ for z
            max_violation_of_eqn = max( max_violation_of_eqn, abs(mysum) )
        #^ fox xy
        # x*z - marginals:
        for xz in b_xz.keys():
            mysum = b_xz[xz]
            for y in self.Y:
                x,z = xz
                if (x,y,z) in self.idx_of_trip.keys():
                    i = self.idx_of_trip[(x,y,z)]
                    q = max(0., self.sol_rpq[q_vidx(i)])
                    mysum -= q
                #^ if
            #^ for z
            max_violation_of_eqn = max( max_violation_of_eqn, abs(mysum) )
        #^ fox xz

        primal_infeasibility = max(max_violation_of_eqn,max_q_negativity)
        
        # Dual infeasiblility
        # -------------------
        idx_of_xy = dict()
        i = 0
        for (x,y) in self.b_xy.keys():
            idx_of_xy[(x,y)] = i
            i += 1
        #^ for

        idx_of_xz = dict()
        i = 0
        for (x,z) in self.b_xz.keys():
            idx_of_xz[(x,z)] = i
            i += 1
        #^ for

        dual_infeasability = 0.
        for i,xyz in enumerate(self.trip_of_idx):
            x,y,z = xyz
            xy_idx = len(self.trip_of_idx) + idx_of_xy[(x,y)]
            xz_idx = len(self.trip_of_idx) + len(self.b_xy) + idx_of_xz[(x,z)]
            dual_infeasability = max( dual_infeasability,  -ln( self.sol_lambda[xy_idx] + self.sol_lambda[xz_idx] + LA.norm(self.sol_lambda,1) ) - 1 + self.sol_lambda[i] )
        #^ for

        return primal_infeasability, dual_infeasability
    #^ check_feasibility()

#^ class Solve_w_ECOS


def marginal_xy(p):
    marg = dict()
    for xyz,r in p.items():
        x,y,z = xyz
        if (x,y) in marg.keys():    marg[(x,y)] += r
        else:                       marg[(x,y)] =  r
    return marg

def marginal_xz(p):
    marg = dict()
    for xyz,r in p.items():
        x,y,z = xyz
        if (x,z) in marg.keys():   marg[(x,z)] += r
        else:                      marg[(x,z)] =  r
    return marg

def pid(pdf_dirty, output=0, keep_solver_object=False):
    # (c) Abdullah Makkeh, Dirk Oliver Theis
    # Permission to use and modify under Apache License version 2.0
    assert type(pdf_dirty) is dict, "broja_2pid.pid(pdf): pdf must be a dictionary"
    if __debug__:
        for k,v in pdf_dirty.items():
            assert type(k) is tuple or type(k) is list,           "broja_2pid.pid(pdf): pdf's keys must be tuples or lists"
            assert len(k)==3,                                     "broja_2pid.pid(pdf): pdf's keys must be tuples/lists of length 3"
            assert type(v) is float or ( type(v)==int and v==0 ), "broja_2pid.pid(pdf): pdf's values must be floats"
            assert v > -.1,                                       "broja_2pid.pid(pdf): pdf's values must not be negative"
        #^ for
    #^ if
    assert type(output) is int, "broja_2pid.pid(pdf,output): output must be an integer"

    pdf = { k:v  for k,v in pdf_dirty.items() if v > 1.e-300 }

    by_xy = marginal_xy(pdf)
    bz_xz = marginal_xz(pdf)

    if output > 0:  print("BROJA_2PID: Preparing Cone Program data",end="...")
    solver = Solve_w_ECOS(by_xy, bz_xz)
    solver.create_model()
    if output > 0: print("done.")

    if output == 1: print("BROJA_2PID: Starting solver",end="...")
    if output > 1: print("BROJA_2PID: Starting solver.")
    if output > 1: solver.verbose = True
    retval = solver.solve()
    if retval != "success":
        print("\nCone Programming solver failed to find (near) optimal solution.\nPlease report the input probability density function to dotheis@ut.ee\n")
        if type(keep_solver_object) is bool  and  keep_solver_object:
            return solver
        else:
            raise BROJA_2PID_Exception("BROJA_2PID_Exception: Cone Programming solver failed to find (near) optimal solution. Please report the input probability density function to dotheis@ut.ee")
        #^ if (keep solver)
    #^ if (solve failure)

    if output > 0:  print("\nBROJA_2PID: done.")

    if output > 1:  print(solver.sol_info)

    entropy_X     = solver.entropy_X(pdf)
    condent       = solver.condentropy()
    condent__orig = solver.condentropy__orig(pdf)
    condYmutinf   = solver.condYmutinf()
    condZmutinf   = solver.condZmutinf()
    dual_val      = solver.dual_value()
    bits = 1/log(2)

    return_data = dict()
    return_data["SI"]  = ( entropy_X - condent - condZmutinf - condYmutinf ) * bits
    return_data["UIY"] = ( condZmutinf                                     ) * bits
    return_data["UIZ"] = ( condYmutinf                                     ) * bits
    return_data["CI"]  = ( condent - condent__orig                         ) * bits

    primal_infeas,dual_infeas = solver.check_feasibility()
    return_data["Num_err"] = (primal_infeas, dual_infeas, abs(condent*ln(2) - dual_val))
    return_data["Solver"] = "ECOS http://www.embotech.com/ECOS"

    if type(keep_solver_object) is bool  and  keep_solver_object:
        return_data["Solver Object"] = solver
    #^ if (keep solver)

    return return_data
#^ pid()

#EOF
