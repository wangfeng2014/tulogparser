import struct


def get_float_from_hex(hexstr):
    bs = bytes.fromhex(hexstr)
    a = struct.unpack('>f', bs)[0]
    return a


def get_sh_path(f):
    f = '/' + f if ":" in f else f
    f = f.replace(":", "").replace("\\", '/')
    return f


def filter_smp_by_crd(smp_list, crdvalue, crdidx):
    return [i for i in smp_list if crdvalue in list(zip(*i.get_crds()))[crdidx]]


if __name__ == '__main__':
    pass