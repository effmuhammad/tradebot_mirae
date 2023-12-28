import math
import pyautogui
import threading
import pandas as pd
import numpy as np
import shutil
import os
from datetime import date, timedelta
import pyuac
import time
import clipboard

def step(val):
    if val >= 50 and val < 200:
        return 1
    elif val >= 200 and val < 500:
        return 2
    elif val >= 500 and val < 2000:
        return 5
    elif val >= 2000 and val < 5000:
        return 10
    elif val >= 5000:
        return 25

def step_sl_layer(val):
    if val >= 50 and val <= 200:
        return 1
    elif val > 200 and val <= 500:
        return 2
    elif val > 500 and val <= 2000:
        return 5
    elif val > 2000 and val <= 5000:
        return 10
    elif val > 5000:
        return 25

def roundbystep(val):
    return step(val) * math.floor(val/step(val))

def get_time():
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%H:%M:%S", named_tuple)
    return time_string

def get_valid_date(): 
    # 7 days after today
    year = str((date.today()+timedelta(days=7)).year)
    month = str((date.today()+timedelta(days=7)).month)
    if len(month)<2:
        month = '0'+month
    day = str((date.today()+timedelta(days=7)).day)
    if len(day)<2:
        day = '0'+day
    return year+month+day

def move_file(filename,src_path,dst_path):
    # menentukan apakah dataset disimpan
    df = pd.read_csv(filename)
    src_file = os.path.join(src_path, filename)
    dst_file = os.path.join(dst_path, filename)
    shutil.move(src_file, dst_file)

def wait_processing():
    while True:
        time.sleep(0.1)
        content = pyautogui.locateOnScreen('libs/processing_img.png', region = (21,646,80,18), confidence = 0.9)
        if content == None:
            break

def order_buy(kode, price, lot, live = False):
    pyautogui.click(x = 77, y = 105) # click tab automatic order
    pyautogui.click(x = 116, y = 170) # click tab buy
    pyautogui.click(x = 116, y = 170) # click tab buy
    wait_processing()
    pyautogui.click(x = 667, y = 137) # click button add setting
    pyautogui.click(x = 30, y = 411) # click input kode
    pyautogui.write(kode)
    pyautogui.press('enter')
    pyautogui.click(x = 474, y = 478, clicks=2) # set condition harga <= ...
    pyautogui.write(str(int(price)))
    pyautogui.click(x = 640, y = 478, clicks=2) # set order quantity
    pyautogui.write(str(int(lot)))
    pyautogui.click(x = 913, y = 478) # dropdown order price 
    pyautogui.click(x = 872, y = 530) # select offer+2
    pyautogui.click(x = 620, y = 618) # set tanggal
    pyautogui.write(get_valid_date())
    pyautogui.click(x = 812, y = 615) # save setting
    wait_processing()
    if live: all_send()

def order_sellSL(kode, price, lot, live = False):                           # dengan fitur 3 layer sl
    new_price = price
    for i in range(3):
        pyautogui.click(x = 77, y = 105) # click tab automatic order
        pyautogui.click(x = 160, y = 170) # click tab sell
        pyautogui.click(x = 160, y = 170) # click tab sell
        wait_processing()
        pyautogui.click(x = 667, y = 137) # click button add setting
        pyautogui.click(x = 30, y = 411) # click input kode
        pyautogui.write(kode)
        pyautogui.press('enter')
        pyautogui.click(x = 431, y = 478) # dropdown condition
        pyautogui.click(x = 431, y = 514) # select <=
        pyautogui.click(x = 474, y = 478, clicks=2) # set condition harga
        pyautogui.write(str(int(new_price)))
        pyautogui.click(x = 640, y = 478, clicks=2) # set order quantity
        pyautogui.write(str(int(lot)))
        pyautogui.click(x = 913, y = 478) # dropdown order price 
        pyautogui.click(x = 872, y = 660) # select bid-4
        pyautogui.click(x = 620, y = 618) # set tanggal
        pyautogui.write(get_valid_date())
        pyautogui.click(x = 812, y = 615) # save setting
        wait_processing()
        new_price -= step_sl_layer(new_price)
    if live: all_send()

