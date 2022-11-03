import tkinter as tk
from tkinter import ttk
from Classes import CelsteWindow


class DeDupConfig(CelsteWindow):
    def __init__(self, title='', w_type=0, back_win='_wback', fin_win='_wfin', time=''):
        super().__init__('DeDup Settings', 1, 'dd_config_wback', 'dd_config_wfin', time)
        self.frm_fields = ttk.Frame(self.frame, style='Container1.TFrame')
        self.fields = self.data['dd_settings']
        self.str_adjacencies = tk.StringVar(self.frame, value=100)

    def add_field(self):
        for child in self.frm_fields.winfo_children():
            child.destroy()

        self.fields.append({"field_name": "Field Name", "match_strength": 100},)
        self.draw_fields()

    def remove_field(self, i):
        for child in self.frm_fields.winfo_children():
            child.destroy()

        self.fields.pop(i)
        self.draw_fields()

    def draw_fields(self):
        for i, field in enumerate(self.fields):
            field['frame'] = ttk.Frame(self.frm_fields, style='Container1.TFrame')
            field['str_field'] = tk.StringVar(field['frame'], value=field['field_name'])
            field['str_match'] = tk.StringVar(field['frame'], value=str(field['match_strength']))
            field['btn_remove'] = ttk.Button(field['frame'], text='Remove', command=lambda c=i: self.remove_field(c))

            ttk.Label(field['frame'], text='Field Name: ', style='Container1.TLabel').pack(side=tk.LEFT)
            ttk.Entry(field['frame'], textvariable=field['str_field']).pack(side=tk.LEFT)
            ttk.Label(field['frame'], text='Match Strength: ', style='Container1.TLabel').pack(side=tk.LEFT)
            ttk.Entry(field['frame'], textvariable=field['str_match']).pack(side=tk.LEFT)

            field['btn_remove'].pack(side=tk.RIGHT, padx=10)
            field['frame'].pack(side=tk.TOP, pady=10)

    def finish(self, next):
        if len(self.fields) == 0:
            self.raise_error('Must have at least one field to perform DeDup')
            return
        if '_wfin' in next:
            for field in self.fields:
                match = field['str_match'].get()
                num_check = match.isnumeric()
                if not num_check:
                    self.raise_error('Error: Match Strength can only contain numbers (no decimal or percent)')
                    return
                if not 1 <= int(match) <= 100:
                    self.raise_error('Error: Match Strength must be between 1 and 100')
                    return

        for field in self.fields:
            field['field_name'] = field['str_field'].get()
            field['match_strength'] = field['str_match'].get()

            field.pop('frame')
            field.pop('str_field')
            field.pop('str_match')
            field.pop('btn_remove')

        if self.get_toggle_value('adjacency_toggle'):
            if not self.str_adjacencies.get().isnumeric():
                self.raise_error('Error: Adjacency Amount must be an integer')
                return

            self.data['dd_adjacencies'] = int(self.str_adjacencies.get())

        self.data['dd_settings'] = self.fields

        super().finish(next)

    def main(self):
        super().main()
            
        self.draw_fields()

        self.frm_fields.pack()

        frm_settings = ttk.Frame(master=self.frame)

        self.btn_toggle_view(frm_settings, 'adjacency_toggle', 'Adjacency Check: ', side=tk.LEFT)
        ttk.Label(frm_settings, text='Adjacency Amount: ').pack(side=tk.LEFT)
        ttk.Entry(frm_settings, textvariable=self.str_adjacencies).pack(side=tk.LEFT)

        frm_settings.pack(side=tk.TOP)

        ttk.Button(self.frm_btn, text='Add Field', command=self.add_field).pack(side=tk.RIGHT)
        

