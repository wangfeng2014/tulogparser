import re


def get_crd_by_addring_mode(crd, addringmode):
    if addringmode == 'WRAP':
        v = float(crd)
        v = v - int(v)
        return v if v > 0 else 1 + v
    elif addringmode == 'CLAMP':
        v = float(crd)
        return 1 if v > 1 else 0 if v < 0 else v
    else:
        print(f"not implemented addressing mode:{addringmode}")
        return None


def get_float_crds_from_file(f, addringmode):
    with open(f) as fp:
        return map(get_float_crds_from_line, fp)


def get_float_crds_from_line(line):
    return [float(i.replace('nan','1')) for i in re.findall("\(([-na0-9.]+)\)", line)]

def get_hex_crds_from_line(line):
    return re.findall("0x[0-9a-f]{8}", line)


def get_hex_crds_from_file(f):
    with open(f) as fp:
        return [get_hex_crds_from_line(line) for line in fp if re.search("^P.: 0x", line)]


def float_eq(a, b):
    return abs(a - b) < 10 ** -6


if __name__ == '__main__':
    lines='''
    P0: 0x3f5049b0(0.813624), 0x3e5fe3ee(0.218643), 0x3f6d1aac(0.926188), 0x00000000(0.000000),
    P1: 0x3f5333fd(0.825012), 0x3e696884(0.227938), 0x3f623702(0.883652), 0x00000000(0.000000),
    P2: 0xfffffff1(-nan), 0x3e6896ac(0.227137), 0x3f6406ed(0.890731), 0x00000000(0.000000),
    P3: 0x7ffffff2(nan), 0x3e6896ac(0.227137), 0x3f6406ed(0.890731), 0x00000000(0.000000),
    '''
    lines = [i.strip() for i in lines.strip().splitlines()]
    for line in lines:
        print(line)
        print(get_hex_crds_from_line(line))
        print(get_float_crds_from_line(line))
    pass



