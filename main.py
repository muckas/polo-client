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

# DEFINE THREADS
def tickerUpdate(oneshot=False):
  while True:
    globalvars.ticker = polo.returnTicker()
    if oneshot:
      break
    time.sleep(1)

def balanceUpdate(oneshot=False):
  while True:
    globalvars.balances = api.getAllBalances()
    globalvars.totalBtcBalance = api.getAllBalances(total=True)
    if oneshot:
      break
    time.sleep(300)

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
balanceUpdate(oneshot=True)
walletDisplayCurrencyVar = StringVar()
walletDisplayCurrencyVar.set('BTC')
walletBalancesLbls = [] # list of balance labels

def convertCurrency(coinFrom, coinTo, amount):
  pair = f'{coinTo}_{coinFrom}'
  return amount * float(globalvars.ticker[pair]['last'])

def walletDrawBalances(*args):
  global walletBalancesLbls
  for lbl in walletBalancesLbls:
    lbl[0].destroy()
    lbl[1].destroy()
  walletBalancesLbls = []
  balance = globalvars.totalBtcBalance
  displayCurrency = walletDisplayCurrencyVar.get()
  if displayCurrency != 'BTC':
    balance = convertCurrency('BTC', displayCurrency, balance)
  walletTotalLbl.config(text=f'Total {displayCurrency}: {str(balance)[:10]}') # formatting for 8 digits after dots
  balances = globalvars.balances
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
  balanceUpdate(oneshot=True)
  walletDrawBalances()

walletRefreshBtn = Button(walletFrame, text='Refresh', command=walletRefreshBtnClick)
walletRefreshBtn.grid(row=0, column=0, columnspan=2)

walletTotalLbl = Label(walletFrame, text='Balance')
walletTotalLbl.grid(row=1, column=0, columnspan=2)

walletDisplayCurrencyDrd = OptionMenu(walletFrame, walletDisplayCurrencyVar, 'BTC', 'USDT', 'USDC')
walletDisplayCurrencyDrd.grid(row=1, column=2)
walletDisplayCurrencyVar.trace('w', walletDrawBalances)

# START
tickerRefreshBtnClick()
walletRefreshBtnClick()
root.mainloop()
