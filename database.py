import time
import sqlite3
import threading
import globalvars
import api
from api import polo

dbConn = None
dbCursor = None

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
def makePairsList():
  pairs = []
  for pair in globalvars.ticker.keys():
    pairs.append(pair)
  return pairs

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

def dbAddGlobalvar(cursor, name, value):
  result = dbExec(cursor, 'SELECT value FROM globalvars WHERE name = ?', [name])
  if len(result) == 0:
    dbExec(cursor, 'INSERT INTO globalvars (name, value) VALUES (?, ?)', [name, str(value)])
    result = dbExec(cursor, 'SELECT value FROM globalvars WHERE name = ?', [name])
  return eval(result[0][0])

def loadInitialData():
  global dbConn, dbCursor

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
  # Create tables
  data = dbExec(dbCursor, 'CREATE TABLE IF NOT EXISTS globalvars (name TEXT, value TEXT)')
  data = dbExec(dbCursor, 'CREATE TABLE IF NOT EXISTS tracked_pairs (name TEXT, base TEXT, coin TEXT)')
  dbConn.commit()
  # CREATE VARIABLES
  globalvars.availablePairs = dbAddGlobalvar(dbCursor, 'availablePairs', updateAvailablePairs())
  globalvars.displayCurrencies = dbAddGlobalvar(dbCursor, 'displayCurrency', updateDisplayCurrencies())
  globalvars.pairsList = dbAddGlobalvar(dbCursor, 'pairsList', makePairsList())

  dbConn.commit()

if __name__ == '__main__':
  loadInitialData()
