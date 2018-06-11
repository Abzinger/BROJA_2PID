# BROJA_2PID: Bertschinger-Rauh-Olbrich-Jost-Ay (BROJA) bivariate Partial Information Decomposition

This Python module implements the Bertschinger-Rauh-Olbrich-Jost-Ay bivariate Partial Information Decomposition (N. Bertschinger, J. Rauh, E. Olbrich, J. Jost, N. Ay, *Quantifying Unique Information.* Entropy 2014, 16, 2161-2183; [doi:10.3390/e16042161](http://dx.doi.org/10.3390/e16042161).).

It uses the Exponential Cone Programming approach described in
* A. Makkeh, D.O. Theis, R. Vicente, *Bivariate Partial Information Decomposition: The Optimization Perspective* (Entropy 19, 530 (2017)),
and
* Abdullah Makkeh's PhD thesis (forthcoming (2018))

The details of the implementation, user interface, and example code are described in
* A. Makkeh, D.O. Theis, R. Vicente, *BROJA-2PID: A cone programming based Partial Information Decomposition estimator*
(currently in preparation).

#### If you use this software...
...we ask that you give proper reference.
If you use it with only small modifications (note the Apache 2.0 license), use 
```
@Article{makkeh2018broja,
  author =       {Makkeh, Abdullah and Theis, Dirk Oliver and Vicente, Raul},
  title =        {BROJA-2PID: A robust estimator for Bertschinger et al.'s bivariate partial information decomposition},
  journal =      {Entropy},
  volume =    {20},
  number =    {4},
  pages =     {271},
  year =         2018,
  publisher={Multidisciplinary Digital Publishing Institute}
}
```
If you make significant modifications but stick to the approach based on the Exponential Cone Programming model, use
```
@Article{makkeh-theis-vicente:pidOpt:2017,
  author =       {Makkeh, Abdullah and Theis, Dirk Oliver and Vicente, Raul},
  title =        {Bivariate Partial Information Decomposition: The Optimization Perspective},
  journal =      {Entropy},
  year =         2017,
  volume =    {19},
  number =    {10},
  pages =     {530},
  note    = {\url{http://dx.doi.org/10.3390/e19100530}}
}
```

#### Files
The following files contain tests:

* `test_from_file_computeUI_dit.py`: testcase for *random* distributions read from files in `randompdfs\` folder to compare the BROJA_2PID algorithms with iterative divergence minimization algorithm from the Github repository [computeUI](https://github.com/jarauh/computeUI)  and  with the Frank-Wolfe implementation in the [dit](https://github.com/dit/dit).

* `test_large_random_computeUI_dit.py`: testcase for *random* distributions generated simultaneously to compare the BROJA_2PID algorithms with iterative divergence minimization algorithm from the Github repository [computeUI](https://github.com/jarauh/computeUI)  and  with the Frank-Wolfe implementation in the [dit](https://github.com/dit/dit).

* `test_large_copy_computeUI_dit.py`: testcase for *Copy gate* to compare the BROJA_2PID algorithms with iterative divergence minimization algorithm from the Github repository [computeUI](https://github.com/jarauh/computeUI)  and  with the Frank-Wolfe implementation in the [dit](https://github.com/dit/dit).

* `test_gates_computeUI_dit.py`: testcase for some *logical gate* to compare the BROJA_2PID algorithms with iterative divergence minimization algorithm from the Github repository [computeUI](https://github.com/jarauh/computeUI)  and  with the Frank-Wolfe implementation in the [dit](https://github.com/dit/dit).
