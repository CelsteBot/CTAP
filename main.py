import tkinter as tk
import json
from States import Menu, FilePicker, DeDupConfig, ProcessingWindow, SaveFiles, TaskSelection, SettingsDisplay
from Style import GetStyle
import os
from time import time
import multiprocessing


class EmailApp:
    def __init__(self) -> None:
        self.settings = {}
        with open('settings.json', 'r') as in_file:
            self.settings = json.load(in_file)

        self.time = str(time())
        self.data = {}
        self.remove_tmp()
        self.run()

    def remove_tmp(self):
        files = os.listdir()
        for file in files:
            if file.startswith('tmp_') and file.endswith('.json') or file.endswith('.csv'):
                os.remove(file)

    def reload_data(self):
        flow = []
        if os.path.exists(f'tmp_data{self.time}.json'):
            with open(f'tmp_data{self.time}.json', 'r') as in_file:
                self.data = json.load(in_file)

            flow = self.data['flow']
            return flow

        return None

    def update_check(self):
        self.root.after(100, self.update_check)
        if len(self.root.children) == 0: # when program starts
            print('here2')
            Menu.Menu(time=self.time).main()
        elif len(self.root.children) == 1: # when a window closes
            state = list(self.root.children.keys())[0]
            check = 0

            if '_wfin' in state: # window going to next state
                flow = self.reload_data()
                state_clean = state[:-5]
                current_i = flow.index(state_clean)
                next_state = flow[current_i + 1]
                check = self.possible_states.index(next_state)
            elif '_wback' in state: # window going to previous state
                flow = self.reload_data()
                state_clean = state[:-6]
                current_i = flow.index(state_clean)
                next_state = flow[current_i - 1]
                check = self.possible_states.index(next_state)
            elif state in self.possible_states: # menu going to either settings or PS
                check = self.possible_states.index(state)
            else: # nothing
                return

            match check:
                case 0:
                    SettingsDisplay.Settings(time=self.time).main()
                    self.state = 0
                case 1:
                    print('heere3')
                    Menu.Menu(time=self.time).main()
                    self.state = 1
                case 2:
                    TaskSelection.TaskSelection(time=self.time).main()
                    self.state = 2
                case 3:
                    FilePicker.FilePicker(time=self.time).main()
                    self.state = 3
                case 4:
                    DeDupConfig.DeDupConfig(time=self.time).main()
                    self.state = 4
                case 7:
                    ProcessingWindow.ProcessingWindow(time=self.time).main()
                case 12:
                    SaveFiles.SaveFiles(time=self.time).main()

            self.root.children[state].destroy() 

    def on_closing(self):
        self.reload_data()
        for file in os.listdir(os.curdir):
            if file.startswith('tmp_'):
                os.remove(file)

        self.root.destroy()

    def run(self):
        self.root = tk.Tk()
        GetStyle(self.root)
        self.root.title("CTAP")
        self.root.configure(bg='#333f50')
        self.root.wm_attributes('-transparentcolor', '#000001')

        self.possible_states = self.settings['HIDDEN-possible_states']
        self.state = 0

        self.root.after(1, self.update_check)
        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.root.mainloop()

if __name__ == '__main__': # make sure ur not a multiprocessing baby
    multiprocessing.freeze_support()
    print('here')
    run = True
    current_dir = os.listdir(os.curdir)
    for i in current_dir:
        if 'tmp_data' in i:
            tmp_time_split = i[:-5].split('tmp_data')
            tmp_time = tmp_time_split[len(tmp_time_split) - 1]
            tmp_time = float(tmp_time)

            if time() - tmp_time < 300:
                run = False

    if run:
        app = EmailApp()
