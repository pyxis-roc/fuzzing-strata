#include <stdint.h>
#include <stdio.h>
#include <assert.h>
#include <math.h>
#include <stdlib.h>

#include "float_sampler.h"

union bit2float {
  uint32_t b;
  float f;
};

static uint32_t uniform_sample(const uint32_t range) {
  // http://www.cs.yale.edu/homes/aspnes/pinewiki/C(2f)Randomization.html
  // essentially rejection sampling
  uint32_t n;

  if(range == 1) return 0;

  assert(range <= RAND_MAX);

  uint32_t limit = RAND_MAX - (RAND_MAX % range);

  n = random();

  while(n >= limit) n = random();

  return n % range;
}

float sample_float() {
  uint32_t br;

  br = uniform_sample(10);

  union bit2float v;

  switch(br) {
  case 0:
    v.b = pzero(uniform_sample(pzero_range));
    break;
  case 1:
    v.b = nzero(uniform_sample(nzero_range));
    break;
  case 2:
    v.b = nsubnormal(uniform_sample(nsubnormal_range));
    break;
  case 3:
    v.b = psubnormal(uniform_sample(psubnormal_range));
    break;
  case 4:
    v.b = pnormal(uniform_sample(pnormal_range));
    break;
  case 5:
    v.b = nnormal(uniform_sample(nnormal_range));
    break;
  case 6:
    v.b = pqnan(uniform_sample(pqnan_range));
    break;
  case 7:
    v.b = nqnan(uniform_sample(nqnan_range));
    break;
  case 8:
    v.b = ninf(uniform_sample(ninf_range));
    break;
  case 9:
    v.b = pinf(uniform_sample(pinf_range));
    break;
  }

  return v.f;
}

int main(int argc, char *argv[]) {
  fprintf(stderr, "RAND_MAX is %u\n", RAND_MAX);

  srand(0);

  int n = 1;
  if(argc == 2) {
    n = atoi(argv[1]);
  }

  fprintf(stderr, "Generating %d numbers\n", n);

  while(n-- > 0) {
    printf("%0.13a\n", sample());
  }
}
