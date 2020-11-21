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
  tickerPriceLbl.config(text=data[pair]['last'][:10])

tickerRefreshBtn = Button(tickerFrame, text='Refresh', command=tickerRefreshBtnClick)
tickerRefreshBtn.grid(row=1)

# WALLET FRAME
walletBalanceLbl = Label(walletFrame, text='Balance')
walletBalanceLbl.grid(row=0, column=0)

def walletRefreshBtnClick():
  balance = api.getTotalBTC()
  walletBalanceLbl.config(text=balance)

walletRefreshBtn = Button(walletFrame, text='Refresh', command=walletRefreshBtnClick)
walletRefreshBtn.grid(row=1)

root.mainloop()
