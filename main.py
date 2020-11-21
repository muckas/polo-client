import time
from tkinter import *
import api
from api import polo
import globalvars
import threading

root = Tk()
root.title('Poloniex Client')
img = PhotoImage(file = 'polo.png')
root.iconphoto(True, img)

# FRAMES
tickerFrame = LabelFrame(root, text='Ticker', padx=5, pady=5)
tickerFrame.grid(row=0, column=0, padx=5, pady=5, sticky='nw')
walletFrame = LabelFrame(root, text='Wallet', padx=5, pady=5)
walletFrame.grid(row=0, column=1, padx=5, pady=5, sticky='nw')

#TICKER THREAD
def tickerUpdate(oneshot=False):
  while True:
    ticker = polo.returnTicker()
    globalvars.ticker = ticker
    time.sleep(1)
    if oneshot:
      break

# START THREADS
tickerThread = threading.Thread(target=tickerUpdate)
tickerThread.start()

# TICKER FRAME
tickerUpdate(oneshot=True)
tickerPairEnt = Entry(tickerFrame, width=10)
tickerPairEnt.grid(row=0, column=0)
tickerPairEnt.insert(0, 'USDT_BTC')

tickerPriceLbl = Label(tickerFrame, text='0.00000000')
tickerPriceLbl.grid(row=0, column=1)

def tickerRefreshBtnClick():
  pair = tickerPairEnt.get()
  price = globalvars.ticker[pair]['last'][:9] # displaying first 8 digits of the price
  tickerPriceLbl.config(text=price)

tickerRefreshBtn = Button(tickerFrame, text='Refresh', command=tickerRefreshBtnClick)
tickerRefreshBtn.grid(row=1)

# WALLET FRAME
walletBalancesLbls = [] # list of balance labels
def walletDrawBalances():
  global walletBalancesLbls
  for lbl in walletBalancesLbls:
    lbl[0].destroy()
    lbl[1].destroy()
  walletBalancesLbls = []
  balance = api.getAllBalances(total=True)
  walletTotalLbl.config(text=f'Total BTC: {balance}') # formatting for 8 digits after dots
  balances = api.getAllBalances()
  for currency in balances:
    walletBalancesLbls.append([
      Label(walletFrame, text=f'{currency}:'),
      Label(walletFrame, text=balances[currency]['available'])
      ])
  line = 3
  for lbl in walletBalancesLbls:
    lbl[0].grid(row=line, column=0, sticky='w')
    lbl[1].grid(row=line, column=1, sticky='w')
    line += 1

def walletRefreshBtnClick():
  walletDrawBalances()

walletRefreshBtn = Button(walletFrame, text='Refresh', command=walletRefreshBtnClick)
walletRefreshBtn.grid(row=0, column=0, columnspan=2)

walletTotalLbl = Label(walletFrame, text='Balance')
walletTotalLbl.grid(row=1, column=0, columnspan=2)

# START
tickerRefreshBtnClick()
walletRefreshBtnClick()
root.mainloop()
