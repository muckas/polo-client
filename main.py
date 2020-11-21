from tkinter import *
import api
from api import polo

root = Tk()
root.title('Poloniex Client')
img = PhotoImage(file = 'polo.png')
root.iconphoto(True, img)
tickerFrame = LabelFrame(root, text='Ticker', padx=5, pady=5)
tickerFrame.grid(row=0, column=0, padx=5, pady=5)
walletFrame = LabelFrame(root, text='Wallet', padx=5, pady=5)
walletFrame.grid(row=0, column=1, padx=5, pady=5)

# TICKER FRAME
tickerPairEnt = Entry(tickerFrame, width=10)
tickerPairEnt.grid(row=0, column=0)
tickerPairEnt.insert(0, 'USDT_BTC')

tickerPriceLbl = Label(tickerFrame, text='0.00000000')
tickerPriceLbl.grid(row=0, column=1)

def tickerRefreshBtnClick():
  data = polo.returnTicker()
  pair = tickerPairEnt.get()
  price = data[pair]['last'][:9] # displaying first 8 digits of the price
  tickerPriceLbl.config(text=price)

tickerRefreshBtn = Button(tickerFrame, text='Refresh', command=tickerRefreshBtnClick)
tickerRefreshBtn.grid(row=1)

# WALLET FRAME
walletBalancesLbls = [] # list of balance labels
def walletDrawBalances():
  global walletBalancesLbls
  for label in walletBalancesLbls:
    label.destroy()
  walletBalancesLbls = []
  balance = api.getAllBalances(total=True)
  walletTotalLbl.config(text=f'Total BTC: {balance}') # formatting for 8 digits after dots
  balances = api.getAllBalances()
  for currency in balances:
    walletBalancesLbls.append(Label(walletFrame, text=f'{currency}: {balances[currency]["available"]}'))
  for label in walletBalancesLbls:
    label.pack(anchor='w')

def walletRefreshBtnClick():
  walletDrawBalances()

walletRefreshBtn = Button(walletFrame, text='Refresh', command=walletRefreshBtnClick)
walletRefreshBtn.pack()

walletTotalLbl = Label(walletFrame, text='Balance')
walletTotalLbl.pack()

# START
tickerRefreshBtnClick()
walletRefreshBtnClick()
root.mainloop()
