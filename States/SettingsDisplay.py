import re
from tkinter import ttk
from copy import copy
from Classes import CelsteWindow
import tkinter as tk


class Settings(CelsteWindow):
    def __init__(self, title='', w_type=0, back_win='_wback', fin_win='_wfin', time=''):
        super().__init__('Settings', w_type, 'a_menu', fin_win, time)
        self.menu = True
        self.frm_settings = ttk.Frame(self.frame)
        self.frm_adv_settings = ttk.Frame(self.frame)
        self.settings_str_vars = {}

    # Helper Functions
    def ppath_to_display_path(self, path: list) -> str:
        path_name = ''
        for i in path:
            add = re.sub('_', ' ', str(i)).title() + '/'
            add = add.replace('"', '')
            path_name += add
        return path_name

    def ppath_to_display_name(self, path: list) -> str:
        path_name = ''
        for i in reversed(path):
            if type(i) != str:
                path_name = str(i) + ' ' + path_name
            else:
                add = re.sub('_', ' ', i).title()
                add = add.replace('"', '')
                path_name = add + ' ' + path_name
                break
        return path_name

    def get_var(self, path, ob):
        path = copy(path)
        i = path.pop(0)
        if len(path) > 0:
            return self.get_var(path, ob[i])
        else:
            return ob[i]

    def set_var(self, path, ob, v):
        path = copy(path)
        i = path.pop(0)
        if len(path) > 0:
            return self.set_var(path, ob[i], v)
        else:
            ob[i] = v
            return ob[i]

    def var_display(self, path, frm, pack=''):
        var = self.get_var(path, self.settings)
        match var:
            case str():
                self.string_setting(path, frm)
            case list():
                self.list_setting(path, frm)
            case dict():
                self.dict_setting(path, frm)
            case int():
                self.int_setting(path, frm)

    def int_field_validate(self, value: str) -> bool:
        if value.isnumeric():
            self.lbl_error.pack_forget()
            return True
        else:
            return False

    # Display Functions
    # Single Displays
    def string_setting(self, path, frm):
        title = self.ppath_to_display_name(path) + ': '
        frm_container = ttk.Frame(frm, style='Container1.TFrame')

        sv = None
        if str(path) in self.settings_str_vars.keys():
            sv = self.settings_str_vars[str(path)]
        else:
            sv = tk.StringVar(frm_container, value=str(self.get_var(path, self.settings)))
            self.settings_str_vars[str(path)] = sv

        ttk.Label(frm_container, text=title, style='Container1.TLabel').pack(side=tk.LEFT)
        ttk.Entry(frm_container, textvariable=sv).pack(side=tk.LEFT, expand=True, fill=tk.X)

        frm_container.pack(side=tk.TOP, fill=tk.X)

    def int_setting(self, path, frm):
        title = self.ppath_to_display_name(path) + ': '
        frm_container = ttk.Frame(frm, style='Container1.TFrame')

        sv = None
        if str(path) in self.settings_str_vars.keys():
            sv = self.settings_str_vars[str(path)]
        else:
            sv = tk.StringVar(frm_container, value=str(self.get_var(path, self.settings)))
            self.settings_str_vars[str(path)] = sv

        vcmd = (frm_container.register(self.int_field_validate), '%P')
        ttk.Label(frm_container, text=title, style='Container1.TLabel').pack(side=tk.LEFT)
        ttk.Entry(frm_container, textvariable=sv, validate='key', validatecommand=vcmd).pack(side=tk.LEFT, expand=1, fill=tk.X)

        frm_container.pack(side=tk.TOP, fill=tk.X)

    # Multiple Displays
    def list_setting(self, path: list, frm):
        # Label
        frm_container = ttk.Frame(frm, style='Container1.TFrame')
        setting_name = self.ppath_to_display_name(path)
        frm_label = ttk.Frame(frm_container)
        ttk.Label(frm_label, text=setting_name).pack(side=tk.LEFT)
        frm_label.pack(side=tk.TOP, expand=1, fill=tk.BOTH)

        # # Scroll Container Setup
        # frm_scroll = ttk.Frame(frm_container, style='Container1.TFrame')
        # cnv_list_view = tk.Canvas(frm_scroll)
        # scr_list_view = ttk.Scrollbar(frm_scroll, orient=tk.VERTICAL, command=cnv_list_view.yview)

        # # Configure
        # cnv_list_view.configure(yscrollcommand=scr_list_view.set)
        # cnv_list_view.bind('<Configure>', lambda a: cnv_list_view.configure(scrollregion=cnv_list_view.bbox('all')))

        # frm_list_view = ttk.Frame(cnv_list_view)
        # cnv_list_view.create_window((0, 0), window=frm_list_view, anchor='nw')
    
        # Make list items        
        var = self.get_var(path, self.settings)
        for i, li in enumerate(var):
            frm_list_item = ttk.Frame(frm_container)

            new_path = copy(path)
            new_path.append(i)
            self.var_display(new_path, frm_list_item)

            frm_list_item.pack(side=tk.TOP)

        # Pack
        # scr_list_view.pack(side=tk.RIGHT, fill=tk.Y)
        # cnv_list_view.pack(side=tk.LEFT, fill=tk.X, expand=0)
        # frm_scroll.pack(side=tk.TOP, fill=tk.X, expand=0)
        frm_container.pack(side=tk.TOP, pady=10)

    def dict_setting(self, path, frm, vrt=False):
        frm_container = ttk.Frame(frm, style='Container1.TFrame')
        
        # Label
        frm_label = ttk.Frame(frm_container, style='Container1.TFrame')
        lbl_label = ttk.Label(frm_label, style='Container1.TFrame')
        lbl_label.pack(side=tk.RIGHT)
        frm_label.pack(side=tk.TOP)

        # Var display
        frm_dict_display = ttk.Frame(frm_container, style='Container1.TFrame')
        var = self.get_var(path, self.settings)
        for key in var.keys():
            frm_dict_item = ttk.Frame(frm_dict_display, style='Container1.TFrame')

            new_path = copy(path)
            new_path.append(key)
            self.var_display(new_path, frm_dict_item)

            frm_dict_item.pack(side=tk.LEFT)

        frm_dict_display.pack(side=tk.TOP)
        frm_container.pack(side=tk.TOP)


    def finish(self, next):
        for key in self.settings_str_vars.keys():
            value = self.settings_str_vars[key].get()
            if value.isnumeric():
                value = int(value)
            
            path = key.strip('][').replace("'", '').split(', ')
            for i, p in enumerate(path):
                if p.isnumeric():
                    path[i] = int(p)
            self.set_var(path, self.settings, value)

        # Special assignments (Im a bad programmer and this section is cope)
        self.settings['HIDDEN-data_template']['dd_settings'] = self.settings['dd_default_settings']

        self.settings_change('NONE', '')
        super().finish(next)

    def main(self):
        super().main()

        for key in self.settings.keys():
            if key.startswith('HIDDEN-') or key.startswith('ADVANCED-'):
                continue

            self.var_display([key], self.frm_settings)

        self.frm_settings.pack(side=tk.TOP)

        ttk.Button(master=self.frm_btn, text='Back', command=lambda c=self.back_win: self.finish(c)).pack(side=tk.LEFT, padx=20)
