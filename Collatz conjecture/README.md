# Collatz-conjecture

Code to calculate the tree of the collatz conjecture in python with numba.

## Explanation/thought process for myself
one starting number:
- if the number is even divide by 2 (n -> n/2)
- if the number is odd multiply with 3 und add 1 (n -> 3n+1) repeat

if n reaches 1 we have the infinite loop 4 -> 2 -> 1 -> 4 ...

every odd number becomes even with 3n+1 and can be directly divided by 2

if n is on the tree of all the chains of numbers from before we can stop calculating and just follow the previous path