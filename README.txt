# BROJA_2PID
A bivariate measure of unique information via gain in decision theoretic settings for discrete variables.

# What it does?
Computes a partial information decomposition (PID) for *only two* sources and one target via the UI meausre. The measure was introduced by N. Bertschinger, J. Rauh, E. Olbrich, J. Jost, N. Ay  from the intuition that unique information emerges if there is an advantage of the agent in a decision theortic setting. The quantification of such intuition requires solving an optimization problem. This estimator is developed by A. Makkeh, D.O. Theis, and R. Vicente by reformulating optimization problem as a cone programme. 


For more details, check the following papers:
* N. Bertschinger, J. Rauh, E. Olbrich, J. Jost, N. Ay *Quantifying Unique Information.* Entropy 2014 
* A. Makkeh, D.O. Theis, R. Vicente, *Bivariate Partial Information Decomposition: The Optimization Perspective.* Entropy 2017
* A. Makkeh, D.O. Theis, R. Vicente, *BROJA-2PID: A Robust Estimator for Bivariate Partial Information Decomposition.* Entropy 2018


# User Guided Exmaple
The example file testing/test_and_gate.py has detailed explanation on how to run the code, in particular the main function `BROJA_2PID.pid()` to compute the partial information decomposition.
