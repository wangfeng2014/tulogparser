def get_general_info(smp_list,ele_list):
    msg = f"total_smp_cnt={len(smp_list)}\n"
    msg += f"total_ele_cnt={len(ele_list)}\n"
    return msg

def get_set_balance_info(smp_list,ele_list,tids_set_cnts_dict):
    return '\n'.join(
        [f'tid={tid} set_cnt_info={set_cnt_info}' for tid, set_cnt_info in tids_set_cnts_dict.items()])
