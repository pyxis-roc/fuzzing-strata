#!/usr/bin/env python3

def make_continuous(pattern):
    last_c = None
    out = []
    for i, c in enumerate(pattern):
        if c == '0' and last_c == 'X': # only X0 introduces discontinuities
            prefix = pattern[:i-1]
            p = make_continuous(pattern[i:])
            out.extend([prefix + "0" + pp for pp in p])
            out.extend([prefix + "1" + pp for pp in p])
            break
        last_c = c
    else:
        out.append(pattern)

    return out

def index_bp(pattern):
    out = 0
    for c in pattern:
        out <<= 1

        if c == '1':
            out |= 1

    return out

def lex_gen(pattern, X='0'):
    out = []
    for c in pattern:
        if c == 'X':
            out.append(X)
        else:
            out.append(c)

    return ''.join(out)

lex_least = lambda pattern: lex_gen(pattern, '0')
lex_highest = lambda pattern: lex_gen(pattern, '1')

def pattern_xtable(pattern):
    out = [0] * len(pattern)

    s = 0
    for i, c in enumerate(reversed(pattern)):
        out[i] = s
        s += 1 if c == 'X' else 0

    return out

def ns(prefix, xtable):
    assert len(prefix) < len(xtable)

    xs_after_prefix = xtable[len(xtable)-len(prefix)]

    # assumes that prefix is a proper prefix
    return 2 ** xs_after_prefix

def index(symbol, ns):
    x = 0
    pfx = "0"
    for s in symbol:
        if s == '1':
            x += ns[pfx]

        pfx += s
    return x

def generate(width, index, ns):
    out = []
    if index > ns["0"]:
        pfx = "1"
        index -= ns["0"]
    else:
        pfx = "0"

    out.append(pfx)

    for i in range(width-1):
        # the > in the original paper is a bug
        # comparing indices to counts
        if index >= ns[pfx + "0"]:
            out.append("1")
            index -= ns[pfx + "0"]
            pfx += "1"
        else:
            out.append("0")
            pfx += "0"

    return out

