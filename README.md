# Stratified Sampling

The code generates a sampler suitable for stratified sampling of bit
patterns. For example, given a random integer, you can choose a strata
and then a sample from that strata.

Although the code includes a sampler intending to sample on the go,
the current sampler does not sample in proportion to the size of the
strata.

## Float sampler

The files `float_sampler.py` generates a header file containing the
code to sample from individual strata in the IEEE 754 FP32 format. The
file `float_sampler.c` contains a sampler that picks a strata and then
samples from that strata. The file `float_sampler_tests.c` contains
exhaustive tests to verify the samplers.

## How it works

The primary technique used is to generate a random integer and then
map the integer to the bit pattern indexed by that integer. Since the
bit patterns being generated may not be continuous, some way of
mapping a continous range of integers to the discontinuous bit
patterns is needed.

Initially, I thought Cover's [enumerative source encoding
algorithm](https://isl.stanford.edu/~cover/papers/transIT/0073cove.pdf)
would work (and the effort is in `cover.py`), but the algorithm was
too general for my needs.

Based on similar ideas, I wrote `pattern.py` which simply identifies
all the discontinuities and accounts for them when generating the
mapping.