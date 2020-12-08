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
tickerFrame.grid(row=0, column=0, padx=5, pady=5, sticky='nwes')
walletFrame = LabelFrame(root, text='Wallet', padx=5, pady=5)
walletFrame.grid(row=0, rowspan = 2, column=1, padx=5, pady=5, sticky='nwes')
trackedFrame = LabelFrame(root, text='Tracked Pairs', padx=5, pady=5)
trackedFrame.grid(row=1, column=0, padx=5, pady=5, sticky='nwes')


# TICKER FRAME
tickerPairBaseVar = StringVar()
tickerPairBaseVar.set('USDT')
tickerPairCoinVar = StringVar()
tickerPairCoinVar.set('BTC')

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
    result = database.dbExec(database.dbCursor, 'SELECT name FROM tracked_pairs WHERE name = ?', [pair])
    if len(result) > 0: 
      tickerTrackPairBtn['text'] = 'Untrack Pair'
    else:
      tickerTrackPairBtn['text'] = 'Track Pair'
    price = globalvars.ticker[pair]['last'][:10] # displaying first 9 digits of the price
    tickerPriceLbl.config(text=price)

def tickerPairBaseChange(*args):
  global tickerPairCoinDrd
  tickerPairCoinDrd.destroy()
  options = globalvars.availablePairs[tickerPairBaseVar.get()]
  tickerPairCoinVar.set(options[0])
  tickerPairCoinDrd = OptionMenu(tickerFrame, tickerPairCoinVar, *options)
  tickerPairCoinDrd.grid(row=1, column=1)

def tickerPairCoinChange(*args):
  tickerRefresh()

def tickerCustomPairClick():
  tickerRefresh(custom=True)

def tickerTrackPairClick():
  base = tickerPairBaseVar.get()
  coin = tickerPairCoinVar.get()
  pair = f'{base}_{coin}'
  result = database.dbExec(database.dbCursor, 'SELECT name FROM tracked_pairs WHERE name = ?', [pair])
  if len(result) == 0: 
    database.dbExec(database.dbCursor, 'INSERT INTO tracked_pairs (name, base, coin) VALUES (?,?,?)', [f'{base}_{coin}', base, coin])
    tickerTrackPairBtn['text'] = 'Untrack Pair'
  else:
    database.dbExec(database.dbCursor, 'DELETE FROM tracked_pairs WHERE name = ?', [pair])
    tickerTrackPairBtn['text'] = 'Track Pair'
  database.dbConn.commit()

tickerRefreshBtn = Button(tickerFrame, text='Refresh', command=tickerRefresh)
tickerRefreshBtn.grid(row=0, column=0, columnspan=2, sticky='nwes')

tickerPairBaseDrd = OptionMenu(tickerFrame, tickerPairBaseVar, *globalvars.availablePairs.keys())
tickerPairBaseDrd.grid(row=1, column=0)
tickerPairCoinDrd = OptionMenu(tickerFrame, tickerPairCoinVar, *globalvars.availablePairs[tickerPairBaseVar.get()])
tickerPairCoinDrd.grid(row=1, column=1)

tickerPriceLbl = Label(tickerFrame, text='0.00000000')
tickerPriceLbl.grid(row=2, column=1)

tickerPairEnt = Entry(tickerFrame, width=10)
tickerPairEnt.grid(row=2, column=0)

tickerCustomPairBtn = Button(tickerFrame, text='Custom Pair', command=tickerCustomPairClick)
tickerCustomPairBtn.grid(row=3, column=0, sticky='nwes')

tickerTrackPairBtn = Button(tickerFrame, text='Track Pair', command=tickerTrackPairClick)
tickerTrackPairBtn.grid(row=3, column=1, sticky='nwes')

tickerRefresh()

tickerPairBaseVar.trace('w', tickerPairBaseChange)
tickerPairCoinVar.trace('w', tickerPairCoinChange)

# WALLET FRAME
walletDisplayCurrencyVar = StringVar()
walletDisplayCurrencyVar.set('USDT')
walletBalancesLbls = [] # list of balance labels

def convertCurrency(coinFrom, coinTo, amount):
  pair = f'{coinTo}_{coinFrom}'
  return float(amount) * float(globalvars.ticker[pair]['last'])

def walletDrawBalances(*args):
  global walletBalancesLbls
  for lbl in walletBalancesLbls:
    for _ in lbl:
      _.destroy()
  walletBalancesLbls = []
  balance = globalvars.totalBtcBalance
  displayCurrency = walletDisplayCurrencyVar.get()
  if displayCurrency != 'BTC':
    balance = convertCurrency('BTC', displayCurrency, balance)
  walletTotalAmountLbl.config(text=str(balance)[:10]) # formatting for 8 digits after dots
  balances = globalvars.balances
  for currency in balances:
    currencyBalance = float(balances[currency]['available']) + float(balances[currency]['onOrders'])
    convertedBalance = balances[currency]['btcValue']
    if displayCurrency != 'BTC':
      convertedBalance = convertCurrency('BTC', displayCurrency, convertedBalance)
    walletBalancesLbls.append([
      Label(walletFrame, text=f'{currency}:'),
      Label(walletFrame, text=str(currencyBalance)[:10]),
      Label(walletFrame, text=str(convertedBalance)[:10])
      ])
  line = 3
  for lbl in walletBalancesLbls:
    lbl[0].grid(row=line, column=0, sticky='w')
    lbl[1].grid(row=line, column=1, sticky='w')
    lbl[2].grid(row=line, column=2, sticky='w')
    line += 1

def walletRefreshClick():
  database.balanceUpdate(oneshot=True)
  walletDrawBalances()

walletRefreshBtn = Button(walletFrame, text='Refresh', command=walletRefreshClick)
walletRefreshBtn.grid(row=0, column=0, columnspan=3, sticky='nesw')

walletTotalLbl = Label(walletFrame, text='Total')
walletTotalLbl.grid(row=1, column=0)
walletTotalAmountLbl = Label(walletFrame)
walletTotalAmountLbl.grid(row=1, column=1)

walletDisplayCurrencyDrd = OptionMenu(walletFrame, walletDisplayCurrencyVar, *globalvars.displayCurrencies)
walletDisplayCurrencyDrd.grid(row=1, column=2)
walletDisplayCurrencyVar.trace('w', walletDrawBalances)

# TRACKED FRAME
trackedPairsLbls = []
def trackedUpdate():
  global trackedPairsLbls
  for lbl in trackedPairsLbls:
    for _ in lbl:
      _.destroy()
  trackedPairsLbls = []
  pairs = database.dbExec(database.dbCursor, 'SELECT name FROM tracked_pairs')
  for row in pairs:
    pair = row[0]
    price = globalvars.ticker[pair]['last'][:9]
    trackedPairsLbls.append([
      Label(trackedFrame, text=pair),
      Label(trackedFrame, text=price)
      ])
  line = 1
  for lbl in trackedPairsLbls:
    lbl[0].grid(row=line, column=0, sticky='w')
    lbl[1].grid(row=line, column=1, sticky='w')
    line += 1

trackedRefreshBtn = Button(trackedFrame, text='Refresh', command=trackedUpdate)
trackedRefreshBtn.grid(row=0, column=0, columnspan = 2, sticky='nwes')

# START
trackedUpdate()
walletRefreshClick()
root.mainloop()