def order_sellTP(kode, price, lot, live = False):
    pyautogui.click(x = 77, y = 105) # click tab automatic order
    pyautogui.click(x = 160, y = 170) # click tab sell
    pyautogui.click(x = 160, y = 170) # click tab sell
    wait_processing()
    pyautogui.click(x = 667, y = 137) # click button add setting
    pyautogui.click(x = 30, y = 411) # click input kode
    pyautogui.write(kode)
    pyautogui.press('enter')
    pyautogui.click(x = 431, y = 478) # dropdown condition
    pyautogui.click(x = 431, y = 498) # select >=
    pyautogui.click(x = 474, y = 478, clicks=2) # set condition harga
    pyautogui.write(str(int(price)))
    pyautogui.click(x = 640, y = 478, clicks=2) # set order quantity
    pyautogui.write(str(int(lot)))
    pyautogui.click(x = 913, y = 478) # dropdown order price 
    pyautogui.click(x = 872, y = 626) # select bid-2
    pyautogui.click(x = 620, y = 618) # set tanggal
    pyautogui.write(get_valid_date())
    pyautogui.click(x = 812, y = 615) # save setting
    wait_processing()
    if live: all_send()

def all_send():
    pyautogui.click(x = 77, y = 105) # click tab automatic order
    pyautogui.click(x = 116, y = 170) # click tab buy
    wait_processing()
    pyautogui.click(x = 730, y = 136) # all send button
    wait_processing()
    pyautogui.click(x = 160, y = 170) # click tab sell
    wait_processing()
    pyautogui.click(x = 730, y = 136) # all send button
    wait_processing()

def all_clear():
    pyautogui.click(x = 77, y = 105) # click tab automatic order
    pyautogui.click(x = 116, y = 170) # click tab buy
    wait_processing()
    pyautogui.click(x = 845, y = 136) # all clear button
    time.sleep(0.5)
    pyautogui.click(x = 460, y = 420) # ok dialogbox
    wait_processing()
    pyautogui.click(x = 160, y = 170) # click tab sell
    wait_processing()
    pyautogui.click(x = 845, y = 136) # all clear button
    time.sleep(0.5)
    pyautogui.click(x = 460, y = 420) # ok dialogbox
    wait_processing()

# belum
def portofolio():
    pyautogui.click(x = 1070, y = 710)
    start = time.time()
    while pyautogui.locateOnScreen('./img_konfirmasi/portofolio_ready.png', region = (388,702,190,15)) == None:
        if pyautogui.locateOnScreen('./img_konfirmasi/portofolio_wait_next.png', region = (388,702,190,15)) != None:
            print('[PERINGATAN] portofolio sedang error tidak dapat di load')
        if time.time() - start >= 5:
            pyautogui.click(x = 1070, y = 710)
            start = time.time()
    time.sleep(0.2)
    pyautogui.click(x = 900, y = 450)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    with open('portofolio.txt', 'w') as f:
        f.write(clipboard.paste())
    pf = pd.read_csv('portofolio.txt', sep='\t').set_index('Stock')
    for x in pf.index:
        pf.at[x, 'Avlb'] = round(pf.loc[x, 'Avlb'])
    return pf

# mengambil informasi pesan ara spekulan
def ara_spekulan(text):
    lines = text.splitlines()
    count = 0
    data = []
    for line in lines:
        if 'Price:' in line:
            ngesplit = lines[count].split('|')
            kode = ngesplit[0].replace('*)', '').replace(' ', '')
            harga = int(ngesplit[1].replace('Price:', '').replace(' ', ''))

            if harga <= 2000:
                kode, sumber = text, 'Ara_Spekulan'
                data.append([kode,sumber])
        count += 1
    return data
            
if __name__ == '__main__':
    print(get_valid_date())
#     if not pyuac.isUserAdmin():
#         print("Re-launching as admin!")
#         pyuac.runAsAdmin()
    
#     order_buy(kode='ANTM', price=1000, lot=1, live = False)


