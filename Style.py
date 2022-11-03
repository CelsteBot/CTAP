from tkinter import ttk


def GetStyle(root):
    style = ttk.Style(root)
    style.theme_use('alt')

    base_font = 'Roboto'
    base_size = 14


    # Base
    style.configure('.', font=f"{base_font} {base_size}", foreground='#ffffff', background='#333f50')
    style.configure('TLabel', font=f'{base_font} {base_size}', color='#ffffff', background='#333f50')
    style.configure('TFrame', background='#333f50')
    style.configure('TButton', font=f'{base_font} {base_size + 2}', expand=True, background='#8497b0', foreground='#ffffff', bordercolor='#000000', relief='FLAT')
    style.map('TButton', background=[('active', '#5a79a3')], relief=[('active', 'FLAT')])
    style.configure('TEntry', font=f'{base_font} {base_size}', fieldbackground ='#8497b0', foreground='#ffffff', bordercolor='#000000', relief='FLAT')

    # Headers
    style.configure('H1.TLabel' , font=f'{base_font} {base_size + 12} bold')
    style.configure('H2.TLabel' , font=f'{base_font} {base_size + 10}  bold')
    style.configure('H3.TLabel' , font=f'{base_font} {base_size + 8}')
    style.configure('H4.TLabel' , font=f'{base_font} {base_size + 6}')

    # Containers
    style.configure('Container1.TFrame' , background='#45546b')
    style.configure('Container1.TLabel' , background='#45546b', font=f'{base_font} {base_size}')
    style.configure('Container1.H4.TLabel' , background='#45546b', font=f'{base_font} {base_size + 6}')

    # On/Off
    style.configure('On.TButton'    )
    style.configure('Off.TButton'   , background='#627482', foreground='#aaaaaa')
    style.map('Off.TButton', background=[('active', '#46545e')], relief=[('active', 'FLAT')])

    # Misc
    style.configure('FilePath.TLabel', font=f'{base_size - 2} underline')
    style.configure('Custom.TButton', font=f"{base_size + 2}")
    style.configure('Error.TLabel', foreground='#ff0000', justify='center', wraplength=500)

    return style




