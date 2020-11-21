from tkinter import *
import api
from api import polo

root = Tk()
root.title('Poloniex Client')
img = PhotoImage(file = 'polo.png')
root.iconphoto(True, img)
tickerFrame = LabelFrame(root, text='Ticker', padx=5, pady=5)
tickerFrame.pack()

pairEnt = Entry(tickerFrame, width=10)
pairEnt.grid(row=0, column=0)
pairEnt.insert(0, 'USDT_BTC')

priceLbl = Label(tickerFrame, text=' ')
priceLbl.grid(row=0, column=1)

def click():
  data = polo.returnTicker()
  pair = pairEnt.get()
  priceLbl.config(text=data[pair]['last'])

refreshBtn = Button(tickerFrame, text='Refresh', command=click)
refreshBtn.grid(row=1)

root.mainloop()
