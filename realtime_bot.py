"""
Start Date: 12/12/2021
End-Date: Still Developing ..
By Effry Muhammad
Untuk impiannya bisa kaya tanpa bekerja :)

UPCOMING :
- masing masing waiting q_saham memiliki timeout 1 menit
"""

from datetime import datetime
import multiprocessing
import os
import math
from statistics import multimode
from tkinter import W
import numpy as np
import cv2
import time
import pyautogui
import threading
import pandas as pd
import libs.miraecommand as miraecommand
import shutil
from collections import Counter
import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel, PhoneCallDiscardReasonBusy
from telethon import TelegramClient, sync, events
import configparser
import dataframe_image as dfi

harga_maks = 1000
value_maks = 100000

# saham apa saja yang mau di analisis [kode, sumber, timeout]
q_saham = []
# antrian order buy [kode,lot,beli,start]
q_buy = []
# antrian order sell [kode,lot,jual,start]
q_sell = []
# list saham yang sedang di hold dalam sistem robot [kode, avg, avlb]
q_hold = []
# list orderbook yang free
free_ob=[1,2,3,4]
# list saham yang sedang di analisis
process_ob=[]
# hasil trade dalam dict {kode, posisi}
trade_result = {}

src_path = os.getcwd()
dst_path = os.path.join(src_path, 'orderbook_dataset', datetime.today().strftime('%Y-%m-%d'))
try:
    os.mkdir(dst_path)
except:
    pass

tradesum = 'tradesum' + '_' + datetime.today().strftime('%Y-%m-%d') + '.csv'

# TELEGRAM START-------------------------------------------------------------------------------------------

# Reading Configs telegream
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values telegram
api_id = 14466036
api_hash = '9c30d487583b899fb22ee5f6a8e6d940'
token = '5034082013:AAG6cvRJb9PDYUwxUWDSmElP7NaI5Yq7K5g'
message = "Working..."

phone = '+6288803146890'
username = 'effmuhammad'

client = TelegramClient(username, api_id, api_hash)
bot = telebot.TeleBot(token)

def trade_bot(text):
    global q_saham
    if text.isupper() and len(text) == 4:
        l_kode = []
        for x,y,z in q_saham:
            l_kode.append(x)
        if text not in l_kode: 
            q_saham.append([text,'Eff',time.time()])
        return 0
    
    # hanya untuk test START-----------------------------------------------------------------
    elif "berpotensi ARA" in text:
        data = miraecommand.ara_spekulan(text)
        q_saham = q_saham + data
        return 0
    # hanya untuk test END-----------------------------------------------------------------

    # perintah-perintah ke BOT
    text = text.lower()
    if text == "info":
        tele_send("Trade Bot By Effry, still developing...")
    elif text == "trad":
        #df_tradesum = pd.read_csv(tradesum)
        if os.path.isfile(tradesum):
            df_tradesum = pd.read_csv(tradesum)
            img_name = 'tradesum.png'
            dfi.export(df_tradesum, img_name)
            tele_send(img_name, 'img')
        else:
            tele_send("Belum ada transaksi hari ini")
    elif text == "port":
        if os.path.isfile('portofolio.txt'):
            df_portofolio = pd.read_csv('portofolio.txt', sep='\t')
            img_name = 'portofolio.png'
            dfi.export(df_portofolio, img_name)
            tele_send(img_name, 'img')
        else:
            tele_send("Tidak ada saham di portofolio")
    else:
        tele_send(
"""Perintah Tidak Dikenali, perintah yang dikenali bot:
info -> informasi mengenai BOT
trad -> catatan transaksi harian
port -> daftar saham yang sedang di hold""")

# kirim pesan ke trade bot telegram
def tele_send(pesan, type = 'txt'):
    if type == 'txt':
        bot.send_message(1939052952, pesan)
    elif type == 'img':
        bot.send_photo(1939052952, photo=open(pesan, 'rb'))

# membaca semua pesan telegram
def tele_listen():
    start_warn = time.time()
    @client.on(events.NewMessage)
    async def my_event_handler(event):
        global sender_id
        global q_saham
        chat = await event.get_chat()
        sender = await event.get_sender()
        chat_id = event.chat_id
        sender_id = event.sender.id
        text = event.raw_text
        # print("chat id", chat_id)
        # print("sender id", sender_id)
        # print(text)

        # id id dan target func pesan telegram
        if sender_id == 1434074023 and "berpotensi ARA" in text:    # ARA Spekulan
            data = miraecommand.ara_spekulan(text)
            q_saham = q_saham + data
        elif sender_id == 1939052952:    # Trade Bot
            trade_bot(text)

    while True:
        try:
            client.start()
            client.run_until_disconnected()
        except:
            if time.time() - start_warn >= 3:
                start_warn = time.time()
                print("[PERINGATAN] koneksi internet telegram terputus, waktu: ", miraecommand.get_time())
