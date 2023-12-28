from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.ttk import Separator
import libs.chart_request as cr
import libs.miraecommand as mc
from datetime import date, timedelta
import pandas as pd
import pyuac
import os

if not pyuac.isUserAdmin():
    print("Re-launching as admin!")
    pyuac.runAsAdmin()

def browse_csv_file():
    filename = filedialog.askopenfilename(initialdir = "./",
                                          title = "Select a File",
                                          filetypes = (("CSV", "*.csv"),))
    
    return filename

def browse_excel_file():
    filename = filedialog.askopenfilename(initialdir = "./",
                                          title = "Select a File",
                                          filetypes = (("Excel", "*.xlsx"),))
    return filename

def browse_daftar_saham():
    global dir_daftar_saham, dir_data_order
    text = browse_csv_file()
    if text != '':
        dir_daftar_saham = text
        lbl_dir_daftar_saham.configure(text='...' + dir_daftar_saham[-20:])
    write_user_data()

def browse_data_order():
    global dir_daftar_saham, dir_data_order
    text = browse_excel_file()
    if text != '':
        dir_data_order = text
        lbl_dir_data_order.configure(text='...' + dir_data_order[-20:])
    write_user_data()

def request_chart():
    try:
        daftar_saham = pd.read_csv(dir_daftar_saham)
        daftar_saham = daftar_saham['Daftar Saham'].tolist()
    except:
        messagebox.showerror("Error Daftar Saham", "File tidak ditemukan, periksa kembali direktori yang dituju!")
        print(dir_daftar_saham)
        return
    
    # try:
    #     order = pd.read_excel(dir_data_order)
    #     order = order['kode'].tolist()
    # except:
    #     messagebox.showerror("Error Auto Order", "File tidak ditemukan, periksa kembali direktori yang dituju!")
    #     print(dir_data_order)
    #     return
    
    # for kode in order:
    #     try: daftar_saham.remove(kode)
    #     except: pass
    
    # daftar_saham = order+daftar_saham
    daftar_saham = [x for x in daftar_saham if str(x) != 'nan']
    cr.run(stocks = daftar_saham)

def request_chart_portfolio():
    try:
        order = pd.read_excel(dir_data_order)
        order = order.fillna('')
    except:
        messagebox.showerror("Error Auto Order", "File tidak ditemukan, periksa kembali direktori yang dituju!")
        print(dir_data_order)
        return

def auto_order():
    try:
        order = pd.read_excel(dir_data_order)
        order = order.fillna('')
    except:
        messagebox.showerror("Error Auto Order", "File tidak ditemukan, periksa kembali direktori yang dituju!")
        print(dir_data_order)
        return
    
    # tanggal, kode, buy, lot_buy, conf_buy, sl, tp
    mc.all_clear()
    for index, row in order.iterrows():
        if row['kode'] == '':
            continue
        # order buy jika belum di buy
        if row['conf_buy'] == '':
            mc.order_buy(kode=row['kode'], price=row['buy'], lot=row['lot_buy'])
        # order sl dan tp
        mc.order_sellSL(kode=row['kode'], price=row['sl'], lot=row['lot_buy'])
        mc.order_sellTP(kode=row['kode'], price=row['tp'], lot=row['lot_buy'])
    mc.all_send()

def write_user_data():
    global dir_daftar_saham, dir_data_order
    with open(user_data_file, 'w') as f:
        f.write(dir_daftar_saham+'\n')
        f.write(dir_data_order)

def read_user_data():
    global dir_daftar_saham, dir_data_order
    with open(user_data_file) as f:
        lines = []
        for line in f:
            lines.append(line.replace('\n',''))
    dir_daftar_saham = lines[0]
    dir_data_order = lines[1]
    lbl_dir_daftar_saham.configure(text='...' + dir_daftar_saham[-20:])
    lbl_dir_data_order.configure(text='...' + dir_data_order[-20:])

# Create the root window
window = Tk()
window.title('Mirae Trade Bot')
window.geometry("375x200")
window.minsize(375, 200)
window.maxsize(375, 200)

# window.config(background = "white")

dir_daftar_saham = 'Browse file untuk memilih'
dir_data_order = 'Browse file untuk memilih'

lbl_daftar_saham = Label(window, text = "Request Chart Saham")
lbl_data_order = Label(window, text = "Input Data Order")

lbl_dir_daftar_saham = Label(window,
                            text = dir_daftar_saham,
                            fg = "green")

lbl_dir_data_order= Label(window,
                            text = dir_data_order,
                            fg = "blue")

btn_explore_all = Button(window,
                        text = "Browse Saham",
                        command = browse_daftar_saham)

btn_explore_order = Button(window,
                        text = "Browse Order",
                        command = browse_data_order)

btn_request_chart = Button(window,
                        text = "Request Chart",
                        command = request_chart)    

btn_auto_order = Button(window,
                        text = "Run Auto Order",
                        command = auto_order)

separator = Separator(window,orient='horizontal')

lbl_daftar_saham.grid(column = 1, row = 1, sticky='w')
lbl_dir_daftar_saham.grid(column = 1, row = 2, padx=5, pady=0)
btn_explore_all.grid(column = 2, row = 2, padx=10, pady=0)

btn_request_chart.grid(column = 3, row = 2, padx=10, pady=0)

# separator.grid(column=1, row=3, columnspan=3, pady=5, sticky='ew')

lbl_data_order.grid(column = 1, row = 4, sticky='w')
lbl_dir_data_order.grid(column = 1, row = 5, padx=5, pady=0)
btn_explore_order.grid(column = 2, row = 5, padx=10, pady=0)

btn_auto_order.grid(column = 3, row = 5, padx=10, pady=0)

# handling user data
user_data_file = 'user_data.txt'
if not os.path.isfile(user_data_file):
    write_user_data()
else:
    read_user_data()

window.mainloop()