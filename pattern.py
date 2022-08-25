#!/usr/bin/env python3
#
# pattern.py
# Generate a decoder for bit-patterns
#
# Initially based on Cover's algorithm, but simplified to just
# decoding interval ranges.
#
# Author: Sreepathi Pai
#
# Copyright (C) 2022 University of Rochester


def lex_gen(pattern, X='0'):
    out = []
    for c in pattern:
        if c == 'X':
            out.append(X)
        else:
            out.append(c)

    return ''.join(out)

class BitPattern:
    def __init__(self, pattern, exclusions = None):
        self.user_pattern = pattern
        self.pattern = pattern.replace(' ', '')
        self.exclusions = [] if exclusions is None else exclusions
        self._xtable = None
        self._ranges = None
        self._xcl_ranges = None

    def __str__(self):
        return f"BitPattern(pattern='{self.user_pattern}')"

    __repr__ = __str__

    @property
    def xtable(self):
        def pattern_xtable(pattern):
            out = [0] * (len(pattern)+1)

            # compute an exclusive sum of Xs below the current position
            s = 0
            for i, c in enumerate(reversed(pattern)):
                out[i] = s
                s += 1 if c == 'X' else 0

            out[len(pattern)] = s

            return out

        if self._xtable is None:
            self._xtable = pattern_xtable(self.pattern)

        return self._xtable

    def direct_range(self):
        # with no exclusions accounted for
        l = lex_gen(self.pattern, '0')
        h = lex_gen(self.pattern, '1')

        return (int(h, base=2), int(l, base=2))

    def direct_count(self):
        print(self.xtable)
        return 2 ** self.xtable[len(self.pattern)]

    def prefix_count(self, prefix):
        assert len(prefix) < len(self.pattern)
        assert len(prefix) > 0

        xs_after_prefix = self.xtable[len(self.pattern) - len(prefix)]
        self_count = 2 ** xs_after_prefix

        # TODO: assumes exclusions do not overlap
        excl_count = sum([xc.prefix_count(prefix) for xc in self.exclusions])

        return self_count - excl_count

    def overlap(self, op):
        assert len(op.pattern) == len(self.pattern)

        for c1, c2 in zip(self.op.pattern, self.pattern):
            if not (c1 == c2 or c1 == 'X' or c2 == 'X'):
                return False

        return True

    def split_disjoint(self, pattern = None):
        if pattern is None:
            pattern = self.pattern

        last_c = None
        out = []
        for i, c in enumerate(pattern):
            if (c == '0' or c == '1') and last_c == 'X': # only X(0|1) introduces discontinuities
                # X0X -> 000 001 100 101
                # X1X -> 010 011 110 111
                prefix = pattern[:i-1]
                p = self.split_disjoint(pattern[i:])
                out.extend([prefix + "0" + pp for pp in p])
                out.extend([prefix + "1" + pp for pp in p])
                break
            last_c = c
        else:
            out.append(pattern)

        return out

    def ranges(self):
        if self._ranges is None:
            xp = self.split_disjoint()
            self._ranges = []

            for p in xp:
                pp = BitPattern(p)
                self._ranges.append((int(pp.least, base=2),
                                     int(pp.highest, base=2)))

        return self._ranges

    def build_excluded_ranges(self):
        def remove_range(orig, remove):
            # orig is a disjoint range

            out = []
            for org in orig:
                if org[1] < remove[0] or org[0] > remove[1]:
                    # no overlap
                    out.append(org)
                else:
                    if org[0] < remove[0]:
                        out.append((org[0], remove[0] - 1))

                    if org[1] > remove[1]:
                        out.append((remove[1] + 1, org[1]))

            return out

        if self._xcl_ranges is None:
            # get our ranges
            sr = self.ranges()

            for xc in self.exclusions:
                xcr = xc.build_excluded_ranges()

                for xr in xcr:
                    #print(sr, xr)
                    sr = remove_range(sr, xr)

            self._xcl_ranges = sr

        return self._xcl_ranges

    def count(self):
        x = self.build_excluded_ranges()
        return sum([(xc[1] - xc[0] + 1) for xc in x])

    def build_decoder(self, excluded_range):
        count = 0
        out = []
        for xc in excluded_range:
            sz = (xc[1] - xc[0] + 1)
            out.append((count, count + sz, xc[0]))
            count += sz

        return count, out

    def decoder_c_code(self, name, qual = ""):
        total, branches = self.build_decoder(self.build_excluded_ranges())
        index = len(self.pattern)
        index_ty = f"uint{index}_t" # assumes index will be a power of 2

        out = []
        out.append(f"{qual}{index_ty} {name}({index_ty} index) {{")
        out.append(f"    index = index % {total};")

        suffix = "u"

        brkey = "if"
        for b in branches:
            out.append(f"    {brkey} (index < {b[1]}) return index + {b[2]}{suffix};")
            brkey = "else if"

        out.append("}")

        return "\n".join(out)

    @property
    def least(self):
        #TODO: take exclusions into account
        return lex_gen(self.pattern, '0')

    @property
    def highest(self):
        #TODO: take exclusions into account
        return lex_gen(self.pattern, '1')

def generate_sampler(name, decoder_names, value_ty = 'int32_t', bit_ty = 'uint32_t', static='static '):
    out = []

    out.append(f"{static}{value_ty} {name}() {{")
    out.append("  union bit2value {")
    out.append(f"    {bit_ty} b;")
    out.append(f"    {value_ty} v;")
    out.append("   } v;")

    out.append("  uint32_t br;")
    out.append(f"  br = uniform_sample({len(decoder_names)});")

    out.append("  switch(br) {")

    for i, dec in enumerate(decoder_names):
        out.append(f"  case {i}:")
        out.append(f"      v.b = {dec}(uniform_sample({dec}_range));") # assumes dec_range variable exists
        out.append("      break;")

    out.append("  }")
    out.append("   return v.v;")
    out.append("}")

    return "\n".join(out)


def test_BitPattern():
    ALL = BitPattern('X XXXX XXXX XXX XXXX XXXX XXXX XXXX XXXX')
    ZEROES = BitPattern('X 0000 0000 000 0000 0000 0000 0000 0000')
    SN = BitPattern('0 0000 0000 XXX XXXX XXXX XXXX XXXX XXXX', [ZEROES])

    assert ALL.least == ZEROES.least
    assert ALL.highest != ZEROES.highest

    # TODO: actually make this a test

    print(len(ALL.pattern))
    print(ALL.direct_range(), ZEROES.direct_range())
    print(ALL.direct_count(), ZEROES.direct_count())

    print(ALL.split_disjoint())
    print(ZEROES.split_disjoint())

    print(ALL.ranges())

    print(ZEROES.ranges())

    ALL.exclusions = [SN, ZEROES]
    all_xr = ALL.build_excluded_ranges()
    sn_xr = SN.build_excluded_ranges()
    print(all_xr)
    print("all-decode", ALL.build_decoder(all_xr))
    print(ALL.decoder_c_code("all"))
    print(ZEROES.decoder_c_code("zeroes"))
    print(SN.decoder_c_code("subnormals"))

if __name__ == "__main__":
    test_BitPattern()

