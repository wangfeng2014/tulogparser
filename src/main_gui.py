import os.path
from tkinter import *
from tkinter import ttk, filedialog

from src.fmt_loginfo import *


class Main_Gui:
    def __init__(self, start_file=None, start_dir=None):
        self.tk = Tk()
        self.logfiles_var = StringVar(value=[1, 2, 3, 4, start_file])
        self.recent_var = StringVar(value=list('hello'))
        self.__init_gui()
        pass

    def __init_gui(self):
        self.tk.geometry('800x400')
        self.pw = PanedWindow(self.tk, orient='horizon')
        self.pw.pack(fill='both', expand=1)

        self.btn_frame = Frame(self.pw)
        self.btn_frame.pack()
        self.pw.add(self.btn_frame)

        self.lst_frame = Frame(self.pw)
        self.lst_frame.pack()
        self.pw.add(self.lst_frame)

        self.info_frame = Frame(self.pw)
        self.info_frame.pack()
        self.pw.add(self.info_frame)

        ttk.Button(self.btn_frame, text='open file', command=self.gui_open_file).pack(fill='x')
        ttk.Button(self.btn_frame, text='open dir', command=self.gui_open_dir).pack(fill='x')
        rbtns = [
            # ['bookmark', '#9ad2f5', 1],
            ['recent', '#cdedd8', 1],
        ]

        self.radioBtnVar = IntVar(value=0)
        self.pre_radioBtnVar = IntVar(value=self.radioBtnVar.get())
        for t, sc, v in rbtns:
            Radiobutton(self.btn_frame, text=t, selectcolor=sc, command=self.btn_show_radiobtn, indicatoron=False,
                        variable=self.radioBtnVar, value=v).pack(fill='x', pady=30)

        self.logfiles_ls = Listbox(self.lst_frame, listvariable=self.logfiles_var)
        self.logfiles_ls.pack(fill='both', expand=True)

        self.logfiles_ls.bind('<Double-Button-1>', self.parse_file)

        self.recent_ls = Listbox(self.lst_frame, listvariable=self.recent_var, bg='#cdedd8')
        self.recent_ls.pack(fill='both', expand=True)
        self.recent_ls.pack_forget()

        # info frame
        self.text = Text(self.info_frame)
        self.text.pack(fill='both', expand=True)

    def start(self):
        self.logfiles = [1, 2, 3, 4, 5]
        # self.logfiles_var.set([1, 2, 1, 2, 1, 12])

        self.tk.mainloop()
        pass

    def handle_drag(self):
        pass

    def btn_show_radiobtn(self):
        if self.pre_radioBtnVar.get() == self.radioBtnVar.get():
            self.radioBtnVar.set(0)
        self.pre_radioBtnVar.set(self.radioBtnVar.get())

        self.recent_ls.pack_forget()
        if 1 == self.radioBtnVar.get():
            self.recent_ls.pack(fill='x', side='bottom')
        pass

    def gui_open_file(self):
        f = filedialog.askopenfilename()
        if f:
            self.open_file(f)

    def open_file(self, f):
        self.logfiles.append(f)
        self.logfiles_var.set(self.logfiles)
        print('open file ', f)

    def gui_open_dir(self):
        f = filedialog.askdirectory(mustexist=True)
        if f:
            self.open_dir(f)
        pass

    def open_dir(self, path):
        self.logfiles = os.listdir(path)
        self.logfiles_var.set(value=self.logfiles)

    def open_path(self):
        item = self.recent_ls.curselection()
        if item:
            fidx = item[0]
            path = self.recent_ls.get(fidx)
            print('click path', path)
        if os.path.exists(path):
            if os.path.isdir(path):
                self.open_dir(path)
            else:
                self.open_file(path)

    def click_recent(self):
        pass


    def parse_file(self, event):
        print('parse file ')
        fidx = self.logfiles_ls.curselection()
        if fidx:
            f = self.logfiles_ls.get(fidx)
            smp_list, ele_list, tids_set_cnts_dict = handle_one_logfile(f)
            msg = get_general_info(smp_list,ele_list)
            msg += get_set_balance_info(smp_list,ele_list,tids_set_cnts_dict)

            # show msg
            self.text.delete('1.0', 'end')
            self.text.insert('1.0', msg)
        pass


if __name__ == '__main__':
    from parse_logfile import *

    f = r'd:\g100\cmodel\gpubin\tu.log'
    gui = Main_Gui(start_file=f, start_dir=None)
    gui.start()
