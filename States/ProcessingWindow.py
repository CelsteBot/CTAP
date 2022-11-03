import tkinter as tk
from tkinter import ttk
from Classes import CelsteWindow
from Tasks import Tasks
import json

class ProcessingWindow(CelsteWindow):

    def __init__(self, title='', w_type=0, back_win='_wback', fin_win='_wfin', time=''):
        super().__init__('Processing', 1, 'NONE', 'a_processing_wfin', time)
        self.menu = True

        self.str_percent = tk.StringVar(self.frame, value='0%')
        self.str_status = tk.StringVar(self.frame, value='loading data')
        self.str_error = tk.StringVar(self.frame, value='')

    def update_percent(self):
        self.window.after(1000, self.update_percent)
        with open(f'tmp_data{self.time}.json', 'r') as in_file:
            try:
                self.data = json.load(in_file)
            except json.decoder.JSONDecodeError:
                return

        if self.data['processing_percent'] >= 95:
            self.finish(self.fin_win)
            return

        self.str_percent.set(str(round(self.data['processing_percent'], 1)) + '%')
        self.str_status.set(self.data['processing_status'])
        self.str_error.set(self.data['processing_error'])

    def main(self):
        super().main()

        frm_percent = ttk.Frame(self.frame)
        ttk.Label(frm_percent, text='Status:  ').pack(side=tk.LEFT)
        ttk.Label(frm_percent, textvariable=self.str_percent).pack(side=tk.LEFT)
        frm_percent.pack(side=tk.TOP)

        ttk.Label(self.frame, textvariable=self.str_status).pack(side=tk.TOP)
        self.lbl_error.configure(textvariable=self.str_error)
        self.lbl_error.pack()

        self.window.after(100, self.update_percent)
        print('im the first icky baby')
        self.window.after(100, Tasks(self.time).main)

        

