all: float_sampler_tests

float_sampler.h:
	python ./float_sampler.py > $@

float_sampler_tests: float_sampler_tests.c float_sampler.h
	gcc -g $< -o $@
