#!/usr/bin/env python3

from pattern import BitPattern as BP, generate_sampler
import argparse

def generate_int_sampler(nbits):
    MIN = BP('1'*nbits)
    ZERO = BP('0'*nbits)
    ONE = BP('0'*(nbits-1) + '1')
    MAX = BP('0' + '1'*(nbits - 1))

    NEG = BP('1' + 'X'*(nbits - 1), [MIN])
    POS = BP('0' + 'X'*(nbits - 1), [ZERO, ONE, MAX])

    decoders = [(f'int{nbits}_min', MIN),
                (f'int{nbits}_zero', ZERO),
                (f'int{nbits}_one', ONE),
                (f'int{nbits}_neg', NEG),
                (f'int{nbits}_pos', POS),
                (f'int{nbits}_max', MAX)]

    print("#pragma once")
    print("#include <stdint.h>")
    print("#include <stdio.h>")
    print("#include <assert.h>")
    print("#include <math.h>")
    print("#include <stdlib.h>")
    print('#include "unisampler.h"')

    count = 0

    range_ty = 'uint32_t' if nbits <= 32 else 'uint64_t'
    range_top = 2**32 if nbits <= 32 else 2**64
    sampler = 'uniform_sample' if nbits <= 32 else 'uniform_sample_64'

    for n, d in decoders:
        dc = d.count()
        assert dc < range_top, f"Out of range for {range_ty}: {dc}"
        # may not require suffix because literals are sized
        print(f"static {range_ty} {n}_range = {dc};")
        print(d.decoder_c_code(n, qual="static "))
        count += dc

    gen_count = count
    tot_count = 2**nbits
    assert gen_count == tot_count, f"{gen_count} == {tot_count}"

    print(generate_sampler(f"sample_int{nbits}_t", [d[0] for d in decoders],
                           value_ty = f"int{nbits}_t",
                           sampler = sampler))

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Generate signed integer sampler")
    p.add_argument("nbits", help="Number of bits", type=int, choices=[8, 16, 32, 64])

    args = p.parse_args()

    generate_int_sampler(args.nbits)
