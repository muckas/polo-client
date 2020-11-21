from tkinter import *
from poloniex import Poloniex

with open('key') as f:
  api_key = f.read().rstrip('\n')
with open('secret') as f:
  api_secret = f.read().rstrip('\n')

polo = Poloniex(key=api_key, secret=api_secret)

root = Tk()
root.title('Poloniex Client')
img = PhotoImage(file = 'polo.png')
root.iconphoto(True, img)

entry = Entry(root)
entry.grid(row=0, column=0)
entry.insert(0, 'USDT_BTC')

def click():
  data = polo.returnTicker()
  pair = entry.get()
  label = Label(root, text=data[pair]['last'])
  label.grid_forget()
  label.grid(row=0, column=1)

button = Button(root, text='Refresh', command=click)
button.grid(row=1)

root.mainloop()
