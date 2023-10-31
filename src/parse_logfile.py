import os

import utils
from tu_smp import *
from tu_ele import *


def get_reduced_tu_log(f):
    df = f + "_reduced"
    f = utils.get_sh_path(f)
    cmd = f'''sh -c 'grep -e element_ -e smp_cnt -e ufoor -e  cmd= -e "^P.: 0x"  -e set0 {f}' > {df} '''
    print(f'cmd is :{cmd}')
    os.system(cmd)


def handle_temp_lines(templines, smp_list, ele_list):
    if templines:
        if 'smp_cnt' in templines[0]:
            smp_list.append(SMP(templines))
            templines.clear()
        elif 'element_' in templines[0]:
            ele_list.append(ELE(templines))
            templines.clear()
            pass
        else:
            templines.clear()


def parse_file(f, maxsmp=-1, maxele=-1):
    templines = []
    smp_list = []
    ele_list = []
    with open(f) as fp:
        for line in fp:
            if 'smp_cnt' in line or 'element_' in line:
                handle_temp_lines(templines, smp_list, ele_list)
            templines.append(line)

            if maxsmp > 0 and len(smp_list) > maxsmp:
                break
            if maxele > 0 and len(ele_list) > maxele:
                break
        handle_temp_lines(templines, smp_list, ele_list)  # handle last smp
    return smp_list, ele_list


def get_tid_set_cnts(tid, smp_list):
    tid_set_cnts = [i.input_set_cnts for i in smp_list if i.tid == tid]
    tid_set_cnts = zip(*tid_set_cnts)
    tid_set_cnts = [sum(i) for i in tid_set_cnts]
    return tid_set_cnts


def get_eid_set_cnts(eid, ele_list):
    eid_set_cnts = [i.input_set_cnts for i in ele_list if i.eid == eid]
    eid_set_cnts = zip(*eid_set_cnts)
    eid_set_cnts = [sum(i) for i in eid_set_cnts]
    return eid_set_cnts


def get_smp_set_cnt_info(smp_list):
    tids = list(set([i.tid for i in smp_list]))
    tids.sort()
    d = dict([(tid, get_tid_set_cnts(tid, smp_list)) for tid in tids])
    return d


def get_ele_set_cnt_info(ele_list):
    eids = list(set([i.eid for i in ele_list]))
    eids.sort()
    d = dict([(eid, get_eid_set_cnts(eid, ele_list)) for eid in eids])
    return d


def save_one_tid_info(tid, smp_list, file_dir):
    crd_f = os.path.join(file_dir, f'crd_tid_{tid}')
    with open(crd_f, 'w') as fp:
        for smp in smp_list:
            if smp.tid == tid:
                fp.write(''.join(smp.lines))

def handle_one_logfile(logfile):
    file_dir = os.path.dirname(logfile)
    get_reduced_tu_log(logfile)
    reduced_f = logfile + "_reduced"

    smp_list, ele_list = parse_file(reduced_f)
    tids_set_cnts_dict = get_smp_set_cnt_info(smp_list)
    [save_one_tid_info(tid, smp_list, file_dir) for tid in tids_set_cnts_dict.keys()]

    return smp_list, ele_list, tids_set_cnts_dict


if __name__ == '__main__':
    # tu_log_file = r'c:\ppa_auto\1013\FireStrike_GT1__F0_L113215D1968_Trim\tu.log'
    # tu_log_file = r'c:\ppa_auto\1013\FireStrike_GT1__F0_L114145D2008_Trim\tu.log'
    # tu_log_file = r'c:\ppa_auto\1013\FireStrike_GT1__F0_L113221D1969_Trim\tu.log'
    tu_log_file = r'd:\g100\cmodel\gpubin\tu.log'
    smp_list, ele_list, tids_set_cnts_dict = handle_one_logfile(tu_log_file)

# cmd=SMP_LZ res_type=TEXTURE_2D_ARRAY fmt=R8G8B8A8_UNORM tid=a7, sid=d0, linear_texture = 1, is_mip = 1, is_horiz_buf = 0, width = 0x200, height = 0x1, depth = 0x2, msaa = 0x0, degamma_en = 0x0, apiMode=3, addr_mode_u_v_r: CLAMP_CLAMP_CLAMP
