# from tu_pixel import *
import re


class ELE:
    def __init__(self, lines):
        self.lines = lines[::]
        self.input_set_cnts = [0, 0, 0, 0]

        for line in lines:
            if 'element_' in line:
                self.eid = re.findall(r'element_(0x[0-9a-f]+) ', line)[0]
            elif 'set0:' in line:
                self.input_set_cnts[0] += 1 if 'set0:1' in line else 0
                self.input_set_cnts[1] += 1 if 'set1:1' in line else 0
                self.input_set_cnts[2] += 1 if 'set2:1' in line else 0
                self.input_set_cnts[3] += 1 if 'set3:1' in line else 0

    def get_ele_line(self):
        return [i for i in self.lines if 'element_' in i][0]

    def __str__(self):
        return f"tid={self.eid} cmdline={self.get_ele_line()}"


if __name__ == '__main__':
    lines = '''
>*****vb element_0x2  format:R32G32B32A32_FLOAT  Element_Offset:0x10 vbid:0x0 instance_en:1 loading:*****<
set0:1 set1:0 set2:0 set3:0
set0:1 set1:1 set2:0 set3:0
set0:1 set1:1 set2:1 set3:0
set0:1 set1:1 set2:1 set3:1
    '''
    lines = lines.strip().splitlines()
    ele = ELE(lines)
    # print(str(smp))
    print(ele.eid)
    print(ele.get_ele_line())
    print(ele.input_set_cnts)
    print(str(ele))
