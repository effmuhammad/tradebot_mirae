import pyautogui
import yfinance as yf
import pandas as pd


def default_chart(stock, cur_x=1180, cur_y=480):
    pyautogui.click(cur_x, cur_y)
    pyautogui.write('/c ' + stock + ' i47,i101,i103,i106,p1,z150')
    pyautogui.press('enter')
    return


def run(stocks):
    for stock in stocks:
        default_chart(stock=stock)


if __name__ == '__main__':
    list_emiten = pd.read_csv('daftar_saham.csv')
    list_emiten = list_emiten['Daftar Saham'].tolist()

    run(list_emiten)
