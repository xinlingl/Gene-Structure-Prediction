STATE_INDICES = {
    'N' : 0,
    'E' : 1,
    'I' : 2,
    'p' : 3,
    'P' : 4,
    'Z' : 5,
    'z' : 6,
    's' : 7,
    'S' : 8,
}


OBSERVATION_INDICES = {
    'A' : 0,
    'C' : 1,
    'G' : 2,
    'T' : 3,
}


def transitionIndex(states, observations):
    row_index = 0
    n = len(states)
    for i in range(0, n):
        o_i = OBSERVATION_INDICES[observations[i]]
        s_i = STATE_INDICES[states[i]]
        row_index += s_i *(9**i * 4**n) + o_i*(4**i)
    return row_index


if __name__!="__main__":
    """TEST CASES"""
    st = 'N'; ob = 'A'
    expected =  0

    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i 
        print expected; exit()

    st = 'N'; ob = 'C'
    expected =  1
    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()
    st = 'N'; ob = 'T'
    expected =  2
    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()
    st = 'N'; ob = 'G'
    expected =  3
    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()
    st = 'E'; ob = 'A'
    expected =  4
    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()
    st = 'E'; ob = 'C'
    expected =  5
    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()
    st = 'E'; ob = 'G'
    expected =  6
    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()
    st = 'E'; ob = 'T'
    expected =  7
    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()
    st = 'I'; ob = 'A'
    expected =  8
    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()
    st = 'I'; ob = 'C'
    expected =  9
    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()
    st = 'I'; ob = 'T'
    expected = 10
    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()
    st = 'I'; ob = 'G'
    expected = 11
    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()
    st = 'S'; ob = 'A'
    expected = 32
    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()
    st = 'S'; ob = 'C'
    expected = 33
    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()
    st = 'S'; ob = 'G'
    expected = 34
    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()
    st = 'S'; ob = 'T'
    expected = 35
    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()

    st='NN';ob='AA'
    expected = 0

    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()

    st='NN';ob='AC'
    expected = 1

    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()

    st='NN';ob='AT'
    expected = 2

    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()

    st='NN';ob='AG'
    expected = 3

    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()

    st='NN';ob='CA'
    expected = 4

    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()

    st='NN';ob='CC'
    expected = 5

    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()

    st='NN';ob='CT'
    expected = 6

    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()

    st='NN';ob='CG'
    expected = 7

    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()

    st='NE';ob='AA'
    expected = 16

    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()

    st='NI';ob='AA'
    expected = 32

    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()

    st='Np';ob='AA'
    expected = 48

    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()

    st='NP';ob='AA'
    expected = 64

    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()

    st='NZ';ob='AA'
    expected = 80

    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()

    st='Nz';ob='AA'
    expected = 96

    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()

    st='Ns';ob='AA'
    expected = 112

    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()

    st='NS';ob='AA'
    expected = 128

    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()

    st='EN';ob='AA'
    expected = 144

    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()

    st='IN';ob='AA'
    expected = 288

    r_i = transitionIndex(st, ob)

    if r_i != expected:
        print r_i
        print expected; exit()




