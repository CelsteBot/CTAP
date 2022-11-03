import tkinter as tk
from tkinter import ttk
from Classes import CelsteWindow
import os


class Menu(CelsteWindow):
    def __init__(self, title='', w_type=0, time=''):
        for file in os.listdir(os.curdir):
            if file.startswith('tmp_'):
                os.remove(file)

        super().__init__('Countinous Process Automation Program', w_type, time=time)
        self.menu = True


    def main(self):
        super().main()
        frm_buttons = ttk.Frame(master=self.frame)
        btn_start = ttk.Button(master=frm_buttons, text='Start', style='Custom.TButton', command=lambda c='a_process_selection': self.finish(c))
        btn_settings = ttk.Button(master=frm_buttons, text='Settings', style='Custom.TButton', command=lambda c='a_settings': self.finish(c))

        btn_start.pack(side=tk.LEFT, padx=20)
        btn_settings.pack(side=tk.LEFT, padx=20)
        frm_buttons.pack(side=tk.TOP)
        
