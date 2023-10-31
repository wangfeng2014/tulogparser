import struct

def get_float_from_hex(hexstr):
    bs = bytes.fromhex(hexstr)
    a = struct.unpack('>f', bs)[0]
    return a


def get_sh_path(f):
    f = '/' + f if ":" in f else f
    f = f.replace(":", "").replace("\\", '/')
    return f


def gbp(i, msb, lsb):
    i = (i >> lsb)
    width = msb - lsb + 1
    mask = (1 << width) - 1
    v = i & mask
    return v


def get_xor_2(comb):
    comb ^= (comb >> 8)
    comb ^= (comb >> 4)
    comb ^= (comb >> 2)
    return comb & 0x3


def get_xor_1(comb):
    even = gbp(comb, 0, 0) \
           ^ gbp(comb, 2, 2) \
           ^ gbp(comb, 4, 4) \
           ^ gbp(comb, 6, 6) \
           ^ gbp(comb, 8, 8) \
           ^ gbp(comb, 10, 10) \
           ^ gbp(comb, 12, 12) \
           ^ gbp(comb, 14, 14)

    odd = \
        gbp(comb, 1, 1) ^ gbp(comb, 3, 3) ^ \
        gbp(comb, 5, 5) ^ gbp(comb, 7, 7) ^ \
        gbp(comb, 9, 9) ^ gbp(comb, 11, 11) ^ \
        gbp(comb, 13, 13)
    set_xor = (odd << 1) | even
    return set_xor



def filter_smp_by_crd(smp_list, crdvalue, crdidx):
    return [i for i in smp_list if crdvalue in list(zip(*i.get_crds()))[crdidx]]

if __name__ == '__main__':
    a = [get_xor_1(i) for i in range(0x7fff)]
    b = [get_xor_2(i) for i in range(0x7fff)]
    for idx,(i ,j) in enumerate(zip(a,b)):
        if i != j:
            print(idx, i,j, get_xor_1(idx), get_xor_2(idx) )
    print(a==b)
