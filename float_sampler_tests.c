#include <stdint.h>
#include <stdio.h>
#include <assert.h>
#include <math.h>

#include "float_sampler.h"

union bit2float {
  uint32_t b;
  float f;
};

void test_psubnormal() {
  int i;
  for(i = 0; i < 8388607; i++) {
    union bit2float v;
    v.b = psubnormal(i);
    assert(fpclassify(v.f) == FP_SUBNORMAL);
    assert(signbit(v.f) == 0);
  }
}

void test_nsubnormal() {
  int i;
  for(i = 0; i < 8388607; i++) {
    union bit2float v;
    v.b = nsubnormal(i);
    assert(fpclassify(v.f) == FP_SUBNORMAL);
    assert(signbit(v.f) != 0);
  }
}

void test_ninf() {
  int i;
  for(i = 0; i < 1; i++) {
    union bit2float v;
    v.b = ninf(i);
    assert(fpclassify(v.f) == FP_INFINITE);
    assert(signbit(v.f) != 0);
  }
}

void test_pinf() {
  int i;
  for(i = 0; i < 1; i++) {
    union bit2float v;
    v.b = pinf(i);
    assert(fpclassify(v.f) == FP_INFINITE);
    assert(signbit(v.f) == 0);
  }
}

void test_nzero() {
  int i;
  for(i = 0; i < 1; i++) {
    union bit2float v;
    v.b = nzero(i);
    assert(fpclassify(v.f) == FP_ZERO);
    assert(signbit(v.f) != 0);
  }
}

void test_pzero() {
  int i;
  for(i = 0; i < 1; i++) {
    union bit2float v;
    v.b = pzero(i);
    assert(fpclassify(v.f) == FP_ZERO);
    assert(signbit(v.f) == 0);
  }
}

void test_nnan() {
  int i;
  for(i = 0; i < 1; i++) {
    union bit2float v;
    v.b = nqnan(i);
    assert(fpclassify(v.f) == FP_NAN);
    assert(signbit(v.f) != 0);
  }
}

void test_pnan() {
  int i;
  for(i = 0; i < 1; i++) {
    union bit2float v;
    v.b = pqnan(i);
    assert(fpclassify(v.f) == FP_NAN);
    assert(signbit(v.f) == 0);
  }
}

void test_pnormal() {
  int i;
  for(i = 0; i < 8388607; i++) {
    union bit2float v;
    v.b = pnormal(i);
    assert(fpclassify(v.f) == FP_NORMAL);
    assert(signbit(v.f) == 0);
  }
}

void test_nnormal() {
  int i;
  for(i = 0; i < 8388607; i++) {
    union bit2float v;
    v.b = nnormal(i);
    assert(fpclassify(v.f) == FP_NORMAL);
    assert(signbit(v.f) != 0);
  }
}

int main(void) {
  test_psubnormal();
  test_nsubnormal();
  test_ninf();
  test_pinf();
  test_nzero();
  test_pzero();
  test_nnan();
  test_pnan();
  test_pnormal();
  test_nnormal();
}
