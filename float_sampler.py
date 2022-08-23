#!/usr/bin/env python3

from pattern import BitPattern as BP


PZERO = BP('0  0000 0000  000 0000 0000 0000 0000 0000')
NZERO = BP('1  0000 0000  000 0000 0000 0000 0000 0000')

PSUBNORMALS = BP('0  0000 0000  XXX XXXX XXXX XXXX XXXX XXXX', [PZERO])
NSUBNORMALS = BP('1  0000 0000  XXX XXXX XXXX XXXX XXXX XXXX', [NZERO])

PINF = BP('0 1111 1111 000 0000 0000 0000 0000 0000')
NINF = BP('1 1111 1111 000 0000 0000 0000 0000 0000')

NAN = BP('X 1111 1111 XXX XXXX XXXX XXXX XXXX XXXX', [PINF, NINF])

PNAN = BP('0 1111 1111 XXX XXXX XXXX XXXX XXXX XXXX', [PINF])
NNAN = BP('1 1111 1111 XXX XXXX XXXX XXXX XXXX XXXX', [NINF])

PQNAN = BP('0 1111 1111 100 0000 0000 0000 0000 0000')
NQNAN = BP('1 1111 1111 100 0000 0000 0000 0000 0000')

PNORMALS = BP('0 XXXX XXXX XXX XXXX XXXX XXXX XXXX XXXX', [PZERO, PSUBNORMALS, NAN, PINF])
NNORMALS = BP('1 XXXX XXXX XXX XXXX XXXX XXXX XXXX XXXX', [NZERO, NSUBNORMALS, NAN, NINF])


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

count = 0
for n, d in decoders:
    print(f"static uint32_t {n}_range = {d.count()};")
    print(d.decoder_c_code(n, qual="static "))
    count += d.count()

gen_count = count - 2 + NAN.count()
tot_count = 2**32
assert gen_count == tot_count, f"{gen_count} == {tot_count}"
