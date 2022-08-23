#!/usr/bin/env python3

from pattern import BitPattern as BP

MIN = BP('1'*32)
ZERO = BP('0'*32)
ONE = BP('0'*31 + '1')
MAX = BP('0' + '1'*31)

NEG = BP('1' + 'X'*31, [MIN])
POS = BP('0' + 'X'*31, [ZERO, ONE, MAX])


decoders = [('int32_min', MIN),
            ('int32_zero', ZERO),
            ('int32_one', ONE),
            ('int32_neg', NEG),
            ('int32_pos', POS),
            ('int32_max', MAX)]

count = 0
for n, d in decoders:
    print(f"static uint32_t {n}_range = {d.count()};")
    print(d.decoder_c_code(n, qual="static "))
    count += d.count()

gen_count = count
tot_count = 2**32
assert gen_count == tot_count, f"{gen_count} == {tot_count}"
