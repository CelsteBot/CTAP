from Classes import CelsteWindow
from shutil import copy
from os.path import exists
from tkinter import ttk
import tkinter as tk


class SaveFiles(CelsteWindow):
    def __init__(self, title='', w_type=0, back_win='_wback', fin_win='_wfin', time=''):
        super().__init__('Save Files', 1, back_win, 'a_menu', time)

        self.menu = True
        self.str_dd_save_path = None

    def save(self, process):
        print('here')
        from_file = 'tmp_' + self.settings[f'ADVANCED-{process}_tmp_file_name'] + self.time + '.xlsx'
        to_file = self.str_dd_save_path.get() + '.xlsx'

        if not exists(from_file):
            self.raise_error('Something went terribly, horribly wrong. Please report the error to me before closing the program to preserve all data')

        copy(from_file, to_file)

    def main(self):
        super().main()
        frm_file_prompts = ttk.Frame(self.frame)

        if 'dd_config' in self.data['flow']:
            self.str_dd_save_path, z = self.file_prompt(
                frm_file_prompts, 
                lbl_text='DeDup', 
                btn_txt='Save File', 
                file_types=(('Excel Workbook', '*.xlsx'), ('All Files', '*')), 
                default_path=self.settings['default_path'], 
                select=False,
                on_file_choose=lambda c='dd': self.save(c),
                side=tk.LEFT
            )
        if 'pe_config' in self.data['flow']:
            pass
        if 'ee_config' in self.data['flow']:
            pass

        frm_file_prompts.pack(side=tk.TOP)

        ttk.Button(self.frame, text='Finish', command=lambda c=self.fin_win: self.finish(c)).pack(side=tk.TOP, pady=20)