# TELEGRAM END-------------------------------------------------------------------------------------------

# state 1
def pre_session():
    pass

# state 1
def sesi_1():
    pass

# state 1
def pre_istirahat():
    pass

# state 1
def istirahat():
    pass

# state 1
def sesi_2():
    pass

# state 1
def pre_closing():
    pass

# program utama ----------------------------------------------------------------------------------------
interrupt_main = False
def main():
    state1 = False; state2 = False; state3 = False; state4 = False; state5 = False; state6 = False; state7 = False; state8 = False; state9 = False; state10 = False
    global q_saham; global q_buy; global q_sell; global q_hold; global free_ob; global process_ob; global trade_result
    global interrupt_read_runningtrade
    while True:
        # menyimpan tiap variabel ke dalam file txt
        #varvar = open("temp_var.txt", 'w')

        # time management pakai range waktu
        waktu = miraecommand.get_time()
        dt = datetime.now()
        hari = dt.weekday()     # 0 : senin
        split_waktu = waktu.split(':')
        jam = split_waktu[0]
        menit = split_waktu[1]
        waktu_des = int(jam + menit)

        if state1 == False and waktu_des <= 858:
            # stop, interrupt semua thread kecuali telegram
            print(f'[{waktu}] Menunggu waktu perdagangan')
            tele_send(f'[{waktu}] Menunggu waktu perdagangan')
            interrupt_read_runningtrade = True
            miraecommand.interrupt_close_notif = True
            interrupt_main = True
            state1 = True
        
        if state2 == False and 859 <= waktu_des < 1130:
            # aktifkan close notif
            print(f'[{waktu}] Persiapan Perdagangan Sesi 1')
            tele_send(f'[{waktu}] Persiapan Perdagangan Sesi 1')
            miraecommand.interrupt_close_notif = False
            time.sleep(10)
            state2 = True
        
        if state3 == False and 900 <= waktu_des < 1100:
            # Mulai program
            print(f'[{waktu}] Memulai Perdagangan Sesi 1')
            tele_send(f'[{waktu}] Memulai Perdagangan Sesi 1')
            interrupt_main = False
            state3 = True

        if hari == 0: 
        if state4 == False and 901 <= waktu_des < 1100:
            print(f'[{waktu}] Running Trade Scrapper ON')
            tele_send(f'[{waktu}] Running Trade Scrapper ON')
            interrupt_read_runningtrade = False
            state4 = True

        if state5 == False and 1125 <= waktu_des < 1129:
            # hapus q_buy dan q_saham, jual semua barang di q_hold, setelah itu stop semua read
            # q_hold[kode, avg, avlb]
            print(f'[{waktu}] Bersiap Istirahat')
            tele_send(f'[{waktu}] Bersiap Istirahat')
            interrupt_read_runningtrade = True
            q_buy = []
            q_saham = []
            for kode,avg,avlb in q_hold:
                if kode not in str(q_sell):
                    q_sell.append([kode, int(avlb), False, 0])
            state5 = True
            
        if state6 == False and 1129 <= waktu_des < 1329:
            # istirahat, interrupt semua thread kecuali telegram
            print(f'[{waktu}] Istirahat')
            tele_send(f'[{waktu}] Istirahat')
            miraecommand.interrupt_close_notif = True
            interrupt_read_runningtrade = True
            interrupt_main = True
            state6 = True

        if state7 == False and 1329 <= waktu_des < 1450:
            # aktifkan close notif
            print(f'[{waktu}] Persiapan Perdagangan Sesi 2')
            tele_send(f'[{waktu}] Persiapan Perdagangan Sesi 2')
            miraecommand.interrupt_close_notif = False
            time.sleep(10)
            state7 = True

        if state8 == False and 1330 <= waktu_des < 1430:
            print(f'[{waktu}] Mulai Perdagangan Sesi 2')
            tele_send(f'[{waktu}] Mulai Perdagangan Sesi 2')
            interrupt_read_runningtrade = False
            interrupt_main = False
            state8 = True

        if state9 == False and 1445 <= waktu_des < 1449:
            # hapus q_buy dan q_saham, jual semua barang di q_hold, setelah itu stop semua read
            print(f'[{waktu}] Bersiap Tutup Perdagangan')
            tele_send(f'[{waktu}] Bersiap Tutup Perdagangan')
            interrupt_read_runningtrade = True
            q_buy = []
            q_saham = []
            for kode,avg,avlb in q_hold:
                if kode not in str(q_sell):
                    q_sell.append([kode, int(avlb), False, 0])
            state9 = True

        if state10 == False and waktu_des >= 1449:
            # stop, interrupt semua thread kecuali telegram
            print(f'[{waktu}] Tutup Perdagangan')
            tele_send(f'[{waktu}] Tutup Perdagangan')
            miraecommand.interrupt_close_notif = True
            interrupt_read_runningtrade = True
            interrupt_main = True
            state10 = True
        
        if interrupt_main:
            continue

        # membuang antrian saham yang melebihi timeout 60 detik
        for x,y,z in q_saham:
            if time.time() - z >= 60:
                q_saham.remove([x,y,z])
        if len(q_saham) > 5:
            interrupt_read_runningtrade = True
        else:
            interrupt_read_runningtrade = False

        # mengisi ruang proses yang kosong
        while len(free_ob)>0 and len(q_saham)>0:
            kode, sumber, timeout = q_saham.pop(0)
            if kode not in str(process_ob): 
                ob = free_ob.pop(0)
                filename = miraecommand.get_time().replace(':', '.') + '-' + kode + '-' + sumber + '.csv'
                process_ob.append([ob, kode, filename, sumber])

                # set orderbook sesuai kode saham yang diinput
                miraecommand.set_ob(ob, kode)
                t_ob = threading.Thread(target=read_ob, args=(ob, kode, filename, sumber), daemon=True)
                t_ob.start()

        if len(q_buy) > 0 or len(q_sell) > 0:
            pf = miraecommand.portofolio()
    
            # order buy
            i = 0
            for kode,lot,beli,start in q_buy:
                if beli == False:   # belum jalankan order
                    # buat order
                    miraecommand.order_buy(kode, lot)
                    q_buy[i][2] = True
                    q_buy[i][3] = time.time()

                elif kode in pf.index:
                    if pf.loc[kode, 'Avlb'] == lot:
                        order = q_buy.pop(i)
                        q_hold.append([kode, pf.loc[kode, 'Avg'], pf.loc[kode, 'Avlb']])
                    else:
                        now = time.time()
                        if pf.loc[kode, 'BuyOpn'] < lot and pf.loc[kode, 'Avlb'] > 0 and now - start >= 60:
                            q_hold.append([kode, pf.loc[kode, 'Avg'], pf.loc[kode, 'Avlb']])
                        if pf.loc[kode, 'BuyOpn'] > 0 and now - start >= 60:
                            q_buy.pop(i)
                            # wd sahamnya
                            miraecommand.withdraw(kode)
                i+=1

            # untuk order sell
            i = 0
            for kode,lot,jual,start in q_sell:
                if jual == False:   # belum jalankan order
                    # buat order
                    miraecommand.order_sell(kode, lot)
                    q_sell[i][2] = True
                    q_sell[i][3] = time.time()

                elif kode not in pf.index:
                    order = q_sell.pop(i)
                    count = 0
                    for x,avg,avlb in q_hold:
                        if x == kode:
                            # menghitung laba/rugi
                            for a,b,c,d in process_ob:
                                if b == kode:
                                    df = pd.read_csv(c)
                                    last = df.iloc[-1]['last']
                            total_beli = avg * avlb * 100
                            fee_beli = total_beli * 0.0019
                            total_jual = last* avlb * 100 
                            fee_jual = total_jual * 0.0029
                            laba_rugi = total_jual - total_beli - fee_beli - fee_jual
                            if laba_rugi > 0:
                                posisi = 'PROFIT'
                            else:
                                posisi = 'LOSS'
                            trade_result[kode] = posisi
                            
                            tele_send(kode + ' | ' + laba_rugi + ' | ' + posisi)

                            # simpan ke csv tradesum
                            head = ['waktu jual', 'kode saham', 'harga beli', 'harga jual', 'jumlah lot', 'laba/rugi', 'posisi']
                            data = [[miraecommand.get_time()] + [kode] + [avg] + [last] + [avlb] + [laba_rugi] + [posisi]]
                            df = pd.DataFrame(data, columns=head)
                            if os.path.exists('./'+tradesum):
                                df.to_csv(tradesum, mode='a', index=False, header=False)
                            else:
                                df.to_csv(tradesum, mode='w', index=False, header=True)

                            q_hold.remove([x,avg,avlb])
                            break
                else:
                    now = time.time()                    
                    if pf.loc[x, 'SellOpn'] > 0 and now - start >= 60:
                        # wd sahamnya
                        miraecommand.withdraw(kode)
                        # bikin jadi order lagi
                        q_sell[i][2] = False
                i += 1

        # menghitung tradesum----------------------------------------------------------------------------
        if os.path.isfile(tradesum):
            df_tradesum = pd.read_csv(tradesum)
            total = df_tradesum['laba/rugi'].sum()
            # jika loss lebih dari 20k maka stop cari saham baru
            if total <= -20000:
                interrupt_read_runningtrade = True
                q_saham = []

if __name__ == "__main__":
    button = pyautogui.confirm(text='Jalankan Eff Trade BOT?', title='Alert', buttons=['OK', 'Cancel'])
    if button == 'Cancel':
        exit()
    p1 = threading.Thread(target=main, daemon=True)
    p1.start()
    # close notif pengganggu
    p2 = threading.Thread(target=miraecommand.close_notif, daemon=True)
    p2.start()
    # jalankan tele_listen
    tele_listen()