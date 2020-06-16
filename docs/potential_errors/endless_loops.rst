.. _endless_loops:

Endless loops of skills
==========================

Problem
--------------------------
Obvious.

Solution A
--------------------------
Skills return self paramaters hash before inferencing.
It’s restricted to run any skill with equal hashes twice in the loop.

Solution B
--------------------------
It`s restricted to run any skill twice in the loop.

Solution C
-------------------------
Limit stack size to some number.
