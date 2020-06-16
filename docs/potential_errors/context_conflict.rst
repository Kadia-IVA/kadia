.. _context_conflict:

Skills names and contexts conflict
=======================================
Problem
-----------
If there are skills with similar contexts, the system may be confused.

Solution
---------
Run only trusted skills (i. e. we need to implement skill installation system)
Sort them by some score. The score must be calculated by using global run counts and this user run counts.
