from tkinter import ttk
from tkinter import filedialog as fd
import os.path as path
import tkinter as tk
import json
import os



class CelsteWindow:
    def __init__(self, title = '', w_type = 0, back_win = '_wback', fin_win='_wfin', time=''):
        # Tkinter setup
        self.window = ttk.Frame(name='nothing')
        self.frame = ttk.Frame(master=self.window)
        self.lbl_error = ttk.Label(self.frame, text='Error', style='Error.TLabel')

        # Var Assignment
        self.window.pack(padx=30, pady=20)
        self.title = title
        self.window_types = [
            'Menu',
            'Function'
        ]
        self.window_type = w_type 
        self.back_win = back_win
        self.fin_win = fin_win
        self.menu = False
        self.frm_btn = None
        self.time = time

        # File Prompt Vars
        self.file_str_vars = []
        self.file_disp_str_vars = []

        # Toggle Vars
        self.toggles = {}
        self.on_img = None
        self.off_img = None

        # Data Loading
        self.settings = {}
        with open('settings.json', 'r') as in_file:
            self.settings = json.load(in_file)

        self.data = {}
        try:
            with open(f'tmp_data{time}.json', 'r') as in_file:
                self.data = json.load(in_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.data = self.settings['HIDDEN-data_template']
            with open(f'tmp_data{time}.json', 'w') as out_file:
                out_str = json.dumps(self.data, indent=4)
                out_file.write(out_str)

    def settings_change(self, key, var):
        if key in self.settings.keys():
            self.settings[key] = var

        with open('settings.json', 'w') as out_file:
            update = json.dumps(self.settings, indent=4)
            out_file.write(update)

    def raise_error(self, msg):
        self.lbl_error.pack_forget()
        self.lbl_error.configure(text=msg)
        self.lbl_error.pack()
   
    # Toggle Functions
    def toggle(self, name, command):
        toggle = self.toggles[name]
        side=toggle['side']
        btn_toggle = toggle['btn']
        toggle['value'] = not toggle['value']

        img_toggle = None
        if toggle['value']:
            img_toggle = self.on_img
        else:
            img_toggle = self.off_img

        btn_toggle.pack_forget()
        btn_toggle.configure(image=img_toggle)
        btn_toggle.pack(side=side)

        if callable(command):
            command()

    def get_toggle_value(self, name):
        return self.toggles[name]['value']

    def set_toggle_value(self, name, value):
        toggle = self.toggles[name]
        toggle['value'] = value
        side = toggle['side']

        img_toggle = None
        if toggle['value']:
            img_toggle = self.on_img
        else:
            img_toggle = self.off_img

        btn_toggle = toggle['btn']
        btn_toggle.pack_forget()
        btn_toggle.configure(image=img_toggle)
        btn_toggle.pack(side=side)

    def btn_toggle_view(self, master, name, lbl_text='', lbl_style='', lbl_side=tk.LEFT, side=tk.TOP, on_toggle=None, default=False):
        if name in self.toggles.keys():
            raise Exception('ERROR: Name of toggles must be unique!')
            return

        if not self.on_img:
            self.on_img =  tk.PhotoImage(master=self.frame, file=self.settings['HIDDEN-toggle_on'])
            self.off_img = tk.PhotoImage(master=self.frame, file=self.settings['HIDDEN-toggle_off'])

        frm_toggle = ttk.Frame(master=master)

        def_img=''
        if default:
            def_img = self.on_img
        else:
            def_img = self.off_img

        lbl_toggle = ttk.Label(master=frm_toggle, text=lbl_text, style=lbl_style)
        btn_toggle = ttk.Button(master=frm_toggle, image=def_img, command=lambda c=name, d=on_toggle: self.toggle(c, d))

        lbl_toggle.pack(side=lbl_side)
        btn_toggle.pack(side=lbl_side)
        frm_toggle.pack(side=side)

        toggle_dict = {'name': name, 'btn': btn_toggle, 'lbl': lbl_toggle, 'value': default, 'side': side}
        self.toggles[name] = toggle_dict

    # File Prompt Functions
    def reload_file_disp(self):
        marks = []
        for str_file, str_disp in zip(self.file_str_vars, self.file_disp_str_vars):
            if str_disp == None:
                marks.append((str_file, str_disp))
                continue
            if path.exists(str_file.get()):            
                path_split = str_file.get().split('/')
                str_disp.set(value=path_split[len(path_split) - 1])

        for mark in marks:
            self.file_str_vars.remove(mark[0])
            self.file_disp_str_vars.remove(mark[1])

    def select_file(self, str_file, file_types=(('All Files', '*')), default_path='C:/', method=None):
        # open file navigator
        file_name = fd.askopenfilename(
            title='Open File',
            initialdir=default_path,
            filetypes=file_types,
        )

        # reload display
        str_file.set(value=file_name)
        self.reload_file_disp()

        # call method
        if method:
            method()

    def save_file(self, str_file, file_types=(('All Files', '*')), default_path='C:/', method=None):
        # open file navigator
        file_name = fd.asksaveasfilename(
            title='Save File',
            initialdir=default_path,
            filetypes=file_types
        )
        
        # reload display
        str_file.set(value=file_name)
        self.reload_file_disp()

        # call method
        if method:
            method()

    def file_prompt(self, master, frm_style='Container1.TFrame', lbl_text='Choose File', lbl_style='Container1.H4.TLabel', btn_txt='Open File', btn_style='On.TButton', side=tk.TOP, file_types=(()), default_file='', default_path='', on_file_choose=None, select=True):
        if not master:
            master = self.frame
        frm_container = ttk.Frame(master=master, style=frm_style)

        # var assignment
        str_file =      tk.StringVar(frm_container, value='')
        str_file_disp = tk.StringVar(frm_container, value=btn_txt)
        self.file_str_vars.append(str_file)
        self.file_disp_str_vars.append(str_file_disp)
        
        if default_file:
            if path.exists(default_file):
                str_file.set(value=default_file)
        if not default_path:
            default_path = path.dirname(default_file)
        command = self.select_file
        if select:
            command = lambda c=str_file, d=file_types, e=default_path, f=on_file_choose: self.select_file(c, d, e, f)
        else:
            command = lambda c=str_file, d=file_types, e=default_path, f=on_file_choose: self.save_file(c, d, e, f)

        # Tkinter stuff
        ttk.Label(master=frm_container, text=lbl_text, style=lbl_style).pack(side=tk.TOP, pady=10)
        ttk.Button(master=frm_container, textvariable=str_file_disp, style=btn_style, command=command).pack(side=tk.TOP, pady=10, padx=10)

        frm_container.pack(side=side)
        return (str_file, str_file_disp)


    def finish(self, next):
        fn = f'tmp_data{self.time}.json'
        with open(fn, 'w') as out_file:
            out_str = json.dumps(self.data, indent=4)
            out_file.write(out_str)

        for child in self.window.winfo_children():
            child.destroy()

        ttk.Frame(name=next).pack()
        self.window.destroy()

    def main(self):
        header_font = ''
        match self.window_type:
            case 0:
                header_font = 'H1.TLabel'
            case 1:
                header_font = 'H3.TLabel'

        ttk.Label(master=self.window, text=self.title, style=header_font).pack(pady=20)
        self.frame.pack(fill=tk.BOTH, expand=1, pady=10)
        self.frm_btn = ttk.Frame(master=self.window)
        self.frm_btn.pack(side=tk.BOTTOM)

        if not self.menu:
            ttk.Button(master=self.frm_btn, text='Back', command=lambda c=self.back_win: self.finish(c)).pack(side=tk.LEFT, padx=20)
            ttk.Button(master=self.frm_btn, text='Continue', command=lambda c=self.fin_win: self.finish(c)).pack(side=tk.RIGHT, padx=20)
        

