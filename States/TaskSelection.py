import tkinter as tk
from tkinter import ttk
from Classes import CelsteWindow


class TaskSelection(CelsteWindow):
    def __init__(self, title='', w_type=0, back_win='a_menu', time=''):
        super().__init__('Task Selection', 1, back_win, 'a_process_selection_wfin', time=time)

        self.btn_dd = None
        self.dd_state = False
        self.pe_state = False
        self.ee_state = False

    def toggle_process(self, process):
        # fix buttons
        match process:
            case 'dd':
                if self.dd_state:
                    self.dd_state = False
                    self.btn_dd.configure(style='Off.TButton')
                else:
                    self.dd_state = True
                    self.btn_dd.configure(style='On.TButton')

        # reconfigure default state
        flow = list(self.settings['HIDDEN-data_template']['flow'])
        i = flow.index('a_file_picker')
        if self.ee_state:
            flow.insert(i + 1, 'ee_config')
            x = flow.index('a_processing')
            flow[x:x] = ['ee_connection_review',
                         'ee_template_choice',
                         'ee_template_review',
                         'ee_sending']
        if self.pe_state:
            flow.insert(i + 1, 'pe_config')
        if self.dd_state:
            flow.insert(i + 1, 'dd_config')

        self.data['flow'] = flow
        
    def main(self):
        super().main()

        frm_p_btns = ttk.Frame(self.frame, style='Container1.TFrame')

        btn_pad = 10
        self.btn_dd = ttk.Button(frm_p_btns, text='DeDup', style='Off.TButton', command=lambda c='dd': self.toggle_process(c))
        self.btn_dd.pack(pady=btn_pad, fill=tk.X)
        ttk.Button(frm_p_btns, style='Off.TButton', text='Participant Evaluation', default=tk.DISABLED).pack(pady=btn_pad, fill=tk.X)
        ttk.Button(frm_p_btns, style='Off.TButton', text='Participant/Employer Emails', default=tk.DISABLED).pack(pady=btn_pad, fill=tk.X)

        self.toggle_process('dd')

        frm_p_btns.pack()




