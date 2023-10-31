# from tu_pixel import *
import re


class SMP:
    def __init__(self, lines):
        self.lines = lines[::]
        self.input_set_cnts=[0, 0, 0, 0]
        self.crds=[]

        for line in lines:
            if 'cmd=' in line:
                self.tid = re.findall(r'tid=([0-9a-f]+),',line)[0]
            elif 'set0:' in line:
                self.input_set_cnts[0] += 1 if 'set0:1' in line else 0
                self.input_set_cnts[1] += 1 if 'set1:1' in line else 0
                self.input_set_cnts[2] += 1 if 'set2:1' in line else 0
                self.input_set_cnts[3] += 1 if 'set3:1' in line else 0
            elif line.startswith('P'):
                x = re.findall(r'0x[0-9a-f]{8}',line)
                self.crds.append(x)

    def get_cmd_line(self):
        return [i for i in self.lines if 'cmd=' in i][0]

    def get_crds(self):
        return self.crds


    def __str__(self):
        return f"tid={self.tid} cmdline={self.get_cmd_line()}"


if __name__ == '__main__':
    lines = '''
>------------------------TU[0.0.0-04-0] TUE0 tex crdinput: entry_idx = 0x0000001b, smp_cnt = 0x0000001a, lane_mask = 0xf, lane_idx = 0x4,shader_type = 0x5-------------------------<
P0: 0x3f5049b0(0.813624),0x3e5fe3ee(0.218643),0x3f6d1aac(0.926188),0x00000000(0.000000),
P1: 0x3f5333fd(0.825012),0x3e696884(0.227938),0x3f623702(0.883652),0x00000000(0.000000),
P2: 0x3f520ad3(0.820478),0x3e65e2a4(0.224497),0x3f670ea5(0.902567),0x00000000(0.000000),
P3: 0x3f52b9df(0.823149),0x3e6896ac(0.227137),0x3f6406ed(0.890731),0x00000000(0.000000),
cmd=SMP_C_LZ res_type=TEXTURE_2D_ARRAY fmt=R16_UNORM tid=80, sid=41, linear_texture = 0, is_mip = 0, is_horiz_buf = 0, width = 0x800, height = 0x800, depth = 0x3, msaa = 0x0, degamma_en = 0x0, apiMode=3, addr_mode_u_v_r: CLAMP_CLAMP_CLAMP, compare_fun = LEQUAL
set0:1 set1:1 set2:1 set3:1
set0:0 set1:1 set2:1 set3:1
set0:0 set1:0 set2:1 set3:1
set0:0 set1:0 set2:0 set3:1

    '''
    lines = lines.strip().splitlines()
    smp = SMP(lines)
    # print(str(smp))
    print(smp.tid)
    print(smp.get_cmd_line())
    print(smp.input_set_cnts)
    print(str(smp))
    # print(smp.get_crds())
    x= smp.get_crds()
    print(x)
    print(list(zip(*x))[2])
    print('xxxxxxx', x)
    x = '0x00000002' in x