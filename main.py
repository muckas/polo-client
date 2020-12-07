import time
from tkinter import *
import api
from api import polo
import globalvars
import threading
import database

database.loadInitialData()

root = Tk()
root.title('Poloniex Client')
img = PhotoImage(file = 'polo.png')
root.iconphoto(True, img)

# FRAMES
tickerFrame = LabelFrame(root, text='Ticker', padx=5, pady=5)
tickerFrame.grid(row=0, column=0, padx=5, pady=5, sticky='nw')
walletFrame = LabelFrame(root, text='Wallet', padx=5, pady=5)
walletFrame.grid(row=0, column=1, padx=5, pady=5, sticky='nw')


# TICKER FRAME
tickerPairBaseVar = StringVar()
tickerPairBaseVar.set('USDT')
tickerPairCoinVar = StringVar()
tickerPairCoinVar.set('BTC')

tickerPriceLbl = Label(tickerFrame, text='0.00000000')
tickerPriceLbl.grid(row=1, column=1)

def tickerRefresh(custom=False):
  if custom:
    if tickerPairEnt.get() in globalvars.pairsList:
      pair = tickerPairEnt.get()
      base, coin = pair.split('_')
      tickerPairBaseVar.set(base)
      tickerPairCoinVar.set(coin)
    else:
      tickerPriceLbl.config(text='Bad pair')
  else:
    pair = f'{tickerPairBaseVar.get()}_{tickerPairCoinVar.get()}'
    price = globalvars.ticker[pair]['last'][:9] # displaying first 8 digits of the price
    tickerPriceLbl.config(text=price)

def tickerPairBaseChange(*args):
  global tickerPairCoinDrd
  tickerPairCoinDrd.destroy()
  options = globalvars.availablePairs[tickerPairBaseVar.get()]
  tickerPairCoinVar.set(options[0])
  tickerPairCoinDrd = OptionMenu(tickerFrame, tickerPairCoinVar, *options)
  tickerPairCoinDrd.grid(row=0, column=1)

def tickerPairCoinChange(*args):
  tickerRefresh()

def tickerCustomPairClick():
  tickerRefresh(custom=True)

tickerPairBaseDrd = OptionMenu(tickerFrame, tickerPairBaseVar, *globalvars.availablePairs.keys())
tickerPairBaseDrd.grid(row=0, column=0)
tickerPairCoinDrd = OptionMenu(tickerFrame, tickerPairCoinVar, *globalvars.availablePairs[tickerPairBaseVar.get()])
tickerPairCoinDrd.grid(row=0, column=1)

tickerPairEnt = Entry(tickerFrame, width=10)
tickerPairEnt.grid(row=1, column=0)

tickerCustomPairBtn = Button(tickerFrame, text='Custom Pair', command=tickerCustomPairClick)
tickerCustomPairBtn.grid(row=3, column=0, columnspan=3, sticky='nwes')

tickerRefresh()

tickerPairBaseVar.trace('w', tickerPairBaseChange)
tickerPairCoinVar.trace('w', tickerPairCoinChange)

# WALLET FRAME
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
  walletTotalAmountLbl.config(text=str(balance)[:10]) # formatting for 8 digits after dots
  balances = globalvars.balances
  for currency in balances:
    walletBalancesLbls.append([
      Label(walletFrame, text=f'{currency}:'),
      Label(walletFrame, text=str(balances[currency]['available'] + balances[currency]['onOrders'])[:10])
      ])
  line = 3
  for lbl in walletBalancesLbls:
    lbl[0].grid(row=line, column=0, sticky='w')
    lbl[1].grid(row=line, column=1, sticky='w')
    line += 1

def walletRefreshClick():
  database.balanceUpdate(oneshot=True)
  walletDrawBalances()

def walletRefresh():
  while True:
    walletDrawBalances()
    print('Bing')
    time.sleep(5)

walletRefreshBtn = Button(walletFrame, text='Refresh', command=walletRefreshClick)
walletRefreshBtn.grid(row=0, column=0, columnspan=3, sticky='nesw')

walletTotalLbl = Label(walletFrame, text='Total')
walletTotalLbl.grid(row=1, column=0)
walletTotalAmountLbl = Label(walletFrame)
walletTotalAmountLbl.grid(row=1, column=1)

walletDisplayCurrencyDrd = OptionMenu(walletFrame, walletDisplayCurrencyVar, *globalvars.displayCurrencies)
walletDisplayCurrencyDrd.grid(row=1, column=2)
walletDisplayCurrencyVar.trace('w', walletDrawBalances)

# START
walletRefreshClick()
root.mainloop()
