import time
import sqlite3
import threading
import globalvars
import api
from api import polo

def dbExec(cursor, query, args=[]):
  cursor.execute(query, args)
  return cursor.fetchall()

# THREAD FUNCTIONS
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

# FUNCTIONS
def updateAvailablePairs():
  pairs = globalvars.ticker.keys()
  availablePairs = {}
  for pair in pairs:
    base, coin = pair.split('_')
    if base in availablePairs.keys():
      availablePairs[base].append(coin)
    else:
      availablePairs[base] = [coin]
  return availablePairs

def updateDisplayCurrencies():
  pairs = globalvars.ticker.keys()
  coins = ['BTC']
  for pair in pairs:
    if pair[-3:] == 'BTC':
      base, coin = pair.split('_')
      coins.append(base)
  return coins

def loadInitialData():
  tickerUpdate(oneshot=True)
  balanceUpdate(oneshot=True)
  # START THREADS
  tickerThread = threading.Thread(target=tickerUpdate)
  tickerThread.start()
  balanceThread = threading.Thread(target=balanceUpdate)
  balanceThread.start()

  # CREATE DATABASE
  dbConn = sqlite3.connect('poloClient.db')
  dbCursor = dbConn.cursor()
  # Create config table
  data = dbExec(dbCursor, 'CREATE TABLE IF NOT EXISTS config (name TEXT, value TEXT)')
  dbConn.commit()
  # CREATE VARIABLES
  # availablePairs
  result = dbExec(dbCursor, 'SELECT * FROM config WHERE name = ?', ['availablePairs'])
  if len(result) == 0:
    dbExec(dbCursor, 'INSERT INTO config (name, value) VALUES (?, ?)', ['availablePairs', str(updateAvailablePairs())])
  result = dbExec(dbCursor, 'SELECT value FROM config WHERE name = "availablePairs"')
  globalvars.availablePairs = eval(result[0][0])
  # displayCurrencies
  result = dbExec(dbCursor, 'SELECT * FROM config WHERE name = ?', ['displayCurrencies'])
  if len(result) == 0:
    dbExec(dbCursor, 'INSERT INTO config (name, value) VALUES (?, ?)', ['displayCurrencies', str(updateDisplayCurrencies())])
  result = dbExec(dbCursor, 'SELECT value FROM config WHERE name = "displayCurrencies"')
  globalvars.displayCurrencies = eval(result[0][0])
  dbConn.commit()

if __name__ == '__main__':
  loadInitialData()
