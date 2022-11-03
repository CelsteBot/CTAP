import tkinter as tk
from Classes import CelsteWindow
from os.path import dirname, exists


class FilePicker(CelsteWindow):
    def __init__(self, title='', w_type=0, back_win='a_menu', fin_win='_wfin', time=''):
        super().__init__('File Picker', 1, 'a_file_picker_wback', 'a_file_picker_wfin', time)

        self.file_paths = ['', '']
        self.str_pp_file_path = None
        self.str_ee_file_path = None

    def check_ee(self):
        for item in self.data['flow']:
            if 'ee' in item:
                return True

        return False

    def finish(self, next):
        # Verify selected files if attempting to continue
        if '_wback' not in next:
            if exists(self.str_pp_file_path.get()):
                self.data['prt_path'] = self.str_pp_file_path.get()
                self.settings_change('default_path', dirname(self.data['prt_path']))
            else:
                self.raise_error('Cannot Proceed without a file for Participants!')
                return
            if self.check_ee(): 
                if exists(self.str_ee_file_path.get()):
                    self.data['emp_path'] = self.str_pp_file_path.get()
                else:
                    self.raise_error('Cannot Proceed without a file for Participants!')
                    return
        super().finish(next)

    def main(self):
        super().main()

        file_types = self.settings['HIDDEN-file_types']
        for i in range(len(file_types)):
            file_types[i] = tuple(file_types[i])

        file_types = tuple(file_types)

        pp_path = self.settings['default_path']
        pp_file = self.file_paths[0]
        if pp_file:
            pp_path = ''
        if self.check_ee():
            ee_path = self.settings['default_path']
            ee_file = self.file_paths[1]
            if ee_file:
                ee_path = ''

            self.str_pp_file_path, z = self.file_prompt(master=self.frame, lbl_text='Participant List', side=tk.LEFT, file_types=file_types, default_file=pp_file, default_path=pp_path)
            self.str_ee_file_path, z = self.file_prompt(master=self.frame, lbl_text='Employers List',   side=tk.LEFT, file_types=file_types, default_file=ee_file, default_path=ee_path)
        else:
            self.str_pp_file_path, z = self.file_prompt(master=self.frame, lbl_text='Participant List', side=tk.TOP, file_types=file_types, default_file=pp_file, default_path=pp_path)
