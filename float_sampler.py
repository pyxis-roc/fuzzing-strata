#!/usr/bin/env python3

from pattern import BitPattern as BP, generate_sampler
import argparse

class F32:
    EXP = 8
    SIGNIFICAND = 23
    TOTAL = 32
    tyname = 'float'

class F64:
    EXP = 11
    SIGNIFICAND = 52
    TOTAL = 64
    tyname = 'double'

def gen_decoders(decoders, NAN, ty):
    count = 0
    nbits = ty.TOTAL

    # this picks the same type for all ranges
    range_ty = 'uint32_t' if nbits <= 32 else 'uint64_t'
    range_top = 2**32 if nbits <= 32 else 2**64
    sampler = 'uniform_sample' if nbits <= 32 else 'uniform_sample_64'

    for n, d in decoders:
        dc = d.count()
        assert dc < range_top, f"Out of range for {range_ty}: {dc}"
        print(f"static {range_ty} {n}_range = {dc};")
        print(d.decoder_c_code(n, qual="static "))
        count += dc

    gen_count = count - 2 + NAN.count()
    tot_count = 2**nbits
    assert gen_count == tot_count, f"{gen_count} == {tot_count}"

    print(generate_sampler(f"sample_{ty.tyname}", [d[0] for d in decoders],
                           value_ty = ty.tyname,
                           sampler = sampler))

def gen_gen(ty):
    def gen_pattern(sign_bit, exp_bit, significand_bit, ty):
        assert len(sign_bit) == 1
        assert len(exp_bit) == 1
        assert len(sign_bit) == 1

        return sign_bit + exp_bit * ty.EXP + significand_bit * ty.SIGNIFICAND

    GP = lambda x, y,z : gen_pattern(x, y, z, ty)
    nbits = ty.TOTAL

    PZERO = BP(GP('0', '0', '0'))
    NZERO = BP(GP('1', '0', '0'))

    PSUBNORMALS = BP(GP('0', '0', 'X'), [PZERO])
    NSUBNORMALS = BP(GP('1', '0', 'X'), [NZERO])

    PINF = BP(GP('0', '1', '0'))
    NINF = BP(GP('1', '1', '0'))

    NAN = BP(GP('X', '1', 'X'), [PINF, NINF])

    PNAN = BP(GP('0', '1', 'X'), [PINF])
    NNAN = BP(GP('1', '1', 'X'), [NINF])

    PQNAN = BP('0' + '1'*ty.EXP + '1' + '0'*(ty.SIGNIFICAND-1))
    NQNAN = BP('1' + '1'*ty.EXP + '1' + '0'*(ty.SIGNIFICAND-1))

    PNORMALS = BP(GP('0', 'X', 'X'), [PZERO, PSUBNORMALS, NAN, PINF])
    NNORMALS = BP(GP('1', 'X', 'X'), [NZERO, NSUBNORMALS, NAN, NINF])

    decoders = [('pzero', PZERO),
                ('nzero', NZERO),
                ('psubnormal', PSUBNORMALS),
                ('nsubnormal', NSUBNORMALS),
                ('pinf', PINF),
                ('ninf', NINF),
                ('pqnan', PQNAN),
                ('nqnan', NQNAN),
                ('pnormal', PNORMALS),
                ('nnormal', NNORMALS)]

    gen_decoders(decoders, NAN, ty)

def gen_f32():
    ty = F32()
    gen_gen(ty)

def gen_f64():
    ty = F64()
    gen_gen(ty)

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Generate float samplers")
    p.add_argument("ty", help="Float type", choices=["f32", "f64"])

    args = p.parse_args()

    if args.ty == "f32":
        gen_f32()
    elif args.ty == "f64":
        gen_f64()
    else:
        raise NotImplementedError(f"Float type {args.ty} not supported yet")

